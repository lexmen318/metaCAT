import Vue from 'vue'
import alertMessage from './alertMessage.vue'

const MessageBox = Vue.extend(alertMessage)
alertMessage.install = (data) => {
  let instance = new MessageBox({
    data
  }).$mount()
  document.body.appendChild(instance.$el)
  Vue.nextTick(() => {
    instance.show = true
  })
}

export default alertMessage
