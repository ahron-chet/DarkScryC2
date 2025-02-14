// types/axios.d.ts
import 'axios';

declare module 'axios' {
  // For Axios v1.x, the signature is `AxiosResponse<T = never, D = any>`
  // so we override them to default to `any`.
  interface AxiosResponse<T = any, D = any> {
    data: T;
  }

  // For Axios v1.x, `AxiosRequestConfig` has a generic for the request body.
  interface AxiosRequestConfig<T = any> {
    data?: T;
  }
}
