<template>
  <div class="AlertMessage" v-if="show">
    <el-dialog
      :title="title"
      :visible.sync="show"
      width="20%">
      <span>{{msg}}</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelCallBack">{{leftBtnText}}</el-button>
        <el-button type="primary" @click="confirmCallBack">{{rigthBtnText}}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AlertMessage',
  data () {
    return {
      // I18N can't be done here
      title: '提示',
      msg: '自定义弹出组件',
      leftBtnText: "取 消",
      rigthBtnText: "确 定",
      show: false,
      cancelCall: function(){},
      confirmCall: function(){},
    }
  },
  methods: {
    cancelCallBack (){
      this.cancelCall()
      this.show = false;
    },
    confirmCallBack (){
      this.confirmCall()
      this.show = false;
    },
  },
}
</script>

<style scoped lang="less">
.AlertMessage{
  .el-dialog__header{

  }
  .el-dialog__body{

  }
  /deep/ .el-dialog__footer{
    display: flex;
    justify-content: center;
    padding: 0 0 15px;
    .el-button{
      height: 28px;
      padding: 0 15px;
    }
  }
}
</style>
