# 网络空间安全概论-图像加密
## 代码运行环境
Python 的版本为 3.7。各个库的版本请查看`requirements.txt`。
## 项目文件的构成
项目文件的部分目录树如下所示。
```
/
│  fatcat.jpg
│  README.md
│  requirements.txt
│
├─.idea
│
└─src
    │  img_transform.py
    │  main_arnold.py
    │  main_arnold_nodct.py
    │  main_randomshift.py
    │  main_randomshift_nodct.py
    │  secret.png
    │  secret_nodct.png
    │  standard_aes.py
    │  standard_des.py
    │  time_analyse.py
    │  util.py
    │  yiyan_test.py
    │  __init__.py
    │
    ├─fatcat_example
    │  ├─arnold
    │  └─randomshift
    │
    ├─result
    │
    └─__pycache__
```

其中：

- `/fatcat.jpg`是测试使用的图片，你也可以在代码文件中更改路径，指定为你要进行加解密的图片。
- `/src`是源代码的文件夹。
    - `/src/util.py`提供了一些方法，进行图像的读写、展示以及混沌随机数的生成。
    - `/src/img_transform.py`提供了一些方法，进行图像的变换（包含 Arnold 变换和随机置乱变换）。
    - `/src/standard_aes.py`提供了 AES 加解密的代码。
    - `/src/standard_des.py`提供了 DES 加解密的代码。
    - `/src/yiyan_test.py`验证了 AES/DES 加密代码的正确性。
    - `/src/main_arnold.py`基于 DCT 变换域测试了 Arnold 加解密算法。
    - `/src/main_arnold_nodct.py`基于空间域测试了 Arnold 加解密算法。
    - `/src/main_randomshift.py`基于 DCT 变换域测试了随机置乱加解密算法。
    - `/src/main_randomshift_nodct.py`基于空间域测试了随机置乱加解密算法。
    - `/src/time_analyse.py`比较了空间域中 Arnold 加解密算法、随机置乱加解密算法、AES 加解密算法、DES 加解密算法的执行时间。

## 输入
文件`/src/main_*.py`用于图像的加解密。这些文件中都存在下面的代码：
```py
img = util.read_img("../fatcat.jpg")
```
更改路径以自定义需要进行加解密的图像。
## 输出
直接运行`/src/main_*.py`，即可看到加解密过程中的一系列图像。
## 测试样例
当前所有的`/src/main_*.py`都已经配备好图像路径为`"../fatcat.jpg"`，可以直接进行测试