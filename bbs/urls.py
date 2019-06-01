"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from bbs import settings
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    # url(r'^get_valid_img.png/', views.get_valid_img),
    url(r'^pc-geetest/register', views.get_geetest),  # 极验请求url
    url(r'^index/', views.index),
    url(r'^upload/', views.upload),
    url(r'^register/', views.register),
    url(r'^check_username/', views.check_username),
    # media相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'blog/article/(\w+)/(\d+)', views.get_article_detal),

    url(r'up_down/', views.up_down),
    url(r'blog/comment/', views.comment),
    url(r'blog/add_article/', views.add_article),
    url(r'blog/add_cat/', views.add_cat),

    url(r'del_catablog/(\d+)/',views.del_catablog),
    url(r'blog/comment_tree/(\w+)/', views.comment_tree),
    url(r'blog/(?P<username>(\w+))/', views.home),  # 个人主页路由
    url(r'article/dele/(\w+)',views.article_dele),
    url(r'aj_add_cata/', views.aj_add_cat),
    url(r'guanli/(\w+)',views.guanli),

]
