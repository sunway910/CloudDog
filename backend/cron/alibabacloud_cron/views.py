import json
from abc import ABC

from alibabacloud_alb20200616 import models as alb_20200616_models
from alibabacloud_alb20200616.client import Client as AlbApiClient
from alibabacloud_cas20200630 import models as cas_20200630_models
from alibabacloud_cas20200630.client import Client as casApiClient
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_ecs20140526.client import Client as EcsApiClient
from alibabacloud_sas20181203 import models as sas_20181203_models
from alibabacloud_sas20181203.client import Client as CscApiClient
from alibabacloud_slb20140515 import models as slb_20140515_models
from alibabacloud_slb20140515.client import Client as SlbApiClient
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_vpc20160428 import models as vpc_20160428_models
from alibabacloud_vpc20160428.client import Client as VpcApiClient
from alibabacloud_waf_openapi20211001 import models as waf_openapi_20211001_models
from alibabacloud_waf_openapi20211001.client import Client as WAFApiClient

from config import settings
from cron.base_cron.views import DjangoJobViewSet
from message.models import Event
from message.views import send_message
from product.alibabacloud_product.models import *
from project.models import Project
from utils import set_api_client_config

logger = logging.getLogger('clouddog')


# cron: sunday 01:10AM exec the job
# @register_job(scheduler, 'cron', day_of_week='sun', hour='1', minute='10', id='get_ali_ecr_api_response')
def get_ecs_api_response() -> None:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False,
                                           cron_toggle=True).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = EcsApiClient(set_api_client_config(project['project_access_key'],
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
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False,
                                           cron_toggle=True).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for endpoint in settings.ENDPOINT['WAF_ENDPOINT']:
            client = WAFApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['WAF_ENDPOINT'][endpoint]))
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
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False,
                                           cron_toggle=True).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = SlbApiClient(set_api_client_config(project['project_access_key'],
                                                    project['project_secret_key'],
                                                    settings.ENDPOINT['SLB_ENDPOINT']['general']))
        for region in project['region']:
            describe_load_balancers_request = slb_20140515_models.DescribeLoadBalancersRequest(region_id=region)
            try:
                res = client.describe_load_balancers_with_options(describe_load_balancers_request, runtime)
                describe_slb_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_slb_attribute_response_json_obj = json.loads(describe_slb_attribute_response_to_str)
                if describe_slb_attribute_response_json_obj['body']['TotalCount'] > 0:
                    slb_info = describe_slb_attribute_response_json_obj['body']['LoadBalancers']
                    for num, slb_instance in enumerate(slb_info):
                        describe_load_balancer_attribute_request = slb_20140515_models.DescribeLoadBalancerAttributeRequest(region_id=region, load_balancer_id=slb_instance['InstanceId'])
                        detail_res = client.describe_load_balancer_attribute_with_options(describe_load_balancer_attribute_request, runtime)
                        describe_slb_detail_attribute_response_to_str = UtilClient.to_jsonstring(detail_res)
                        describe_slb_detail_attribute_response_json_obj = json.loads(describe_slb_detail_attribute_response_to_str)
                        slb_instance_detail = describe_slb_detail_attribute_response_json_obj['body']
                        slb = AlibabacloudSLBApiResponse(api_request_id=(describe_slb_attribute_response_json_obj['body']['RequestId'] + str(num)),
                                                         instance_id=slb_instance['InstanceId'],
                                                         project_name=project['project_name'],
                                                         project_id=project['id'],
                                                         bandwidth=slb_instance_detail['Bandwidth'],
                                                         end_time_stamp=slb_instance_detail['EndTimeStamp'],
                                                         end_time=slb_instance_detail['EndTime'],
                                                         auto_release_time=slb_instance_detail['AutoReleaseTime'],
                                                         renewal_status=slb_instance_detail['RenewalStatus'],
                                                         renewal_duration=slb_instance_detail['RenewalDuration'],
                                                         renewal_cyc_unit=slb_instance_detail['RenewalCycUnit'],
                                                         create_time=slb_instance['CreateTime'],
                                                         pay_type=slb_instance['PayType'],
                                                         internet_charge_type=slb_instance['InternetChargeType'],
                                                         load_balancer_name=slb_instance['LoadBalancerName'],
                                                         address=slb_instance['Address'],
                                                         address_type=slb_instance['AddressType'],
                                                         address_ip_version=slb_instance['AddressIPVersion'],
                                                         region_id=slb_instance['RegionId'],
                                                         load_balancer_status=slb_instance['LoadBalancerStatus'],
                                                         load_balancer_spec=slb_instance['LoadBalancerSpec'],
                                                         instance_charge_type=slb_instance['InstanceChargeType'],
                                                         master_zone_id=slb_instance['MasterZoneId'],
                                                         slave_zone_id=slb_instance['SlaveZoneId'],
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
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False,
                                           cron_toggle=True).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for region in project['region']:
            client = AlbApiClient(set_api_client_config(project['project_access_key'],
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


# @register_job(scheduler, 'cron', day_of_week='sun', hour='1', minute='50', id='get_ali_alb_api_response')
def get_eip_api_response() -> None:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False,
                                           cron_toggle=True).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for region in project['region']:
            client = VpcApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['VPC_ENDPOINT'][region]))
            describe_eip_addresses_request = vpc_20160428_models.DescribeEipAddressesRequest(region_id=region)
            try:
                res = client.describe_eip_addresses_with_options(describe_eip_addresses_request, runtime)
                describe_eip_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_eip_attribute_response_json_obj = json.loads(describe_eip_attribute_response_to_str)
                if describe_eip_attribute_response_json_obj['body']['TotalCount'] > 0:
                    eip_info = describe_eip_attribute_response_json_obj['body']['EipAddresses']
                    for num, eip_instance in enumerate(eip_info):
                        eip = AlibabacloudEIPApiResponse(api_request_id=(describe_eip_attribute_response_json_obj['body']['RequestId'] + str(num)),
                                                         instance_id=eip_instance['InstanceId'],
                                                         project_name=project['project_name'],
                                                         project_id=project['id'],
                                                         name=eip_instance['Name'],
                                                         region_id=eip_instance['RegionId'],
                                                         expired_time=eip_instance['ExpiredTime'],
                                                         allocation_id=eip_instance['AllocationId'],
                                                         instance_type=eip_instance['InstanceType'],
                                                         internet_charge_type=eip_instance['InternetChargeType'],
                                                         business_status=eip_instance['BusinessStatus'],
                                                         reservation_bandwidth=eip_instance['ReservationBandwidth'],
                                                         bandwidth=eip_instance['Bandwidth'],
                                                         ip_address=eip_instance['IpAddress'],
                                                         reservation_internet_charge_type=eip_instance['ReservationInternetChargeType'],
                                                         charge_type=eip_instance['ChargeType'],
                                                         net_mode=eip_instance['Netmode'],
                                                         allocation_time=eip_instance['AllocationTime'],
                                                         status=eip_instance['Status'],
                                                         reservation_active_time=eip_instance['ReservationActiveTime'],
                                                         )
                        logger.info(eip.get_basic_info())
                        eip.save()
                        if eip.status != 'Associating':
                            message = "project {} eip {} status is no Associating".format(project['project_name'], eip_instance['Status'])
                            event = Event(
                                project_name=project['project_name'],
                                event_type="exception",
                                instance_id=eip_instance['InstanceId'],
                                product_type='eip',
                                event_message=message)
                            event.save()
                            send_message(event)
                            logger.info(message)
            except Exception as error:
                UtilClient.assert_as_string(error)


