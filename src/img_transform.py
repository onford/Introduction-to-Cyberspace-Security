import scipy.fft
import numpy as np

def dct_img(img):
	"""
	对图像进行二维离散余弦变换
	:param img: 表示待变换的图像的二维数组
	:return: 变换后图像的二维数组
	"""
	size = img.shape[0] * img.shape[1]
	return scipy.fft.dct(scipy.fft.dct(img, type=2, norm='ortho', axis=0), type=2, norm='ortho', axis=1) / 1024 / np.sqrt(size) + 0.5

def idct_img(img_dct):
	"""
	对图像进行二维离散余弦逆变换
	:param img_dct: 表示待逆变换的图像的二维数组
	:return: 逆变换后图像的二维数组
	"""
	size = img_dct.shape[0] * img_dct.shape[1]
	return scipy.fft.idct(scipy.fft.idct((img_dct - 0.5) * 1024 * np.sqrt(size),type=2,norm='ortho',axis=1),type=2,norm='ortho',axis=0)

def arnold_trans(img,a,b,shuffle_times):
	"""
	对图像进行 arnold 变换
	:param img: 表示待变换的图像的二维数组
	:param a: arnold 参数 a
	:param b: arnold 参数 b
	:param shuffle_times: 进行 arnold 变换的次数
	:return: 变换后图像的二维数组
	"""
	if(shuffle_times <= 0):
		raise ValueError("shuffle_times shoule be at least 1 but received " + str(shuffle_times))
	if(len(img.shape) != 2):
		raise ValueError("img received must be 2d-array")
	if(img.shape[0] != img.shape[1]):
		raise ValueError("img size illeagal")
	if((len(a) != shuffle_times) | (len(b) != shuffle_times)):
		raise ValueError("size of chaos array imcompatible with shuffle_times")
	n = img.shape[0]
	new_img = np.zeros((n,n))
	T = np.array([[1,b[0]],[a[0],a[0] * b[0] + 1]])
	for t in range(1,shuffle_times):
		T = np.dot(np.array([[1,b[t]],[a[t],a[t] * b[t] + 1]]),T) % n
	for x in range(n):
		for y in range(n):
			res = np.dot(T,np.array([[x],[y]])) % n
			new_img[res[0][0]][res[1][0]] = img[x][y]
	return new_img

def arnold_detrans(img,a,b,shuffle_times):
	"""
	对图像进行 arnold 逆变换
	:param img: 表示待逆变换的图像的二维数组
	:param a: arnold 逆变换参数 a
	:param b: arnold 逆变换参数 b
	:param shuffle_times: 进行 arnold 逆变换的次数
	:return: 逆变换后图像的二维数组
	"""
	if (shuffle_times <= 0):
		raise ValueError("shuffle_times shoule be at least 1 but received " + str(shuffle_times))
	if (len(img.shape) != 2):
		raise ValueError("img received must be 2d-array")
	if (img.shape[0] != img.shape[1]):
		raise ValueError("img size illeagal")
	if ((len(a) != shuffle_times) | (len(b) != shuffle_times)):
		raise ValueError("size of chaos array imcompatible with shuffle_times")
	n = img.shape[0]
	new_img = np.zeros((n, n))
	T = np.array([[a[-1] * b[-1] + 1, -b[-1]], [-a[-1], 1]])
	for t in range(1,shuffle_times):
		T = np.dot(np.array([[a[-1-t] * b[-1-t] + 1,-b[-1-t]],[-a[-1-t],1]]),T) % n
	for x in range(n):
		for y in range(n):
			res = np.dot(T,np.array([[x],[y]])) % n
			new_img[res[0][0]][res[1][0]] = img[x][y]
	return new_img

def randomshift_trans(img,a,b,c,d):
	"""
	对图像进行随机置乱变换
	:param img: 表示待变换的图像的二维数组
	:param a: 行随机置乱变换参数
	:param b: 行随机置乱变换参数
	:param c: 列随机置乱变换参数
	:param d: 列随机置乱变换参数
	:return: 变换后图像的二维数组
	"""
	if (len(img.shape) != 2):
		raise ValueError("img received must be 2d-array")
	if((len(a) != len(b)) | (len(c) != len(d))):
		raise ValueError("bad shape for parameters a,b,c,d")
	n1,n2 = img.shape[0],img.shape[1]
	new_img = np.zeros((n1, n2))
	row_refl = np.arange(n1)
	col_refl = np.arange(n2)
	for x in range(len(a)):
		row_refl[a[x]],row_refl[b[x]] = row_refl[b[x]],row_refl[a[x]]
	for y in range(len(c)):
		col_refl[c[y]],col_refl[d[y]] = col_refl[d[y]],col_refl[c[y]]
	for x in range(n1):
		new_x = row_refl[x]
		for y in range(n2):
			new_y = col_refl[y]
			new_img[new_x][new_y] = img[x][y]
	return new_img

def randomshift_detrans(img,a,b,c,d):
	"""
		对图像进行随机置乱逆变换
		:param img: 表示待逆变换的图像的二维数组
		:param a: 行随机置乱逆变换参数
		:param b: 行随机置乱逆变换参数
		:param c: 列随机置乱逆变换参数
		:param d: 列随机置乱逆变换参数
		:return: 逆变换后图像的二维数组
		"""
	if (len(img.shape) != 2):
		raise ValueError("img received must be 2d-array")
	if((len(a) != len(b)) | (len(c) != len(d))):
		raise ValueError("bad shape for parameters a,b,c,d")
	n1,n2 = img.shape[0],img.shape[1]
	new_img = np.zeros((n1, n2))
	row_refl = np.arange(n1)
	col_refl = np.arange(n2)
	for y in range(len(c)):
		col_refl[c[-y-1]],col_refl[d[-y-1]] = col_refl[d[-y-1]],col_refl[c[-y-1]]
	for x in range(len(a)):
		row_refl[a[-x-1]],row_refl[b[-x-1]] = row_refl[b[-x-1]],row_refl[a[-x-1]]
	for x in range(n1):
		new_x = row_refl[x]
		for y in range(n2):
			new_y = col_refl[y]
			new_img[new_x][new_y] = img[x][y]
	return new_img