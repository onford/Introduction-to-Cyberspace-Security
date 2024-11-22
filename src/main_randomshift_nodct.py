import src.img_transform as img_transform
import src.util as util
import numpy as np
import cv2

if __name__ == '__main__':
	# ============================================================
	# 加解密功能测试
	# ============================================================
	# 读取 1:1 标量图图像
	img = util.read_img("../fatcat.jpg")
	util.show_img(img,"原图像") # 展示该图像

	# 获取 4 组随机数
	n1,n2 = 3915,3916
	a,b = util.get_chaos(n1,img.shape[0],114)
	c,d = util.get_chaos(n2,img.shape[1],514)

	# 根据伪随机数，对图像进行随机置乱加密
	secreted_img = img_transform.randomshift_trans(img,a,b,c,d)
	util.show_img(secreted_img,"加密后图像")

	# 根据伪随机数，对加密后的图像进行解密
	solved_img = img_transform.randomshift_detrans(secreted_img,a,b,c,d) # 随机置乱逆变换
	util.show_img(solved_img,"解密后的图像")

	# ============================================================
	# 鲁棒性测试
	# ============================================================
	# 从存储中加载图片

	# 对该图片加入干扰
	mode = 2 # 1 代表随机扰动，2代表涂抹攻击，3代表裁剪攻击
	if(mode == 1):
		len1, len2 = secreted_img.shape[0], secreted_img.shape[1]
		for _ in range(int(.1 * len1 * len2)):
			x = int(np.random.rand() * len1)
			y = int(np.random.rand() * len2)
			secreted_img[x][y] = np.uint8(np.random.rand() * 256)
	elif(mode == 2):
		cv2.imwrite("secret_nodct.png", secreted_img)
		input("对 secret_nodct.png 进行涂抹攻击后按下回车")
		secreted_img = util.read_img("secret_nodct.png")
	else:
		len1, len2 = secreted_img.shape[0], secreted_img.shape[1]
		for x in range(len1):
			for y in range(len2//5):
				secreted_img[x][len2 - 1 - y] = secreted_img[x][y]
	util.show_img(secreted_img,"干扰后的密文图片")
	util.show_img(img_transform.randomshift_detrans(secreted_img, a, b, c,d),"攻击后还原的图像")