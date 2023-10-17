import asyncio
import json

from alibabacloud_alb20200616 import models as alb_20200616_models
from alibabacloud_alb20200616.client import Client as AlbApiClient
from alibabacloud_cas20200630 import models as cas_20200630_models
from alibabacloud_cas20200630.client import Client as casApiClient
from alibabacloud_cloudfw20171207 import models as cloudfw_20171207_models
from alibabacloud_cloudfw20171207.client import Client as CfwApiClient
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_ecs20140526.client import Client as EcsApiClient
from alibabacloud_r_kvstore20150101 import models as r_kvstore_20150101_models
from alibabacloud_r_kvstore20150101.client import Client as R_kvstoreApiClient
from alibabacloud_rds20140815 import models as rds_20140815_models
from alibabacloud_rds20140815.client import Client as RdsApiClient
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
from asgiref.sync import sync_to_async
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from config import settings
from handler import APIResponse
from paginator import CustomPaginator
from product.alibabacloud_product.serializers import *
from project.models import Project
from utils import set_api_client_config

logger = logging.getLogger('clouddog')


@sync_to_async
def get_ecs_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    ecs_total_count = 0
    for project in project_list:
        client = EcsApiClient(set_api_client_config(
            project['project_access_key'],
            project['project_secret_key'],
            settings.ENDPOINT['ECS_ENDPOINT']['oversea'])
        )
        for region in project['region']:
            describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(region_id=region)
            try:
                # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstances
                describe_instance_response = client.describe_instances_with_options(describe_instances_request, runtime)
                describe_instance_response_to_str = UtilClient.to_jsonstring(describe_instance_response)
                describe_instance_response_json_obj = json.loads(describe_instance_response_to_str)
                instance_list = describe_instance_response_json_obj['body']['Instances']['Instance']
                ecs_total_count += describe_instance_response_json_obj['body']['TotalCount']
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
                return APIResponse(code=0, msg='request successfully', total=ecs_total_count)
            except Exception as error:
                UtilClient.assert_as_string(error)
                return APIResponse(code=1, msg=error)


@sync_to_async
def get_waf_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for endpoint in settings.ENDPOINT['WAF_ENDPOINT']:
            client = WAFApiClient(set_api_client_config(
                project['project_access_key'],
                project['project_secret_key'],
                settings.ENDPOINT['WAF_ENDPOINT'][endpoint])
            )
            describe_instance_info_request = waf_openapi_20211001_models.DescribeInstanceRequest()
            try:
                # https://next.api.aliyun.com/api/waf-openapi/2019-09-10/DescribeInstanceInfo
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
                return APIResponse(code=0, msg='request successfully')
            except Exception as error:
                UtilClient.assert_as_string(error)
                return APIResponse(code=1, msg=error)


@sync_to_async
def get_slb_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    slb_total_count = 0
    for project in project_list:
        client = SlbApiClient(set_api_client_config(project['project_access_key'],
                                                    project['project_secret_key'],
                                                    settings.ENDPOINT['SLB_ENDPOINT']['general']))
        for region in project['region']:
            describe_load_balancers_request = slb_20140515_models.DescribeLoadBalancersRequest(region_id=region)
            try:
                # https://next.api.aliyun.com/api/Slb/2014-05-15/DescribeLoadBalancers
                res = client.describe_load_balancers_with_options(describe_load_balancers_request, runtime)
                describe_slb_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_slb_attribute_response_json_obj = json.loads(describe_slb_attribute_response_to_str)
                count = describe_slb_attribute_response_json_obj['body']['TotalCount']
                slb_total_count += count
                if count > 0:
                    slb_info = describe_slb_attribute_response_json_obj['body']['LoadBalancers']
                    for num, slb_instance in enumerate(slb_info):
                        describe_load_balancer_attribute_request = slb_20140515_models.DescribeLoadBalancerAttributeRequest(region_id=region, load_balancer_id=slb_instance['InstanceId'])
                        # https://next.api.aliyun.com/api/Slb/2014-05-15/DescribeLoadBalancerAttribute
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
                return APIResponse(code=0, msg='request successfully', total=slb_total_count)
            except Exception as error:
                UtilClient.assert_as_string(error)
                return APIResponse(code=1, msg=error)


