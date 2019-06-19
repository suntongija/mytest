# web服务

## Nginx

### Nginx平滑升级

.configure --with ....添加除默认功能意外的模块：到源码包src中找到相对应的源码

make把选中的源码编译成二进制数：<u>升级即升级src中的源码</u>

平滑升级过程：

1.在新的源码包添加模块后编译（make）

2.备份老的Nginx主程序，并使用编译好的新版本主程序替换老版本的。

3.make upgrade： 

nginx -t 检查nginx配置问题 

```
kill -USR2  `cat /usr/local/nginx/logs/nginx.pid` //抓取nginx的PID值给进程传递信号
```

使用 ps -aux | grep nginx 可以查看到nginx新旧进程同时存在

logs文件夹内会出现nginx.pid(新进程PID号)  和 nginx.pid.oldbin原进程PID号

杀掉旧进程:

```
kill -QUIT `cat /usr/local/nginx/logs/nginx.pid.oldbin`
```



### Nginx常用模块

**用户认证:(server下添加)**

    auth_basic "TEST FIRST:";     //添加标题
    auth_basic_user_file "/usr/local/nginx/pass";   添加pass文件
```
htpasswd -c /usr/local/nginx/pass tom    //http-tools软件
//-c create建立新文件（第一次建立pass文件追加不需要加-c） 
//输入两次密码
```



**--with-http_ssl_module  加密网站**

加密方式:

对称加密（AES，DES）   123 ---->123 加密和解密相同（不适合网路加密，只适合单击加密）

非对称加密（RSA，DSA）  123--->u9_ 加密和解密完全不同（应用于网络加密）

信息摘要（MD5，sha256）主要应用在数据完整性校验

MD5值只与文件内容有关，与文件名，时间无关

对称加密和非对称加密都是同等安全的

公钥：用户使用网站给的公钥加密自己的用户名密码(证书

私钥：私钥为网站所有，只有服务端可以解密用户的输入

    ssl_certificate      cert.pem;         #这里是证书文件
    ssl_certificate_key  cert.key;         #这里是私钥文件
    ssl_session_cache    shared:SSL:1m; 
    //1M大约可以存4000个Session
    ssl_session_timeout  5m;    //超时时间5分钟
    ssl_ciphers  HIGH:!aNULL:!MD5; //网站加密不能为空，不能用MD5
    ssl_prefer_server_ciphers  on;  //优先使用服务器的加密套件


**--with-stream  nginx实现TCP/UDP调度器功能(4层协议)**

ngx_stream_core_module模块

nginx可以做7层代理也可以做4层调度

```
stream {
         upstream backend {
           server 192.168.2.100:22; //后端SSH服务器的IP和端口
           server 192.168.2.200:22;
}
server {
             listen 12345;  //修改Nginx监听的端口,  安全性高
             proxy_connect_timeout 1s;
             proxy_timeout 3s;
             proxy_pass backend;
        }
}
```



**--with-http_stub_status_module 开启状态页面模块**

```
location /status {
                     stub_status on;
                     #allow IP地址;
                     #deny IP地址;  //deny all禁止所有
}
```

10（三次握手） 10 （处理数量：安全策略可能过滤）3（请求数量） 

Reading: 0 （现在在拆几个包读几个包）Writing: 1 Waiting: 0
Active connections：当前活动的连接数量。
Accepts：已经接受客户端的连接总数量。
Handled：已经处理客户端的连接总数量。
（一般与accepts一致，除非服务器限制了连接数量）。

Requests：客户端发送的请求数量。
Reading：当前服务器正在读取客户端请求头的数量。
Writing：当前服务器正在写响应信息的数量。
Waiting：当前多少客户端在等待服务器的响应。

```
keepalive_timeout  65;   //一次连接多次请求,65s保持
//减少连接服务器消耗的资源, 但太大容易让大量连接占用服务器资源
//网页关闭,但当前活动连接数量不会立即发生变化因为没到超时时间
```



**反向代理功能:**

```
修改/usr/local/nginx/conf/nginx.conf配置文件
[root@proxy ~]# vim /usr/local/nginx/conf/nginx.conf
.. ..
http {
.. ..
#使用upstream定义后端服务器集群，集群名称任意(如webserver)
#使用server定义集群中的具体服务器和端口
upstream webserver {
                server 192.168.2.100:80;
                server 192.168.2.200:80;
        }
.. ..
server {
        listen        80;
        server_name  localhost;
            location / {
#通过proxy_pass将用户的请求转发给webserver集群
            proxy_pass http://webserver;
        }
}
```

```
upstream webserver {
                ip_hash;
                server 192.168.2.100 weight=1 max_fails=1 fail_timeout=30;
                server 192.168.2.200 weight=2 max_fails=2 fail_timeout=30;
                server 192.168.2.101 down;
        }
#weight设置服务器权重值，默认值为1
#max_fails设置最大失败次数
#fail_timeout设置失败超时时间，单位为秒
#down标记服务器已关机，不参与集群调度 节省带宽资源

#通过ip_hash设置调度规则为：相同客户端访问相同服务器
#hash加密IP：echo IP 前三个8位| md5sum 结果是16进制数，数据不变hash值一直不变    将结果对二取余，结果0将服务转给web1  ，结果1 将服务转给web2
```

#通过ip_hash设置调度规则为：相同客户端访问相同服务器
           ip_hash;   //hash加密IP：echo IP 前三个8位| md5sum 结果是16进制数，数据不变hash值一直不变    将结果对二取余，结果0将服务转给web1  ，结果1 将服务转给web2



### Nginx 与FastCGI连接方式(套接字)

Nginx连接FastCGI的方式有两种:  unix domain socket   TCP

unix domain socket: IPC(inter-process communication 进程间通信) socket 用于实现同一主机上的进程间通信.

TCP:使用端口127.0.0.1:9000端口连接

套接字:

修改PHP配置文件:

```
]# vim /etc/php-fpm.d/www.conf
;listen = 127.0.0.1:9000
listen = /dev/shm/php-cgi.sock  
//路径/dev/shm是tmpfs,在内存上,要比磁盘路径快得多
```

修改Nginx配置文件:

```
fastcgi_pass unix:/dev/shm/php-cgi.sock;
#fastcgi_pass   127.0.0.1:9000;
//重启php-fpm , Nginx 服务
```

优点:unix socket 套接字方式比tcp的方式快,消耗资源少,无需经过本地回环接口,找端口,走TCP协议.

缺点:1.进程间通信要求Nginx和php-fpm搭建到同一台服务器.          2.并发连接数爆发时,会产生大量的长时缓存,有可能直接出错并不反回异常,不如面向连接协议稳定.

### Nginx 优化

Nginx并发量:

```
worker_processes  1;  //修改与CPU内核数量一致
events {
worker_connections  65535;  //尽量写高，达不到没关系
use epoll;  //处理模型  选项 epoll（nginx默认设置） select（http默认设置）
}
```

