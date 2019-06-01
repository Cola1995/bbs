from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from geetest import GeetestLib   # 极验依赖库
from django.contrib import auth  # auto 模块
from django.contrib.auth.decorators import login_required   # author 登录验证装饰器
from django.views.decorators.csrf import csrf_exempt       # 城csrf 装饰器
from bbs import forms
from app01 import models
from django.db.models import Count, F
# Create your views here.


def login(request):
    return render(request,'login2.html')


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"


# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 使用极验滑动验证码的登录

def login(request):
    """
    # 登录视图
    :param request:
    :return:
    """
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)
                ret["msg"] = "/index/"

            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"
        print(ret)
        return JsonResponse(ret)
    return render(request, "login2.html")


def logout(request):
    """
    # 注销视图
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect('/login/')


@login_required    # auth 装饰器验证用户是否登录，没登录默认跳转登录页
def index(request):
    article_list = models.Article.objects.all()
    return render(request,'index.html', {"article_list": article_list})


from bbs import  settings
import os ,json


def upload(request):
    """
    # 上传演示
    :param request:
    :return:
    """
    print("上传视图")

    print(request.POST)
    file_obj = request.FILES.get("upload_img")
    print(file_obj.name)
    path = os.path.join(settings.MEDIA_ROOT, 'article_pic', file_obj.name)
    with open(path, "wb") as f:

        for line in file_obj.chunks():
            f.write(line)
        f.close()

        res = {
            "error": 0,
            "url": "/media/article_pic/" + file_obj.name
        }

    return HttpResponse(json.dumps(res))


def register(request):
    """
    # 注册页面
    :param request:
    :return:
    """
    if request.method == "POST":
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        ret = {"status": 0, "msg": ""}
        if form_obj.is_valid():
            print('校验通过')
            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_pwd")
            avatar_img = request.FILES.get("avatar")
            print(form_obj.cleaned_data.get('username'))
            print("@@@@@@@@@@@@@@@@@@@@@",avatar_img)

            # 创建默认的个人站点信息
            site = form_obj.cleaned_data.get('username')
            b_title = form_obj.cleaned_data.get('username')+"的个人博客"
            blog = models.Blog.objects.create(title=b_title, site=site, theme="ma.css")
            if not avatar_img:
                avatar_img = 'avatar/default.png'
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img, blog=blog)
            print('ssssssssssssssssssssssss')
            ret["msg"] = "/index/"
            return JsonResponse(ret)
        else:
            print('校验不通过')
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
        # return render(request, 'register.html', {"form_obj": form_obj})
    form_obj = forms.RegForm()
    return render(request, 'register.html', {"form_obj": form_obj})


@csrf_exempt
def check_username(request):
    ret = {"status": 0, "msg": ""}
    if request.method == 'POST':
        username = request.POST.get('username')
        r = models.UserInfo.objects.filter(username=username)
        if r:
            ret['status'] = 1
            ret['msg'] = "用户名已存在"
            return JsonResponse(ret)
    return JsonResponse(ret)


def home(request, username):
    """
    # 个人blog试图
    :param request:
    :param username:
    :return:
    """
    print('个人blog视图')
    print(username)
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return redirect('/login/')
        # 如果用户存在需要将TA写的所有文章找出来
    blog = user.blog
    print(blog)
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
    return render(request, "home.html",
                  {"blog": blog, "article_list": article_list,
                   "catablog_list": catablog_list, "tag_list": tag_list, "time_art_list": time_art_list,
                   "username": username})


def guanli(request, username):
    """
    # 个人blog试图
    :param request:
    :param username:
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return redirect('/login/')
        # 如果用户存在需要将TA写的所有文章找出来
    blog = user.blog
    print(blog)
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
    return render(request, "user_article.html",
                  {"blog": blog, "article_list": article_list,
                   "catablog_list": catablog_list, "tag_list": tag_list, "time_art_list": time_art_list,
                   "username": username})


def get_left_list(username):
    """
    # 获取分类列表工具类
    :param username:  用户姓名
    :return:
    """
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
    return article_list, tag_list, catablog_list,time_art_list


