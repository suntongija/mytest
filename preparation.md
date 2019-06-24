# web服务

## Nginx

### Nginx与Apache区别

同步:当一个同步调用发出去后,调用者要一直等待调用结果的通知后,才能进行后续的执行;

异步:当一个异步调用发出去后,调用者不能立即得到调用结果的返回;

异步调用想获得结果的方式:1.主动轮询异步调用的结果;   2. 被调用方通过callback来通知调用方调用结果;

阻塞:阻塞调用在发出后,在消息返回之前,当前进/线程会被挂起,直到有消息返回,当前进/线程才会被激活;

非阻塞:非阻塞调用在发出去后,不会阻塞当前进/线程,而会立即返回;

Nginx:异步非阻塞

I/O多路复用:多个I/O可以复用一个进程,允许进程同时检查 多个fd(文件描述符),以找出其中可执行I/O操作的fd.

I/O复用模式:

1.select():可观察许多流的I/O事件,在空闲时,会把线程阻塞掉,当有流事件需要处理时,进程采用轮询的方式来检查一遍所有fd是否就绪,当fd数量较多时,性能欠佳.

2.epoll():能更高效的检查大量fd,当连接有I/O流事件产生的时候,epoll就会告诉进程哪个连接有I/O流事件产生,然后进程就去处理这个事件.即进程对这些流的操作都是有意义的

在一个Web服务中，延迟最多的就是等待网络传输。nginx在启动后，会有一个master进程和多个worker进程。master进程主要用来管理worker进程，包含：接收来自外界的信号，向各worker进程发送信号，监控worker进程的运行状态，当worker进程退出后(异常情况下)，会自动重新启动新的worker进程。而基本的网络事件，则是放在worker进程中来处理了。在一个请求需要等待的时候，worker可以空闲出来处理其他的请求，少数几个worker进程就能够处理大量的并发。

Nginx服务器每进来一个request，会有一个worker进程去处理。但不是全程的处理,处理到可能发生阻塞的地方。比如向后端服务器转发request，并等待请求返回。那么，这个处理的worker不会挂起，他会在发送完请求后，注册一个事件：“如果upstream返回了，告诉我一声，我再接着干”。然后worker进程去处理其他事件, 此时，如果再有request 进来，他就可以很快再按这种方式处理。而一旦上游服务器返回了，就会触发这个事件，worker才会来接手，这个request才会接着往下走。<u>*这就是异步非阻塞callback的方式*</u>.

Apache:同步阻塞

每一个连接,apache就会创建一个进程,每隔进程内单线程,最多创建256个进程.使用select()复用模式;

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

### Fastcgi(php-fpm)

php-fpm（服务）：PHP进程管理的服务 **9000端口**
 <u>php-fpm是 FastCGI 的实现，并提供了进程管理的功能。</u> 
        进程包含 **master** 进程和 **worker** 进程两种进程 
        master 进程只有一个，负责监听端口，接收来自 Web Server 的请求，而 <u>worker 进程则一般有多个</u>(具体数量根据实际需要配置)，每个进程内部都嵌入了一个 PHP 解释器，是 PHP 代码真正执行的地方。
 FastCGI是语言无关的、可伸缩架构的CGI开放扩展，其主要行为是将CGI解释器进程保持在内存中并因此获得较高的性能。众所周知，<u>CGI解释器的反复加载是CGI性能低下的主要原因</u>，CGI解释器保持在内存中并接受FastCGI进程管理器调度，则可以提供良好的性能、伸缩性、Fail-Over特性等等
如果
将脚本传送9000端口自动执行，能同时接收8个脚本

```
[root@proxy etc]# vim /etc/php-fpm.d/www.conf
[www]:
listen = 127.0.0.1:9000      //PHP端口号
pm.max_children = 32         //最大进程数量根据服务器内存配置以及需求
pm.start_servers = 15        //最小进程数量
pm.min_spare_servers = 5     //最少需要几个空闲着的进程
pm.max_spare_servers = 32    //最多允许几个进程处于空闲状态
```

### 地址重写

```
#这里，~符号代表正则匹配(;模糊匹配)，*符号代表不区分大小写
if ($http_user_agent ~* firefox) {            //识别客户端firefox浏览器   ～正则，*忽略大小写
rewrite / /test.html    //防止访问IP出现找不到网页
rewrite ^(.*)$ /firefox/$1;
}
//根据客户端浏览器不同访问不同目录下的网站
```



### Nginx 与FastCGI连接方式(套接字)

Nginx连接FastCGI的方式有两种:  unix domain socket   TCP

unix domain socket: IPC(inter-process communication 进程间通信) socket 用于实现同一主机上的进程间通信.

TCP:使用端口127.0.0.1:9000端口连接

*套接字:*

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

*TCP协议:*(实现)

```
fastcgi_pass   127.0.0.1:9000;  #将请求转发给本机9000端口
```



### Nginx 优化

#### Nginx并发量:

```
worker_processes  1;  //修改与CPU内核数量一致(进程数)
events {
worker_connections  65535;  //尽量写高，达不到没关系
use epoll;  //处理模型  选项 epoll（nginx默认设置） select（http默认设置）
}
```

优化内核参数（最大文件数量默认1024）：在计算机中最大打开1024个文件，影响所有软件

