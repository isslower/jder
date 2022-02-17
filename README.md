

###个人学习demo，请勿传播使用，24小时内请删除！！！
<br>

#####根据此基础进行二开
>sh <(curl -s https://gitee.com/shoujiyanxishe/shjb/raw/main/jd/ptkey.sh)

#配置参数

1.编辑login.html第37行，替换成自己的服务器ip  
2.编辑config.ini文件，添加ql参数


#部署界面

1.下载

```shell

git clone https://github.com/pigKinger/jder.git /root/jder
```

2.安装httpd


```shell
#检查是否安装httpd
rpm -qa | grep httpd
#如果没安装，进行安装
yum -y install httpd
#启动
service httpd start
```
3.复制页面
```shell
cd /root/jder
cp jder/html/login.html /var/www/html
```
4.启动web  
打开web页面，访问地址（ip:80/login.html）



#启动后台
```shell
cd /root/jder
chmod 777 getcode.sh inputcode.sh
nohup python3 jdcode.py  1>"$(pwd)"/log 2>&1 &
```


