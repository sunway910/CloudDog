export function changeTimePattern(time: any) {
    const date = new Date(time);
    return date.toISOString().slice(0, 19).replace('T', ' ')
}

export const base_i18n = {
    api_request_id: "api_request_id",
    instance_id: "instance_id",
    request_time: "request_time",
    product_type: "product_type",
    project: "project",
    projectName: "projectName",
    cloudPlatform: "cloudPlatform",
    search: "search",
    export: "export",
    refresh: "refresh",
    new: "new",
    operation: "operation",
    status: "status",
    create_time: "create_time",
}

export const dashboard_i18n = {
    id: "id",
    region: "region",
    cloud_platform: "cloud_platform",
    project_name: "project_name",
    project_access_key: "project_access_key",
    project_secret_key: "project_secret_key",
    cron_toggle: "cron_toggle",
    account: "account",

}

export const ecr_i18n = {
    instance_name: "instance_name",
    auto_renew_enabled: "auto_renew_enabled",
    renewal_status: "renewal_status",
    period_init: "period_init",
    duration: "duration",
    region_id: "region_id",
    ecs_status: "ecs_status",
    instance_charge_type: "instance_charge_type",
    internet_charge_type: "internet_charge_type",
    expired_time: "expired_time",
    stopped_mode: "stopped_mode",
    start_time: "start_time",
    auto_release_time: "auto_release_time",
    lock_reason: "lock_reason",
}
export const waf_i18n = {
    waf_status: "waf_status",
    waf_start_time: "waf_start_time",
    end_time: "end_time",
    edition: "edition",
    remain_day: "remain_day",
    region: "region",
    pay_type: "pay_type",
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
