import axios, { AxiosError, type AxiosResponse } from 'axios'

const API = axios.create({
    baseURL: "http://localhost:8000" // Django backend
    // baseURL: process.env.VUE_APP_API_BASE_URL
})

// Generic GET method
const get = async <T>(url: string): Promise<T> => {
    try {
        const response: AxiosResponse<T> = await API.get(url)
        return response.data
    } catch(err) {
        handleError(err as AxiosError)
        throw err
    }
}

// Generic POST method
const post = async <T>(url: string, payload: object): Promise<T> => {
    try {
        const response: AxiosResponse<T> = await API.post(url, payload)
        return response.data
    } catch(err) {
        handleError(err as AxiosError)
        throw err
    }
}

// Generic PUT method
const put = async <T>(url: string, payload: object): Promise<T> => {
    try {
        const response: AxiosResponse<T> = await API.put(url, payload)
        return response.data
    } catch(err) {
        handleError(err as AxiosError)
        throw err
    }
}

// Generic DELETE method
const del = async <T>(url: string, payload?: object): Promise<T> => {
    try {
        const response: AxiosResponse<T> = await API.delete(url, { data: payload })
        return response.data
    } catch(err) {
        handleError(err as AxiosError)
        throw err
    }
}

const handleError = (error: AxiosError) => {
    console.error('API Error:', error.name, error.response?.status, error.response?.data)
    throw error
}

export default {
    get,
    post,
    put,
    del
}
