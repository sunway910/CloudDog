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
    expired_time: "expired_time",
    stopped_mode: "stopped_mode",
    start_time: "start_time",
    lock_reason: "lock_reason",
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

    region_id: "region_id",
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
