from django.db import models
from django.utils import timezone

from product.alibabacloud_product.models import ProductType


class Event(models.Model):
    EventType = (
        ('expired', '资源已过期'),
        ('expiring', '资源即将过期'),
        ('exception', '资源状态异常'),
    )

    MessageStatus = (
        ('unread', '未读'),
        ('read', '已读'),
        ('trash', '垃圾箱'),
    )

    id = models.AutoField(primary_key=True, db_comment='主键ID')
    project_name = models.CharField(default="", max_length=100, verbose_name='ProjectName', db_comment='项目名称')
    instance_id = models.CharField(default="", max_length=200, verbose_name='InstanceId', db_comment='实例ID')
    create_time = models.DateField(default=timezone.now, verbose_name='CreateTime', db_comment='事件创建时间')
    event_message = models.TextField(default="", verbose_name="MessageInfo", db_comment="事件内容")
    event_type = models.CharField(default="", max_length=100, verbose_name='EventType', db_comment='事件类型', choices=EventType)
    product_type = models.CharField(default="", max_length=100, verbose_name='ProductType', db_comment='云产品类型', choices=ProductType.choices)
    status = models.CharField(default="unread", max_length=100, verbose_name='MessageStatus', db_comment='消息状态', choices=MessageStatus)

    def __str__(self):
        return self.project_name

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)

    class Meta:
        db_table = 'event'
        ordering = ['-id']
