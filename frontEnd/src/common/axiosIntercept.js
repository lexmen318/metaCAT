import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$axios = axios

var axiosIntercept = (router) => {
  console.log(this)
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