@sync_to_async
def get_alb_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    alb_total_count = 0
    for project in project_list:
        for region in project['region']:
            client = AlbApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['ALB_ENDPOINT'][region]))
            list_load_balancers_request = alb_20200616_models.ListLoadBalancersRequest()
            try:
                # https://next.api.aliyun.com/api/Alb/2020-06-16/ListLoadBalancers
                res = client.list_load_balancers_with_options(list_load_balancers_request, runtime)
                describe_alb_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_alb_attribute_response_json_obj = json.loads(describe_alb_attribute_response_to_str)
                count = describe_alb_attribute_response_json_obj['body']['TotalCount']
                alb_total_count += count
                if count > 0:
                    alb_info = describe_alb_attribute_response_json_obj['body']['LoadBalancers']
                    for num, alb_instance in enumerate(alb_info):
                        alb = AlibabacloudALBApiResponse(api_request_id=(describe_alb_attribute_response_json_obj['body']['RequestId'] + str(num)),
                                                         instance_id=alb_instance['LoadBalancerId'],
                                                         project_name=project['project_name'],
                                                         project_id=project['id'],
                                                         create_time=alb_instance['CreateTime'],
                                                         address_allocated_mode=alb_instance['AddressAllocatedMode'],
                                                         address_type=alb_instance['AddressType'],
                                                         dns_name=alb_instance['DNSName'],
                                                         pay_type=alb_instance['LoadBalancerBillingConfig']['PayType'],
                                                         load_balancer_bussiness_status=alb_instance['LoadBalancerBussinessStatus'],
                                                         load_balancer_edition=alb_instance['LoadBalancerEdition'],
                                                         load_balancer_name=alb_instance['LoadBalancerName'],
                                                         load_balancer_status=alb_instance['LoadBalancerStatus'],
                                                         address_ip_version=alb_instance['AddressIpVersion'],
                                                         )
                        if alb.address_ip_version != 'Ipv4':
                            alb.ipv6_address_type = alb_instance['Ipv6AddressType']
                        logger.info(alb.get_basic_info())
                        alb.save()
                return APIResponse(code=0, msg='request successfully', total=alb_total_count)
            except Exception as error:
                UtilClient.assert_as_string(error)
                return APIResponse(code=1, msg=error)


@sync_to_async
def get_eip_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    eip_total_count = 0
    for project in project_list:
        for region in project['region']:
            client = VpcApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['VPC_ENDPOINT'][region]))
            describe_eip_addresses_request = vpc_20160428_models.DescribeEipAddressesRequest(region_id=region)
            try:
                # https://next.api.aliyun.com/api/Vpc/2016-04-28/DescribeEipAddresses
                res = client.describe_eip_addresses_with_options(describe_eip_addresses_request, runtime)
                describe_eip_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_eip_attribute_response_json_obj = json.loads(describe_eip_attribute_response_to_str)
                count = describe_eip_attribute_response_json_obj['body']['TotalCount']
                eip_total_count += count
                if count > 0:
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
                return APIResponse(code=0, msg='request successfully', total=eip_total_count)
            except Exception as error:
                UtilClient.assert_as_string(error)
                return APIResponse(code=1, msg=error)


@sync_to_async
def get_ssl_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for endpoint in settings.ENDPOINT['SSL_ENDPOINT']:
            client = casApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['SSL_ENDPOINT'][endpoint]))
            list_client_certificate_request = cas_20200630_models.ListClientCertificateRequest()
            ssl_certificate_count = 0
            try:
                # https://next.api.aliyun.com/api/cas/2020-06-30/ListClientCertificate
                res = client.list_client_certificate_with_options(list_client_certificate_request, runtime)
                describe_ssl_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_ssl_attribute_response_json_obj = json.loads(describe_ssl_attribute_response_to_str)
                count = describe_ssl_attribute_response_json_obj['body']['TotalCount']
                ssl_certificate_count += count
                if count > 0:
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
                return APIResponse(code=0, msg='request successfully', total=ssl_certificate_count)
            except Exception as error:
                UtilClient.assert_as_string(error)
                return APIResponse(code=1, msg=error)


