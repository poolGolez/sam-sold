import axios from 'axios';

const api = axios.create({
  baseURL: 'https://gzmipog4ig.execute-api.ap-southeast-1.amazonaws.com/Prod',
  headers: { 'Content-Type': 'application/json' },
});

export default api;