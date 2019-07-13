# Generated by Django 2.2.2 on 2019-07-02 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ANTblog', '0004_auto_20190702_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.FileField(default='article/timg.jpg', upload_to='./article/image/', verbose_name='缩略图'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.FileField(unique=True, upload_to='./article/%Y/%m/%d/', verbose_name='博客文件'),
        ),
        migrations.AlterField(
            model_name='indexbanner',
            name='image',
            field=models.ImageField(upload_to='./banner', verbose_name='轮播图片'),
        ),
    ]