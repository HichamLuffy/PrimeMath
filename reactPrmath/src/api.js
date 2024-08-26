import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

const apiUrl = "/choreo-apis/awbo/backend/rest-api-be2/v1.0";

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    console.log("Token retrieved:", token); // Log the token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
        console.warn("No token found in localStorage");
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

export const updateTeacherProfile = async (profileData) => {
  try {
    const response = await api.post("/teacher-profile/", profileData);
    return response.data;
  } catch (error) {
    console.error("Error updating teacher profile:", error);
    throw error;
  }
};

export const fetchUserList = async () => {
  try {
    const response = await api.get('/api/users/');
    return response.data;
  } catch (error) {
    console.error("Error fetching user list:", error);
    throw error;
  }
};

export default api;