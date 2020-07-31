<template>
	<div class="sysSetting" v-loading="uploading">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>{{ $t('sysSetting.adminForm.title') }}</span>
      </div>
      <div class="change-password">
        <el-form ref="adminForm" :model="adminForm" :rules="adminFormRules" :label-width="labelWith">
          <el-form-item :label="$t('sysSetting.adminForm.oldPassWord')" prop="oldPassWord">
            <el-input v-model="adminForm.oldPassWord" type="password" ></el-input>
          </el-form-item>
          <el-form-item :label="$t('sysSetting.adminForm.passWord')" prop="passWord">
            <el-input v-model="adminForm.passWord" type="password" ></el-input>
          </el-form-item>
          <el-form-item :label="$t('sysSetting.adminForm.confirmPassWord')" prop="confirmPassWord">
            <el-input v-model="adminForm.confirmPassWord" type="password" ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitChangePwd">{{ $t('sysSetting.adminForm.submitChangePwd') }}</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>{{ $t('sysSetting.settingForm.title') }}</span>
      </div>
      <div class="system-setting-form">
        <el-form ref="settingForm" :model="settingForm" :label-width="labelWith">
          <el-form-item :label="$t('sysSetting.settingForm.annotatingTitle')">
            <el-switch
              v-model="settingForm.annotating.sysAnnotating"
              :active-text="$t('sysSetting.settingForm.annotating.sysAnnotating')">
            </el-switch>
            <el-switch
              v-model="settingForm.annotating.turnDeleteFlag"
              :active-text="$t('sysSetting.settingForm.annotating.turnDeleteFlag')">
            </el-switch>
            <el-switch
              v-model="settingForm.annotating.turnAddFlag"
              :active-text="$t('sysSetting.settingForm.annotating.turnAddFlag')">
            </el-switch>
          </el-form-item>
          <el-form-item :label="$t('sysSetting.settingForm.paraphrasingTitle')">
            <el-switch
              v-model="settingForm.paraphrasing.asrOption"
              :active-text="$t('sysSetting.settingForm.paraphrasing.asrOption')">
            </el-switch>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitSysSetting">{{ $t('sysSetting.settingForm.paraphrasing.submitSysSetting') }}</el-button>
            <el-button @click="resetSysSetting">{{ $t('sysSetting.settingForm.paraphrasing.resetSysSetting') }}</el-button>
          </el-form-item>

        </el-form>
      </div>
    </el-card>
	</div>
</template>

<script>
	export default {
	  name: "SysSetting",
	  data() {
	    return {
	      uploading: false,
	      adminForm: {
	        oldPassWord: "",
	        passWord: "",
	        confirmPassWord: ""
	      },

	      settingForm: {
	        annotating: {
	          sysAnnotating: true,
	          turnDeleteFlag: true,
	          turnAddFlag: true
	        },
	        paraphrasing: {
	          asrOption: true
	        }
	      }
	    };
		},
		computed: {
      labelWith (){
        if(this.$i18n.locale === "en"){
          return "155px"
        }else{
          return "110px"
        }
      },
			adminFormRules() {
				return {
	        oldPassWord: [
	          { required: true, message: this.$t('sysSetting.adminForm.oldPassWordHolder'), trigger: "blur" }
	        ],
	        passWord: [{ required: true, message: this.$t('sysSetting.adminForm.passWordHolder'), trigger: "blur" }],
	        confirmPassWord: [
	          { required: true, message: this.$t('sysSetting.adminForm.confirmPassWordHolder'), trigger: "blur" }
	        ]
	      }
			}
		},
	  methods: {
	    submitChangePwd() {
	      this.$refs["adminForm"].validate(valid => {
	        if (valid) {
	          this.changeAdminPwd(this.adminForm).then(res => {
	            this.$alertMessage({
	              msg: res.data.msg
	            });
	          });
	        }
	      });
	    },
	    submitSysSetting() {
	      this.sysSettingChange(
	        this.settingForm.annotating,
	        this.settingForm.paraphrasing
	      ).then(res => {
					if (res.data.status === "SUCCESS") {
	          this.$alertMessage({
	            msg: this.$t('alert.lblSettingSuccess')
	          });
	        }
	      });
	    },
	    resetSysSetting() {
        this.getSysSettingView()
        .then(res => {
	        this.settingForm.annotating = res.data.annotating;
	        this.settingForm.paraphrasing = res.data.paraphrasing;
	      });
	    }
	  },
	  created() {
      this.getSysSettingView()
      .then(res => {
	      this.settingForm.annotating = res.data.annotating;
	      this.settingForm.paraphrasing = res.data.paraphrasing;
	    });
	  }
	};
</script>

<style lang="less" scoped>
.sysSetting {
  /deep/.box-card{
    margin: 0 10px 10px;
    .el-card__header {
      padding: 10px 20px;
    }
    .change-password{
      width: 30%;
      margin-top: 10px;
    }
  }
}
</style>
