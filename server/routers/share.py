from __future__ import annotations

import hashlib
import json
import secrets
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse

from .assets import ValidateResult, validate_payload  # reuse existing validators


router = APIRouter(prefix="/api/share", tags=["share"])

# Repo root
ROOT = Path(__file__).resolve().parents[2]
STORE_DIR = ROOT / "server" / "uploads" / "share"
INDEX_PATH = STORE_DIR / "index.json"


def _now_iso() -> str:
    # time.strftime ensures fixed formatting without importing datetime
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _ensure_store():
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(json.dumps({"items": []}, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_index() -> Dict[str, Any]:
    _ensure_store()
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_index(idx: Dict[str, Any]) -> None:
    with INDEX_PATH.open("w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)


def _gen_id(existing: set[str]) -> str:
    # short, URL-safe id
    for _ in range(10):
        cand = secrets.token_urlsafe(6).replace("_", "-")  # ~8 chars
        if cand not in existing:
            return cand
    # very unlikely; fall back to longer
    return secrets.token_urlsafe(10).replace("_", "-")


def _hash_token(tok: str) -> str:
    return hashlib.sha256(tok.encode("utf-8")).hexdigest()


# ---- API ----


@router.post("")
async def create_share(request: Request) -> Dict[str, Any]:
    """
    Accept JSON body with shape:
    {
      "meta": {"title": str, "author": str|None, "note": str|None, "baseDataVersion": str|None, "createdAt": str|None},
      "data": { "cards"?: CardRoot, "pendants"?: PendantRoot }
    }
    """
    try:
        body = await request.json()
    except Exception:  # noqa: PIE786
        raise HTTPException(status_code=400, detail="请求体必须为 JSON")

    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="请求体格式错误")

    meta = body.get("meta") or {}
    data = body.get("data")
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="data 必须为对象")

    title = meta.get("title")
    author = meta.get("author")
    description = meta.get("description") or meta.get("note")  # backward compat: accept note
    base_ver = meta.get("baseDataVersion")
    created_at = meta.get("createdAt") or _now_iso()

    if not isinstance(title, str) or not title.strip():
        raise HTTPException(status_code=400, detail="meta.title 必填")
    if author is not None and not isinstance(author, str):
        raise HTTPException(status_code=400, detail="meta.author 必须为字符串")
    if description is not None and not isinstance(description, str):
        raise HTTPException(status_code=400, detail="meta.description 必须为字符串")
    if base_ver is not None and not isinstance(base_ver, str):
        raise HTTPException(status_code=400, detail="meta.baseDataVersion 必须为字符串")

    has_any = False
    # Validate supported kinds using existing validators
    if "cards" in data and data["cards"] is not None:
        if not isinstance(data["cards"], dict):
            raise HTTPException(status_code=400, detail="data.cards 必须为对象")
        res: ValidateResult = validate_payload("card", data["cards"])  # type: ignore[arg-type]
        if not res.ok:
            raise HTTPException(status_code=400, detail={"kind": "card", "errors": res.errors})
        has_any = True
    if "pendants" in data and data["pendants"] is not None:
        if not isinstance(data["pendants"], dict):
            raise HTTPException(status_code=400, detail="data.pendants 必须为对象")
        res = validate_payload("pendant", data["pendants"])  # type: ignore[arg-type]
        if not res.ok:
            raise HTTPException(status_code=400, detail={"kind": "pendant", "errors": res.errors})
        has_any = True
    if "mapEvents" in data and data["mapEvents"] is not None:
        if not isinstance(data["mapEvents"], list):
            raise HTTPException(status_code=400, detail="data.mapEvents 必须为数组")
        res = validate_payload("mapevent", data["mapEvents"])  # type: ignore[arg-type]
        if not res.ok:
            raise HTTPException(status_code=400, detail={"kind": "mapevent", "errors": res.errors})
        has_any = True
    if "beginEffects" in data and data["beginEffects"] is not None:
        if not isinstance(data["beginEffects"], list):
            raise HTTPException(status_code=400, detail="data.beginEffects 必须为数组")
        res = validate_payload("begineffect", data["beginEffects"])  # type: ignore[arg-type]
        if not res.ok:
            raise HTTPException(status_code=400, detail={"kind": "begineffect", "errors": res.errors})
        has_any = True

    if not has_any:
        raise HTTPException(status_code=400, detail="data 至少包含 cards 或 pendants 之一")

    # Normalize write object
    pkg_obj = {
        "meta": {
            "title": title.strip(),
            "author": author or "",
            "description": description or "",
            "baseDataVersion": base_ver or "",
            "createdAt": created_at,
        },
        "data": {k: v for k, v in data.items() if k in ("cards", "pendants", "mapEvents", "beginEffects") and v is not None},
    }

    # Persist
    idx = _load_index()
    existing_ids = {it["id"] for it in idx.get("items", [])}
    share_id = _gen_id(existing_ids)
    raw_text = json.dumps(pkg_obj, ensure_ascii=False, indent=2)
    _ensure_store()
    fpath = STORE_DIR / f"{share_id}.json"
    fpath.write_text(raw_text, encoding="utf-8")
    size = fpath.stat().st_size

    # Management token (hash stored in index only)
    manage_token = secrets.token_urlsafe(18)
    token_hash = _hash_token(manage_token)

    entry = {
        "id": share_id,
        "title": pkg_obj["meta"]["title"],
        "author": pkg_obj["meta"].get("author", ""),
        "description": pkg_obj["meta"].get("description", ""),
        "baseDataVersion": pkg_obj["meta"].get("baseDataVersion", ""),
        "createdAt": created_at,
        "size": size,
        "downloads": 0,
        "tokenHash": token_hash,
    }

    items: List[Dict[str, Any]] = idx.get("items", [])
    items.append(entry)
    # Cap total items to prevent unbounded growth
    MAX_ITEMS = 1000
    if len(items) > MAX_ITEMS:
        # delete oldest files beyond cap
        items.sort(key=lambda x: x.get("createdAt", ""))
        to_remove = items[:-MAX_ITEMS]
        for it in to_remove:
            try:
                (STORE_DIR / f"{it['id']}.json").unlink(missing_ok=True)
            except Exception:
                pass
        items = items[-MAX_ITEMS:]
    # Persist index
    idx["items"] = items
    _save_index(idx)

    return {
        "id": share_id,
        "url": f"/api/share/{share_id}",
        "manageToken": manage_token,
    }


@router.get("")
def list_shares(q: Optional[str] = Query(None), limit: int = Query(30, ge=1, le=200)) -> Dict[str, Any]:
    idx = _load_index()
    items: List[Dict[str, Any]] = idx.get("items", [])
    # filter and sort by createdAt desc
    if q:
        qs = q.lower()
        items = [it for it in items if qs in str(it.get("title", "")).lower()]
    items.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
    # enrich description from file if not present, and strip tokenHash
    out: List[Dict[str, Any]] = []
    for it in items[:limit]:
        safe = {k: v for k, v in it.items() if k != "tokenHash"}
        desc = safe.get("description")
        if not desc:
            try:
                with (STORE_DIR / f"{it['id']}.json").open("r", encoding="utf-8") as f:
                    obj = json.load(f)
                    meta = obj.get("meta") or {}
                    desc = meta.get("description") or meta.get("note") or ""
            except Exception:
                desc = ""
            safe["description"] = desc
        out.append(safe)
    return {"items": out}


@router.get("/{share_id}")
def get_share(share_id: str) -> JSONResponse:
    fpath = STORE_DIR / f"{share_id}.json"
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="未找到分享")

    # read content
    with fpath.open("r", encoding="utf-8") as f:
        obj = json.load(f)

    # bump downloads (best-effort)
    try:
        idx = _load_index()
        changed = False
        for it in idx.get("items", []):
            if it.get("id") == share_id:
                it["downloads"] = int(it.get("downloads", 0)) + 1
                changed = True
                break
        if changed:
            _save_index(idx)
    except Exception:
        pass

    return JSONResponse(content=obj)


@router.delete("/{share_id}")
def delete_share(share_id: str, manageToken: Optional[str] = Query(None)) -> Dict[str, Any]:
    token = manageToken
    if not token:
        raise HTTPException(status_code=400, detail="缺少 manageToken")
    idx = _load_index()
    items: List[Dict[str, Any]] = idx.get("items", [])
    pos = None
    for i, it in enumerate(items):
        if it.get("id") == share_id:
            pos = i
            if it.get("tokenHash") != _hash_token(token):
                raise HTTPException(status_code=403, detail="无权限删除该分享")
            break
    if pos is None:
        raise HTTPException(status_code=404, detail="未找到分享")

    # remove file and index entry
    try:
        (STORE_DIR / f"{share_id}.json").unlink(missing_ok=True)
    except Exception:
        pass
    del items[pos]
    idx["items"] = items
    _save_index(idx)
    return {"ok": True}
