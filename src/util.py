import cv2
import matplotlib.pyplot as plt
import numpy as np
import struct

def read_rgbimg(src):
	"""
	读取一个路径为 src 的图像，并将其转为 RGB 形式的多维数组
	:param src: 图像路径
	:return: RGB 形式的三维数组
	"""
	return cv2.cvtColor(cv2.imread(src), cv2.COLOR_BGR2RGB) # imread 返回的是 BGR，需要改变通道顺序为 RGB

def show_rgbimg(img,title=""):
	"""
	展示一个 RGB 图像
	:param img: RGB 图像所对应的多维数组
	:param title: 图片标题
	:return: 无
	"""
	plt.imshow(img)
	plt.axis("off")
	plt.title(title)
	plt.show()

def read_img(src):
	"""
		读取一个路径为 src 的灰度图像，并将其转为多维数组
		:param src: 图像路径
		:return: 灰度图像二维数组
	"""
	return cv2.imread(src,cv2.IMREAD_GRAYSCALE)

def show_img(img,title=""):
	"""
	展示一个灰度图像
	:param img: 灰度图像所对应的多维数组
	:param title: 图片标题
	:return: 无
	"""
	plt.imshow(img,cmap='gray')
	plt.axis("off")
	plt.title(title)
	plt.show()

def to_storage(img):
	"""
	将 img 转化为外存形式
	:param img: 待转换的图像数组
	:return:
	"""
	img = img.astype(np.float32)
	len1, len2 = img.shape[0], img.shape[1]
	storage = np.zeros((2 * len1, 2 * len2)).astype(np.uint8)
	for i in range(len1):
		for j in range(len2):
			bytes_value = [byte for byte in struct.pack('<f', img[i][j])]
			storage[2 * i][2 * j] = bytes_value[0]
			storage[2 * i][2 * j + 1] = bytes_value[1]
			storage[2 * i + 1][2 * j] = bytes_value[2]
			storage[2 * i + 1][2 * j + 1] = bytes_value[3]
	return storage.astype(np.uint8)

def save_secret(img,path):
	"""
	将某个加密后的图像以图片形式进行存储，所有密文图像矩阵的元素都应该是 float32 类型
	:param img: 二维图像矩阵
	:param path: 存储路径和文件名，必须使用 png 图像
	:return: 无
	"""
	cv2.imwrite(path,to_storage(img))

def to_memory(img):
	"""
	将 img 转换为内存形式
	:param img: 待转换的图像数组
	:return:
	"""
	len1, len2 = img.shape[0] // 2, img.shape[1] // 2
	result = np.zeros((len1, len2)).astype(np.float32)
	for i in range(len1):
		for j in range(len2):
			result[i][j] = struct.unpack('<f', bytes(
				[img[2 * i][2 * j], img[2 * i][2 * j + 1], img[2 * i + 1][2 * j], img[2 * i + 1][2 * j + 1]]))[0]
	return result.astype(np.float32)

def load_secret(path,transfer=True):
	"""
	将外存中存储的密文图片经过转换加载到内存
	:param path: 图像路径
	:return: 加载后的图像矩阵
	"""
	img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
	if(transfer):
		return to_memory(img)
	else:
		return img

def get_chaos(size,upper_bound=1000,seed=0):
	"""
	以 seed 为随机数种子，获取 size 组混沌随机数，每组 2 个
	:param size: 随机数组数
	:param upper_bound: 生成随机数的范围，[0,upperbound)
	:param seed: 随机数种子
	:return: 生成的随机数
	"""
	if(seed):
		np.random.seed(seed)
	a = np.zeros(size)
	b = np.zeros(size)
	a[0] = np.random.rand() * 2 * np.pi
	b[0] = np.random.rand() * 2 * np.pi
	k_val = np.random.rand()
	for i in range(1,size):
		a[i] = (a[i - 1] + b[i - 1]) % (2. * np.pi)
		b[i] = (b[i - 1] + k_val * np.sin(a[i - 1] + b[i - 1])) % (2. * np.pi)
	return (a / (2 * np.pi) * upper_bound).astype(np.int64),(b / (2 * np.pi) * upper_bound).astype(np.int64)