```
[root@proxy ~]# ulimit -a
ulimit -a  ------>open files                      (-n) 1024  //-a 查所有
[root@proxy ~]# ulimit -Hn 100000    //H硬限制 临时有效
[root@proxy ~]# ulimit -Sn 100000    //S软限制 临时有效
```

永久有效需要改配置文件:

```
[root@proxy ~]# vim /etc/security/limits.conf
    .. ..

*       soft    nofile            100000

*       hard    nofile            100000
*代表用户名和组
```



#### 解决414问题(地址过长)

```
client_header_buffer_size    1k;     //默认请求包头信息的缓存    
large_client_header_buffers  4 4k;   
//最大请求包头部信息的缓存个数与容量16K(真实环境)每个人给16k
//设置太大消耗太大内存资源
```

#### 设置静态网页缓存

```
location ~* \.(jpg|jpeg|gif|png|css|js|ico|xml)$ {
                expires        30d;
    }
```

静态网站缓存,查看网页缓存: firefox地址栏输入 about:cache   在disk里面List Cache Entries中可以查寻到每条缓存信息

#### 日志切割

日志切割:在日志文件没有太大时提前切割(access.log error.log)

```
mv access.log access.log.bak
kill -USR1 +nginx进程号  //kill严格来讲是发送信号给某个进程
```

```shell
[root@proxy ~]# vim /usr/local/nginx/logbak.sh
#!/bin/bash
date=`date +%Y%m%d`
logpath=/usr/local/nginx/logs
mv $logpath/access.log $logpath/access-$date.log
mv $logpath/error.log $logpath/error-$date.log
kill -USR1 $(cat $logpath/nginx.pid)
```

```
[root@proxy ~]# crontab -e
03 03 * * 5  /usr/local/nginx/logbak.sh
```



#### 网页压缩

网页压缩减少数据流量,节省访问时间,浏览器自带解压缩功能

```
[root@proxy ~]# cat /usr/local/nginx/conf/nginx.conf
http {
.. ..
gzip on;                            //开启压缩
gzip_min_length 1000;                //小文件不压缩
gzip_comp_level 4;                //压缩比率
gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
                                    //对特定文件压缩，类型参考/usr/local/nginx/conf/mime.types
.. ..
}
```

多媒体文件:jpg,png,avi,mp3,mp4 已经压缩过了不需要再压缩

压缩文本文档 txt html css pdf  xls比较适合压缩

#### 服务器内存缓存:

```
如果需要处理大量静态文件，可以将文件缓存在内存，下次访问会更快。
http { 
open_file_cache          max=2000  inactive=20s;
        open_file_cache_valid    60s;
        open_file_cache_min_uses 5;
        open_file_cache_errors   off;
//设置服务器最大缓存2000个文件句柄，关闭20秒内无请求的文件句柄
//文件句柄的有效时间是60秒，60秒后过期
//只有访问次数超过5次会被缓存
} 
```



### Nginx安全

#### 禁用 --without-http_autoindex_module模块

访问页面路径不加网页名，会将文件夹下的所有网页都列出存在风险

```
[root@host50 nginx-1.12.2]# ./configure --without-http_autoindex_module
[root@host50 nginx-1.12.2]# make && make install
```

#### 修改nginx的版本

```
[root@host50 nginx-1.12.2]# curl -I http://192.168.4.50 //获取版本号
Server: nginx/1.12.2   //查看到nginx版本
[root@host50 nginx-1.12.2]# nginx -s stop
[root@host50 nginx-1.12.2]# vim src/http/ngx_http_header_filter_module.c
static u_char ngx_http_server_string[] = "Server: hehe" CRLF;
static u_char ngx_http_server_full_string[] = "Server: hehe "  CRLF;
static u_char ngx_http_server_build_string[] = "Server: hehe "  CRLF;
[root@host50 nginx-1.12.2]# ./configure --without-http_autoindex_module
[root@host50 nginx-1.12.2]# make && make install
[root@host50 nginx-1.12.2]# curl -I 192.168.4.50
Server: hehe
```



#### 限制并发（DDOS攻击）

***ngx_http_limit_req_module***  默认安装的

```
[root@host50 nginx-1.12.2]# vim /usr/local/nginx/conf/nginx.conf
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
//http下添加
limit_req zone=one burst=5;
//server下添加
```

——将客户端IP信息存储名称为one的共享内存，空间为10M
——1M可以存储8千个IP的信息，10M存8万个主机状态
——每秒中仅接受1个请求，多余的放入漏斗 rate=1r/s
——漏斗超过5个则报错





# iptables 防火墙

![防火墙报文流向](/root/图片/防火墙报文流向.png)

报文流向:

到本机进程的报文:PREROUTING→INPUT

由本机转发的报文:PREROUTING→FORWARD→POSTROUTING

由本机的某进程发出的报文(通常为响应报文) :OUTPUT →POSTROUTING


|  raw   | 状态跟踪表                          |              PREROUTING OUTPUT              |
| :----: | ----------------------------------- | :-----------------------------------------: |
| mangle | 包标记表:拆解报文做出修改并重新封装 | PREROUTING POSTROUTING INPUT OUTPUT FORWARD |
|  nat   | 地址转换表                          |        PREROUTING POSTROUTING OUTPUT        |
| filter | 过滤表                              |           INPUT  FORWARD  OUTPUT            |

优先级:

![优先级](/root/图片/优先级.png)

