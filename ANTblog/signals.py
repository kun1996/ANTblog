import django.dispatch
from django.dispatch import receiver

# 定义一个信号
from django.shortcuts import get_object_or_404

from ANTblog.models import Article

article_like_num_add = django.dispatch.Signal(providing_args=['id', ])

article_look_num_add = django.dispatch.Signal(providing_args=['id', ])

article_comment_num_add = django.dispatch.Signal(providing_args=['id', ])


# 可以通过反射获取属性，这样就只用写一个信号了
@receiver(article_like_num_add, sender=Article)
def like_num_callback(sender, **kwargs):
    id = kwargs['id']
    if id:
        # art = Article.objects.filter(id=id).first()
        obj = get_object_or_404(sender, id=id)
        obj.like_num += 1
        obj.save()


@receiver(article_look_num_add, sender=Article)
def look_num_callback(sender, **kwargs):
    id = kwargs['id']
    if id:
        obj = get_object_or_404(sender, id=id)
        obj.look_num += 1
        obj.save()


@receiver(article_comment_num_add, sender=Article)
def like_num_callback(sender, **kwargs):
    id = kwargs['id']
    if id:
        # art = Article.objects.filter(id=id).first()
        obj = get_object_or_404(sender, id=id)
        obj.comment_num += 1
        obj.save()