@sync_to_async
def get_csc_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
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
                csc = AlibabacloudCSCApiResponse(api_request_id=(describe_csc_attribute_response_json_obj['body']['RequestId']),
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
                return APIResponse(code=0, msg='request successfully')
            except Exception as error:
                UtilClient.assert_as_string(error)
                return APIResponse(code=1, msg=error)


@sync_to_async
def get_rds_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    rds_total_count = 0
    for project in project_list:
        for endpoint in settings.ENDPOINT['RDS_ENDPOINT']:
            client = RdsApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['RDS_ENDPOINT'][endpoint]))
            for region in project['region']:
                describe_db_instances_request = rds_20140815_models.DescribeDBInstancesRequest(region_id=region)
                try:
                    # https://next.api.aliyun.com/api/Rds/2014-08-15/DescribeDBInstances
                    db_list_res = client.describe_dbinstances_with_options(describe_db_instances_request, runtime)
                    describe_rds_attribute_response_to_str = UtilClient.to_jsonstring(db_list_res)
                    describe_rds_attribute_response_json_obj = json.loads(describe_rds_attribute_response_to_str)
                    rds_list = describe_rds_attribute_response_json_obj['Items']
                    rds_total_count += len(rds_list)
                    for rds_instance in rds_list:
                        # https://next.api.aliyun.com/api/Rds/2014-08-15/DescribeDBInstanceAttribute
                        describe_db_instance_detail = rds_20140815_models.DescribeDBInstanceAttributeRequest(dbinstance_id=rds_instance['DBInstanceId'])
                        db_instance_detail_res = client.describe_dbinstance_attribute_with_options(describe_db_instance_detail, runtime)
                        describe_rds_attribute_detail_response_to_str = UtilClient.to_jsonstring(db_instance_detail_res)
                        db_instance_detail = json.loads(describe_rds_attribute_detail_response_to_str)
                        request_id = describe_rds_attribute_response_json_obj['body']['RequestId'] + " " + db_instance_detail['body']['RequestId']
                        rds = AlibabacloudRDSApiResponse(api_request_id=request_id,
                                                         instance_id=rds_instance['InstanceId'],
                                                         project_name=project['project_name'],
                                                         project_id=project['id'],
                                                         master_instance_id=rds_instance['MasterInstanceId'],
                                                         guard_db_instance_id=rds_instance['GuardDBInstanceId'],
                                                         db_instance_description=rds_instance['DBInstanceDescription'],
                                                         engine=rds_instance['Engine'],
                                                         db_instance_status=rds_instance['DBInstanceStatus'],
                                                         db_instance_type=rds_instance['DBInstanceType'],
                                                         category=rds_instance['Category'],
                                                         db_instance_class_type=db_instance_detail['DBInstanceClassType'],  # detail
                                                         db_instance_storage=db_instance_detail['DBInstanceStorage'],  # detail
                                                         db_instance_memory=db_instance_detail['DBInstanceMemory'],  # detail
                                                         db_instance_cpu=db_instance_detail['DBInstanceCPU'],  # detail
                                                         region_id=rds_instance['RegionId'],
                                                         instance_network_type=rds_instance['InstanceNetworkType'],
                                                         db_instance_net_type=rds_instance['DBInstanceNetType'],
                                                         db_instance_class=rds_instance['DBInstanceClass'],
                                                         engine_version=rds_instance['EngineVersion'],
                                                         pay_type=rds_instance['PayType'],
                                                         connection_mode=rds_instance['ConnectionMode'],
                                                         connection_string=rds_instance['ConnectionString'],
                                                         create_time=rds_instance['CreateTime'],
                                                         expire_time=rds_instance['ExpireTime'],
                                                         destroy_time=rds_instance['DestroyTime'],
                                                         lock_mode=rds_instance['LockMode'],
                                                         lock_reason=rds_instance['LockReason'],
                                                         )
                        logger.info(rds.get_basic_info())
                        rds.save()
                    return APIResponse(code=0, msg='request successfully', total=rds_total_count)
                except Exception as error:
                    UtilClient.assert_as_string(error)
                    return APIResponse(code=1, msg=error)


