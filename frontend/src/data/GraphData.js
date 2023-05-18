import axios from 'axios'
import { CONFIG } from '../config'
const apiPath = '/api/data'

axios.defaults.baseURL = CONFIG.BACKEND_URL

const response = await axios.get(apiPath)
const GraphData = response.data

export default GraphData;
