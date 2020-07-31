<template>
<div class="systemAdmin">
  <el-card v-loading="uploading" :text="$t('adminMenu.menuTitle')">
    <div class="systemAdmin-title-box">
      <ul class="systemAdmin-menu">
        <li :class="{'active-menu-item': currentTab === 'sysProgress'}" @click="selectMemu('sysProgress')">{{ $t('adminMenu.tabTaskProgress') }}</li>
				<li :class="{'active-menu-item': currentTab === 'dataMgmt'}" @click="selectMemu('dataMgmt')">{{ $t('adminMenu.tabDataMgmt') }}</li>
        <li :class="{'active-menu-item': currentTab === 'sysMgmt'}" @click="selectMemu('sysMgmt')">{{ $t('adminMenu.tabSysMgmt') }}</li>
				<li :class="{'active-menu-item': currentTab === 'sysSetting'}" @click="selectMemu('sysSetting')">{{ $t('adminMenu.tabSysSetting') }}</li>
      </ul>
    </div>
    <div class="main-box">
      <SysProgress v-if="currentTab === 'sysProgress'"></SysProgress>
			<DataMgmt v-if="currentTab === 'dataMgmt'"></DataMgmt>
			<SysMgmt v-if="currentTab === 'sysMgmt'"></SysMgmt>
			<SysSetting v-if="currentTab === 'sysSetting'"></SysSetting>
    </div>
  </el-card>
</div>
</template>

<script>
import SysProgress from '../components/sysProgress'
import DataMgmt from '../components/dataMgmt'
import SysMgmt from '../components/sysMgmt'
import SysSetting from '../components/sysSetting'

export default {
  name: 'BatchAllotment',
  components: {
		SysProgress,
		DataMgmt,
		SysMgmt,
		SysSetting
  },
  data() {
    return {
      uploading: false,
      currentTab: "sysProgress"
    }
  },
  methods: {
    selectMemu(select) {
      this.currentTab = select
    },
    systemInit() {
      this.sys_init()
        .then(res => {
          if (res.data.code === 200) {
            this.$alertMessage({
              msg: res.data.msg
            })
          }
        })
    }
  },

}
</script>

<style lang="less" scoped>
.systemAdmin {
  height: 100%;
  .el-button {
    margin-left: 10px;
    font-size: 14px;
  }

  .el-card {
    height: 100%;
    width: 100%;
    overflow-y: auto;

    /deep/.el-card__body {
      padding: 0;
    }

    .systemAdmin-title-box {
      position: relative;
      background-color: #ebeef2;
      margin-bottom: 15px;

      .systemAdmin-menu {
        height: 40px;
        width: 50%;
        border-top: 1px solid #e4e7ed;
        border-bottom: 1px solid #e4e7ed;

        li {
          float: left;
          height: 41px;
          box-sizing: border-box;
          padding: 10px 15px;
          cursor: pointer;
          font-size: 14px;

          &:hover {
            color: #409eff;
          }
        }

        .active-menu-item {
          color: #409eff;
          background-color: #fff;
          border-right-color: #dcdfe6;
          border-left-color: #dcdfe6;
          transition: all .3s cubic-bezier(.645, .045, .355, 1);
        }
      }
    }
  }
}
</style>
