import axios from 'axios';

const api = axios.create({
  baseURL: 'https://6wl25djvr3.execute-api.ap-southeast-1.amazonaws.com/Prod',
  headers: { 'Content-Type': 'application/json' },
});

export default api;