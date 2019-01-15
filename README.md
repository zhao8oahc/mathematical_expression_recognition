# 机器学习工程师纳米学位
## 毕业项目——算式识别

### 项目描述

本项目需要使用深度学习来识别一张图片中的手写体算式内容，最低达到90%的准确率。并且为了能够让他人使用此 OCR 服务，使用了Flask将模型部署到服务器上。


此项目要求的计算量较大，使用了亚马逊 p3.2xlarge 云服务器

### 数据

数据集可以通过这个链接下载：

[https://s3.cn-north-1.amazonaws.com.cn/static-documents/nd009/MLND+Capstone/Mathematical_Expression_Recognition_train.zip](https://s3.cn-north-1.amazonaws.com.cn/static-documents/nd009/MLND+Capstone/Mathematical_Expression_Recognition_train.zip)

此数据集包含10万张图片，每张图里面都有一个算式。

* 可能包含 `+-*` 三种运算符
* 可能包含一对括号，也可能不包含括号
* 每个字符都可能旋转，所以 `+` 号可能长得像我们平时手写的 `*` 号，不过 `*` 号有六个瓣

![](example.jpg)

