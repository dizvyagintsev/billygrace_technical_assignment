import axios from 'axios';
// config
import { API_BASE_URL } from '../config-global';

// ----------------------------------------------------------------------

const axiosInstance = axios.create({ baseURL: API_BASE_URL });

// axiosInstance.interceptors.response.use(
//   (response) => response,
//   (error) => Promise.reject((error.response && error.response.data) || 'Something went wrong')
// );

export default axiosInstance;