# @register_job(scheduler, 'cron', day_of_week='sun', hour='1', minute='55', id='get_ali_alb_api_response')
def get_ssl_api_response() -> None:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False,
                                           cron_toggle=True).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for endpoint in settings.ENDPOINT['SSL_ENDPOINT']:
            client = casApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['SSL_ENDPOINT'][endpoint]))
            list_client_certificate_request = cas_20200630_models.ListClientCertificateRequest()
            try:
                res = client.list_client_certificate_with_options(list_client_certificate_request, runtime)
                describe_ssl_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_ssl_attribute_response_json_obj = json.loads(describe_ssl_attribute_response_to_str)
                if describe_ssl_attribute_response_json_obj['body']['TotalCount'] > 0:
                    ssl_info = describe_ssl_attribute_response_json_obj['body']['CertificateList']
                    for num, ssl_instance in enumerate(ssl_info):
                        ssl = AlibabacloudSSLApiResponse(api_request_id=(describe_ssl_attribute_response_json_obj['body']['RequestId'] + str(num)),
                                                         instance_id=ssl_instance['Identifier'],
                                                         project_name=project['project_name'],
                                                         project_id=project['id'],
                                                         subject_dn=ssl_instance['SubjectDN'],
                                                         common_name=ssl_instance['CommonName'],
                                                         organization_unit=ssl_instance['OrganizationUnit'],
                                                         organization=ssl_instance['Organization'],
                                                         status=ssl_instance['Status'],
                                                         BeforeDate=ssl_instance['BeforeDate'],
                                                         AfterDate=ssl_instance['AfterDate'],
                                                         days=ssl_instance['Days'],
                                                         )
                        logger.info(ssl.get_basic_info())
                        ssl.save()
                        if ssl.status != 'ISSUE':
                            message = "project {} ssl certificate {} status is REVOKE".format(project['project_name'], ssl_instance['Status'])
                            event = Event(
                                project_name=project['project_name'],
                                event_type="exception",
                                instance_id=ssl_instance['Identifier'],
                                product_type='ssl',
                                event_message=message)
                            event.save()
                            send_message(event)
                            logger.info(message)
            except Exception as error:
                UtilClient.assert_as_string(error)


