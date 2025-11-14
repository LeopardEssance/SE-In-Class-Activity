import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Session management
let sessionId = localStorage.getItem('sessionId') || null;

export const setSessionId = (id) => {
  sessionId = id;
  if (id) {
    localStorage.setItem('sessionId', id);
  } else {
    localStorage.removeItem('sessionId');
  }
};

export const getSessionId = () => sessionId;

// Authentication API
export const authAPI = {
  login: async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password });
      if (response.data.success && response.data.session_id) {
        setSessionId(response.data.session_id);
      }
      return response.data;
    } catch (error) {
      throw error.response?.data || { success: false, message: 'Login failed' };
    }
  },

  logout: async () => {
    try {
      const response = await api.post('/auth/logout', null, {
        params: { session_id: sessionId }
      });
      setSessionId(null);
      return response.data;
    } catch (error) {
      throw error.response?.data || { success: false, message: 'Logout failed' };
    }
  },
};

// Devices API
export const devicesAPI = {
  getDevices: async () => {
    try {
      const response = await api.get('/devices', {
        params: { session_id: sessionId }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch devices' };
    }
  },

  createDevice: async (deviceType, deviceName) => {
    try {
      const response = await api.post('/devices',
        { device_type: deviceType, device_name: deviceName },
        { params: { session_id: sessionId } }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to create device' };
    }
  },

  setBrightness: async (deviceId, brightness) => {
    try {
      const response = await api.put(
        `/devices/${deviceId}/light/brightness`,
        { brightness },
        { params: { session_id: sessionId } }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to set brightness' };
    }
  },

  toggleDevice: async (deviceId) => {
    try {
      const response = await api.post(
        `/devices/${deviceId}/toggle`,
        null,
        { params: { session_id: sessionId } }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to toggle device' };
    }
  },

  deleteDevice: async (deviceId) => {
    try {
      const response = await api.delete(`/devices/${deviceId}`, {
        params: { session_id: sessionId }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to delete device' };
    }
  },
};

// Scheduler API
export const schedulerAPI = {
  getTasks: async () => {
    try {
      const response = await api.get('/schedule', {
        params: { session_id: sessionId }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch tasks' };
    }
  },

  createTask: async (deviceId, action, scheduledTime) => {
    try {
      const response = await api.post('/schedule',
        {
          device_id: deviceId,
          action: action,
          scheduled_time: scheduledTime
        },
        { params: { session_id: sessionId } }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to create task' };
    }
  },

  cancelTask: async (taskId) => {
    try {
      const response = await api.delete(`/schedule/${taskId}`, {
        params: { session_id: sessionId }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to cancel task' };
    }
  },
};

// Notifications API
export const notificationsAPI = {
  getNotifications: async (limit = 20) => {
    try {
      const response = await api.get('/notifications', {
        params: { 
          session_id: sessionId,
          limit: limit
        }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch notifications' };
    }
  },
};

// Integrations API
export const integrationsAPI = {
  getIntegrations: async () => {
    try {
      const response = await api.get('/integrations');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch integrations' };
    }
  },

  getStats: async () => {
    try {
      const response = await api.get('/integrations/stats');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch integration stats' };
    }
  },

  getIntegration: async (name) => {
    try {
      const response = await api.get(`/integrations/${name}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch integration' };
    }
  },

  createIntegration: async (integration) => {
    try {
      const response = await api.post('/integrations', integration);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to create integration' };
    }
  },

  toggleIntegration: async (name) => {
    try {
      const response = await api.post(`/integrations/${name}/toggle`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to toggle integration' };
    }
  },

  activateIntegration: async (name) => {
    try {
      const response = await api.post(`/integrations/${name}/activate`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to activate integration' };
    }
  },

  deactivateIntegration: async (name) => {
    try {
      const response = await api.post(`/integrations/${name}/deactivate`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to deactivate integration' };
    }
  },

  getSkills: async (name) => {
    try {
      const response = await api.get(`/integrations/${name}/skills`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch skills' };
    }
  },

  addSkill: async (name, skill) => {
    try {
      const response = await api.post(`/integrations/${name}/skills`, { skill });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to add skill' };
    }
  },
};

export default api;
