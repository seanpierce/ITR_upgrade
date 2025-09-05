import axios, { AxiosError } from 'axios'

const API = axios.create({
    baseURL: axios.defaults.baseURL = "http://localhost:8000" // Django backend
    // baseURL: process.env.VUE_APP_API_BASE_URL
})

const get = async (url: string) => {
    try {
        const response = await API.get(url);
        return response;
    } catch(err) {
        handleError(err as AxiosError)
    }
}

const post = async (url: string, payload: object) => {
    try {
        const response = await API.post(url, payload)
        return response
    } catch(err) {
        handleError(err as AxiosError)
    }
}

const put = async (url: string, payload: object) => {
    try {
        const response = await API.put(url, payload)
        return response
    } catch(err) {
        handleError(err as AxiosError)
    }
}

const del = async (url: string, payload: object) => {
    try {
        const response = await API.delete(url, payload)
        return response
    } catch(err) {
        handleError(err as AxiosError)
    }
}

const handleError = (error: AxiosError) => {
    console.error('Error seen by apiClient', error.name, error.status, error.response)
    throw error
}

export default {
    get,
    post,
    put,
    del
}