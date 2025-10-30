import axios from 'axios'

const API_BASE = (import.meta as any).env?.VITE_API_BASE || 'http://localhost:8000'

export async function getData(kind: 'card' | 'pendant') {
  // Prefer new /data route; fallback to /baseline for compatibility
  try {
    const { data } = await axios.get(`${API_BASE}/api/data/${kind}`)
    return data
  } catch {
    const { data } = await axios.get(`${API_BASE}/api/baseline/${kind}`)
    return data
  }
}

export async function validate(kind: 'card' | 'pendant', payload: any): Promise<{ ok: boolean; errors: string[] }> {
  const { data } = await axios.post(`${API_BASE}/api/validate`, payload, { params: { kind } })
  return data
}

export async function decodeEncrypted(file: File) {
  const fd = new FormData()
  fd.append('file', file)
  const { data } = await axios.post(`${API_BASE}/api/decode`, fd, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return data
}

export async function encodeEncrypted(payload: any): Promise<string> {
  const { data } = await axios.post(`${API_BASE}/api/encode`, { payload }, { responseType: 'text' })
  return data
}
