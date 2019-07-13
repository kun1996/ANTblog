# Generated by Django 2.2.2 on 2019-07-02 17:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ANTblog', '0002_auto_20190702_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='push_datetime',
        ),
        migrations.AddField(
            model_name='article',
            name='push_date',
            field=models.DateField(default=django.utils.timezone.now, editable=False, verbose_name='上传日期'),
        ),
        migrations.AddField(
            model_name='article',
            name='push_time',
            field=models.TimeField(default=django.utils.timezone.now, editable=False, verbose_name='上传时间'),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(default='ANT锟', editable=False, max_length=32, verbose_name='作者'),
        ),
    ]
