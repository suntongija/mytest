# web服务

## Nginx



### nginx 与FastCGI连接方式(套接字)

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
        