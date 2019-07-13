from django.contrib import admin

# Register your models here.
from ANTblog import models

admin.site.register(models.Article)
admin.site.register(models.Tag)
admin.site.register(models.IndexBanner)
admin.site.register(models.Reply)
admin.site.register(models.Category)

admin.site.site_title = "ANTblog后台管理"
admin.site.site_header = "ANTblog"
