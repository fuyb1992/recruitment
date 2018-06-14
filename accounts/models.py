from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class provience(models.Model):
    name=models.CharField('分校',max_length=5)
    def __str__(self):
        return  self.name
    class Meta:
        verbose_name='分校'
        verbose_name_plural='分校管理'

class department(models.Model):
    name=models.CharField("部门",max_length=20)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='部门'
        verbose_name_plural='部门管理'
class my_authority(models.Model):
    admin_user=models.OneToOneField(User,on_delete=models.CASCADE)
    admin_authority_dep=models.ManyToManyField(department,verbose_name="部门")
    admin_authority_pro=models.ManyToManyField(provience,verbose_name="分校")
    def __str__(self):
        return self.admin_user.username
    def getdep(self):
        return ','.join([obj.name for obj in self.admin_authority_dep.all()])
    getdep.short_description='部门权限'
    def getpro(self):
        return ','.join([obj.name for obj in self.admin_authority_pro.all()])
    getpro.short_description='分校权限'
    class Meta:
        verbose_name='权限'
        verbose_name_plural='权限管理'