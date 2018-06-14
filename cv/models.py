from django.db import models
from post.models import positions
from accounts.models import provience as pro
from duals.models import schools
#from interview.models import interview_choices
# Create your models here.
from django.contrib.auth.models import User
from django.template.defaultfilters import default
minzu_choices=(
    ('1','汉族'),('2','蒙古族'),('3','回族'),('4','藏族'),('5','维吾尔族'),('6','苗族'),
    ('7','彝族'),('8','壮族'),('9','布依族'),('10','朝鲜族'),('11','满族'),('12','侗族'),
    ('13','瑶族'),('14','白族'),('15','土家族'),('16','哈尼族'),('17','哈萨克族'),('18','傣族'),
    ('19','黎族'),('20','傈僳族'),('21','佤族'),('22','畲族'),('23','高山族'),('24','拉祜族'),
    ('25','水族'),('26','东乡族'),('27','纳西族'),('28','景颇族'),('29','柯尔克孜族'),('30','土族'),
    ('31','达斡尔族'),('32','仫佬族'),('33','羌族'),('34','布朗族'),('35','撒拉族'),('36','毛南族'),
    ('37','仡佬族'),('38','锡伯族'),('39','阿昌族'),('40','普米族'),('41','塔吉克族'),('42','怒族'),
    ('43','乌孜别克族'),('44','俄罗斯族'),('45','鄂温克族'),('46','崩龙族'),('47','保安族'),('48','裕固族'),
    ('49','京族'),('50','塔塔尔族'),('51','独龙族'),('52','鄂伦春族'),('53','赫哲族'),('54','门巴族'),
    ('55','珞巴族'),('56','基诺族'),('57','其他'),('58','外国血统')
)
provience_choices=(
    ('1','北京'),('2','天津'),('3','河北'),('4','山西'),('5','内蒙古'),('6','辽宁'),('7','吉林'),('8','黑龙江'),
    ('9','上海'),('10','江苏'),('11','浙江'),('12','安徽'),('13','福建'),('14','江西'),('15','山东'),('16','河南'),
    ('17','湖北'),('18','湖南'),('19','广东'),('20','广西'),('21','海南'),('22','重庆'),('23','四川'),('24','贵州'),
    ('25','云南'),('26','西藏'),('27','陕西'),('28','甘肃'),('29','青海'),('30','宁夏'),('31','新疆'),('32','香港'),
    ('33','澳门'),('34','台湾')
)
marital_choices=(('1','未婚'),('2','已婚'),('3','离异'),('4','丧偶'))
politics_choices=(('1','共青团员'),('2','中共党员'),('3','群众'),('4','预备党员'),('5','其它'))
sex_choices=(('m','男'),('f','女'))
inter_status_choices=(('0','简历待处理'),('1','已预约'),('2','通过'),('3','淘汰'),('4','已提交预入职'),('5','预入职通过'),('6','已入职'),('7','未入职'))

class base_info(models.Model):
    cuser=models.OneToOneField(User,verbose_name='用户名')
    position=models.ForeignKey(positions,verbose_name='申请职位',null=True,blank=True)
    provience_applied=models.ForeignKey(pro,verbose_name='申请分校',null=True,blank=True)
    channel=models.CharField('应聘渠道',max_length=10)
    name=models.CharField('姓名',max_length=10)
    sex=models.CharField('性别',max_length=1,choices=sex_choices)
    minzu=models.CharField('民族',max_length=2,choices=minzu_choices)
    provience=models.CharField('籍贯',max_length=2,choices=provience_choices)
    phone_num=models.CharField('手机号',max_length=11)
    marital_status=models.CharField('婚姻状况',max_length=1,choices=marital_choices,default='1')
    politics_status=models.CharField('政治面貌',max_length=1,choices=politics_choices)
    id_num=models.CharField('身份证号',max_length=18)
    language=models.CharField('外语语种',max_length=20)
    language_leve=models.CharField('外语水平',max_length=20)
    teacher_cert=models.BooleanField('教师资格证')
    #other_cert=models.TextField('证书',max_length=300,null=True,blank=True)
    address=models.CharField('现居住地',max_length=100,null=True,blank=True)
    photo=models.ImageField("一寸照片",upload_to='photos/%Y/%m/%d')
    salary_except=models.PositiveIntegerField('期望月薪(元)')
    salary_monthly=models.PositiveIntegerField('基本月薪(元)',null=True,blank=True)
    salary_annual=models.PositiveIntegerField('目标年薪(元)',null=True,blank=True)
    update_time=models.DateTimeField('填写时间',auto_now_add=True)
    stage=models.ForeignKey('interview.interview_choices',verbose_name='面试阶段',null=True,blank=True)
    status=models.CharField('面试状态',max_length=1,choices=inter_status_choices,default='0')
    remark=models.CharField('备注',max_length=100,null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '应聘者'
        verbose_name_plural = '应聘者管理'
class education_info(models.Model):
    name=models.ForeignKey(base_info,editable=False,verbose_name='姓名',related_name='base_edu_info')
    degree=models.CharField('学历',max_length=1,choices=(('a','专科'),('b','本科'),('c','硕士'),('d','博士')))
    school=models.ForeignKey(schools,verbose_name='毕业院校')
    major=models.CharField('专业',max_length=20)
    start_date=models.DateField('教育经历起始日期')
    end_date=models.DateField('教育经历结束日期')
    activities=models.TextField('在校期间获得的活动',max_length=200,null=True,blank=True)
    awards=models.TextField('在校期间获得的奖项',max_length=200,null=True,blank=True)
    def __str__(self):
        return self.school.pc
    class Meta:
        verbose_name = '应聘者教育经历'
        verbose_name_plural = '应聘者教育经历管理'
class work_info(models.Model):
    name=models.ForeignKey(base_info,editable=False,verbose_name='姓名')
    company=models.CharField('公司名称',max_length=30)
    position=models.CharField('职位名称',max_length=30)
    start_date=models.DateField('教育经历起始日期')
    end_date=models.DateField('教育经历结束日期')
    activities=models.TextField('工作/实习期间主要工作内容',max_length=200,null=True,blank=True)
    def __str__(self):
        return self.company
    class Meta:
        verbose_name = '应聘者工作/实习经历'
        verbose_name_plural = '应聘者工作/实习经历管理'