# Generated by Django 2.2.2 on 2019-07-03 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ANTblog', '0007_tag_css'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='desc',
            field=models.CharField(default='', max_length=128, verbose_name='文章简介'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(default='', verbose_name='内容'),
        ),
    ]
