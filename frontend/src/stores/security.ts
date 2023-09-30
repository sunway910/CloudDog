/**
 * 转码编码数据 使用 btoa 结合 encodeURIComponent 编码转码数据
 * @param data 需要转码编码的数据
 */
export function btoaEncode(data: any) {
    if (!data) {
        return ''
    }
    try {
        data = window.btoa(encodeURIComponent(JSON.stringify(data)))
    } catch (e) {
        toast.warning("An error occurred while encoding")
    }

    return data
}

/**
 * 解码转码数据 使用 atob 结合 decodeURIComponent 解码转码数据
 * @param data 需要解码转码的数据
 */
export function atobDecode(data: any) {
    if (!data) {
        return ''
    }
    try {
        data = JSON.parse(decodeURIComponent(window.atob(data)))
    } catch (e) {
        toast.warning("An error occurred while decoding")
    }
    return data
}
