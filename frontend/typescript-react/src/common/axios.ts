import Axios, { AxiosRequestConfig } from "axios";

// import localStorage from "@/common/local-storage"
import localStorage from "./local-storage";

function authRequestInterceptor(config: AxiosRequestConfig) {
  const token = localStorage.getToken();
  if (token) {
    // @ts-ignore
    config.headers.authorization = `Bearer ${token}`;
  }
  // @ts-ignore
  config.headers.authorization =
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzA4NDAwMDgsImVtYWlsIjoiZWxvdmVyb2NrMEBzaHV0dGVyZmx5LmNvbSJ9.8V5cYljopDGa4L_dm2p2_anpiUDJNpEJt3ZznkKY0Cw";
  // @ts-ignore
  config.headers.Accept = "application/json";
  return config;
}

export const axios = Axios.create({
  baseURL: "http://127.0.0.1:2000",
});

axios.interceptors.request.use(authRequestInterceptor);
axios.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.log("error =>", error.response);
    return Promise.reject(error);
  }
);
