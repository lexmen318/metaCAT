import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

let defaultAlreadyVisited = JSON.parse(sessionStorage.getItem('alreadyVisited')) || []
sessionStorage.removeItem('alreadyVisited')
let userInfo = JSON.parse(sessionStorage.getItem('userInfo')) || null
sessionStorage.removeItem('userInfo')

let store = new Vuex.Store({
  state: {
    alreadyVisited: defaultAlreadyVisited,
    editSourceFile: {},
    userInfo: userInfo,
    activeMenu: ''
  },
  mutations: {
    add_already_visited_list (state, selectId) {
      if (!state.alreadyVisited.includes(selectId)) {
        state.alreadyVisited.push(selectId)
      }
    },
    remove_dialogue_from_visited_list (state, deletId) {
      state.alreadyVisited.forEach((id, index) => {
        if (id === deletId) {
          state.alreadyVisited.splice(index, 1)
          return false
        }
      })
    },
    resetAlreadyVisitedList (state) {
      state.alreadyVisited = []
    },
    setSourceFile (state, file) {
      state.editSourceFile = file
    },
    clearSourceFile (state) {
      state.editSourceFile = {}
    },
    setUserInfo (state, userInfo) {
      state.userInfo = userInfo
    },
    removeUserInfo (state) {
      state.userInfo = null
    },
    setActiveMenu (state, value) {
      state.activeMenu = value
    }
  },
  actions: {

  }
})

export default store
