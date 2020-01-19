from django import forms
from django.contrib.auth import get_user_model, login, password_validation
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from ANTblog.models import Code, Reply

UserModel = get_user_model()


# 注册表单
class RegisterForm(forms.Form):
    error_messages = {
        'password_mismatch': _("两次输入密码不一致"),
        'user_exist': _('用户名已存在'),
        'email_exist': _('邮箱已存在'),
    }

    username = forms.CharField(
        label=_('用户名'),
        label_suffix=':',
        min_length=3,
        max_length=100,
        error_messages={
            'required': '请输入用户名',
            'min_length': u'用户名最少为3个字符',
            'max_length': u'用户名最多为100个字符',
        },

    )
    password = forms.CharField(
        label=_('密码'),
        min_length=6,
        max_length=100,
        error_messages={
            'required': '请输入密码',
            'min_length': u'密码最少为6个字符',
            'max_length': u'密码最多为100个字符',
        },
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=_('确认密码'),
        min_length=6,
        max_length=100,
        error_messages={
            'required': '请确认密码',
            'min_length': u'密码最少为6个字符',
            'max_length': u'密码最多为100个字符',
        },
        widget=forms.PasswordInput,
    )
    email = forms.EmailField(
        label=_('邮箱'),
        error_messages={
            'required': '请输入邮箱',
            'invalid': '邮箱格式错误',
        })

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        # password_validation.validate_password(password2, self.user)
        return password2

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        if UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['user_exist'],
                code='user_exist',
            )
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_exist'],
                code='email_exist',
            )
        return self.cleaned_data

    def _post_clean(self):
        if self._errors: return
        username = self.cleaned_data['username']
        pwd = self.cleaned_data['password']
        email = self.cleaned_data['email']
        UserModel.objects.create_user(username, email, pwd)


# 忘记密码表单
class ChangePwdForm(forms.Form):
    error_messages = {
        'password_mismatch': _("两次输入密码不一致"),
        'email_no_exist': _('邮箱不存在'),
        'code_error': _('验证码错误')
    }

    email = forms.EmailField(
        label=_('邮箱'),
        error_messages={
            'required': '请输入邮箱',
            'invalid': '邮箱格式错误',
        })

    password = forms.CharField(
        label=_('密码'),
        min_length=6,
        max_length=100,
        error_messages={
            'required': '请输入密码',
            'min_length': u'密码最少为6个字符',
            'max_length': u'密码最多为100个字符',
        },
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=_('确认密码'),
        min_length=6,
        max_length=100,
        error_messages={
            'required': '请确认密码',
            'min_length': u'密码最少为6个字符',
            'max_length': u'密码最多为100个字符',
        },
        widget=forms.PasswordInput,
    )
    code = forms.CharField(
        label=_('验证码'),
        error_messages={
            'required': '请输入邮箱获取验证码',
        })

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        # password_validation.validate_password(password2, self.user)
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        if not UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_no_exist'],
                code='email_no_exist',
            )
        return email

    def clean(self):
        if self.cleaned_data.get('email'):
            code = Code.objects.filter(user__email=self.cleaned_data['email']).first()
            if self.cleaned_data.get('code') != code.code:
                raise forms.ValidationError(
                    self.error_messages['code_error'],
                    code='code_error',
                )
            code.delete()
        return self.cleaned_data

    def _post_clean(self):
        if self._errors: return
        User.objects.filter(email=self.cleaned_data['email']).update(
            password=make_password(self.cleaned_data['password']))


# 登陆表单
class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('用户名'),
        label_suffix=':',
        min_length=3,
        max_length=100,
        error_messages={
            'required': '请输入用户名',
            'min_length': u'用户名最少为3个字符',
            'max_length': u'用户名最多为100个字符',
        },

    )
    password = forms.CharField(
        label=_('密码'),
        min_length=6,
        max_length=100,
        error_messages={
            'required': '请输入密码',
            'min_length': u'密码最少为6个字符',
            'max_length': u'密码最多为100个字符',
        },
        widget=forms.PasswordInput(),
    )

    def clean(self):

        username = self.cleaned_data['username']
        pwd = self.cleaned_data['password']

        user = UserModel.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(
                '用户名不存在',
                code='username_error',
            )

        result = check_password(pwd, user.password)
        if not result:
            raise forms.ValidationError(
                '密码错误',
                code='password_error',
            )
        self.user = user

        return self.cleaned_data


# 验证码
class CodeForm(forms.Form):
    error_messages = {
        'email_no_exist': _('邮箱不存在'),
    }

    email = forms.EmailField(
        label=_('邮箱'),
        error_messages={
            'required': '请输入邮箱',
            'invalid': '邮箱格式错误',
        })

    def clean_email(self):
        email = self.cleaned_data['email']
        if not UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_no_exist'],
                code='email_no_exist',
            )
        return email

    def save(self, num):
        email = self.cleaned_data['email']
        user = UserModel.objects.filter(email=email).first()
        Code.objects.update_or_create({'code': num}, user=user)
        return user.username


# 回复
class ReplyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReplyForm, self).__init__(*args, **kwargs)

    content = forms.CharField(
        label=_('回复'),
        error_messages={
            'required': '请输入内容',
        })

    father_id = forms.IntegerField(
        label=_('父id'),
        required=False
    )

    article_id = forms.IntegerField(
        label=_('文章id'),
        error_messages={
            'required': '请输入文章id',
        }
    )

    def _post_clean(self):
        if self._errors: return
        Reply.objects.create(user=self.user, **self.cleaned_data)
