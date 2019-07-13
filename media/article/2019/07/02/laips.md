title: lua lapis安装
tags:
  - lua
  - 基础
  - lapis
categories:
  - back-end
comments: true
type: categories
author: ANT锟
date: 2019-06-19 16:11:00
---
### lapis安装

[lapis](http://leafo.net/lapis/)是lua中的web框架，基于[openresty](http://openresty.org/cn/),直接和nginx整合在一起，
支持lua和[moonscript](http://moonscript.org/).
<!-- more -->
#### 安装openresty
openresty有win，linux，mac等版本，但为了更方便的安装lapis，建议在linux上安装，我这边使用的是centos7(我在win10上折腾了一天，还没装好lapis)

首先下载openresty，现在最新的是1.15版本，不建议安装（会出现一个全局变量导致的线程竞争的警告），建议用比这低一点的版本，但是也别太低，我用的是1.13.6.2版本
```bash
# 安装依赖包
yum install pcre-devel openssl-devel gcc curl unzip
# 下载openresty
wget https://openresty.org/download/openresty-1.13.6.2.tar.gz
tar zxvf openresty-1.13.6.2.tar.gz
cd openresty-1.13.6.2/
./configure
gmake && gmake install
```
默认安装在/usr/local/openresty中
可以进去看看
```bash
cd /usr/local/openresty
ls
# bin  COPYRIGHT  luajit  lualib  nginx  pod  resty.index  site
cd site/lualib
mkdir work
cd work
mkdir logs/ conf/
vim /conf/nginx/conf
worker_processes  1;
error_log logs/error.log;
events {
    worker_connections 1024;
}
http {
    server {
        listen 8080;
        location / {
            default_type text/html;
            content_by_lua_block {
                ngx.say("<p>hello, world</p>")
            }
        }
    }
}

/usr/local/openresty/nginx/sbin/nginx -p `pwd`/ -c conf/nginx.conf

curl http://localhost:8080
# <p>hello, world</p>

```
openresty安装成功,**最后记得把nginx进程杀掉哟**
#### 安装luarocks
luarocks是lua的包管理器，centos7自带lua5.1版本，但是我们用openresty自带的luajit更好，因此不需要安装lua，直接装luarocks就行
```bash
 wget http://luarocks.github.io/luarocks/releases/luarocks-3.1.3.tar.gz
 tar zxvf luarocks-3.1.3.tar.gzcd 
 cd luarocks-3.1.3/
 ./configure --prefix=/usr/local/openresty/luajit \
    --with-lua=/usr/local/openresty/luajit/ \
    --lua-suffix=jit \
    --with-lua-include=/usr/local/openresty/luajit/include/luajit-2.1
make && make install

vim ~/.bash_profile
 #加入PATH=$PATH:/usr/local/openresty/luajit/bin
 source ~/.bash_profile
 
 luarocks install moonscript
 luarocks install lapis
```
到这里lapis就安装完成了
#### 测试lapis
```bash
cd /usr/local/openresty/site/lualib
lapis new --lua
lapis server

 curl http://localhost:8080
#<!DOCTYPE HTML><html lang="en"><head><title>Lapis Page</title></head><body>Welcome to Lapis 1.7.0</body></html>[root@VM_0_6_centos ~]
```
lapis默认前台运行，方便开发