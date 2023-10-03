import json
from abc import ABC

from alibabacloud_alb20200616 import models as alb_20200616_models
from alibabacloud_alb20200616.client import Client as AlbApiClient
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_ecs20140526.client import Client as EcsApiClient
from alibabacloud_slb20140515 import models as slb_20140515_models
from alibabacloud_slb20140515.client import Client as SlbApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_waf_openapi20211001 import models as waf_openapi_20211001_models
from alibabacloud_waf_openapi20211001.client import Client as WAFApiClient

from config import settings
from cron.base_cron.views import DjangoJobViewSet
from message.models import Event
from message.views import send_message
from product.alibabacloud_product.models import *
from project.models import Project

logger = logging.getLogger('cpm')


def set_client_config(access_key_id: str, access_key_secret: str, endpoint: str) -> open_api_models.Config:
    """
    use AK&SK to init Client
    @param access_key_id: AK
    @param access_key_secret: SK
    @param endpoint: xxx-cn-region.aliyuncs.com
    @return: open_api_models.Config
    @throws Exception
    """
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )
    # Endpoint Ref: https://api.aliyun.com/product/Ecs
    config.endpoint = endpoint
    return config


# cron: sunday 01:10AM exec the job
# @register_job(scheduler, 'cron', day_of_week='sun', hour='1', minute='10', id='get_ali_ecr_api_response')
def get_ecr_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = EcsApiClient(set_client_config(project['project_access_key'],
                                                project['project_secret_key'],
                                                settings.ENDPOINT['ECS_ENDPOINT']['mainland']))
        for region in project['region']:
            describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(region_id=region)
            try:
                # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstances
                describe_instance_response = client.describe_instances_with_options(describe_instances_request, runtime)
                describe_instance_response_to_str = UtilClient.to_jsonstring(describe_instance_response)
                describe_instance_response_json_obj = json.loads(describe_instance_response_to_str)
                instance_list = describe_instance_response_json_obj['body']['Instances']['Instance']
                for instance in instance_list:
                    describe_instance_auto_renew_attribute_request = ecs_20140526_models.DescribeInstanceAutoRenewAttributeRequest(region_id=region, instance_id=instance['InstanceId'])
                    # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstanceAutoRenewAttribute
                    describe_instance_auto_renew_attribute_response = client.describe_instance_auto_renew_attribute_with_options(describe_instance_auto_renew_attribute_request, runtime)
                    describe_instance_auto_renew_attribute_response_to_str = UtilClient.to_jsonstring(describe_instance_auto_renew_attribute_response)
                    describe_instance_auto_renew_attribute_response_json_obj = json.loads(describe_instance_auto_renew_attribute_response_to_str)
                    instance_auto_renew_info = describe_instance_auto_renew_attribute_response_json_obj['body']['InstanceRenewAttributes']['InstanceRenewAttribute'][0]
                    # request 2 API and get two request id, so the new request id is formed by combining two request id
                    request_id = describe_instance_response_json_obj['body']['RequestId'] + " " + describe_instance_auto_renew_attribute_response_json_obj['body']['RequestId']
                    ecs = AlibabacloudEcsApiResponse(api_request_id=request_id,
                                                     instance_id=instance['InstanceId'],
                                                     project_name=project['project_name'],
                                                     instance_name=instance['InstanceName'],
                                                     project_id=project['id'],
                                                     region_id=instance['RegionId'],
                                                     ecs_status=instance['Status'],
                                                     instance_charge_type=instance['InstanceChargeType'],
                                                     internet_charge_type=instance['InternetChargeType'],
                                                     expired_time=instance['ExpiredTime'],
                                                     stopped_mode=instance['StoppedMode'],
                                                     start_time=instance['StartTime'],
                                                     auto_release_time=instance['AutoReleaseTime'],
                                                     lock_reason=instance['OperationLocks']['LockReason'],
                                                     auto_renew_enabled=instance_auto_renew_info['AutoRenewEnabled'],
                                                     renewal_status=instance_auto_renew_info['RenewalStatus'],
                                                     period_init=instance_auto_renew_info['PeriodUnit'],
                                                     duration=instance_auto_renew_info['Duration'],
                                                     )
                    logger.info(ecs.get_basic_info())
                    ecs.save()
                    if ecs.ecs_status != "Running":
                        message = "project {} ecs {} status is no Running".format(project['project_name'], instance['InstanceId'])
                        event = Event(
                            project_name=project['project_name'],
                            event_type="exception",
                            instance_id=instance['InstanceId'],
                            product_type='ecs',
                            event_message=message)
                        event.save()
                        send_message(event)
                        logger.info(message)
            except Exception as error:
                UtilClient.assert_as_string(error)


# cron: sunday 01:20AM exec the job
# @register_job(scheduler, 'cron', day_of_week='sun', hour='1', minute='20', id='get_ali_waf_api_response')
def get_waf_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = WAFApiClient(set_client_config(project['project_access_key'],
                                                project['project_secret_key'],
                                                settings.ENDPOINT['WAF_ENDPOINT']['oversea']))
        describe_instance_info_request = waf_openapi_20211001_models.DescribeInstanceRequest()
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.describe_instance_with_options(describe_instance_info_request, runtime)
            describe_waf_attribute_response_to_str = UtilClient.to_jsonstring(res)
            describe_waf_attribute_response_json_obj = json.loads(describe_waf_attribute_response_to_str)
            waf_info = describe_waf_attribute_response_json_obj['body']
            waf = AlibabacloudWafApiResponse(api_request_id=waf_info['RequestId'],
                                             instance_id=waf_info['InstanceId'],
                                             project_name=project['project_name'],
                                             project_id=project['id'],
                                             waf_status=waf_info['Status'],
                                             end_time=waf_info['EndTime'],
                                             edition=waf_info['Edition'],
                                             region=waf_info['RegionId'],
                                             pay_type=waf_info['PayType'],
                                             in_debt=waf_info['InDebt'],
                                             start_time=waf_info['StartTime'],
                                             )
            logger.info(waf.get_basic_info())
            waf.save()
            if waf.waf_status != 1:
                message = "project {} waf {} status is no Running".format(project['project_name'], waf_info['Status'])
                event = Event(
                    project_name=project['project_name'],
                    event_type="exception",
                    instance_id=waf_info['InstanceId'],
                    product_type='waf',
                    event_message=message)
                event.save()
                send_message(event)
                logger.info(message)
        except Exception as error:
            UtilClient.assert_as_string(error)


