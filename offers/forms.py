from django import forms
from django.forms import ModelForm
from .models import *
import re
from dal import autocomplete

def checkIdcard(idcard):
    Errors=[u'验证通过!',u'身份证号码位数不对!',u'身份证号码出生日期超出范围或含有非法字符!',u'身份证号码校验错误!',u'身份证地区非法!']
    area={"11":u"北京","12":u"天津","13":u"河北","14":u"山西","15":u"内蒙古","21":u"辽宁","22":u"吉林","23":u"黑龙江","31":u"上海","32":u"江苏","33":u"浙江","34":u"安徽","35":u"福建","36":u"江西","37":u"山东","41":u"河南","42":u"湖北","43":u"湖南","44":u"广东","45":u"广西","46":u"海南","50":u"重庆","51":u"四川","52":u"贵州","53":u"云南","54":u"西藏","61":u"陕西","62":u"甘肃","63":u"青海","64":u"宁夏","65":u"新疆","71":u"台湾","81":u"香港","82":u"澳门","91":u"国外"}
    idcard=str(idcard)
    idcard=idcard.strip()
    idcard_list=list(idcard)
    error_message=[]

    #地区校验
    if(idcard[0:2] not in area):
        error_message.append(Errors[4])
    #15位身份号码检测
    if(len(idcard)==15):
        if((int(idcard[6:8])+1900) % 4 == 0 or((int(idcard[6:8])+1900) % 100 == 0 and (int(idcard[6:8])+1900) % 4 == 0 )):
            erg=re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')#//测试出生日期的合法性
        else:
            ereg=re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')#//测试出生日期的合法性
        if(re.match(ereg,idcard)):
            #error_message.append(Errors[0])
            pass
        else:
            error_message.append(Errors[2])
    #18位身份号码检测
    elif(len(idcard)==18):
        #出生日期的合法性检查
        #闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
        #平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
        if(int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10])%4 == 0 )):
            ereg=re.compile('[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')#//闰年出生日期的合法性正则表达式
        else:
            ereg=re.compile('[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')#//平年出生日期的合法性正则表达式
        #//测试出生日期的合法性
        if(re.match(ereg,idcard)):
            #//计算校验位
            S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(idcard_list[11])) * 9 + (int(idcard_list[2]) + int(idcard_list[12])) * 10 + (int(idcard_list[3]) + int(idcard_list[13])) * 5 + (int(idcard_list[4]) + int(idcard_list[14])) * 8 + (int(idcard_list[5]) + int(idcard_list[15])) * 4 + (int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 + int(idcard_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]#判断校验位
            if(M == idcard_list[17]):#检测ID的校验位
                #error_message.append(Errors[0])
                pass
            else:
                error_message.append(Errors[3])
        else:
            error_message.append(Errors[2])
    else:
        error_message.append(Errors[1])
    return error_message
def validateEmail(email):
        error_email=''
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
                error_email=u'邮箱格式错误！'
        else:
            error_email=u'邮箱长度过短！'
            
        return error_email
class candidatesForm(ModelForm):
    class Meta:
        model = candidates
        exclude=()
        widgets = {
            'first_school':autocomplete.ModelSelect2(url='schools-autocomplete'),
            'finnal_school':autocomplete.ModelSelect2(url='schools-autocomplete'),
        }
    def clean_id_num(self):
        id_num=self.cleaned_data['id_num']
        error_message=checkIdcard(id_num)
        if error_message:
            raise forms.ValidationError(error_message)
        return id_num
    def clean_phone_num(self):
        error_message=''
        phone_num=self.cleaned_data['phone_num']
        if len(phone_num)<11:
            error_message='手机号长度不足'
        else:
            p=re.match("([1][0-9]{10})",phone_num)
            if p:
                phone_num=p.group()
            else:
                error_message='手机号校验失败'
        if error_message:
            raise forms.ValidationError(error_message)
        return phone_num
    def clean_email(self):
        email=self.cleaned_data['email']
        error_message=validateEmail(email)
        if error_message:
            raise forms.ValidationError(error_message)
        return email