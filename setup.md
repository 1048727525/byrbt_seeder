# byrbt_seeder运行环境安装与配置说明文档

使用的Linux基础环境：

yi@ubuntu:~$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 16.04.5 LTS
Release:	16.04
Codename:	xenial

yi@ubuntu:~$ uname -a
Linux ubuntu 4.15.0-29-generic #31~16.04.1-Ubuntu SMP Wed Jul 18 08:54:04 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

yi@ubuntu:~$ cat /proc/version
Linux version 4.15.0-29-generic (buildd@lcy01-amd64-024) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.10)) #31~16.04.1-Ubuntu SMP Wed Jul 18 08:54:04 UTC 2018

## 一、Transmission下载器

### 安装过程

```shell
sudo apt-get install transmission-daemon 
```

### 配置文件

/etc/transmission-daemon/settings.json

### 运行和停止

启动：

```sh
sudo service transmission-daemon start
```

停止：

```shell
sudo service transmission-daemon stop
```

### 其他说明

web端：http://127.0.0.1:9091/transmission/web/

源码：https://github.com/transmission/transmission

参考：https://blog.csdn.net/stripe3385/article/details/50482996/



## 二、Python3.x

Tip： Ubuntu系统默认已经安装好了一些版本的python环境，可以使用以下命令查看python的指向。

```shell
ls -l /usr/bin | grep python
```

### 安装基础环境

解决python运行时报错：no module named'_bz2'

```shell
sudo apt-get install libbz2-dev
```

参考：https://www.jianshu.com/p/58d6bc42bfd1

### 安装python3.7过程

1.下载安装包

```shell
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
```

2.解压安装包

```shell
tar -zxvf Python-3.7.0.tgz
```

3.配置 configure 

```shell
cd Python-3.7.0

./configure
# 或者
./configure --prefix=/usr/local/python3.7.0
```

4.编译及测试（需要安装make）

```shell
make

make test
```

5.安装

```shell
sudo make install
```

若步骤5执行的是 ./configure，则安装后可执行文件默认放在/usr /local/bin，库文件默认放在/usr/local/lib，配置文件默认放在/usr/local/include，其它的资源文件放在/usr /local/share

若步骤5执行的是./configure --prefix=/usr/local/python3.7.0，则可执行文件放在/usr /local/python3.7.0/bin，库文件放在/usr/local/python3.7.0/lib，配置文件放在/usr/local/python3.7.0/include，其它的资源文件放在/usr /local/python3.7.0/share

6.配置环境变量（选）

若步骤3执行“./configure --prefix=/usr/local/python3.7.0”，则需要添加环境变量。步骤3是“./configure”的跳过此步骤。

 添加环境变量 

```shell
PATH=$PATH:$HOME/bin:/usr/local/python3.7.0/bin
```

 查看环境变量 

```shell
echo $PATH
```

7.查看安装目录并测试

python3.7安装到了/usr/local/lib/

（若步骤5执行./configure --prefix=/usr/local/python3.7.0，python3.7安装到/usr/local/python3.7.0/lib/） 

测试python3.7

```shell
python3.7
```

### 建立python3默认指向为python3.x

本程序使用的环境在python3.x下均可运行，系统调用python编译器时使用的命令脚本均为“python3”，因此需要建立“python3”的命令指向，在已经装有python3.x的计算机环境下，可以使用以下命令查看“python3”的命令指向

```shell
ls -l /usr/bin | grep python3

#或者
python3 --version
```

若窗口的打印输出列表中不存在“python3”的命令指向，或者已经存在但是指向不为期望版本的python，则需要继续执行以下命令。

1.删除原有链接（更新命令指向时使用，否则跳过本步骤）

```shell
rm /usr/bin/python3
```

2.建立新链接

由于python3.7是自己安装的，不在/usr/bin下，而在usr/local/bin或者/usr/local/python3.7.0/bin下（取决于前面执行的./configure还是./configure --prefix=/usr/local/python3.7.0。因此需要先加一条软链接并且把之前的python命令改为python.bak，同时pip也需要更改。依次执行以下命令：

① 若python3.7安装时，执行的是./configure，则：

```shell
mv /usr/bin/python /usr/bin/python.bak
ln -s /usr/local/bin/python3 /usr/bin/python3
mv /usr/bin/pip /usr/bin/pip.bak
ln -s /usr/local/bin/pip3 /usr/bin/pip3
```

② 若python3.7安装时，执行的是./configure --prefix=/usr/local/python3.7.0，则为：

```shell
mv /usr/bin/python /usr/bin/python.bak
ln -s /usr/local/python3.7.0/bin/python3.7 /usr/bin/python3
mv /usr/bin/pip /usr/bin/pip.bak
ln -s /usr/local/python3.7.0/bin/pip3 /usr/bin/pip3
```

3.测试链接

```shell
python3
```



参考：https://blog.csdn.net/u014775723/article/details/85213793



## 三、python库文件的安装

### python代码中的import列表

