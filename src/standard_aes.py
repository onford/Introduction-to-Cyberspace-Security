# 该代码文件来自生成式 AI 文心一言
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt(data):
	# 生成一个随机的 AES 密钥（例如 AES-128）
	key = get_random_bytes(16)

	# 将 NumPy 数组转换为字节序列
	# 注意：这里我们简单地将数组展平并转换为 tobytes()，但这种方法可能不适用于所有数据类型和数组形状
	# 对于更复杂的数组，你可能需要自定义序列化方法
	array = data.flatten().astype(np.uint8)
	array_bytes = array.tobytes()

	# 创建一个 AES 加密器对象，使用 CBC 模式（需要 IV）
	cipher = AES.new(key, AES.MODE_CBC)
	iv = cipher.iv  # 获取并存储 IV（在实际应用中，你需要安全地存储和传输 IV）

	# 对数据进行填充并加密
	return key,iv,cipher.encrypt(pad(array_bytes, AES.block_size)),array.size

def decrypt(key,iv,data,size):
	# 解密时，我们需要相同的密钥和 IV
	decipher = AES.new(key, AES.MODE_CBC, iv=iv)

	# 解密数据并去除填充
	pt_bytes = unpad(decipher.decrypt(data), AES.block_size)

	# 将解密后的字节序列转换回 NumPy 数组
	# 注意：这里我们假设解密后的数据可以直接转换为原始数组的形状和类型
	return np.frombuffer(pt_bytes, dtype=np.uint8)

if __name__ == '__main__':
	test_data = np.array([1,1,4,5,1,4,1,9,1,9,8,1,0])
	print("Original array: ",test_data)
	key,iv,encrypted_data,size = encrypt(test_data)
	decrypted_data = decrypt(key,iv,encrypted_data,size)
	print("Decrypted array: ",decrypted_data)