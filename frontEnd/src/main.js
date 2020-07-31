// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueI18n from 'vue-i18n'
import App from './App'
import router from './router'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/resetCss.css'
import alertMessage from './common/messageComponents'
import axiosIntercept from './common/axiosIntercept'
import routerGuards from './common/vueRouterGuards'
import backend from './utils/backend'
import Store from './store/index'
import messages from './locale'


Vue.mixin(backend)
Vue.use(ElementUI)
Vue.use(VueI18n)
Vue.prototype.$Store = Store
Vue.prototype.$axios = axios
Vue.prototype.$alertMessage = alertMessage.install

Vue.config.productionTip = false
axiosIntercept(router)
routerGuards(Store, router)

const i18n = new VueI18n({
	// 设置语言
	locale: sessionStorage.getItem('languageCode') ? sessionStorage.getItem('languageCode') : 'cn',
	fallbackLocale: 'en',
	// 语言包
	messages
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
	router,
	i18n,
  components: { App },
  template: '<App/>'
})
