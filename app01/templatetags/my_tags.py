from django import template
from app01 import models
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count

# 编写自定义模板
register = template.Library()


@register.inclusion_tag("left_menu.html")
def get_left_list(username):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
        # 如果用户存在需要将TA写的所有文章找出来
    blog = user.blog
    # 我的文章列表
    article_list = models.Article.objects.filter(user=user)
    # 我的便签列表
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values('title', 'c')
    # 我的分类列表
    catablog_list = models.Category.objects.filter(blog=blog)
    # catablog_list = models.Category.objects.filter(blog=blog).annotate(cc=Count("article")).values('article',cc)
    # 时间归档
    time_art_list = models.Article.objects.filter(user=user).extra(
        select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")

    return {"catablog_list": catablog_list,
            "tag_list": tag_list,
            "time_art_list": time_art_list}