# @register_job(scheduler, 'cron', day_of_week='sun', hour='2', minute='00', id='get_ali_alb_api_response')
def get_csc_api_response() -> None:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False,
                                           cron_toggle=True).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for endpoint in settings.ENDPOINT['CSC_ENDPOINT']:
            client = CscApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['CSC_ENDPOINT'][endpoint]))
            describe_version_config_request = sas_20181203_models.DescribeVersionConfigRequest()
            try:
                # https://next.api.aliyun.com/api/Sas/2018-12-03/DescribeVersionConfig
                res = client.describe_version_config_with_options(describe_version_config_request, runtime)
                describe_csc_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_csc_attribute_response_json_obj = json.loads(describe_csc_attribute_response_to_str)
                csc_info = describe_csc_attribute_response_json_obj['body']
                csc = AlibabacloudSSLApiResponse(api_request_id=(describe_csc_attribute_response_json_obj['body']['RequestId']),
                                                 instance_id=csc_info['InstanceId'],
                                                 project_name=project['project_name'],
                                                 project_id=project['id'],
                                                 mv_auth_count=csc_info['MVAuthCount'],
                                                 sas_log=csc_info['SasLog'],
                                                 sas_screen=csc_info['SasScreen'],
                                                 honeypot_capacity=csc_info['HoneypotCapacity'],
                                                 mv_unused_auth_count=csc_info['MVUnusedAuthCount'],
                                                 web_lock=csc_info['WebLock'],
                                                 app_white_list_auth_count=csc_info['AppWhiteListAuthCount'],
                                                 last_trail_end_time=csc_info['LastTrailEndTime'],
                                                 version=csc_info['Version'],
                                                 web_lock_auth_count=csc_info['WebLockAuthCount'],
                                                 release_time=csc_info['ReleaseTime'],
                                                 highest_version=csc_info['HighestVersion'],
                                                 asset_level=csc_info['AssetLevel'],
                                                 is_over_balance=csc_info['IsOverBalance'],
                                                 sls_capacity=csc_info['SlsCapacity'],
                                                 vm_cores=csc_info['VmCores'],
                                                 allow_partial_buy=csc_info['AllowPartialBuy'],
                                                 app_white_list=csc_info['AppWhiteList'],
                                                 image_scan_capacity=csc_info['ImageScanCapacity'],
                                                 is_trial_version=csc_info['IsTrialVersion'],
                                                 user_defined_alarms=csc_info['UserDefinedAlarms'],
                                                 open_time=csc_info['OpenTime'],
                                                 is_new_container_version=csc_info['IsNewContainerVersion'],
                                                 is_new_multi_version=csc_info['IsNewMultiVersion'],
                                                 threat_analysis_capacity=csc_info['ThreatAnalysisCapacity'],
                                                 cspm_capacity=csc_info['CspmCapacity'],
                                                 vul_fix_capacity=csc_info['VulFixCapacity'],
                                                 )
                logger.info(csc.get_basic_info())
                csc.save()
            except Exception as error:
                UtilClient.assert_as_string(error)


class AliECSDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_ecs_api_response()


class AliWAFDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_waf_api_response()


class AliSLBDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_slb_api_response()


class AliALBDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_alb_api_response()


class AliSSLDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_ssl_api_response()


class AliCSCDjangoJobViewSet(DjangoJobViewSet, ABC):
    def custom_job(self):
        get_csc_api_response()
