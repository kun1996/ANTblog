# Django 博客 - Python

### 在线实例
http://134.175.39.46/

本项目以debug模式运行

### 安装步骤

一:将本项目clone到你的本地
```bash
git clone https://github.com/kun1996/ANTblog.git
```
二:创建虚拟环境
```bash
pip3 install virtualenv

virtualenv --no-site-packages venv # 如果你的环境有2.7的python可以加--python=python3参数指定python版本
source venv/bin/activate
```
三:下载环境依赖
```bash
cd ANTblog
pip install -r requirements.txt # 如果下载速度太慢，可以在后面加上 -i https://pypi.doubanio.com/simple/
```
四:添加邮箱配置文件
```python
# ANTblog/conf.py 即在app目录下，与views.py同级,需要自己创建 找回密码
EMAIL_HOST_USER = "你的邮箱"  # 发送邮件的邮箱
EMAIL_HOST_PASSWORD = "你的邮箱的授权密码（不是登陆密码）"  # #邮箱的授权密码
```
五:运行
```bash
python manage.py runserver
# 如果你出现了django.core.exceptions.ImproperlyConfigured: SQLite 3.8.3 or later is required (found 3.7.17).错误
# 请更新sqlite版本，可以参考https://www.jianshu.com/p/cdacf4b74646
```
### 注意
因为自带了sqlite3,所以可以直接使用，如需更换mysql则自行更换

管理员账号ent

管理员密码123456

这只是测试用的，如需自己使用，记得重新生成sqlite3或者其他数据库

### 配置
```python
# blog/setting.py

# ANTblog使用 显示个人的一些简介 右边栏的个人简介
AUTHOR_NAME = 'ANT锟'
AUTHOR_IMG = "/media/article/image/timg.jpg"
AUTHOR_DESC = "欢迎大家来到我的博客,我是来自南京的一枚全栈小码农."

# 分页
PAGE_NUM = 10 # 文章每页数目
RIGHT_LIKE_NUM = 5 # 猜你喜欢数目
INDEX_HOT_NUM = 5 # 首页热门文章数目
```

### 计划
搜索功能的实现

后台管理的实现（目前使用的是django的admin）

### 交流
qq群:488242300

