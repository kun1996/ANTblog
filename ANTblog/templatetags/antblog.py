import json

from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.safestring import mark_safe

register = template.Library()

s = '''
    <div style="padding-left: {num}px;" class="comment-detail" >
        <div class="image">
            <img src="{img_url}" alt="">
        </div>
        <span>
            <div class="child-reply-content" reply-id="{id}">
                {content}
                <div style="display:none;">
                    <textarea name="content" placeholder="在这里输入你的回复哦"></textarea>
                    <span style="padding:0;border:0;color:blue;">提交</span>
                </div>
            </div>
            <div style="float: right" class="child-reply" >
                {author} {time} <span style="padding:0;border:0;color:blue;">回复</span>
            </div>
        </span>
    </div>
'''


@register.simple_tag
def antcomment(reply):
    html = ''
    img_url = static('ANTblog/images/timg.jpg')

    for _, rep in enumerate(reply):
        html += s.format(
            num=0,
            img_url=img_url,
            content=rep['data'].content,
            id=rep['data'].id,
            author=rep['data'].user.username,
            time=rep['data'].add_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        )

        # print(rep['childs'])
        for i in rep['childs']:
            html += get_html_comment(
                i,
                img_url=img_url,
                rep=i
            )

    return mark_safe(html)


# 递归获取评论
def get_html_comment(childs, dep=1, **kwargs):

    data = {
        'num': dep * 50,
        'img_url': kwargs['img_url'],
        'content': kwargs['rep']['data'].content,
        "id": kwargs['rep']['data'].id,
        'author': kwargs['rep']['data'].user.username,
        'time': kwargs['rep']['data'].add_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    }
    if not childs['childs']:
        return s.format(**data)

    html = ''

    for index, i in enumerate(childs['childs']):
        if index == 0:
            html += s.format(**data)
        html += get_html_comment(
            i,
            dep + 1,
            img_url=kwargs['img_url'],
            rep=i,
        )
    return html
