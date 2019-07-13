from collections import namedtuple

from django.conf import settings
from django.db import connection
from django.db.models import Count

from ANTblog import models


class MenuMinin:
    def extra_context(self, *args, **kwargs):
        data = {
            'menu': self.menu(),
        }
        data.update(super(MenuMinin, self).extra_context(*args, **kwargs))
        return data

    def menu(self):
        data_list = models.Category.objects.all()
        result = []
        for data in data_list:
            if data.parent is None:
                result.append(
                    {
                        'id': data.id,
                        'name': data.name,
                        'path_name': data.path_name,
                        'icon': data.icon,
                        'has_child': data.has_child,
                        'childs': [],
                    }
                )
            else:
                for i in result:
                    if i['id'] == data.parent_id:
                        i['childs'].append(
                            {
                                'id': data.id,
                                'name': data.name,
                                'path_name': data.path_name,
                                'icon': data.icon,
                            }
                        )

        # print(result)
        return result


class ArticleMixin:

    def extra_context(self, *args, **kwargs):
        data = {
            'article': self.article(),
        }
        data.update(super(ArticleMixin, self).extra_context(*args, **kwargs))
        return data

    def article(self):
        return models.Article.objects.all()[:settings.PAGE_NUM]


class MenuArticleMixin(MenuMinin, ArticleMixin):
    pass


class RightMixin:

    def extra_context(self, *args, **kwargs):
        return {
            'author': self.author_desc(),
            'guess_article': self.guess_article(),
            'tag': self.tag(),
            'tar': self.tar(),
        }

    def author_desc(self):
        return {
            'name': settings.AUTHOR_NAME,
            'img': settings.AUTHOR_IMG,
            'desc': settings.AUTHOR_DESC,
        }

    def guess_article(self):
        return models.Article.objects.filter(guess_like=True).order_by('look_num', )[:settings.INDEX_HOT_NUM]

    def tag(self):
        return models.Tag.objects.annotate(count=Count('article')).order_by('-count')

    def tar(self):
        result = []
        with connection.cursor() as cursor:
            # mysql和sqlite的函数不同
            if settings.DATABASES['default']['ENGINE'].index("sqlite3") >= 0:
                sql = '''
                     SELECT substr(date( push_datetime ),1,7) as `date`,
                         count(push_datetime) as `count`
                     FROM ANTblog_article
                     GROUP BY `date` 
                     ORDER BY `date` DESC 
                 '''
            else:
                sql = '''
                     SELECT LEFT(date( push_datetime ),7) as `date`,
                         count(push_datetime) as `count`
                     FROM ANTblog_article
                     GROUP BY `date` 
                     ORDER BY `date` DESC 
                 '''
            cursor.execute(sql)
            desc = cursor.description

            nt_result = namedtuple('Tar', [col[0] for col in desc])
            result = [nt_result(*row) for row in cursor.fetchall()]

        return result


class MenuRightMixin(MenuMinin, RightMixin):
    pass


class MenuArticleRightMixin(MenuArticleMixin, RightMixin):
    pass
