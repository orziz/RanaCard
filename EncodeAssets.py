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


# 指定要处理的目标文件
target_file = "Card.json"  # 可灵活更改此文件名
# target_file = "MapEvent.json"  # 可灵活更改此文件名

# 源目录和目标目录
source_directory = './Data'
destination_directory = r"C:\Program Files (x86)\Steam\steamapps\common\RanaCard\RanaCard_Data\StreamingAssets"

# 构建完整的源文件路径和目标文件路径
src_file_path = os.path.join(source_directory, target_file)
dst_file_path = os.path.join(destination_directory, target_file)

# 检查源文件是否存在
if not os.path.isfile(src_file_path):
    print(f"源文件不存在: {src_file_path}")
else:
    try:
        # 读取JSON文件并加密
        with open(src_file_path, 'r', encoding='utf-8') as f:
            json_content = f.read()
        encrypted_result = encrypt(json_content)
        
        # 写回到目标路径
        with open(dst_file_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_result)
        
        print(f"已加密并写回: {target_file}")
    except Exception as e:
        # 如果加密失败，输出错误信息
        print(f"加密失败 {target_file}: {e}")