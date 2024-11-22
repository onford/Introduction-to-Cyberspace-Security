import src.img_transform as img_transform
import src.util as util
import numpy as np

if __name__ == '__main__':
	# ============================================================
	# 加解密功能测试
	# ============================================================
	# 读取 1:1 标量图图像
	img = util.read_img("../fatcat.jpg")
	util.show_img(img,"原图像") # 展示该图像

	# 对图像进行离散余弦变换
	dct_img = img_transform.dct_img(img)
	util.show_img(dct_img,"离散余弦变换后图像")

	# 获取 4 组随机数
	n1,n2 = 3915,3916
	a,b = util.get_chaos(n1,img.shape[0],114)
	c,d = util.get_chaos(n2,img.shape[1],514)

	# 根据伪随机数，对 dct 后的图像进行随机置乱加密
	secreted_img = img_transform.randomshift_trans(dct_img,a,b,c,d)
	util.show_img(secreted_img,"加密后图像")

	# 根据伪随机数，对加密后的图象进行解密（随机置乱逆变换以及 idct）
	dearnold_img = img_transform.randomshift_detrans(secreted_img,a,b,c,d) # 随机置乱逆变换
	solved_img = img_transform.idct_img(dearnold_img) # idct
	util.show_img(solved_img,"解密后的图像")

	util.save_secret(secreted_img,"secret.png") # 以图像形式存储密文图片

	# ============================================================
	# 鲁棒性测试
	# ============================================================
	# 从存储中加载图片
	img = util.load_secret("secret.png",False)
	util.show_img(img,"外存形式的图片")

	# 对该图片加入干扰
	len1, len2 = img.shape[0], img.shape[1]
	for _ in range(100):
		x = int(np.random.rand() * len1)
		y = int(np.random.rand() * len2)
		img[x][y] = np.uint8(np.random.rand() * 256)
	util.show_img(img,"外存形式干扰后的图片")

	# 转化为内存形式
	img = util.to_memory(img)
	util.show_img(img,"内存形式干扰后的图片")

	# 初步去除非法的像素点
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if((str(img[x][y]) == 'nan') | (img[x][y] < 0.5-255/512) | (img[x][y] > 0.5+255/512)):
				img[x][y] = 0.5
	util.show_img(img,"去除部分错误点后的图片")

	util.show_img(img_transform.idct_img(img_transform.randomshift_detrans(img, a, b, c,d)),"攻击后还原的图像")