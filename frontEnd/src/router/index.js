import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/pages/login'
import Home from '@/pages/homePage'

import AnnotatingBatchList from '@/pages/annotatingBatchList'
import AnnotatingDialogueList from '@/pages/annotatingDialogueList'
import AnnotatingDialogueDetail from '@/pages/annotatingDialogueDetail'

import ParaphrasingBatchList from '@/pages/paraphrasingBatchList'
import ParaphrasingDialogueList from '@/pages/paraphrasingDialogueList'
import ParaphrasingDialogueDetail from '@/pages/paraphrasingDialogueDetail'

import SystemAdmin from '@/pages/systemAdmin'


Vue.use(Router)

const routerPush = Router.prototype.push
Router.prototype.push = function push (location) {
  return routerPush.call(this, location).catch(error => error)
}

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      children: [
        {
          path: '/',
          name: 'AnnotatingBatchList',
          component: AnnotatingBatchList,
          meta: {
            activeMenu: 'annotatingBatchList'
          }
        },
        {
          path: 'annotatingBatchList',
          name: 'AnnotatingBatchList',
          component: AnnotatingBatchList,
          meta: {
            activeMenu: 'annotatingBatchList'
          }
        },
        {
          path: 'annotatingDialogueList',
          name: 'AnnotatingDialogueList',
          component: AnnotatingDialogueList,
          meta: {
            activeMenu: 'annotatingBatchList'
          }
        },
        {
          path: 'annotatingDialogueDetail',
          name: 'AnnotatingDialogueDetail',
          component: AnnotatingDialogueDetail,
          meta: {
            activeMenu: 'annotatingBatchList'
          }
        },
        {
          path: 'paraphrasingBatchList',
          name: 'ParaphrasingBatchList',
          component: ParaphrasingBatchList,
          meta: {
            activeMenu: 'paraphrasingBatchList'
          }
        },
        {
          path: 'paraphrasingDialogueList',
          name: 'ParaphrasingDialogueList',
          component: ParaphrasingDialogueList,
          meta: {
            activeMenu: 'paraphrasingBatchList'
          }
        },
        {
          path: 'paraphrasingDialogueDetail',
          name: 'ParaphrasingDialogueDetail',
          component: ParaphrasingDialogueDetail,
          meta: {
            activeMenu: 'paraphrasingBatchList'
          }
        },
        {
          path: 'systemAdmin',
          name: 'SystemAdmin',
          component: SystemAdmin,
          meta: {
            activeMenu: 'systemAdmin'
          }
        }
      ]
    }
  ]
})