# @register_job(scheduler, 'cron', day_of_week='sun', hour='1', minute='30', id='get_ali_slb_api_response')
def get_slb_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = SlbApiClient(set_client_config(project['project_access_key'],
                                                project['project_secret_key'],
                                                settings.ENDPOINT['SLB_ENDPOINT']['general']))
        for region in project['region']:
            describe_load_balancers_request = slb_20140515_models.DescribeLoadBalancersRequest(region)
            try:
                res = client.describe_load_balancers_with_options(describe_load_balancers_request, runtime)
                describe_slb_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_slb_attribute_response_json_obj = json.loads(describe_slb_attribute_response_to_str)
                slb_info = describe_slb_attribute_response_json_obj['body']['LoadBalancers']
                slb = AlibabacloudSLBApiResponse(api_request_id=slb_info['RequestId'],
                                                 instance_id=slb_info['InstanceId'],
                                                 project_name=project['project_name'],
                                                 project_id=project['id'],
                                                 create_time=slb_info['CreateTime'],
                                                 pay_type=slb_info['PayType'],
                                                 internet_charge_type=slb_info['InternetChargeType'],
                                                 load_balancer_name=slb_info['LoadBalancerName'],
                                                 address=slb_info['Address'],
                                                 address_type=slb_info['AddressType'],
                                                 address_ip_version=slb_info['AddressIPVersion'],
                                                 region_id=slb_info['RegionId'],
                                                 load_balancer_status=slb_info['LoadBalancerStatus'],
                                                 load_balancer_spec=slb_info['LoadBalancerSpec'],
                                                 instance_charge_type=slb_info['InstanceChargeType'],
                                                 master_zone_id=slb_info['MasterZoneId'],
                                                 slave_zone_id=slb_info['SlaveZoneId'],
                                                 )
                logger.info(slb.get_basic_info())
                slb.save()
                if slb.load_balancer_status != 'active':
                    message = "project {} slb {} status is no active".format(project['project_name'], slb_info['LoadBalancerStatus'])
                    event = Event(
                        project_name=project['project_name'],
                        event_type="exception",
                        instance_id=slb_info['InstanceId'],
                        product_type='slb',
                        event_message=message)
                    event.save()
                    send_message(event)
                    logger.info(message)
            except Exception as error:
                UtilClient.assert_as_string(error)


# @register_job(scheduler, 'cron', day_of_week='sun', hour='1', minute='40', id='get_ali_alb_api_response')
def get_alb_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for region in project['region']:
            client = AlbApiClient(set_client_config(project['project_access_key'],
                                                    project['project_secret_key'],
                                                    settings.ENDPOINT['ALB_ENDPOINT'][region]))
            list_load_balancers_request = alb_20200616_models.ListLoadBalancersRequest()
            try:
                res = client.list_load_balancers_with_options(list_load_balancers_request, runtime)
                describe_alb_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_alb_attribute_response_json_obj = json.loads(describe_alb_attribute_response_to_str)
                if describe_alb_attribute_response_json_obj['body']['TotalCount'] > 0:
                    alb_info = describe_alb_attribute_response_json_obj['body']['LoadBalancers']
                    alb = AlibabacloudALBApiResponse(api_request_id=describe_alb_attribute_response_json_obj['body']['RequestId'],
                                                     instance_id=alb_info['LoadBalancerId'],
                                                     project_name=project['project_name'],
                                                     project_id=project['id'],
                                                     create_time=alb_info['CreateTime'],
                                                     address_allocated_mode=alb_info['AddressAllocatedMode'],
                                                     address_type=alb_info['AddressType'],
                                                     dns_name=alb_info['DNSName'],
                                                     pay_type=alb_info['PayType'],
                                                     load_balancer_bussiness_status=alb_info['LoadBalancerBussinessStatus'],
                                                     load_balancer_edition=alb_info['LoadBalancerEdition'],
                                                     load_balancer_name=alb_info['LoadBalancerName'],
                                                     load_balancer_status=alb_info['LoadBalancerStatus'],
                                                     address_ip_version=alb_info['AddressIPVersion'],
                                                     ipv6_address_type=alb_info['Ipv6AddressType'],
                                                     )
                    logger.info(alb.get_basic_info())
                    alb.save()
                    if alb.load_balancer_status != 'Active':
                        message = "project {} alb {} status is no active".format(project['project_name'], alb_info['LoadBalancerStatus'])
                        event = Event(
                            project_name=project['project_name'],
                            event_type="exception",
                            instance_id=alb_info['InstanceId'],
                            product_type='alb',
                            event_message=message)
                        event.save()
                        send_message(event)
                        logger.info(message)
            except Exception as error:
                UtilClient.assert_as_string(error)


class AliECSDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_ecr_api_response()


class AliWAFDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_waf_api_response()


class AliSLBDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_slb_api_response()


class AliALBDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_alb_api_response()
