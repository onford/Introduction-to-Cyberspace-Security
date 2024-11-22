import src.util as util
import src.img_transform
import src.standard_aes as aes
import src.standard_des as des

# 测试一下文心一言生成的 AES 和 DES 代码的正确性

def test_aes(src):
	img = util.read_img(src)
	len1,len2 = img.shape[0],img.shape[1]
	key, iv, data, size = aes.encrypt(img)
	img = aes.decrypt(key,iv,data,size)
	util.show_img(img.reshape((len1,len2)),"Test for AES")

def test_des(src):
	img = util.read_img(src)
	len1, len2 = img.shape[0], img.shape[1]
	key, data, size = des.encrypt(img)
	img = des.decrypt(key, data, size)
	util.show_img(img.reshape((len1, len2)), "Test for DES")

if __name__ == '__main__':
	test_aes("../fatcat.jpg")
	test_des("../fatcat.jpg")