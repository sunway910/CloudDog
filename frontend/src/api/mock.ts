import {UnwrapRef} from "vue";

const serverUrl = "http://127.0.0.1:8000/api"
import {useRequest} from 'vue-request'
import axios from "axios";

export const testRequest = () => {
    const {data, loading, error} = useRequest(() => http.post('/mock/post'))
    return {data, loading, error}
}

export const sendGetReq = async ({uri}: { uri: string }) => {
    return await axios.get(serverUrl + uri)
}

export const sendPostReq = async ({uri, payload, config_obj}: { uri: string, payload: any, config_obj: any }) => {
  return await axios.post(serverUrl + uri, payload, config_obj)
}

export const sendPutReq = async ({uri, payload, config_obj}: { uri: string, payload: any, config_obj: any }) => {
    return await axios.put(serverUrl + uri, payload, config_obj)
}

export const sendPatchReq = async ({uri, payload, config_obj}: { uri: string, payload: any, config_obj: any }) => {
    return await axios.patch(serverUrl + uri, payload, config_obj)
}

export const sendDeleteReq = async ({uri, config_obj}: { uri: string, config_obj: any }) => {
    return await axios.delete(serverUrl + uri, config_obj)
}
