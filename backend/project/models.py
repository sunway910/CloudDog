from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Project(models.Model):
    CloudPlatform = (
        ('Alibabacloud', '阿里云国际'),
        ('Aliyun', '阿里云大陆'),
        ('AWS', '亚马逊云平台'),
        ('Azure', '微软云平台'),
        ('GCP', '谷歌云平台'),
    )

    Status = (
        ('Running', '运行中'),
        ('Stopped', '已终止'),
    )

    """Project Account Property"""
    id = models.AutoField(primary_key=True, db_comment='主键ID')
    cloud_platform = models.CharField(default='AlibabaCloud', max_length=100, verbose_name='CloudPlatform', db_comment='云平台类型', choices=CloudPlatform)
    account = ArrayField(models.CharField(), default=list, verbose_name='Account', db_comment='项目RAM账号')
    region = ArrayField(models.CharField(default='Hongkong'), default=list, verbose_name='Region', db_comment='地域')
    project_name = models.CharField(unique=True, default='MTR', max_length=500, verbose_name='ProjectName', db_comment='项目名称')
    project_access_key = models.CharField(default='', max_length=100, verbose_name='AK', db_comment='Access Key')
    project_secret_key = models.CharField(default='', max_length=100, verbose_name='SK', db_comment='Secret Key')
    key_authority = models.CharField(default='ReadOnlyAccess', max_length=50, verbose_name='KeyAuthority', db_comment='Key的权限')
    status = models.CharField(default='Running', max_length=30, verbose_name='ProjectStatus', db_comment='项目状态', choices=Status)
    create_time = models.DateField(default=timezone.now, verbose_name='CreateTime', db_comment='账号创建时间')

    def __str__(self):
        return self.project_name

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

    class Meta:
        db_table = 'project'
        ordering = ['-id']
