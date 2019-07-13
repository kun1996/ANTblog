from django.db import models

# Create your models here.
from django.utils import timezone
from django.conf import settings


# 文章类别
class Category(models.Model):
    name = models.CharField('分类名', max_length=24)
    path_name = models.CharField('路径名', max_length=24, default='', null=True, blank=True)
    parent = models.ForeignKey('self', models.CASCADE, null=True, blank=True)
    icon = models.CharField('图标', help_text='fontawesome里获取', max_length=128, null=True, blank=True, default=None)
    has_child = models.BooleanField("是否有子菜单", default=True)
    order_num = models.IntegerField("排序号", default=0)
    add_datetime = models.DateTimeField("添加时间", auto_now_add=True, editable=False)

    class Meta:
        verbose_name = '博客类别'
        verbose_name_plural = verbose_name
        ordering = ('parent_id', 'order_num', 'add_datetime')

    def __str__(self):
        return self.name


# 博客文章
class Article(models.Model):
    category = models.ForeignKey('Category', models.CASCADE, )
    title = models.CharField(verbose_name='标题', max_length=32)
    tag = models.ManyToManyField('Tag')
    author = models.CharField(verbose_name='作者', max_length=32, default=settings.AUTHOR_NAME, editable=False)
    push_datetime = models.DateTimeField(verbose_name='上传时间', default=timezone.now, editable=False)
    look_num = models.IntegerField('浏览次数', default=0, editable=False)
    comment_num = models.IntegerField('评论次数', default=0, editable=False)
    like_num = models.IntegerField('喜欢人数', default=0, editable=False)
    # content = models.FileField('博客文件', upload_to='./article/%Y/%m/%d/', unique=True)
    image = models.FileField('缩略图', upload_to='./article/image/', )
    guess_like = models.BooleanField(default=False)

    desc = models.TextField("文章简介", max_length=335, )
    content = models.TextField('内容')

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name
        ordering = ('-push_datetime',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        为每个对象生成一个URL
        应用：在对象列表中生成查看详细的URL，使用此方法即可！！！
        :return:
        """
        # return '/%s/%s' % (self._meta.db_table, self.id)
        # 或
        from django.urls import reverse
        return reverse('detail', kwargs={'id': self.id})


# 博客标签
class Tag(models.Model):
    css_choise = [(1, 'first'), (2, 'sec'), (3, 'thrid')]
    name = models.CharField('标签名', max_length=32, unique=True)
    css = models.IntegerField(choices=css_choise, default=1)

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # def natural_key(self):
    #     return (self.name,)


# 首页轮播图
class IndexBanner(models.Model):
    image = models.ImageField('轮播图片', upload_to='./banner')
    article = models.OneToOneField('Article', on_delete=models.CASCADE)

    order_num = models.IntegerField('播出顺序', default=0)
    add_datetime = models.DateTimeField('上传时间', auto_now_add=True, editable=False)
    update_datetime = models.DateTimeField('更新时间', auto_now=True, editable=False)

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name
        ordering = ('order_num', 'update_datetime')

    def __str__(self):
        return self.article.title


# 回复
class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', models.CASCADE)
    father = models.ForeignKey('self', models.CASCADE, blank=True, null=True)
    content = models.TextField(verbose_name='回复内容')
    add_datetime = models.DateTimeField('回复时间', auto_now_add=True, editable=False)

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name
        ordering = ('add_datetime',)

    def __str__(self):
        return self.content


# 验证码
class Code(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
