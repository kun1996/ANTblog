# Generated by Django 2.2.2 on 2019-07-11 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ANTblog', '0011_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-push_datetime',), 'verbose_name': '博客文章', 'verbose_name_plural': '博客文章'},
        ),
        migrations.AlterModelOptions(
            name='indexbanner',
            options={'ordering': ('order_num', 'update_datetime'), 'verbose_name': '首页轮播图', 'verbose_name_plural': '首页轮播图'},
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='回复内容')),
                ('add_datetime', models.DateTimeField(auto_now_add=True, verbose_name='回复时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ANTblog.Article')),
                ('father', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ANTblog.Reply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '回复',
                'verbose_name_plural': '回复',
                'ordering': ('add_datetime',),
            },
        ),
    ]