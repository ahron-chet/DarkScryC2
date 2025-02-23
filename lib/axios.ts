import axios from "axios";

process.env.NEXT_DJANGO_API_URL_V2
const BASE_URL = "http://127.0.0.1:8000/api/v2";
export default axios.create({
  baseURL: process.env.NEXT_DJANGO_API_URL_V2,
  headers: { "Content-Type": "application/json" },
});
export const axiosAuth = axios.create({
  baseURL: process.env.NEXT_DJANGO_API_URL_V2,
  headers: { "Content-Type": "application/json" },
});
