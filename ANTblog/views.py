from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import login as dj_login, logout as dj_logout
from ANTblog import models
from ANTblog.forms import RegisterForm, LoginForm, ChangePwdForm, CodeForm, ReplyForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 注册
from ANTblog.mixin import MenuArticleRightMixin, MenuRightMixin
from ANTblog.signals import article_like_num_add, article_look_num_add, article_comment_num_add


# 注册
def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'ANTblog/register.html', context={'form': form})


# 登陆
def login(request, *args, **kwargs):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            dj_login(request, form.user)
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'ANTblog/login.html', context={'form': form})


# 离开
def logout(request, *args, **kwargs):
    dj_logout(request)
    return redirect('index')


# 忘记密码
def forget_pwd(request, *args, **kwargs):
    if request.method == 'POST':
        form = ChangePwdForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            return redirect('login')
    else:
        form = ChangePwdForm()

    return render(request, 'ANTblog/forget_pwd.html', context={'form': form})


# 验证码
def code(request, *args, **kwargs):
    from_email = settings.DEFAULT_FROM_EMAIL
    form = CodeForm(request.GET)
    # 生成验证码
    import random
    num = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    if form.is_valid():  # 如果提交的数据合法
        username = form.save(num)
        msg = "您(用户名为 %s )正在修改密码，验证码是 %s ,如果不是本人操作，请忽略此邮件" % (username, num)
        send_mail("ANTblog|修改密码", msg, from_email, recipient_list=[form.cleaned_data['email'], ], )
        return JsonResponse({'msg': "发送成功"})

    return JsonResponse({'msg': form.errors['email'][0]})


# 点击喜欢后触发
def add_like_num(request, *args, **kwargs):
    article_like_num_add.send(models.Article, id=request.GET.get('id'))
    # 永远返回成功
    return JsonResponse({'msg': "success"})


# 分页的文章获取，采用ajax
def article(request, *args, **kwargs):
    path = request.GET.get('path', '').strip("/")

    p_list = path.rsplit('/', )

    if len(p_list) == 2:
        if p_list[0] == "category":
            data = {'category__parent__path_name': p_list[-1]}
        elif p_list[0] == "tag":
            data = {'tag__name__iexact': p_list[-1]}
        elif p_list[0] == "date":
            year, month = p_list[1].split('-', maxsplit=1)
            data = {
                'push_datetime__year': year,
                'push_datetime__month': month,
            }
        else:
            data = {}
    elif len(p_list) == 3:
        data = {'category__path_name': p_list[-1]}
    else:
        data = {}

    art_list = models.Article.objects.filter(**data)
    p = Paginator(art_list, settings.PAGE_NUM)
    page = request.GET.get('page', 2)
    try:
        result = p.page(page)
    except PageNotAnInteger:
        result = p.page(1)
    except EmptyPage:
        result = p.page(p.num_pages)

    data = {
        'now_page': result.number,
        'has_next': result.has_next(),
        'article': serializers.serialize("json", result.object_list, ),
        'tag': serializers.serialize("json", models.Tag.objects.all()),
    }
    # data['article'] = json.loads(data['article'])
    return JsonResponse(data, safe=False)


