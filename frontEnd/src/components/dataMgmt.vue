<template>
<div class="dataMgmt">

	<el-row :gutter="30">
		<el-col :span="12">
      <div class="table-title-box">
        <h4>{{ $t('dataMgmt.datasetMetadata') }}</h4>
      </div>
			<el-table :data="tableMetaDataList" border style="width: 100%">
				<el-table-column type="index" :label="$t('dataMgmt.number')" width="60">
        </el-table-column>
				<el-table-column property="category" :label="$t('dataMgmt.metadataCategory')" min-width="80">
        </el-table-column>
				<el-table-column property="metadata_name" :label="$t('dataMgmt.metadataName')">
        </el-table-column>
				<el-table-column fixed="right" :label="$t('dataMgmt.operation')" width="100">
					<template slot-scope="scope">
						<el-button style="margin: 0" @click="viewMetaDataDetail(scope.row)" type="text" size="small">{{ $t('dataMgmt.view') }}</el-button>
					</template>
				</el-table-column>
			</el-table>
    </el-col>
		<el-col :span="12">
			<p style="margin-top: 20px;"><b>{{ $t('dataMgmt.metadata') }}</b>{{ $t('dataMgmt.metadataDesc') }}</p>
			<p style="margin-top: 5px;"><b>★&nbsp;{{ $t('dataMgmt.metadataGeneral') }}</b>{{ $t('dataMgmt.metadataGeneralDesc') }}</p>
			<p style="margin-top: 5px;"><b>★&nbsp;{{ $t('dataMgmt.metadataDomain') }}</b>{{ $t('dataMgmt.metadataDomainDesc') }}</p>
			<p style="margin-top: 5px;"><b>★&nbsp;{{ $t('dataMgmt.metadataIntent') }}</b>{{ $t('dataMgmt.metadataIntentDesc') }}</p>
			<p style="margin-top: 5px;"><b>★&nbsp;{{ $t('dataMgmt.metadataSlot') }}</b>{{ $t('dataMgmt.metadataSlotDesc') }}</p>
		</el-col>
	</el-row>
  <el-dialog
    :title="metaDataDetailTitle"
    :visible.sync="showMetaDataDetail"
    width="50%">
    <div class="metadata-detail-body">
      <JSONView
        :value="metaDataDetailText"
        :expand-depth="5"
        copyable
        boxed
        sort
      ></JSONView>
    </div>
    <span slot="footer" class="dialog-footer">
      <el-button @click="showMetaDataDetail = false">{{ $t('general.btnClose') }}</el-button>
    </span>
  </el-dialog>

	<el-divider><h3>{{ $t('dataMgmt.batchDivider') }}</h3></el-divider>

	<div class="allocation-batch-containt">
    <label for="" class="allocation-user-select-label">{{ $t('dataMgmt.userAllocate') }}:</label>
    <el-select v-model="selectUser" :placeholder="$t('dataMgmt.userAllocateHint')">
      <el-option v-for="user in userList" :key="user.login_name" :label="user.user_name" :value="user.login_name">
      </el-option>
    </el-select>
  </div>

  <el-row :gutter="30">
    <el-col :span="12">
      <div class="table-title-box">
        <h4>{{ $t('dataMgmt.annotating.title') }}</h4>
        <el-button type="primary" @click="commitAllotmention($event, 'annotating')" class="allocation-btn">{{ $t('dataMgmt.batchAllocate') }}</el-button>
      </div>
      <el-table class="allocationTable" :data="tableAnnotatingData" border @select="annotatingSelectSingleBatch" @select-all="annotatingSelectAllBatch" :max-height="tableHeight">
        <el-table-column type="selection" width="50">
        </el-table-column>
        <el-table-column type="index" :label="$t('dataMgmt.annotating.number')"  width="60">
        </el-table-column>
        <el-table-column property="batch_id" :label="$t('dataMgmt.annotating.batchNo')" min-width="120">
        </el-table-column>
        <el-table-column property="metadata_name" :label="$t('dataMgmt.annotating.metadataName')" min-width="120">
        </el-table-column>
      </el-table>
    </el-col>
    <el-col :span="12">
      <div class="table-title-box">
        <h4>{{ $t('dataMgmt.paraphrasing.title') }}</h4>
        <el-button type="primary" @click="commitAllotmention($event, 'paraphrasing')" class="allocation-btn">{{ $t('dataMgmt.batchAllocate') }}</el-button>
      </div>
      <el-table class="allocationTable" :data="tableparaphrasingData" border @select="paraphrasingSelectSingleBatch" @select-all="paraphrasingSelectAllBatch" :max-height="tableHeight">
        <el-table-column type="selection" width="50">
        </el-table-column>
        <el-table-column type="index" :label="$t('dataMgmt.paraphrasing.number')" width="60">
        </el-table-column>
        <el-table-column property="batch_id" :label="$t('dataMgmt.paraphrasing.batchNo')" min-width="120">
        </el-table-column>
        <el-table-column property="metadata_name" :label="$t('dataMgmt.paraphrasing.metadataName')" min-width="120">
        </el-table-column>
      </el-table>
    </el-col>
  </el-row>

