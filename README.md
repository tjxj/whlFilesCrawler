# 在公司内网搭建 pip 镜像站
auto download whl files from lfd.uci.edu


很多公司的生产环境不能联网，但是又需要安装Python搞点事情，各种包及其依赖安装起来就麻烦极了。本文咱们就折腾一番，将本地环境搬家到内网，在内网搭建一套 pip 镜像站。

## 下载包
批量导出当前开发环境的包信息
```
pip freeze > requirements.txt
```

下载requirements内的包及其依赖到【某文件夹】
```
pip download -r requirements.txt
```
![.whl文件](https://my-wechat.oss-cn-beijing.aliyuncs.com/image_20210430202642.png)


只有本地对应版本的Python才能安装这些包，如果想要要搭建pip镜像站并兼容更多版本的Python怎么办呢？

这里有一个网站  
https://www.lfd.uci.edu/~gohlke/pythonlibs/  
里面有常用的532个包，每一个对应的有各种版本的whl文件，一共6000+

这就要爬虫了，我写了一个，代码就不贴了，已上传github  

![https://github.com/tjxj/whlFilesCrawler](https://my-wechat.oss-cn-beijing.aliyuncs.com/image_20210430212419.png)

## 建立索引

本地安装pip2pi
```
pip install pip2pi
```

命令行切换到下载的 .whl文件夹，建立索引（自动生成了index.html）
```
dir2pi -S 【某文件夹】
```

然后文件夹内就出现了一个simple文件夹，这里的内容就和阿里、清华、豆瓣的源差别没那么大了。

## nginx发布镜像源

准备好Linux or Windows 的 Nginx 安装程序  

http://nginx.org/en/download.html

将【某文件夹】和Nginx 安装包一起copy到内网的服务器

Nginx 安装很简单，Terminal里执行nginx不报错就算大功告成。

找到nginx.conf文件，仅需修改如下几个内容，其他的都不需要动：

```
server{
listen 80；
server_name 你的IP地址
root 【某文件夹】的路径
}
```
重启nginx服务器
```
# Linux
sudo systemctl restart nginx
# Windows
nginx -s reload
```

浏览器打开http://你的IP/simple

![](https://my-wechat.oss-cn-beijing.aliyuncs.com/image_20210430220313.png)

现在如果内网的服务器墙是通的，其他机器应该也能访问这个网址，pip 镜像站就搭建好了，so easy。

如果内网内的主机想要pip安装所需的包，还需要配置一下pip

在 Linux & macOS 中，配置需要写到 ~/.pip/pip.conf 文件中；Windows 中，配置文件位置为 %HOMEPATH%\pip\pip.ini，%HOMEPATH% 即你的用户文件夹，一般为“\Users\<你的用户名>”，具体值可以使用 echo %HOMEPATH% 命令查看。

通常你需要手动创建对应的目录和文件，然后写入下面的内容：
```
[global]
index-url = http://你的IP/simple
[install]
trusted-host = 你的IP
```

内网的主机安装Python的包及其依赖
```
pip install [所需的包名]
```

## reference

https://github.com/Light-City/AutoDownloadWhl