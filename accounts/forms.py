from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _
import re
class my_authorityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(my_authorityForm, self).__init__(*args, **kwargs)
        self.fields['admin_user'].queryset = User.objects.filter(is_staff=True)
class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名', required=True,
        error_messages={'required': '请填写您的用户名'}, widget=forms.TextInput(attrs={'placeholder': '用户名'}))
    password = forms.CharField(
        label='密码', required=False, widget=forms.PasswordInput())
    def clean_username(self):
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username):
            raise forms.ValidationError("用户名不存在")
        return username


class ChangeForm(forms.Form):
    password = forms.CharField(
        error_messages={'required': '请输入密码', 'max_length': '最多只能输入20个字符', 'min_length': '至少输入6个字符'},
        label='密码', required=True, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': '长度在6~20个字符以内'}))
    confirm_password = forms.CharField(
        error_messages={'required': '请输入密码', 'max_length': '最多只能输入20个字符', 'min_length': '至少输入6个字符'},
        label='确认密码', required=True, max_length=20, min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': '长度在6~20个字符以内'}))
    class Meta:
        model = get_user_model()
        fields = ("password",)
    def clean_confirm_password(self):
        #cleaned_data=super(SignupForm,self).clean()
        password = self.cleaned_data.get("password",False)
        confirm_password = self.cleaned_data["confirm_password"]
        if  not( password == confirm_password):
            raise forms.ValidationError("确认密码和密码不一致")
        else:
            return confirm_password
    
def lowercase_email(email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name.lower(), domain_part.lower()])
        return email

class SignupForm (forms.ModelForm):
    
    username =forms.CharField( 
        label='用户名',required=True,error_messages={'required': '请填写你的用户名','max_length':'最多只能输入15个字符','min_length':'至少输入3个字符'},max_length=15,min_length=3,widget=forms.TextInput(attrs={'placeholder':'3~15位字母/数字/汉字'}))
    email = forms.EmailField( error_messages={'required': '请填写你的email','invalid':'email格式不正确'},
        label='邮箱',required=True,widget=forms.EmailInput(attrs={'placeholder':'填写正确的email以方便您能通过邮箱找回密码'}))
    password =forms.CharField( error_messages={'required': '请输入密码','max_length':'最多只能输入20个字符','min_length':'至少输入6个字符'},
        label='密码',required=True,max_length=20,widget = forms.PasswordInput(attrs={'placeholder':'长度在6~20个字符以内'}))
    confirm_password= forms.CharField(error_messages={'required': '请输入密码','max_length':'最多只能输入20个字符','min_length':'至少输入6个字符'},
        label='确认密码',required=True,max_length=20,min_length=6,widget = forms.PasswordInput(attrs={'placeholder':'长度在6~20个字符以内'}))
    
    class Meta:
        model = get_user_model()
        fields = ("username","email","password",)
                                

    def clean_email(self):
        UserModel = get_user_model()
        email=self.cleaned_data["email"]
        lower_email=lowercase_email(email)
        try:
            UserModel._default_manager.get(email=lower_email)
        except UserModel.DoesNotExist:
            return lower_email
        raise forms.ValidationError("有人已经注册了这个email地址")
    
    def clean_confirm_password(self):
        #cleaned_data=super(SignupForm,self).clean()
        password = self.cleaned_data.get("password",False)
        confirm_password = self.cleaned_data["confirm_password"]
        if  not( password == confirm_password):
            raise forms.ValidationError("确认密码和密码不一致")
        return confirm_password
    
        
    
    def clean_username(self):
        UserModel = get_user_model()
        username = self.cleaned_data["username"]
        #过滤用户名敏感词的注册用户
        n=re.sub('[^\u4e00-\u9fa5a-zA-Z]','',username)
        
        mgc=['admin']        
        
        if n in mgc:
            raise forms.ValidationError("这么好的用户名当然被人提前预定啦，换一个试试^-^")
    
        try:
            UserModel._default_manager.get(username = username)
    
        except UserModel.DoesNotExist:
            return username
        raise forms.ValidationError("有人已经注册了这个用户名")
class ForgetPasswordForm(forms.Form):
    username =forms.CharField( label='用户名',required=True,error_messages={'required': '请填写你的用户名','max_length':'最多只能输入15个字符','min_length':'至少输入3个字符'},max_length=15,min_length=3,widget=forms.TextInput(attrs={'placeholder':'3~15位字母/数字/汉字'}))
    email = forms.EmailField( error_messages={'required': '请填写你的email','invalid':'email格式不正确'},label='邮箱',required=True,widget=forms.EmailInput(attrs={'placeholder':'填写你注册时使用的email'}))
    class Meta:
        model = get_user_model()
        fields = ("username","email","password",)
    def clean_email(self):
        UserModel = get_user_model()
        email=self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        lower_email=lowercase_email(email)
        try:
            UserModel._default_manager.get(email=lower_email,username = username)
            return email
        except UserModel.DoesNotExist:
            raise forms.ValidationError("用户名或email地址有误")