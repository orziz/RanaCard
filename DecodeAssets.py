import os
import base64
# pip install cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

key = "sd14WDS66sdwgy423Sbfhk"
iv = "sdagjusasxa"

def get_valid_key(key_str):
    num = 16
    key_bytes = key_str.encode('utf-8')
    if len(key_bytes) < num:
        return key_bytes.ljust(num, b'\0')
    elif len(key_bytes) > num:
        return key_bytes[:num]
    return key_bytes

def get_valid_iv(iv_str):
    iv_bytes = iv_str.encode('utf-8')
    if len(iv_bytes) < 16:
        return iv_bytes.ljust(16, b'\0')
    elif len(iv_bytes) > 16:
        return iv_bytes[:16]
    return iv_bytes

def decrypt(encrypted_json):
    cipher = Cipher(algorithms.AES(get_valid_key(key)), modes.CBC(get_valid_iv(iv)), backend=default_backend())
    decryptor = cipher.decryptor()
    encrypted_data = base64.b64decode(encrypted_json)
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # 移除PKCS7填充
    unpadder = padding.PKCS7(128).unpadder()  # 128位 = 16字节
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return unpadded_data.decode('utf-8')

def encrypt(json_str):
    cipher = Cipher(algorithms.AES(get_valid_key(key)), modes.CBC(get_valid_iv(iv)), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # 添加PKCS7填充
    padder = padding.PKCS7(128).padder()  # 128位 = 16字节
    padded_data = padder.update(json_str.encode('utf-8')) + padder.finalize()
    
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode('utf-8')

# 处理文件
directory = r"C:\Program Files (x86)\Steam\steamapps\common\RanaCard\RanaCard_Data\StreamingAssets"
for file in os.listdir(directory):
    file_path = os.path.join(directory, file)
    dst = os.path.join('./Data', file)
    if not os.path.isfile(file_path):
        continue  # 跳过非文件项目
    if file.endswith(".json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                encrypted_content = f.read()
            result = decrypt(encrypted_content)
            with open(dst, 'wb') as f:
                f.write(result.encode('utf-8'))
            print(f"已解密: {file}")
        except Exception as e:
            # 如果解密失败，直接复制原文件
            print(f"解密失败 {file}，直接复制: {e}")
            with open(file_path, 'rb') as src:
                content = src.read()
            with open(dst, 'wb') as dst:
                dst.write(content)
            print(f"已复制: {file}")
    else:
        # 直接复制其他文件
        with open(file_path, 'rb') as src:
            content = src.read()
        with open(dst, 'wb') as dst:
            dst.write(content)
        print(f"已复制: {file}")
