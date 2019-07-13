"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from ANTblog.views import IndexView, CategoryView, CategorySecView, DetailView, login, register, logout, forget_pwd, \
    code, article, TagView, DateView, add_like_num

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login.html', login, name='login'),
    path('logout.html', logout, name='logout'),
    path('forget_pwd.html', forget_pwd, name='forget_pwd'),
    path('register.html', register, name='register'),
    path('code/', code, name='code'),
    path('add_like_num/', add_like_num, name='add_like_num'),
    path('article/', article, name='article'),
    path('category/<str:path>/<str:path_sec>/', CategorySecView.as_view(), name='category_sec'),
    path('category/<str:path>/', CategoryView.as_view(), name='category'),
    path('tag/<str:path>/', TagView.as_view(), name='tag'),
    path('date/<str:path>/', DateView.as_view(), name='date'),
    path('detail/<int:id>.html', DetailView.as_view(), name='detail'),
]