def get_article_detal(request, username, pk):
    """
    # 文章详情视图
    :param request:
    :param username: 用户姓名
    :param pk:  文章主键
    :return:
    """
    print('文章详情视图')
    print(username, pk)
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    # 找到当前的文章
    # article_obj = models.Article.objects.filter(pk=pk).first()
    # article_list, tag_list, catablog_list, time_art_list = get_left_list(username)
    article = models.Article.objects.filter(pk=pk, user__username=username).first()  # 根据文章主键,用户姓名查询文章信息
    # 评论列表
    comment_list = models.Comment.objects.filter(article_id=pk)
    return render(request, 'article-detal.html',{"article": article,
                                                 # "catablog_list": catablog_list,
                                                 # "tag_list": tag_list, "time_art_list": time_art_list,

                                                 'username': username, 'blog': blog, "comment_list": comment_list})


def up_down(request):
    """
    # 文章详情页面点赞视图
    :param request:
    :return:
    """
    print('点赞视图')
    import json
    # print(request.POST)
    # print(type(request.POST.get('article_id')))
    user = request.user
    article_id = request.POST.get("article_id")   # 文章ID
    is_up = json.loads(request.POST.get('is_up'))
    msg = {"status": True}
    try:
        models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
        if is_up:  # 判断是点赞还是踩
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
        else:
            models.Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    except Exception as e:
        msg["first_action"] = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up
        msg["status"] = False
    # print("数据写入成功")
    print(msg)
    return JsonResponse(msg)


def comment(request):
    """
    # 评论视图
    :param request:
    :return:
    """
    print('评论视图')
    print(request.POST)
    ret = {}
    article_id = request.POST.get("article_id")
    user_id = request.user.pk
    content = request.POST.get("content")
    pid = request.POST.get("pid")
    if pid: # 子评论
        comment = models.Comment.objects.create(article_id=article_id, user_id=user_id, content=content,parent_comment_id=pid)
    else:
        comment = models.Comment.objects.create(article_id=article_id, user_id=user_id, content=content)
    ret["content"] = comment.content
    ret["create_time"] = comment.create_time.strftime("%Y-%m-%d")
    ret["username"] = comment.user.username

    return JsonResponse(ret)


def comment_tree(request, artile_id):
    print("树")
    ret = list(models.Comment.objects.filter(article_id=artile_id).values('user', 'content', 'parent_comment_id', 'pk',
                                                                          'user__username','create_time'))
    return JsonResponse(ret, safe=False)   # 传非字典的数据要加safe参数


def add_article(request):
    print("添加文章视图")
    if request.method == "POST":
        print(request.POST)
        catablog = request.POST.get("cata")
        title = request.POST.get("title")
        content = request.POST.get("content")
        user = request.user

        from bs4 import BeautifulSoup
        bs = BeautifulSoup(content, "html.parser")
        desc = bs.text[0:150] + "..."
        # 过滤非法标签
        for tag in bs.find_all():

            print(tag.name)

            if tag.name in ["script", "link"]:   # 过滤非法标签
                tag.decompose()
        article = models.Article.objects.create(user=user, title=title, desc=desc, category_id=catablog)  # 文章表添加数据
        models.ArticleDetail.objects.create(article=article, content=str(bs))  # 文章详情表添加数据
        return redirect('/guanli/'+user.username)
    username = request.user.username
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    cata = models.Category.objects.filter(blog=blog)
    return render(request, "add_article.html",{'cata': cata})


def article_dele(request, pk):
    models.Article.objects.filter(pk=pk).delete()

    return redirect('/guanli/'+request.user.username)


def add_cat(request):
    """
    # 个人分类详情 catablog
    :param request:
    :return:
    """
    username = request.user.username
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    print(username, blog)
    catablog_list = models.Category.objects.filter(blog=blog).annotate(cc=Count("article")).values('title', 'cc','pk')
    return render(request, 'add_article_tag.html', {'catablog_list': catablog_list})


def aj_add_cat(request):
    """
    # ajax 提交cata数据

    :param request:
    :return:
    """
    print("添加cata")
    ret = {"error": 0}
    username = request.user.username
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    title = request.POST.get("cata")
    cata_obj = models.Category.objects.create(title=title, blog=blog)
    ret['pk'] = cata_obj.pk
    ret['title'] = cata_obj.title
    return JsonResponse(ret)



def del_catablog(request, pk):
    """
    # 删除文章分类信息
    :param request:
    :return:
    """
    print("delcatablog")
    models.Category.objects.filter(pk=pk).delete()
    return redirect("/blog/add_cat")
