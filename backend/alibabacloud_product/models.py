from django.utils import timezone
from django.db import models
from project.models import Project
from abc import abstractmethod
import logging

logger = logging.getLogger('cpm')


class ProductType(models.TextChoices):
    ECS = ('ecs', '服务器')
    WAF = ('waf', 'Web应用防火墙')

    class Meta:
        app_label = 'ProductType'


class ProductBaseModel(models.Model):
    api_request_id = models.CharField(primary_key=True, default='', max_length=100, db_comment='API Request Id')
    instance_id = models.CharField(default='', max_length=50, verbose_name='InstanceId', db_comment='实例ID')
    request_time = models.DateTimeField(default=timezone.now, max_length=30, verbose_name='RequestTime', db_comment='API请求时间')
    product_type = models.CharField(default=ProductType.ECS.value, max_length=60, verbose_name='ProductType', db_comment='云产品类型', choices=ProductType.choices)
    project_name = models.CharField(default='', max_length=30, verbose_name='Project Name', db_comment='项目名称')
    project = models.ForeignKey(
        to="project.Project",  # which table
        to_field="id",  # which column in table
        # https://foofish.net/django-foreignkey-on-delete.html
        on_delete=models.CASCADE,  # When a project is deleted, all products belonging to that project will be deleted
        related_name='productInProject'  # query a product info from project: project.productInProject.all()
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'ProductBasicInfo'

    @abstractmethod
    def get_basic_info(self):
        pass


class AlibabacloudEcsApiResponse(ProductBaseModel):
    Status = (
        ('Pending', '创建中'),
        ('Running', '运行中'),
        ('Starting', '启动中'),
        ('Stopping', '停止中'),
        ('Stopped', '已停止'),
    )
    LockReason = (
        ('financial', '因欠费被锁定'),
        ('security', '因安全原因被锁定'),
        ('Recycling', '抢占式实例的待释放锁定状态'),
        ('dedicatedhostfinancial', '因为专有宿主机欠费导致ECS实例被锁定'),
        ('refunded', '因退款被锁定'),
    )
    InternetChargeType = (
        ('PayByBandwidth', '按固定带宽计费'),
        ('PayByTraffic', '按使用流量计费'),
    )
    InstanceChargeType = (
        ('PostPaid', '按量付费'),
        ('PrePaid', '包年包月')
    )
    StoppedMode = (
        ('KeepCharging', '停机后继续收费，为您继续保留库存资源'),
        ('StopCharging', '停机后不收费。停机后，我们释放实例对应的资源，例如vCPU、内存和公网IP等资源。重启是否成功依赖于当前地域中是否仍有资源库存'),
        ('Not-applicable', '本实例不支持停机不收费功能'),
    )
    project = models.ForeignKey(
        to="project.Project",
        to_field="id",
        on_delete=models.CASCADE,
        related_name='ECSInProject'
    )

    """ ECS Instance Property """
    product_type = models.CharField(default=ProductType.ECS.value, max_length=60, verbose_name='ProductType', db_comment='云产品类型', choices=ProductType.choices)
    auto_renew_enabled = models.BooleanField(default=True, verbose_name='AutoRenewEnabled', db_comment='是否已开启自动续费功能')
    instance_name = models.CharField(default='', max_length=30, verbose_name='InstanceName', db_comment='实例的自定义名称')
    renewal_status = models.CharField(default='', max_length=30, verbose_name='RenewalStatus', db_comment='实例的自动续费状态')
    period_init = models.CharField(default='', max_length=20, verbose_name='PeriodUnit', db_comment='自动续费时长的单位')
    duration = models.IntegerField(default=0, verbose_name='Duration', db_comment='自动续费时长')
    region_id = models.CharField(default='', max_length=30, verbose_name='RegionId', db_comment='实例地域')
    ecs_status = models.CharField(default='', max_length=20, verbose_name='EcsStatus', db_comment='实例状态', choices=Status)
    instance_charge_type = models.CharField(default='', max_length=30, verbose_name='InstanceChargeType', db_comment='实例付费类型', choices=InstanceChargeType)
    internet_charge_type = models.CharField(default='', max_length=30, verbose_name='InternetChargeType', db_comment='按固定带宽/使用流量计费', choices=InternetChargeType)
    expired_time = models.CharField(default='', max_length=30, verbose_name='ExpiredTime', db_comment='过期时间')
    stopped_mode = models.CharField(default='', max_length=30, verbose_name='StoppedMode', db_comment='实例停机后是否继续收费', choices=StoppedMode)
    start_time = models.CharField(default='', max_length=50, verbose_name='StartTime', db_comment='实例最近一次的启动时间')
    auto_release_time = models.CharField(default='', max_length=50, verbose_name='AutoReleaseTime', db_comment='按量付费实例的自动释放时间')
    lock_reason = models.CharField(default='', max_length=30, verbose_name='LockReason', db_comment='实例的锁定原因', choices=LockReason)

    def get_basic_info(self):
        to_string = 'ECS LOG: {} \'s instance {} in {} status is {}'.format(self.project_name, self.instance_name, self.region_id, self.ecs_status)
        return to_string

    class Meta:
        db_table = 'alibabacloud_ecs_api_response'


class AlibabacloudWafApiResponse(ProductBaseModel):
    Status = (
        (1, '表示正常'),
        (2, '表示到期'),
        (3, '表示释放'),
    )
    Edition = (
        ('Basic', '基础版'),
        ('Pro', '高级版'),
        ('Business', '企业版'),
        ('Enterprise', '旗舰版'),
    )
    Region = (
        ('cn-hangzhou', '表示中国内地'),
        ('ap-southeast-1', '表示非中国内地'),
    )
    PayType = (
        ('POSTPAY', '已开通按量付费WAF实例'),
        ('PREPAY', '表示已开通包年包月WAF实例'),
    )
    InDebt = (
        (0, '表示已欠费'),
        (1, '表示正常'),
    )
    project = models.ForeignKey(
        to="project.Project",
        to_field="id",
        on_delete=models.CASCADE,
        related_name='WAFInProject'
    )

    """ WAF Instance Property """
    product_type = models.CharField(default=ProductType.WAF.value, max_length=60, verbose_name='ProductType', db_comment='云产品类型', choices=ProductType.choices)
    waf_status = models.IntegerField(default=None, verbose_name='WafStatus', db_comment='WAF实例的当前状态', choices=Status)
    end_time = models.BigIntegerField(default=None, verbose_name='EndDate', db_comment='WAF实例的到期时间')
    edition = models.CharField(default='', max_length=40, verbose_name='Edition', db_comment='WAF实例的版本', choices=Edition)
    region = models.CharField(default='', max_length=30, verbose_name='Region', db_comment='WAF实例的地域', choices=Region)
    pay_type = models.CharField(default=None, verbose_name='PayType', db_comment='WAF实例的付费类型', choices=PayType)
    in_debt = models.IntegerField(default=1, verbose_name='InDebt', db_comment='WAF实例是否存在欠费', choices=InDebt)
    start_time = models.BigIntegerField(verbose_name='StartTime', db_comment='购买时间')

    def get_basic_info(self):
        to_string = 'WAF LOG: {} \'s instance {} in {} status is {}'.format(self.project_name, self.instance_id, self.region, self.waf_status)
        return to_string

    class Meta:
        db_table = 'alibabacloud_waf_api_response'
