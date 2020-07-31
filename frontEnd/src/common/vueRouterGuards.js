var routerGuards = (store, router) => {
  let linkToLogin = false
  router.beforeEach((to, from, next) => {
    linkToLogin && next()
    if (store.state.userInfo) {
      linkToLogin = false
      if (to.name === 'Login') {
        store.state.userInfo = null
      }
      if (to.name === 'SystemAdmin') {
        if (store.state.userInfo.user_role !== 'ADMIN') {
          next(false)
          return
        }
      } else {
        if (store.state.userInfo.user_role === 'ADMIN') {
          next(false)
          return
        }
      }
      if (to.meta.activeMenu) {
        store.commit('setActiveMenu', to.meta.activeMenu)
      }
      next()
    } else {
      linkToLogin = true
      next('/login')
    }
  })
}

export default routerGuards
