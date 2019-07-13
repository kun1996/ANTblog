# Django 博客 - Python

### 安装步骤

一:将本项目clone到你的本地
```bash
git clone https://github.com/kun1996/ANTblog.git
```
二:创建虚拟环境
```bash
pip3 install virtualenv
virtualenv --no-site-packages venv
source venv/bin/activate
```
三:下载环境依赖
```bash
pip install -r requirements.txt
```
四:添加邮箱配置文件
```python
# ANTblog/conf.py 即在app目录下，与views.py同级
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
待更新

### 计划
搜索功能的实现
后台管理的实现（目前使用的是django的admin）

### 交流
qq群:488242300

