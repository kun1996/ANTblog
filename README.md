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
# 请更新sqlite版本
```
