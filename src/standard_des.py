# 该代码文件来自生成式 AI 文心一言
import numpy as np
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt(data):
	# DES 需要一个 8 字节的密钥（尽管实际上只有 56 位被使用）
	# 在这里，我们生成一个随机的 8 字节密钥
	key = get_random_bytes(8)  # 正确的做法

	# 将 NumPy 数组转换为字节序列
	# 注意：这里我们简单地将数组展平为一维并转换为 tobytes()
	# 对于更复杂的数组，你可能需要自定义序列化方法
	array = data.flatten().astype(np.uint8)
	array_bytes = array.tobytes()

	# 创建一个 DES 加密器对象，使用 ECB 模式（注意：ECB 模式不安全，仅用于示例）
	# 在实际应用中，你应该使用更安全的模式，如 CBC，并正确地管理 IV
	cipher = DES.new(key, DES.MODE_ECB)

	# 对数据进行填充并加密
	# 注意：DES 的块大小是 8 字节，所以我们需要确保数据长度是 8 的倍数
	return key,cipher.encrypt(pad(array_bytes, DES.block_size)),array.size

def decrypt(key,data,size):
	# 解密时，我们需要相同的密钥
	decipher = DES.new(key, DES.MODE_ECB)

	# 解密数据并去除填充
	pt_bytes = unpad(decipher.decrypt(data), DES.block_size)

	# 将解密后的字节序列转换回 NumPy 数组
	# 注意：这里我们假设解密后的数据可以直接转换为原始数组的形状和类型
	decrypted_array = np.frombuffer(pt_bytes, dtype=np.uint8)
	# 然而，由于可能存在填充，我们需要切片来获取正确的数据部分
	return decrypted_array[:size]  # 切片以匹配原始数组的大小

if __name__ == '__main__':
	test_data = np.array([1,1,4,5,1,4,1,9,1,9,8,1,0])
	print("Original array: ",test_data)
	key,encrypted_data,size = encrypt(test_data)
	decrypted_data = decrypt(key,encrypted_data,size)
	print("Decrypted array: ",decrypted_data)