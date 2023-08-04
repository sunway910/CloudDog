# 获取多台ECS实例信息

获取多台ECS实例信息。

文档示例，该示例**无法在线调试**，如需调试可下载到本地后替换 [AK](https://usercenter.console.aliyun.com/#/manage/ak) 以及参数后进行调试。

## 运行条件

- 下载并解压需要语言的代码;

- 在阿里云帐户中获取您的 [凭证](https://usercenter.console.aliyun.com/#/manage/ak)并通过它替换下载后代码中的 ACCESS_KEY_ID 以及 ACCESS_KEY_SECRET;

- 执行代码

```

- Python
*Python 版本要求 Python3*
```sh
python3 setup.py install && python ./alibabacloud_sample/sample.py
```

## 使用的 API

- DescribeInstances 获取多台ECS实例的状态信息。文档示例，可以参考：[文档](https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstances)
- DescribeInstanceAutoRenewAttribute 获取多台ECS实例的自动续费状态。文档示例，可以参考：[文档](https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstanceAutoRenewAttribute)

## 返回示例

*实际输出结构可能稍有不同，属于正常返回；下列输出值仅作为参考，以实际调用为准*

- JSON 格式

DescribeInstances返回结果模板

```json
{
  "Instances": {
    "Instance": [
      {
        "ResourceGroupId": "",
        "Memory": 65536,
        "InstanceChargeType": "PrePaid----------------包年包月 PostPaid--------------按量付费",
        "Cpu": 32,
        "OSName": "CentOS  7.6 64位",
        "InstanceNetworkType": "vpc",
        "InnerIpAddress": {
          "IpAddress": []
        },
        "ExpiredTimeExpiredTime": "2024-05-25T16:00Z  过期时间",
        "ImageId": "centos_7_6_x64_20G_alibase_20211130.vhd",
        "EipAddress": {
          "AllocationId": "",
          "IpAddress": "",
          "InternetChargeType": ""
        },
        "ImageOptions": {},
        "HostName": "iZj6c95bgai7gfxcsvq7ilZ",
        "VlanId": "",
        "Status": "Running",
        "HibernationOptions": {
          "Configured": false
        },
        "MetadataOptions": {
          "HttpTokens": "",
          "HttpEndpoint": ""
        },
        "InstanceId": "i-j6c95bgai7gfxcsvq7il",
        "StoppedMode": "实例停机后是否继续收费： Not-applicable -----KeepCharging：停机后继续收费，为您继续保留库存资源。\nStopCharging：停机后不收费。停机后，我们释放实例对应的资源，例如vCPU、内存和公网IP等资源。重启是否成功依赖于当前地域中是否仍有资源库存。\nNot-applicable：本实例不支持停机不收费功能。",
        "CpuOptions": {
          "ThreadsPerCore": 2,
          "Numa": "",
          "CoreCount": 16
        },
        "StartTime": "2023-05-22T01:38Z  实例最近一次的启动时间",
        "DeletionProtection": false,
        "SecurityGroupIds": {
          "SecurityGroupId": [
            "sg-j6cgomnjya8566i0m08k"
          ]
        },
        "VpcAttributes": {
          "PrivateIpAddress": {
            "IpAddress": [
              "10.0.1.1"
            ]
          },
          "VpcId": "vpc-j6ccrb61nyelh5syspk4k",
          "VSwitchId": "vsw-j6ckgzg22ooaillmgmvoc",
          "NatIpAddress": ""
        },
        "InternetChargeType": "PayByTraffic -------PayByBandwidth：按固定带宽计费。\nPayByTraffic：按使用流量计费。",
        "InstanceName": "ECS-Master",
        "DeploymentSetId": "",
        "InternetMaxBandwidthOut": 0,
        "SerialNumber": "c434e140-4591-41c6-853d-6a0b4ab7d5d1",
        "OSType": "linux",
        "CreationTime": "2023-05-21T11:23Z",
        "AutoReleaseTime": "按量付费实例的自动释放时间",
        "Description": "",
        "InstanceTypeFamily": "ecs.c7",
        "DedicatedInstanceAttribute": {
          "Tenancy": "",
          "Affinity": ""
        },
        "PublicIpAddress": {
          "IpAddress": []
        },
        "GPUSpec": "",
        "NetworkInterfaces": {
          "NetworkInterface": [
            {
              "Type": "Primary",
              "PrimaryIpAddress": "10.0.1.1",
              "MacAddress": "00:16:3e:0a:b9:da",
              "NetworkInterfaceId": "eni-j6cgomnjya8566i5a78u",
              "PrivateIpSets": {
                "PrivateIpSet": [
                  {
                    "PrivateIpAddress": "10.0.1.1",
                    "Primary": true
                  }
                ]
              }
            }
          ]
        },
        "SpotPriceLimit": 0,
        "DeviceAvailable": true,
        "SaleCycle": "",
        "InstanceType": "ecs.c7.8xlarge",
        "SpotStrategy": "NoSpot",
        "OSNameEn": "CentOS  7.6 64 bit",
        "IoOptimized": true,
        "ZoneId": "cn-hongkong-b",
        "ClusterId": "",
        "EcsCapacityReservationAttr": {
          "CapacityReservationPreference": "",
          "CapacityReservationId": ""
        },
        "DedicatedHostAttribute": {
          "DedicatedHostId": "",
          "DedicatedHostName": "",
          "DedicatedHostClusterId": ""
        },
        "GPUAmount": 0,
        "OperationLocks": {
          "LockReason": [
            "financial：因欠费被锁定。security：因安全原因被锁定。Recycling：抢占式实例的待释放锁定状态。dedicatedhostfinancial：因为专有宿主机欠费导致ECS实例被锁定。refunded：因退款被锁定。"
          ]
        },
        "InternetMaxBandwidthIn": -1,
        "Recyclable": false,
        "RegionId": "cn-hongkong",
        "CreditSpecification": ""
      }
    ]
  },
  "TotalCount": 1,
  "NextToken": "",
  "PageSize": 10,
  "RequestId": "8EF55501-2518-36D6-B301-E13DCBBE90AC",
  "PageNumber": 1
}
```

DescribeInstanceAutoRenewAttribute返回结果模板

```json
{
  "TotalCount": 2,
  "InstanceRenewAttributes": {
    "InstanceRenewAttribute": [
      {
        "AutoRenewEnabled": false,
        "InstanceId": "i-j6c7410fc4iw45kd6laa",
        "RenewalStatus": "Normal",
        "Duration": 0,
        "PeriodUnit": "Month"
      },
      {
        "AutoRenewEnabled": false,
        "InstanceId": "i-j6c95bgai7gfxcsvq7bb",
        "RenewalStatus": "Normal",
        "Duration": 0,
        "PeriodUnit": "Month"
      }
    ]
  },
  "RequestId": "2CE00AB1-C146-3619-B1DF-1256B5C7A53B",
  "PageSize": 100,
  "PageNumber": 1
}
```