@sync_to_async
def get_redis_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    redis_total_count = 0
    for project in project_list:
        for endpoint in settings.ENDPOINT['REDIS_ENDPOINT']:
            client = R_kvstoreApiClient(set_api_client_config(project['project_access_key'],
                                                              project['project_secret_key'],
                                                              settings.ENDPOINT['REDIS_ENDPOINT'][endpoint]))
            for region in project['region']:
                describe_instances_request = r_kvstore_20150101_models.DescribeInstancesRequest(region_id=region)
                try:
                    # https://next.api.aliyun.com/api/R-kvstore/2015-01-01/DescribeInstances
                    redis_list_res = client.describe_instances_with_options(describe_instances_request, runtime)
                    describe_redis_attribute_response_to_str = UtilClient.to_jsonstring(redis_list_res)
                    describe_redis_attribute_response_json_obj = json.loads(describe_redis_attribute_response_to_str)
                    redis_list = describe_redis_attribute_response_json_obj['body']['Instances']
                    redis_total_count += len(redis_list)
                    for num, redis_instance in enumerate(redis_list):
                        redis = AlibabacloudRedisApiResponse(api_request_id=(describe_redis_attribute_response_json_obj['body']['RequestId'] + str(num)),
                                                             instance_id=redis_instance['InstanceId'],
                                                             project_name=project['project_name'],
                                                             project_id=project['id'],
                                                             private_ip=redis_instance['PrivateIp'],
                                                             capacity=redis_instance['Capacity'],
                                                             architecture_type=redis_instance['ArchitectureType'],
                                                             network_type=redis_instance['NetworkType'],
                                                             bandwidth=redis_instance['Bandwidth'],
                                                             instance_name=redis_instance['InstanceName'],
                                                             shard_count=redis_instance['ShardCount'],
                                                             user_name=redis_instance['UserName'],
                                                             instance_class=redis_instance['InstanceClass'],
                                                             instance_type=redis_instance['InstanceType'],
                                                             instance_status=redis_instance['InstanceStatus'],
                                                             region_id=redis_instance['RegionId'],
                                                             engine_version=redis_instance['EngineVersion'],
                                                             charge_type=redis_instance['ChargeType'],
                                                             connection_mode=redis_instance['ConnectionMode'],
                                                             connection_domain=redis_instance['ConnectionDomain'],
                                                             create_time=redis_instance['CreateTime'],
                                                             expire_time=redis_instance['ExpireTime'],
                                                             destroy_time=redis_instance['DestroyTime'],
                                                             )
                        logger.info(redis.get_basic_info())
                        redis.save()
                    return APIResponse(code=0, msg='request successfully', total=redis_total_count)
                except Exception as error:
                    UtilClient.assert_as_string(error)
                    return APIResponse(code=1, msg=error)


