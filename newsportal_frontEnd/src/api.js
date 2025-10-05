// newsportal_frontEnd/src/api.js

import axios from 'axios';

// 🚨 CRITICAL FIX: Define the base URL for the Django backend
const DJANGO_BASE_URL = 'http://localhost:8000/api/';

const api = axios.create({
    baseURL: DJANGO_BASE_URL,
    // Add headers if needed, but not strictly necessary for this fix
});

export default api;