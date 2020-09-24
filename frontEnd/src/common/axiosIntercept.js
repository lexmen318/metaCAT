import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$axios = axios

var axiosIntercept = (router) => {
  axios.interceptors.response.use(
    (respone) => {
      if (respone) {
       return respone
      }
    },
    (error) => {
      // router.push({
      //   path: '/login'
      // })
    }
  )
}

export default axiosIntercept
