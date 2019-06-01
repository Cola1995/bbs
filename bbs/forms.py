from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01 import  models


class RegForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=16,
        error_messages={
            "required": "不能为空",
            "invalid": "格式错误",
            "min_length": "用户名最长16位"

        },
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(

        min_length=6,
        label="密码",
        error_messages={
            "required": "不能为空",
            "invalid": "格式错误",
            "min_length": "密码最短6位"
        },
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
    )

    re_pwd = forms.CharField(
        min_length=6,
        label="密码",
        error_messages={
            "required": "不能为空",
            "invalid": "格式错误",
            "min_length": "密码最短6位"
        },
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
    )
    email = forms.CharField(
        label="邮箱",
        error_messages={
            "required": "不能为空",
            "invalid": "邮箱格式不正确"
        },
        widget=forms.widgets.EmailInput(attrs={'class': 'form-control'})
    )
    # phone = forms.CharField(
    #     label="手机",
    #     # 自己定制校验规则
    #     validators=[
    #         RegexValidator(r'^[0-9]+$', '手机号必须是数字'),
    #         RegexValidator(r'^1[3-9][0-9]{9}$', '手机格式有误')
    #     ],
    #     widget=forms.widgets.TextInput(attrs={"class": "form-control"}),
    #
    #     error_messages={
    #         "required": "该字段不能为空",
    #     }
    # )
    # ava = forms.CharField(
    #     label="头像",
    #     widget=forms.widgets.FileInput()
    # )

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_pwd")

        if re_password and re_password != password:
            self.add_error("re_pwd", ValidationError("两次密码不一致"))
        else:
            return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exi = models.UserInfo.objects.filter(username=username)

        if is_exi:
            self.add_error('username',ValidationError('用户名已被注册'))
        else:
            return self.cleaned_data.get('username')
                      
    def clean_email(self):
        email =self.cleaned_data.get('email')
        is_exi = models.UserInfo.objects.filter(email=email)
        if is_exi:
            self.add_error('email', ValidationError('邮箱已被注册'))
