<template>
  <div id="HomePage">
    <div class="menu-containt">
      <el-menu
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        :default-active="activeIndex"
        class="metaCAT-menu" mode="horizontal"
        @select="changSelectMemu">
        <template v-if="$Store.state.userInfo.user_role === 'USER' || $Store.state.userInfo.user_role == 'SUPER'">
          <el-menu-item index="annotatingBatchList">{{ $t('topMenu.annotatingTitle') }}</el-menu-item>
          <el-menu-item index="paraphrasingBatchList">{{ $t('topMenu.paraphrasingTitle') }}</el-menu-item>
        </template>
        <el-menu-item index="systemAdmin" v-if="$Store.state.userInfo.user_role === 'ADMIN'">{{ $t('adminMenu.menuTitle') }}</el-menu-item>
      </el-menu>
      <div class="menu-button-box">
        <div class="lang-name" @click="changeLanguage">{{ $t('lang.targetLanguageName') }}</div>
        <div class="user-guide" @click="openUserGuide">{{ $t('topMenu.helpTitle') }}</div>
        <div class="user-name">{{ $t('topMenu.welcomeTitle') }} {{this.$Store.state.userInfo.user_name}}</div>
        <div class="login-out" @click="loginout">{{ $t('topMenu.logoutTitle') }}</div>
      </div>
    </div>
    <div class="main-body">
      <router-view/>
    </div>
    <div class="foot-bar"></div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data (){
    return {
			langSwitchValue: true,
			languageCode: "cn"
    }
  },
  computed: {
    activeIndex (){
      return this.$Store.state.activeMenu
    }
  },
  methods: {
		changeLanguage (){
      if(this.languageCode === "cn"){
        this.languageCode = "en"
      }else{
        this.languageCode = "cn"
      }
      this.$i18n.locale = this.languageCode
      let lang = this.languageCode == "cn" ? "zh" : "en"
      // 后端国际化代码不一样
      this.change_language(lang)
        .then((response) => {
          console.log(response.msg)
          sessionStorage.setItem("languageCode", this.languageCode)
        });
    },
		changSelectMemu (name){
      var path = ""
      if(name == "annotatingBatchList"){
        path = "/home/annotatingBatchList"
      }else if(name == "systemAdmin"){
        path = "/home/systemAdmin"
      }else if(name == "paraphrasingBatchList"){
        path = "/home/paraphrasingBatchList"
      }
      this.$router.push({
        path: path
      })
    },
    openUserGuide() {
			var user_guide = 'annotator_guide_en.pdf'
			if (this.$Store.state.userInfo.user_role === 'ADMIN') {
				if(this.languageCode === "cn"){
					user_guide = 'administrator_guide_cn.pdf'
				}else{
					user_guide = 'administrator_guide_en.pdf'
				}
			} else {
				if(this.languageCode === "cn"){
					user_guide = 'annotator_guide_cn.pdf'
				}else{
					user_guide = 'annotator_guide_en.pdf'
				}
			}
			
			window.open("/static/" + user_guide)
    },
    showMsg (){
      this.$alertMessage({
        title: "tip"
      })
    },
    loginout () {
      this.logout()
      .then(() => {
        this.$Store.commit("removeUserInfo")
        this.$router.push({
          path: "/login"
        })
      })
    }
	},
  created (){
		this.languageCode = sessionStorage.getItem("languageCode")
  },
  mounted (){

  }
}
</script>

<style lang="less" scope>
#HomePage {
  display: grid !important;
  grid-template-columns: 1fr;
  // grid-template-rows: minmax(0,1fr) minmax(0, 10fr) minmax(0,0.7fr);
  grid-template-rows: 51px minmax(0, 10fr) 35px;
  height: 100vh;
  min-height: 0;
  min-width: 0;
  overflow: hidden;
  background-color: #f3f1f3;
  .menu-containt{
    position: relative;
    /deep/.el-menu-item{
      height: 50px;
      line-height: 50px;
    }
    .menu-button-box{
      position: absolute;
      right: 20px;
      top: 25px;
      transform: translateY(-50%);
      div{
        float: left;
        margin-left: 15px;
        cursor: pointer;
      }
      .lang-name {
        color: rgb(255, 208, 75);
        font-size: 14px;
        &:hover{
          color: #0080ff;
        }
      }
      .user-guide{
        color: rgb(255, 208, 75);
        font-size: 14px;
      }
      .user-guide:hover{
        color: #0080ff;
      }
      .user-name{
        color: #fff;
        font-size: 14px;
      }
      .login-out{
        color: #fff;
        font-size: 14px;
      }
      .login-out:hover{
        color: #0080ff;
      }
    }
  }
  .main-body{
    overflow: hidden;
    height: 100%;
    -webkit-user-select: text!important;
    -moz-user-select: text!important;
    -ms-user-select: text!important;
    user-select: text!important;
  }
  .foot-bar{
    background: rgb(84, 92, 100);
  }
}
</style>
