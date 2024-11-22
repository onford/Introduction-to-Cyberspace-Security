import src.util as util
import src.img_transform as img_transform
import src.standard_aes as aes
import src.standard_des as des
from time import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm # 进度条

times = 100 # AES 和 DES 各跑多少次
aes_encrypt = .0
aes_decrypt = .0
des_encrypt = .0
des_decrypt = .0

shifts = np.array([1,2,4,8,16,32,64,128,256,512,1024,2048,4096])
arnold_encrypt = []
arnold_decrypt = []
randomshift_encrypt = []
randomshift_decrypt = []

if __name__ == '__main__':
	img = util.read_img("../fatcat.jpg")

	# 测试 AES 的加解密时间
	for _ in range(times):
		start = time()
		key,iv,data,size = aes.encrypt(img)
		end = time()
		aes_encrypt += end - start
		start = time()
		aes.decrypt(key,iv,data,size)
		end = time()
		aes_decrypt += end - start
	aes_encrypt /= times
	aes_decrypt /= times
	print("AES 的加解密时间: ",aes_encrypt,aes_decrypt)

	# 测试 DES 的加解密时间
	for _ in range(times):
		start = time()
		key, data, size = des.encrypt(img)
		end = time()
		des_encrypt += end - start
		start = time()
		des.decrypt(key, data, size)
		end = time()
		des_decrypt += end - start
	des_encrypt /= times
	des_decrypt /= times
	print("DES 的加解密时间: ",des_encrypt,des_decrypt)

	# 测试平均每次 Arnold 变换的加解密时间
	for i in  tqdm(range(len(shifts)), desc="Arnold 处理进度", ncols=100):
		# 获取 k 组随机数
		k = shifts[i]
		a, b = util.get_chaos(k, img.shape[0])

		# 根据伪随机数，对图像进行 arnold 加密
		start = time()
		secreted_img = img_transform.arnold_trans(img, a, b, k)
		end = time()
		arnold_encrypt.append((end - start) / k)

		# 根据伪随机数，对加密后的图象进行解密
		start = time()
		solved_img = img_transform.arnold_detrans(secreted_img, a, b, k)  # arnold 逆变换
		end = time()
		arnold_decrypt.append((end - start) / k)

	# 测试平均每次随机置换变换的加解密时间
	for i in tqdm(range(len(shifts)), desc="随机置乱处理进度", ncols=100):
		# 获取 4 组随机数
		k = shifts[i]
		a, b = util.get_chaos(k, img.shape[0], 114)
		c, d = util.get_chaos(k, img.shape[1], 514)

		# 根据伪随机数，对图像进行随机置乱加密
		start = time()
		secreted_img = img_transform.randomshift_trans(img, a, b, c, d)
		end = time()
		randomshift_encrypt.append((end - start) / k)

		# 根据伪随机数，对加密后的图像进行解密
		start = time()
		solved_img = img_transform.randomshift_detrans(secreted_img, a, b, c, d)  # 随机置乱逆变换
		end = time()
		randomshift_decrypt.append((end - start) / k)

	print("开始画图")
	# 画图分析
	plt.grid()
	plt.title("加密时长分析")
	shifts = np.log(shifts)
	plt.xticks(fontproperties='Euclid')
	plt.yticks(fontproperties='Euclid')
	plt.plot(shifts,[aes_encrypt] * len(shifts),label="$\mathrm{AES}$")
	plt.plot(shifts,[des_encrypt] * len(shifts),label="$\mathrm{DES}$")
	plt.plot(shifts,arnold_encrypt,label="$\mathrm{Anold}$ 变换")
	plt.plot(shifts,randomshift_encrypt,label="随机置乱变换")
	plt.xlabel("$\log_2($加密次数$)$")
	plt.ylabel("平均一次加密时长/秒")
	plt.legend() # 展示标签
	plt.savefig("result/encrypt.pdf")
	plt.savefig("result/encrypt.png")
	plt.show()

	plt.grid()
	plt.title("解密时长分析")
	shifts = np.log(shifts)
	plt.xticks(fontproperties='Euclid')
	plt.yticks(fontproperties='Euclid')
	plt.plot(shifts, [aes_encrypt] * len(shifts), label="$\mathrm{AES}$")
	plt.plot(shifts, [des_encrypt] * len(shifts), label="$\mathrm{DES}$")
	plt.plot(shifts, arnold_encrypt, label="$\mathrm{Anold}$ 变换")
	plt.plot(shifts, randomshift_encrypt, label="随机置乱变换")
	plt.xlabel("$\log_2($加密次数$)$")
	plt.ylabel("平均一次解密时长/秒")
	plt.legend()  # 展示标签
	plt.savefig("result/decrypt.pdf")
	plt.savefig("result/decrypt.png")
	plt.show()