| 导入的外部包                  |                                                |
| ----------------------------- | ---------------------------------------------- |
| import json                   | from requests.cookies import RequestsCookieJar |
| import requests               | import numpy as np                             |
| import urllib.request         | import scipy.special                           |
| import re                     | import math                                    |
| import csv                    | import sys                                     |
| from bs4 import BeautifulSoup | import pandas as pd                            |
| from scrapy import Selector   | import shutil                                  |
| from lxml import etree        | import pickle                                  |
| import os                     | from sklearn.svm import SVR                    |
| import argparse               | import matplotlib.pyplot as plt                |
| import time                   | import cv2 as cv                               |
| import socket                 |                                                |

其中，需要导入的包有：

| 需要导入的包列表 |            |
| ---------------- | ---------- |
| requests         | scipy      |
| bs4              | pandas     |
| scrapy           | sklearn    |
| lxml             | matplotlib |
| numpy            | cv2        |

### 更换pip源

```shell
cd ~
mkdir .pip
sudo vim .pip/pip.conf
```

写入文件内容：

```json
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com
```

参考：https://blog.csdn.net/w5688414/article/details/82832292

### 导入命令

```shell
sudo pip3 install requests

sudo pip3 install bs4

sudo pip3 install scrapy

sudo pip3 install lxml

sudo pip3 install numpy

sudo pip3 install scipy

sudo pip3 install pandas

sudo pip3 install sklearn

sudo pip3 install matplotlib

sudo pip3 install opencv-python
```

或者

```shell
sudo pip3 install requests bs4 scrapy lxml numpy scipy pandas sklearn matplotlib opencv-python
```



### 异常处理

出现如下报错信息：

```shell
subprocess.CalledProcessError: Command '('lsb_release', '-a')' returned non-zero exit status 1.
```

解决方法：

```shell
sudo find / -name lsb_release
sudo rm -rf /usr/bin/lsb_release
```

参考：https://blog.csdn.net/itdabaotu/article/details/83142918



## 四、安装Qt5.9.8

1.下载qt安装文件

```shell
wget http://download.qt.io/official_releases/qt/5.9/5.9.8/qt-opensource-linux-x64-5.9.8.run
```

2.修改文件权限

```shell
chmod +x qt-opensource-linux-x64-5.9.8.run 
```

3.运行安装程序

```shell
./qt-opensource-linux-x64-5.9.8.run 
```

4.Install g++

Open a terminal and execute the following command to install g++:

```shell
sudo apt-get install build-essential
```

5.Install generic font configuration library - runtime

Open a terminal and execute the following command to install the full runtime files for the generic font configuration library:

```shell
sudo apt-get install libfontconfig1
```

6.Install OpenGL libraries

Execute the following command to install OpenGL libraries:

```shell
sudo apt-get install mesa-common-dev
```

Note: Just installing the above-mentioned mesa-common-dev kit is not sufficient for more recent Ubuntu versions. Based on a comment in the Qt forum[[1\]](https://wiki.qt.io/Install_Qt_5_on_Ubuntu#cite_note-1) an additional package needs installation. Execute following command:

```shell
sudo apt-get install libglu1-mesa-dev -y
```

参考：https://wiki.qt.io/Install_Qt_5_on_Ubuntu



### 异常处理

解决qmake找不到问题：

1.接下来就需要配置环境变量了,和Windows平台下的环境变量原理是一样的,首先请回忆上面步骤1中,Qt5.8的安装位置.在我的系统中是在/home/useraccount/Qt5.8.0,编辑环境变量

```shell
sudo vim /etc/bash.bashrc
```

2.在环境变量中加入以下路径：

```shell
export QIDIR=/home/useraccount/Qt5.8.0/5.8/gcc_64/
export PATH=$QTDIR/bin:$PATH
export MANPATH=$QTDIR/man/:$MANPATH
export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH
```

3.保存后,在终端输入source .bashrc来更新环境变量

```shell
source .bashrc
```

参考：https://www.jianshu.com/p/798d8b0ba58d



## 五、运行程序

1.修改文件夹及其中的文件权限

```shell
sudo chmod 777 byrbt_seeder/ -R
```

2.更改脚本文件编码

由于脚本是在window环境下编写的，传到linux服务器上后，doc下的文本内容格式和unix下的格式有所不同。比如dos文件传输到unix系统时，会在每行的结尾多一个^M结束符，导致脚本文件不能被正确运行，因此需要更改文件的编码格式，采用如下命令：

```shell
sudo apt-get install vim

vim work.sh
:set fileformat=unix
:wq
```

或者

```shell
sudo apt-get install dos2unix

dos2unix work.sh
```

参考：https://blog.csdn.net/u013948858/article/details/79637851

3.打开配置文件bt_auto.conf，修改种子监视文件夹和资源下载文件夹路径（必须改为绝对地址）

```shell
#基础设置
watch_dir="./watch"   # 种子监视文件夹
download_dir="./download"     # 资源下载文件夹
```

4.运行程序

```shell
./work.sh
```



## 备注：

1) Ubuntu 16.04 已经自动安装了unzip 软件，解压命令：

```shell
unzip FileName.zip
```

2) 如果没有安装unzip,可以使用下面的命令安装：

```shell
sudo apt install unzip
```

3) 安装unrar软件

```shell
sudo apt install unrar
```

4) 解压rar文件：

```shell
unrar x FileName.rar
```


