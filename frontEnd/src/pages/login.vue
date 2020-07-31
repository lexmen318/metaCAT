<template>
  <div id="Login">
    <el-card class="login-from">
      <div class="project-info">
        <ul>
          <li>{{ $t('login.appTitle') }}</li>
          <li>{{ $t('login.appDesc') }}</li>
        </ul>
      </div>
      <div class="right-login-from">
        <p class="changeLanguage" @click="changeLanguage">{{ $t('lang.targetLanguageName') }}</p>
				<el-form label-position="right" label-width="0" :model="userLoginFrom" ref="userLoginFrom" :rules="userLoginFromRules">
          <el-form-item label="" prop="loginName">
            <el-input v-model="userLoginFrom.loginName" :placeholder="$t('login.loginNameHolder')"></el-input>
          </el-form-item>
          <el-form-item label="" prop="userName" v-if="!showLoginFrom">
            <el-input v-model="userLoginFrom.userName" :placeholder="$t('login.userNameHolder')"></el-input>
          </el-form-item>
          <el-form-item label="" prop="passWord">
            <el-input v-model="userLoginFrom.passWord"  type="password" :placeholder="$t('login.passWordHolder')"></el-input>
          </el-form-item>
          <el-form-item label="" prop="confirmPassWord" v-if="!showLoginFrom">
            <el-input v-model="userLoginFrom.confirmPassWord"  type="password" :placeholder="$t('login.confirmPassWordHolder')"></el-input>
          </el-form-item>
        </el-form>
        <p class="err-message" v-if="isErr">{{errMessage}}</p>
        <div class="form-button">
          <el-button type="primary" @click="loginHandle" v-if="showLoginFrom" class="login-btn">{{ $t('login.btnLogin') }}</el-button>
            <el-button type="primary" @click="registration" v-else>{{ $t('login.btnRegister') }}</el-button>
          <el-button @click="showRegistrationFrom" v-if="!showLoginFrom">{{ $t('login.btnCancel') }}</el-button>
        </div>
        <p v-if="showLoginFrom">
          <span>{{ $t('login.registrationHint') }}</span>
          <span class="registration" @click="showRegistrationFrom">{{ $t('login.btnRegister') }}</span>
        </p>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data (){
    return {
			isErr: false,
			languageCode: "cn",
			languageName: this.$t('lang.languageEnName'),
      showLoginFrom: true,
      userLoginFrom: {
        // loginName: "lwx925289",
        // loginName: "Administrator",
        // passWord: "SuperUser",
        loginName: "",
        passWord: "",
        userName: "",
        confirmPassWord: "",
      },

    }
  },
  watch: {
    showLoginFrom (newVal, oldVal) {
      this.$nextTick(()=>{
        this.$refs["userLoginFrom"].resetFields()
        this.resetFromData()
      })
    },
    userLoginFrom:{
      deep: true,
      handler (newVal, oldVal){
        this.isErr = false
      }
    }
  },
  methods: {
    resetFromData () {
      this.userLoginFrom = {
        loginName: "",
        userName: "",
        passWord: "",
        confirmPassWord: "",
      }
    },
    showRegistrationFrom (){
      this.showLoginFrom = !this.showLoginFrom;
		},
		changeLanguage (){

			// 后端国际化代码不一样
      if(this.languageCode === "en"){
        this.languageCode = "cn"
      }else{
        this.languageCode = "en"
      }
      this.$i18n.locale = this.languageCode
      let lang = this.languageCode == "cn" ? "zh" : "en"
      this.change_language(lang)
        .then((response) => {
          console.log(response.msg)
          sessionStorage.setItem("languageCode", this.languageCode)
        });

		},
    registration () {
      if(!this.$refs["userLoginFrom"]){
        return
      }
      this.$refs["userLoginFrom"].validate((valid) => {
        if (valid) {
					let login_name = this.userLoginFrom.loginName;
					let user_name = this.userLoginFrom.userName;
					let password = this.userLoginFrom.passWord;
					this.register (login_name, user_name, password)
						.then( (response) => {
							if(response.register_result){
								this.showLoginFrom = !this.showLoginFrom;
							} else {
                this.isErr = true
                this.errMessage = response.register_msg
							}

						});
        }
      });
    },
    loginHandle (){
      this.$refs["userLoginFrom"].validate((valid) => {
        if (valid) {
					let login_name = this.userLoginFrom.loginName;
					let password = this.userLoginFrom.passWord;
					this.login(login_name, password)
						.then( (response) => {
							if(response.authenticate_result){
                var path
                if(response.user_info.user_role === 'ADMIN'){
                  path = "/home/systemAdmin"
                }else{
                  path = "/home/annotatingBatchList"
                }
                this.$Store.commit("setUserInfo", response.user_info)
								this.$router.push({
									path: path
								})
								this.$Store.commit("resetAlreadyVisitedList")
							} else {
                this.isErr = true
                this.errMessage = response.authenticate_msg
							}
						});
        }
      });
    },
    enterKeyLogin (event){
      if(event.code === "Enter"){
        this.showLoginFrom && this.loginHandle()
      }
    }
	},
	computed: {
		userLoginFromRules() {
			return {
        loginName: [
          { required: true, message: this.$t('login.loginNameHint'), trigger: 'blur' },
        ],
        userName: [
          { required: true, message: this.$t('login.userNameHint'), trigger: 'blur' },
        ],
        passWord: [
          { required: true, message: this.$t('login.passWordHint'), trigger: 'blur' },
        ],
        confirmPassWord: [
          { required: true, message: this.$t('login.confirmPassWordHint'), trigger: 'blur' },
        ],
      }
		}
	},
  mounted (){
    var _this = this
    document.addEventListener("keydown", _this.enterKeyLogin)
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.enterKeyLogin)
  },
}
</script>