</div>
</template>

<script>
import JSONView from 'vue-json-viewer'

export default {
  name: 'DataMgmt',
  data() {
    return {
      showMetaDataDetail: false,
			metaDataList: [],
			metaDataDetail: {},
			metaDataDetailTitle: '',
			metaDataDetailText: '',
			uploading: false,
      annotatingData: [],
      paraphrasingData: [],
      userList: [],
      selectUser: "",
      selectedAnnotatingBatch: [],
      selectedparaphrasingBatch: [],
      tableHeight: 500
    }
  },
  components: {
    JSONView
  },
  computed: {
		tableMetaDataList() {
      return this.metaDataList
    },
		tableAnnotatingData() {
      return this.annotatingData
    },
    tableparaphrasingData() {
      return this.paraphrasingData
    }
  },
  methods: {
    annotatingSelectSingleBatch(selection, row) {
			this.selectedAnnotatingBatch = selection
    },
    annotatingSelectAllBatch(row) {
      this.selectedAnnotatingBatch = row
    },
    paraphrasingSelectSingleBatch(selection, row) {
      this.selectedparaphrasingBatch = selection
    },
    paraphrasingSelectAllBatch(row) {
      this.selectedparaphrasingBatch = row
		},
		getMetadataList() {
      var _this = this
      this.metadata().
			then(res => {
				_this.metaDataList = res.data
			})
		},
		viewMetaDataDetail(row) {
			this.metadata_detail(row.category, row.metadata_name).
			then(res => {
        this.showMetaDataDetail = true
				this.metaDataDetail = res.data
				this.metaDataDetailTitle = row.metadata_name + '-[' + row.category + ']'
        this.metaDataDetailText = this.metaDataDetail
			})
		},
    getAllocationList(batchCategory) {
      var _this = this
      if(batchCategory === "paraphrasing"){
        this.batch_allocation_list(batchCategory).
        then(res => {
          _this.paraphrasingData = res.data
        })
      }else{
        this.batch_allocation_list(batchCategory).
        then(res => {
          _this.annotatingData = res.data
        })
      }
    },
    commitAllotmention(event, batchCategory) {
      let selectBatch = batchCategory === "paraphrasing"? this.selectedparaphrasingBatch: this.selectedAnnotatingBatch
      if (selectBatch.length == 0) {
        this.$alertMessage({
          msg: this.$t('alert.lblSelectBatch')
        })
        return
      }
      if (!this.selectUser) {
        this.$alertMessage({
          msg: this.$t('alert.lblSelectUser')
        })
        return
      }
      let arr = []
      selectBatch.forEach(batchItem => {
				// arr.push(batchItem.batch_id)
				arr.push({"batch_id":batchItem.batch_id, "metadata_name": batchItem.metadata_name})
      })
      batchCategory === "paraphrasing"? (this.selectedparaphrasingBatch = []) : (this.selectedAnnotatingBatch = [])

      this.batch_allocation(arr, this.selectUser, batchCategory)
        .then(res => {
          if (res.data.code === 200 || res.data.code === 100) {
            this.$alertMessage({
              msg: res.data.msg
            })
          }
          this.getAllocationList(batchCategory)
        })
    }
  },
  created() {
		this.getMetadataList()
		this.getAllocationList("annotating")
    this.getAllocationList("paraphrasing")
    this.user_list().
    then(res => {
      this.userList = res.data
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
.metadata-detail-body{
  max-height: 500px;
  overflow-y: auto;
  border: 1px solid #eee;
  .jv-container.boxed:hover{
    border-color: #eee;
  }
}
.dataMgmt {
  padding: 0 15px;
  .el-button {
    height: 28px;
    margin-left: 15px;
    font-size: 14px;
  }

  .allocation-batch-containt {
    margin-bottom: 15px;
    .allocation-user-select-label{
      font-size: 15px;
      margin-right: 10px;
    }
    /deep/.el-select {
      .el-input__inner {
        height: 28px;
      }

      .el-select__caret {
        line-height: 31px !important;
      }
    }
  }
  .table-title-box{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    .allocation-btn{
      align-self: flex-end;
      margin-bottom: 10px;
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
