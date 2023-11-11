export function changeTimePattern(time: any) {
    const date = new Date(time);
    return date.toISOString().slice(0, 19).replace('T', ' ')
}

export const base_i18n = {
    api_request_id: "api_request_id",
    instance_id: "instance_id",
    request_time: "request_time",
    product_type: "product_type",
    project_name: "project_name",
    cloud_platform: "cloud_platform",
    search: "search",
    export: "export",
    refresh: "refresh",
    new: "new",
    operation: "operation",
    status: "status",
    create_time: "create_time",
    pay_type: "pay_type",
    instance_charge_type: "instance_charge_type",
    internet_charge_type: "internet_charge_type",
    master_zone_id: "master_zone_id",
    slave_zone_id: "slave_zone_id",
    bandwidth: "bandwidth",
    renewal_status: "renewal_status",
    end_time_stamp: "end_time_stamp",
    end_time: "end_time",
    auto_release_time: "auto_release_time",
    renewal_duration: "renewal_duration",
    renewal_cyc_unit: "renewal_cyc_unit",
    region_id: "region_id",
    address: "address",
    name: "name",
    expired_time: "expired_time",
}

export const dashboard_i18n = {
    id: "id",
    region: "region",
    cloud_platform: "cloud_platform",
    project_access_key: "project_access_key",
    project_secret_key: "project_secret_key",
    cron_toggle: "cron_toggle",
    account: "account"
}

export const ecs_i18n = {
    instance_name: "instance_name",
    auto_renew_enabled: "auto_renew_enabled",
    period_init: "period_init",
    duration: "duration",
    ecs_status: "ecs_status",
    stopped_mode: "stopped_mode",
    start_time: "start_time",
    lock_reason: "lock_reason",
    instance_type: "ecs_instance_type", // ecs.c5.xlarge
    osname: "osname", // centos
    zone_id: "zone_id", // cn-hongkong-b
    cpu_ram: "cpu_ram", // 4C8G
}
export const waf_i18n = {
    waf_status: "waf_status",
    waf_start_time: "waf_start_time",
    edition: "edition",
    remain_day: "remain_day",
    region: "region",
    in_debt: "in_debt",
    subscription_type: "subscription_type",
    trial: "trial",
}
export const job_i18n = {
    job_name: "job_name",
    next_run_time: "next_run_time",
    job_state: "job_state",
}

export const job_history_i18n = {
    job: "job",
    id: "id",
    status: "status",
    runtime: "runtime",
    duration: "job_duration",
    finished: "finished",
    exception: "exception",
    traceback: "traceback",
}

export const message_i18n = {
    unread: "unread",
    read: "read",
    trash: "trash",
    message_id: "message_id",
    event_message: "event_message",
    event_type: "event_type",
    message_time: "message_time",
}
export const lb_i18n = {
    load_balancer_spec: "load_balancer_spec",
    address_allocated_mode: "address_allocated_mode",
    address_type: "address_type",
    dns_name: "dns_name",
    load_balancer_bussiness_status: "load_balancer_bussiness_status",
    load_balancer_edition: "load_balancer_edition",
    load_balancer_name: "load_balancer_name",
    load_balancer_status: "load_balancer_status",
    address_ip_version: "address_ip_version",
    ipv6_address_type: "ipv6_address_type",
}
export const eip_i18n = {
    allocation_id: "allocation_id",
    instance_type: "eip_instance_type",
    business_status: "business_status",
    reservation_bandwidth: "reservation_bandwidth",
    bandwidth: "bandwidth",
    ip_address: "ip_address",
    reservation_internet_charge_type: "reservation_internet_charge_type",
    charge_type: "charge_type",
    net_mode: "net_mode",
    allocation_time: "allocation_time",
    status: "status",
    reservation_active_time: "reservation_active_time",
}

export const ssl_i18n = {
    subject_dn: "subject_dn",
    common_name: "common_name",
    organization_unit: "organization_unit",
    organization: "organization",
    before_date: "before_date",
    after_date: "after_date",
    days: "days",
}


export const csc_i18n = {
    mv_auth_count: "mv_auth_count",
    sas_log: "sas_log",
    sas_screen: "sas_screen",
    honeypot_capacity: "honeypot_capacity",
    mv_unused_auth_count: "mv_unused_auth_count",
    web_lock: "web_lock",
    app_white_list_auth_count: "app_white_list_auth_count",
    last_trail_end_time: "last_trail_end_time",
    version: "version",
    web_lock_auth_count: "web_lock_auth_count",
    release_time: "release_time",
    highest_version: "highest_version",
    asset_level: "asset_level",
    is_over_balance: "is_over_balance",
    sls_capacity: "sls_capacity",
    vm_cores: "vm_cores",
    allow_partial_buy: "allow_partial_buy",
    app_white_list: "app_white_list",
    image_scan_capacity: "image_scan_capacity",
    is_trial_version: "is_trial_version",
    user_defined_alarms: "user_defined_alarms",
    open_time: "open_time",
    is_new_container_version: "is_new_container_version",
    is_new_multi_version: "is_new_multi_version",
    threat_analysis_capacity: "threat_analysis_capacity",
    cspm_capacity: "cspm_capacity",
    vul_fix_capacity: "vul_fix_capacity",
    rasp_capacity: "rasp_capacity",
}