@sync_to_async
def get_cfw_api_response() -> APIResponse:
    project_list = (Project.objects.filter(status='Running',
                                           project_access_key__isnull=False,
                                           project_secret_key__isnull=False).
                    values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id'))
    runtime = util_models.RuntimeOptions()
    cfw_total_count = 0
    for project in project_list:
        for endpoint in settings.ENDPOINT['CFW_ENDPOINT']:
            client = CfwApiClient(set_api_client_config(project['project_access_key'],
                                                        project['project_secret_key'],
                                                        settings.ENDPOINT['CFW_ENDPOINT'][endpoint]))
            describe_vpc_firewall_list_request = cloudfw_20171207_models.DescribeVpcFirewallListRequest()
            try:
                # https://next.api.aliyun.com/api/Cloudfw/2017-12-07/DescribeVpcFirewallList
                cfw_list_res = client.describe_vpc_firewall_list_with_options(describe_vpc_firewall_list_request, runtime)
                describe_redis_attribute_response_to_str = UtilClient.to_jsonstring(cfw_list_res)
                describe_redis_attribute_response_json_obj = json.loads(describe_redis_attribute_response_to_str)
                cfw_list = describe_redis_attribute_response_json_obj['body']['VpcFirewalls']
                cfw_total_count += describe_redis_attribute_response_json_obj['body']['TotalCount']
                if cfw_total_count > 0:
                    for num, cfw_instance in enumerate(cfw_list):
                        cfw = AlibabacloudCFWApiResponse(api_request_id=(describe_redis_attribute_response_json_obj['body']['RequestId'] + str(num)),
                                                         instance_id=cfw_instance['InstanceId'],
                                                         project_name=project['project_name'],
                                                         project_id=project['id'],
                                                         connect_type=cfw_instance['ConnectType'],
                                                         region_status=cfw_instance['RegionStatus'],
                                                         bandwidth=cfw_instance['Bandwidth'],
                                                         vpc_firewall_name=cfw_instance['VpcFirewallName'],
                                                         firewall_switch_status=cfw_instance['FirewallSwitchStatus'],
                                                         )
                        logger.info(cfw.get_basic_info())
                        cfw.save()
                return APIResponse(code=0, msg='request successfully', total=cfw_total_count)
            except Exception as error:
                UtilClient.assert_as_string(error)
                return APIResponse(code=1, msg=error)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_ecs_api(request):
    return asyncio.run(get_ecs_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ecs_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_ecs_api_response = AlibabacloudEcsApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_ecs_api_response = alibabacloud_ecs_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_ecs_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudEcsApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudEcsApiResponseSerializer(data, many=True)
    logger.info("{} call ecs list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_waf_api(request):
    return asyncio.run(get_waf_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_waf_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_waf_api_response = AlibabacloudWafApiResponse.objects.all().order_by("project_id")

        if project_name:
            alibabacloud_waf_api_response = alibabacloud_waf_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_waf_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudWafApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudWafApiResponseSerializer(data, many=True)
    logger.info("{} call waf list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_slb_api(request):
    return asyncio.run(get_slb_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_slb_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_slb_api_response = AlibabacloudSLBApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_slb_api_response = alibabacloud_slb_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_slb_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudSLBApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudSlbApiResponseSerializer(data, many=True)
    logger.info("{} call slb list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_alb_api(request):
    return asyncio.run(get_alb_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_alb_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_alb_api_response = AlibabacloudALBApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_alb_api_response = alibabacloud_alb_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_alb_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudSLBApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudAlbApiResponseSerializer(data, many=True)
    logger.info("{} call alb list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_eip_api(request):
    return asyncio.run(get_eip_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_eip_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_eip_api_response = AlibabacloudEIPApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_eip_api_response = alibabacloud_eip_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_eip_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudEIPApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudEipApiResponseSerializer(data, many=True)
    logger.info("{} call eip list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_ssl_api(request):
    return asyncio.run(get_ssl_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ssl_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_ssl_api_response = AlibabacloudSSLApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_ssl_api_response = alibabacloud_ssl_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_ssl_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudSSLApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudSSLApiResponseSerializer(data, many=True)
    logger.info("{} call ssl certificate list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_csc_api(request):
    return asyncio.run(get_csc_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_csc_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_csc_api_response = AlibabacloudCSCApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_csc_api_response = alibabacloud_csc_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_csc_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudCSCApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudCSCApiResponseSerializer(data, many=True)
    logger.info("{} call csc list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_rds_api(request):
    return asyncio.run(get_rds_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_rds_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_rds_api_response = AlibabacloudRDSApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_rds_api_response = alibabacloud_rds_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_rds_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudRDSApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudRDSApiResponseSerializer(data, many=True)
    logger.info("{} call rds list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_redis_api(request):
    return asyncio.run(get_redis_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_redis_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_redis_api_response = AlibabacloudRedisApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_redis_api_response = alibabacloud_redis_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_redis_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudRedisApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudRedisApiResponseSerializer(data, many=True)
    logger.info("{} call redis list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def call_cfw_api(request):
    return asyncio.run(get_cfw_api_response())


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_cfw_list(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_cfw_api_response = AlibabacloudCFWApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_cfw_api_response = alibabacloud_cfw_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_cfw_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudCFWApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudCFWApiResponseSerializer(data, many=True)
    logger.info("{} call cfw list api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)