# 首页
class IndexView(MenuArticleRightMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ANTblog/index.html', context=self.extra_context(*args, **kwargs))

    def extra_context(self, *args, **kwargs):
        data = {
            'index_banner': self.index_banner(),
            'hot_article': self.hot_article(),
        }
        data.update(super(IndexView, self).extra_context(*args, **kwargs))
        return data

    def index_banner(self):
        return models.IndexBanner.objects.all()

    def hot_article(self):
        return models.Article.objects.all().order_by('-like_num')[:settings.INDEX_HOT_NUM]


# 文章列表页
class CategoryView(MenuRightMixin, View):
    def extra_context(self, *args, **kwargs):
        data = {
            'article': self.article(*args, **kwargs),
        }
        data.update(super(CategoryView, self).extra_context(*args, **kwargs))
        return data

    def article(self, *args, path=None, **kwargs):
        category = get_object_or_404(models.Category, path_name=path)
        return models.Article.objects.filter(category__parent=category)[:settings.PAGE_NUM]

    def get(self, request, *args, **kwargs):
        return render(request, 'ANTblog/blog.html', context=self.extra_context(*args, **kwargs))


# 文章二级列表页
class CategorySecView(CategoryView):
    def article(self, *args, path=None, **kwargs):
        path_sec = kwargs.get('path_sec', None)
        if models.Category.objects.filter(path_name=path_sec, parent__path_name=path).exists():
            return models.Article.objects.filter(category__path_name=path_sec)[:settings.PAGE_NUM]
        raise Http404


# 标签列表页
class TagView(CategoryView):
    def article(self, *args, path=None, **kwargs):
        obj = get_object_or_404(models.Tag, name__iexact=path)
        return obj.article_set.all()[:settings.PAGE_NUM]


# 时间列表页
class DateView(CategoryView):
    def article(self, *args, path=None, **kwargs):
        year, month = path.split('-', maxsplit=1)
        return get_list_or_404(models.Article, push_datetime__year=year, push_datetime__month=month)[:settings.PAGE_NUM]


# 详情页
class DetailView(MenuRightMixin, View):

    def extra_context(self, *args, **kwargs):
        id = kwargs.pop('id', None)
        article = self.article(id)
        data = {
            'article': article,
            'reply': self.reply(id),
            'detail_menu': self.detail_menu(article)
        }
        data.update(super(DetailView, self).extra_context(*args, **kwargs))

        return data

    def get(self, request, *args, **kwargs):
        article_look_num_add.send(models.Article, id=kwargs.get('id'))

        return render(request, 'ANTblog/detail.html', context=self.extra_context(*args, **kwargs))

    @method_decorator(login_required(login_url="/login.html"))
    def post(self, request, *args, **kwargs):
        form = ReplyForm(request.POST, user=request.user)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            article_comment_num_add.send(models.Article, id=kwargs.get('id'))
            return redirect('detail', id=kwargs['id'])
        return HttpResponse("请输入合法的数据")

    def reply(self, id):
        rep_list = models.Reply.objects.filter(article=id).select_related('user').order_by('father_id', '-add_datetime')

        # 根据father_id升序，时间降序，会让根回复在前面，
        # 而后回复的id肯定比先回复的id大
        # id_list判断现在的id是不是在这个节点上
        # 然后深度遍历
        result_list = []
        for rep in rep_list:
            if rep.father_id is None:
                result_list.append(
                    {
                        'id': rep.id,
                        'data': rep,
                        'id_list': [rep.id, ],
                        'childs': [],
                        'father': None,
                    }
                )
            else:
                for result in result_list:
                    if rep.father_id not in result['id_list']:
                        continue
                    # print(rep.id)
                    # print(result_list)
                    child = result
                    while child['childs']:
                        for i in child['childs']:
                            if rep.father_id in i['id_list']:
                                child = i
                                break
                        else:
                            break

                    child['childs'].append({
                        'id': rep.id,
                        'data': rep,
                        'id_list': [rep.id, ],
                        'childs': [],
                        'father': child,
                    })
                    # child['id_list'].append(rep.id)
                    # 递归到根节点，添加rep.id
                    parent = child
                    while parent:
                        parent['id_list'].append(rep.id)
                        parent = parent['father']

        # print(result_list)
        return result_list

    def article(self, id):
        art = get_object_or_404(models.Article, id=id)
        # return HttpResponseNotFound("None")
        return art

    def detail_menu(self, article):
        result = []
        c = article.category
        if c.parent_id is None:
            result.append(reverse('category', kwargs={'path': c.path_name}))
            return result
        parent_name = c.parent.path_name
        result.append(reverse('category', kwargs={'path': parent_name}))
        result.append(reverse('category_sec', kwargs={'path': parent_name, 'path_sec': c.path_name}))
        return result