<style lang="less" scope>
@media screen and (max-width: 1500px){
  .login-from{
    width: 60%!important;
  }
}

#Login {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eaf7f4;
  background-size: cover;
  background-image: url("../assets/images/loginBackground.jpg");
  .login-from{
    position: relative;
    box-shadow: 12px 16px 13px -2px rgba(1,1,1,0.1);
    width: 40%;
    transition: 0s;
    border: 0;
    background: transparent;
    .changeLanguage{
      color: #0080ff;
      position: absolute;
      top: 5px;
      right: 10px;
      height: 30px;
      line-height: 30px;
      cursor: pointer;
    }
    .el-card__header{
      padding: 10px;
      .login-from-header{
        height: 50px;
        img{
          height: 100%;
        }
      }
    }
    .el-card__body{
      display: flex;
      justify-content: space-around;
      padding: 0;
      .project-info{
        width: 60%;
        padding: 100px 20px;
        background: rgba(123,109,228,0.8);
        color: white;
        ul{
          li:first-child{
            text-align: center;
            font-weight: 1000;
            font-size: 18px;
            text-indent: 0;
            margin-bottom: 20px;
          }
          li{
            margin-bottom: 10px;
            text-indent: 30px;
          }
        }
      }
      .right-login-from{
        width: 40%;
        padding: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        background: #fff;
        .err-message{
          width: 100%;
          color: #F56C6C;
          margin-top: -15px;
          margin-bottom: 5px;
        }
        .el-form{
          width: 70%;
          .el-form-item{
            height: 35px;
            margin-bottom: 20px;
            .el-form-item__content{
              height: 35px;
              .el-input__inner{
                height: 30px;
                border-left: 0;
                border-right: 0;
                border-top: 0;
                border-radius: 0;
                padding: 0;
              }
            }
          }
        }
        .form-button{
          display: flex;
          justify-content: flex-start;
          .el-button{
            height: 28px;
          }
          .el-button--primary:hover{
            opacity: 0.8;
          }
          .el-button--primary{
            background-color: #7b6de4;
            border-color: #7b6de4;
            padding: 0 10px;
          }
        }
        p{
          font-size: 12px;
          font-weight: 400;
          .registration{
            color: #0080ff;
            display: inline-block;
            height: 30px;
            line-height: 30px;
            cursor: pointer;
					}
        }
      }
    }
  }
  .login-footer{
    display: flex;
    justify-content: center;
  }
}
</style>
