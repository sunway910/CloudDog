from django.db import models
from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField

class ProjectAccount(models.Model):
    """Project Account Property"""
    id = models.AutoField(primary_key=True, db_comment='主键ID')
    account = models.CharField(default='', max_length=100, verbose_name='Account', db_comment='项目账号')
    project_name = models.CharField(default='', max_length=100, verbose_name='ProjectName', db_comment='项目名称')
    project_access_key = models.CharField(default='', max_length=100, verbose_name='AK', db_comment='RAM Access Key')
    project_secret_key = models.CharField(default='', max_length=100, verbose_name='SK', db_comment='RAM Secret Key')
    key_authority = models.CharField(default='', max_length=100, verbose_name='KeyAuthority', db_comment='Key的权限')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='CreateTime', db_comment='账号创建时间')
    region = models.CharField(default='cn-hongkong', max_length=200, verbose_name='Region', db_comment='项目地域，可以多地域，逗号分隔')

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'project_account'
        ordering = ['-id']
