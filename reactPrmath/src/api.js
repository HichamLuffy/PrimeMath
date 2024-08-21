import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

const apiUrl = "/choreo-apis/awbo/backend/rest-api-be2/v1.0";

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const fetchCurrentUser = async () => {
  try {
    const response = await api.get('/api/current_user/');
    return response.data;
  } catch (error) {
    console.error("Error fetching current user:", error);
    throw error;
  }
};

const token = localStorage.getItem(ACCESS_TOKEN);

const config = {
    headers: {
        'Authorization': `Bearer ${token}`
    }
};

try {
    const res = await api.post("/api/teacher-profile/", requestData, config);
    // Handle success
} catch (error) {
    console.error("Error updating teacher profile:", error);
    alert(`Error: ${error.response ? error.response.data : error.message}`);
}

export default api;