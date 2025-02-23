import axios from "axios";


export default axios.create({
  baseURL: process.env.NEXT_DJANGO_API_URL_V2,
  headers: { "Content-Type": "application/json" },
});
export const axiosAuth = axios.create({
  baseURL: process.env.NEXT_DJANGO_API_URL_V2,
  headers: { "Content-Type": "application/json" },
});
