title: nginx变量浅析
tags:
  - nginx
categories:
  - back-end
comments: true
type: categories
author: ANT锟
date: 2019-06-20 18:46:00
---
### nginx变量
```conf
    server {
        listen 8080;

        location /test {
            set $foo hello;
            echo "foo: $foo";
        }
    }
```
set指令是ngx_rewrite模块的，$foo是变量，可以在字符串中直接引用或者${foo}，但是怎么使用$符号呢
<!-- more -->
```conf
    geo $dollar {
        default "$";
    }

    server {
        listen 8080;

        location /test {
           echo "$dollar";
        }
        location /foo {
            set $a hello;
            rewrite ^ /bar;
        }

        location /bar {
            echo "a = [$a]";
        }
    }
```
ngx_geo的geo模块可以解决,而且set定义的变量的生命周期是和请求的周期一样的
```conf
    location /test {
        echo "uri = $uri";
        echo "request_uri = $request_uri";
    }
    location /test {
        echo "name: $arg_name";
        echo "class: $arg_class";
    }
location /test {
        set_unescape_uri $name $arg_name;
        set_unescape_uri $class $arg_class;

        echo "name: $name";
        echo "class: $class";
    }
```
ngx_http_core 模块提供的内建变量 $uri，可以用来获取当前请求的 URI（经过解码，并且不含请求参数），而 $request_uri 则用来获取请求最原始的 URI （未经解码，并且包含请求参数）  
以 arg_ 开头的所有变量，称之为 $arg_XXX 变量群。一个例子是 $arg_name，这个变量的值是当前请求名为 name 的 URI 参数的值，而且还是未解码的原始形式的值
$arg_name 不仅可以匹配 name 参数，也可以匹配 NAME 参数，抑或是 Name，等等  
第三方 ngx_set_misc 模块提供的 set_unescape_uri 配置指令对 URI 参数值中的 %XX 这样的编码序列进行解码,set_unescape_uri 指令也像 set 指令那样，拥有自动创建 Nginx 变量的功能.  
类似 $arg_XXX 的内建变量还有不少，比如用来取 cookie 值的 $cookie_XXX 变量群，用来取请求头的 $http_XXX 变量群，以及用来取响应头的 $sent_http_XXX 变量群,可以参考 ngx_http_core 模块的官方文档。
$args参数可以改写