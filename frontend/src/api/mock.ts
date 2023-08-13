import {UnwrapRef} from "vue";

const tagUrl = "http://127.0.0.1:8000/api"
import {useRequest} from 'vue-request'
import axios from "axios";

export const testRequest = () => {
    const {data, loading, error} = useRequest(() => http.post('/mock/post'))
    return {data, loading, error}
}

export const sendGetReq = async ({resUrl}: { resUrl: any }) => {
    const response = await axios.get(tagUrl + resUrl)
    return response.data
}

export const sendPostReq = async ({surl, payload, config_obj = ""}: { surl: any, payload: any, config_obj: any }) => {
  return await axios.post(tagUrl + surl, payload, config_obj)
}

export const sendPutReq = async ({surl, payload, config_obj}: { surl: any, payload: any, config_obj: any }) => {
    return await axios.put(tagUrl + surl, payload, config_obj)
}

export const sendPatchReq = async ({surl, payload, config_obj}: { surl: any, payload: any, config_obj: any }) => {
    return await axios.patch(tagUrl + surl, payload, config_obj)
}

export const sendDeleteReq = async ({surl, config_obj}: { surl: any, config_obj: any }) => {
    return await axios.delete(tagUrl + surl, config_obj)
}
