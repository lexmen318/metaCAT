<template>
<div class="sysMgmt" v-loading="uploading">

  <el-row :gutter="20">
    <el-col :span="8">
      <h4>{{ $t('sysMgmt.lblInit') }}</h4>
      <div class="action-btn-box">
        <el-button type="primary" @click="systemInit">{{ $t('sysMgmt.btnInit') }}</el-button>
      </div>

        <h4>{{ $t('sysMgmt.btnImportMetadata') }}</h4>
        <div class="action-btn-box">
        <el-upload ref="uploadFile"
        name="metadata_file"
        :show-file-list="false"
        :action="uploadMetaDataUrl"
        :before-upload="handleBeforeUploadMetaData"
        :on-success="handleSuccessUpload"
        :on-exceed="handleOverFile">
          <el-button type="primary">{{ $t('sysMgmt.btnImportMetadata') }}</el-button>
        </el-upload>
      </div>

      <h4>{{ $t('sysMgmt.lblBatchImporting') }}</h4>
      <div class="action-btn-box">
        <el-upload ref="uploadFile"
        class="upload-batch-zip"
        name="batch_file"
        :show-file-list="false"
        :action="uploadJsonBatchUrl"
        :before-upload="handleBeforeUploadBatch"
        :on-success="handleSuccessUpload"
        :on-exceed="handleOverFile">
          <el-button type="primary">{{ $t('sysMgmt.btnUploadJsonBatch') }}</el-button>
        </el-upload>
      </div>
      <div class="action-btn-box">
        <el-upload ref="uploadFile"
        class="upload-batch-zip"
        name="batch_file"
        :show-file-list="false"
        :action="ploadRawBatchUrl"
        :before-upload="handleBeforeUploadBatch"
        :on-success="handleSuccessUpload"
        :on-exceed="handleOverFile">
          <el-button type="primary">{{ $t('sysMgmt.btnUploadRawBatch') }}</el-button>
        </el-upload>
      </div>

      <h4>{{ $t('sysMgmt.lblBatchExporting') }}</h4>
      <div class="action-btn-box">
        <el-button type="primary" @click="download_all_dialogues_from_server($event, 'annotating')">{{ $t('sysMgmt.btnDownloadAnnotatingBatch') }}</el-button>
        <el-button type="primary" @click="download_all_dialogues_from_server_multiwoz()">{{ $t('sysMgmt.btnDownloadMultiwozBatch') }}</el-button>
      </div>

      <div class="action-btn-box">
        <el-button type="primary" @click="download_all_dialogues_from_server($event, 'paraphrasing')">{{ $t('sysMgmt.btnDownloadParaphrasingBatch') }}</el-button>
      </div>

      <h4>{{ $t('sysMgmt.lblDataConverting') }}</h4>
      <div class="action-btn-box">
        <el-button type="primary" v-for="(item,index) in convertOperation" :key="index+'opertion'" @click="formatData(item.url)">{{item.title}}</el-button>
      </div>
      <h4>{{ $t('sysMgmt.lblDataCleaning') }}</h4>
      <div class="action-btn-box">
        <el-button type="primary" v-for="(item,index) in clearOperation" :key="index+'opertion'" @click="formatData(item.url)">{{item.title}}</el-button>
      </div>

    </el-col>

    <el-col :span="16">
      <div class="active-error-log">
        <h4>{{ $t('sysMgmt.lblOperationErrorRecord') }}</h4>
      </div>
      <el-table class="errorTable" :data="errorTableData" border :max-height="tableHeight">
        <el-table-column type="index" :label="$t('sysMgmt.tblIndex')" width="60">
        </el-table-column>
        <el-table-column property="error_key" :label="$t('sysMgmt.tblErrorNo')" min-width="200">
        </el-table-column>
        <el-table-column property="error_type" :label="$t('sysMgmt.tblErrorType')" min-width="120">
        </el-table-column>
        <el-table-column property="error_time" :label="$t('sysMgmt.tblErrorTime')" min-width="150">
        </el-table-column>
        <el-table-column property="json_url" :label="$t('sysMgmt.tblErrorDetail')" min-width="90">
          <template slot-scope="scope">
            <a :href="scope.row.json_url">{{ $t('sysMgmt.tblDownload') }}</a>
          </template>
        </el-table-column>
        <el-table-column property="zip_url" :label="$t('sysMgmt.tblErrorFile')" min-width="90">
          <template slot-scope="scope">
            <a :href="scope.row.zip_url">{{ $t('sysMgmt.tblDownload') }}</a>
          </template>
        </el-table-column>
        <el-table-column fixed="right" :label="$t('sysMgmt.tblOperation')" width="120">
          <template slot-scope="scope">
            <el-button @click.native.prevent="deleteErrorLog(scope.row)" type="text" size="small">
              {{ $t('sysMgmt.tblDelete') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

    </el-col>
  </el-row>

</div>
</template>

<script>
	export default {
	  name: "SysMgmt",
	  data() {
	    return {
	      uploadMetaDataUrl: "/sys_mgmt/upload_metadata",
	      uploadJsonBatchUrl: "/sys_mgmt/upload_batch_allocation/JSON",
	      ploadRawBatchUrl: "/sys_mgmt/upload_batch_allocation/RAW",
	      uploading: false,
	      errorTableData: [],
	      tableHeight: 500,
	      showErrorLog: false,
	      convertOperation: [],
	      clearOperation: []
	    };
	  },
	  computed: {},
	  methods: {
	    systemInit() {
	      this.sys_init().then(res => {
	        if (res.data.code === 200) {
	          this.$alertMessage({
	            msg: res.data.msg
	          });
	        }
	      });
	    },
	    handleBeforeUploadMetaData(file) {
	      return new Promise((resolve, reject) => {
	        if (file.type !== "application/json") {
	          this.$alertMessage({
	            msg: this.$t('alert.lblOnlyJsonAllowed')
	          });
	          reject(false);
	        } else {
	          this.uploading = true;
	          resolve(true);
	        }
	      });
	    },
	    handleBeforeUploadBatch(file) {
	      return new Promise((resolve, reject) => {
					if (file.type !== "application/zip") {
						this.$alertMessage({
							msg: this.$t('alert.lblOnlyZipAllowed')
						});
						reject(false);
					} else {
						this.uploading = true;
						resolve(true);
						
					}
					
					// this.$alertMessage({
	        //   leftBtnText: this.$t('general.btnNo'),
	        //   rigthBtnText: this.$t('general.btnYes'),
	        //   msg: this.$t('alert.lblAllocateWarning'),
	        //   confirmCall: () => {
	        //     if (file.type !== "application/zip") {
	        //       this.$alertMessage({
	        //         msg: this.$t('alert.lblOnlyZipAllowed')
	        //       });
	        //       reject(false);
	        //     } else {
	        //       this.uploading = true;
	        //       resolve(true);
	        //     }
	        //   }
	        // });
	      });
	    },
	    handleOverFile(file, fileList) {},
	    handleSuccessUpload(res) {
	      this.uploading = false;
	      if (res.code === 100 || res.code === 200) {
	        this.$alertMessage({
	          msg: res.msg
	        });
				}

				// Refresh error table
				this.error_file_list().then(res => {
					this.errorTableData = res.data;
				});
	    },
	    download_all_dialogues_from_server(event, type) {
	      const link = document.createElement("a");
	      let time = new Date();
	      let url = "";
	      if (type == "paraphrasing") {
	        url = "/sys_mgmt/paraphrasing_export_origin?time=" + time.getTime();
	      } else {
	        url = "/sys_mgmt/annotating_export_origin?time=" + time.getTime();
	      }
	      link.href = url;
	      document.body.appendChild(link);
	      link.click();
	      document.body.removeChild(link);
	    },
	    download_all_dialogues_from_server_multiwoz(event) {
	      const link = document.createElement("a");
	      let time = new Date();
	      link.href = "/sys_mgmt/annotating_export_multiwox?time=" + time.getTime();
	      document.body.appendChild(link);
	      link.click();
	      document.body.removeChild(link);
	    },
	    getDataOperations() {
	      this.data_convert_operations().then(res => {
	        this.convertOperation = res.data.convertOperation;
	        this.clearOperation = res.data.clearOperation;
	      });
	    },
	    formatData(url) {
				debugger
				this.$alertMessage({
	        msg: this.$t('alert.lblConfirmToRun'),
	        confirmCall: () => {
	          this.$axios.get(url).then(res => {
	            if (res.data.status) {
	              this.$alertMessage({
	                msg: this.$t('alert.lblOperationSuccess')
	              });
	            }
	          });
	        }
	      });
	    },
	    deleteErrorLog(row) {
	      console.log(row);
	      this.remove_error(row.error_key).then(res => {
	        this.$alertMessage({
	          msg: res.data.msg
	        });
	        this.error_file_list().then(res => {
	          this.errorTableData = res.data;
	        });
	      });
	    }
	  },
	  created() {
	    this.error_file_list().then(res => {
	      this.errorTableData = res.data;
	    });
	    this.getDataOperations();
	    window.onresize = () => {
	      this.tableHeight = Math.ceil(document.body.offsetHeight * 0.6) - 110;
	    };
	  },
	  mounted() {
	    this.tableHeight = Math.ceil(document.body.offsetHeight * 0.6) - 110;
	  }
	};
</script>

<style lang="less" scoped>
.sysMgmt {
  padding: 0 15px;
  .action-btn-box {
    margin-top: 10px;
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    .el-button {
      height: 28px;
      margin-left: 0;
      margin-right: 10px;
      margin-bottom: 10px;
    }
  }
  .active-error-log {
    display: flex;
    justify-content: flex-start;
    h4 {
      margin-bottom: 15px;
    }
  }
  /deep/.el-table {
    .is-leaf {
      padding: 8px 0;
      border-right: 0;
      background: #ebeef5;
      div {
        border-right: 1px solid #fff;
      }
    }
    th.gutter:last-of-type {
      background: #ebeef5;
    }
    .el-table__body td {
      border-right: 0;
      padding: 8px 0;
    }
  }
}
</style>
