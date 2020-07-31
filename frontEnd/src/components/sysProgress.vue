<template>
<div class="sysProgress" v-loading="uploading">

  <el-row :gutter="20">
    <el-col :span="24">
      <div class="active-error-log">
        <h4>{{ $t('taskProgress.tabTitle') }}</h4>
      </div>
      <el-table class="progressTable" :data="progressTableData" border :max-height="tableHeight">
        <el-table-column type="index" :label="$t('taskProgress.number')" width="60">
        </el-table-column>
        <el-table-column property="user_name" :label="$t('taskProgress.userName')" min-width="20">
        </el-table-column>
        <el-table-column property="batch_id" :label="$t('taskProgress.batch')" min-width="40">
        </el-table-column>
				<el-table-column property="category" :label="$t('taskProgress.metadataCategory')" min-width="40">
        </el-table-column>
        <el-table-column property="metadata_name" :label="$t('taskProgress.metadataName')" min-width="40">
        </el-table-column>
				<el-table-column property="batch_progress" :label="$t('taskProgress.progress')" min-width="40">
        </el-table-column>
				<el-table-column property="batch_description" :label="$t('taskProgress.description')">
        </el-table-column>
      </el-table>

    </el-col>
  </el-row>

</div>
</template>

<script>
export default {
  name: 'SysProgress',
  data() {
    return {
      uploading: false,
      progressTableData: [],
      tableHeight: 500
    }
  },
  created() {
    this.getProgressData()
      .then(res => {
        this.progressTableData = res.data
      })
    window.onresize = () => {
      this.tableHeight = Math.ceil(document.body.offsetHeight * 0.6) - 110
    }
  },
  mounted() {
    this.tableHeight = Math.ceil(document.body.offsetHeight * 0.6) - 110
  }

}
</script>

<style lang="less" scoped>
.sysProgress {
  padding: 0 15px;
  .active-error-log{
    display: flex;
    justify-content: flex-start;
    h4{
      margin-bottom: 15px;
    }
  }
  /deep/.el-table {
    .is-leaf{
      padding: 8px 0;
      border-right: 0;
      background: #EBEEF5;
      div{
        border-right: 1px solid #fff;
      }
    }
    th.gutter:last-of-type{
      background: #EBEEF5;
    }
    .el-table__body td{
      border-right: 0;
      padding: 8px 0;
    }
  }
}
</style>
