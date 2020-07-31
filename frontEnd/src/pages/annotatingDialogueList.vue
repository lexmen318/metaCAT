<template>
  <div id="annotatingDialogueList">
    <div class="all-dialogues-container"
      id="listedDialoguesContainer">
      <div class="dialogue-list-title-container">
        <div class="all-dialogues-list-title">
            <h2 v-if="!(dragging)" >
                {{ allDialogueMetadata.length }} {{ $t('annotatingFunction.main.counterHeader') }},
								{{ finished }} {{ $t('annotatingFunction.main.counterTail') }}
            </h2>
            <h2 v-else>
                {{ $t('annotatingFunction.main.counterHint') }}
            </h2>
        </div>

        <div class="file-name-container">
          <div class="inner">
            <p>{{batchId}}</p>
          </div>
        </div>

        <div class="help-button-container">
        </div>

      </div>

      <div class="inner-wrap">
        <!-- <ul class="btn-set">
          <li class="add-dialogue-button">
            <el-button v-if="$Store.state.userInfo.user_role == 'SUPER'"
            type="primary"  @click="create_new_dialogue($event)">{{ $t('annotatingFunction.main.btnCreateNewDialogue') }}</el-button>
          </li>
        </ul> -->
        <FileFormat :isShow="showFileFormat" @closeModal='closeFileFormat'></FileFormat>
        <ul class="dialogue-list">
          <el-row :gutter="15" justify="center">
            <el-col :span="12" v-for="(dat, index) in allDialogueMetadata" :key="index">
              <li class="listed-dialogue">
                <div class="dialogue-list-single-item-container">
                  <el-button plain type="danger" v-if="$Store.state.userInfo.user_role == 'SUPER'"
                  class="del-dialogue-button" @click="delete_dialogue(dat)">{{ $t('annotatingFunction.main.btnDeleteDialogue') }}</el-button>
                  <div class="dialouge-info">
                    <div class="dialogue-id"  @click="clicked_dialogue(dat,$event)">{{dat.id}}</div>
                    <div v-if="dialogue_already_visited(dat.id)" class="visited-indicator" @click="clicked_dialogue(dat,$event)">{{ $t('annotatingFunction.main.lblVisited') }}</div>
                    <el-switch
                      class="switch-status"
                      style="display: block"
                      @change="updataDialogueStatus(dat.id, dat.status)"
                      v-model="dat.status"
                      active-value="FINISHED"
                      inactive-value="PROCESSING"
                      :active-text="dat.status === 'FINISHED'?$t('annotatingFunction.main.lblStatusFinished'):$t('annotatingFunction.main.lblStatusProcessing')">
                    </el-switch>
                    <div class="dialogue-num-turns" >{{dat.num_turns}} {{ $t('annotatingFunction.main.lblTurn') }}</div>
                  </div>
                </div>
              </li>
            </el-col>
          </el-row>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import FileFormat from '../components/FileFormat'
export default {
  name: 'AnnotatingDialogueList',
  components: {
    FileFormat
  },
  data () {
    return {
      allDialogueMetadata: [],
      dragging: false,
      showFileFormat: false,
      userName : '',
      batchId : '',
      finished: 0
    }
  },
  watch: {
    allDialogueMetadata: {
      deep: true,
      handler: function(newVal, oldVal){
        this.finished = 0
        this.allDialogueMetadata.forEach(item => {
          if(item.status === 'FINISHED'){
            this.finished += 1
          }
        })
      }
    }
  },
  methods: {
    updataDialogueStatus (dialogeId, status){
      this.annotating_dialogue_status(this.batchId, dialogeId, status)
        .then(res => {

        })
    },
    closeFileFormat (val) {
      this.showFileFormat = val
    },
    init () {
      this.getAllDialogueIdsFromServer(this.batchId);
    },
    handleDragOver(event) {
      event.stopPropagation();
      event.preventDefault();
      let elem = document.getElementById('listedDialoguesContainer');
      elem.style.transition = '0.3s';
      elem.style.backgroundColor = '#c2c6c4';
      event.dataTransfer.effectAllowed = 'copyMove';
      event.dataTransfer.dropEffect = 'copy';
      this.dragging = true;
    },
    handleDragOut(event) {
      event.preventDefault();
      let elem = document.getElementById('listedDialoguesContainer');
      elem.style.backgroundColor = 'inherit';
      this.dragging = false;
    },
    handleDrop(event) {
      event.preventDefault();
      let elem = document.getElementById('listedDialoguesContainer');
      elem.style.backgroundColor = 'inherit';
      this.dragging = false;
      let file = event.dataTransfer.files[0];
      this.handle_file(file);
    },
    getAllDialogueIdsFromServer(batch_id) {
      this.annotating_dialogues_metadata(batch_id)
        .then( (response) => {
          this.allDialogueMetadata = response;
        });
    },
    dialogue_already_visited(id) {
      return this.$Store.state.alreadyVisited.includes(id)
    },
    clicked_dialogue(clickedDialogue,event) {
      this.$Store.commit('add_already_visited_list', clickedDialogue.id)
      this.$router.push({
        name: "AnnotatingDialogueDetail",
        query: {
          batchId:this.batchId,
					dialogId: clickedDialogue.id
        }
      })
    },
    create_new_dialogue(event) {
      this.post_empty_dialogue(this.batchId)
        .then( (newDialogueId) => {
          this.allDialogueMetadata.unshift({id: newDialogueId, num_turns: 0});
        });
    },
    delete_dialogue(deletDialog) {
      var _this = this
      this.$alertMessage({
        title: this.$t('annotatingFunction.main.lblDeleteHint'),
        msg: this.$t('annotatingFunction.main.lblDeleteWarning'),
        confirmCall: function(){
          _this.del_single_dialogue_async(_this.batchId, deletDialog.id)
            .then( () => {
                _this.getAllDialogueIdsFromServer(_this.batchId);
            });
          _this.$Store.commit('remove_dialogue_from_visited_list', deletDialog.id)
        },
      })
    },
    open_file(event){
      let file = event.target.files[0];
      this.handle_file(file);
    },
    handle_file(file) {
      let textType = /text.plain/;
      let jsonType = /application.json/;
      if (file.type.match(textType)) {
        this.handle_loaded_text_file(file);
      } else if (file.type.match(jsonType)) {
        let reader = new FileReader();
        reader.onload = (event) => {
          let text = reader.result;
          this.post_new_dialogue_from_json_string_async(text)
            .then( (response) => {
              if ('error' in response.data) {
								debugger
								let errorMsg = this.$t('alert.lblJsonFormatError')
								this.$alertMessage({
                  msg: `"${file.name}\" JSON文件格式不正确，错误来自服务器: ${response.data.error}`
                })
              } else {
                  this.getAllDialogueIdsFromServer();
              }
            });
        };
        reader.readAsText(file);
      } else {
        this.$alertMessage({
          msg: this.$t('alert.lblTxtJsonOnlySupport')
        })
      }
    },
    handle_loaded_text_file (file) {
      sessionStorage.setItem('editSourceFile', JSON.stringify(file))
      this.$Store.commit("setSourceFile", file)
      this.$router.push({
        path: "/home/textSplitter"
      })
    },
    handle_file_name_change : function(event){
			return;

      console.log('---- CHANGING FILE NAME ----');
      console.log(event);
      this.put_name(`USER_${this.userName}.json`)
        .then( (response) => {
          if (response) {
            this.$alertMessage({
              msg: this.$t('annotatingFunction.main.msgNameChanged')
            })
          } else {
            this.$alertMessage({
              msg: this.$t('annotatingFunction.main.msgNameChangedError')
            })
          }
        })
    },
    download_all_dialogues_from_server(event) {
      this.get_all_dialogues_async()
        .then( (response) => {
          let blob = new Blob([JSON.stringify(response, null, 4)], {type: 'application/json'});
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          let fileName = "USER_" + this.userName + ".json";
          link.setAttribute('download', fileName );
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link)
        });
    },
    download_all_dialogues_from_server_multiwoz(event) {
      this.get_all_dialogues_async_multiwoz()
        .then( (response) => {
          let blob = new Blob([JSON.stringify(response, null, 4)], {type: 'application/json'});
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          let fileName = "USER_" + this.userName + ".json";
          link.setAttribute('download', fileName );
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link)
        });
    },

  },
  created (){
    this.batchId = this.$route.query.batchId;
    this.init();
  },
  mounted (){

  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@media screen and (max-width: 1182px) {
  .inner-wrap{
    width: 95%!important;
  }
}
#annotatingDialogueList{
  overflow: hidden;
  height: 100%;
  .all-dialogues-container{
    height: 100%;
    overflow-y: scroll;
    overflow-x: hidden;
    .dialogue-list-title-container{
      display: grid;
      grid-template: [row1-start] "title-zone name-zone help-button-zone" [row1-end] / 1fr 1fr 1fr;
      background: rgba(0,0,0,0.02);
      border-top: 1px solid #e6e6e6;
      border-bottom: 1px solid #e6e6e6;
      padding: 10px 25px;
      grid-template-rows: 100%;
      height: 40px;
      .all-dialogues-list-title{
        grid-area: title-zone;
        align-self: center;
        h2{
          font-size: 16px;
          font-weight: 500;
          color: #222;
        }
      }
      .file-name-container{
        grid-area: name-zone;
        align-self: center;
        padding-left: 20px;
        position: relative;
        .inner{
          display: flex;
          align-items: flex-end;
          justify-content: center;
          .el-input{
            width: 38%;
            margin: 0 5px;
            /deep/ .el-input__inner{
              height: 28px;
            }
          }
        }
      }
      .help-button-container{
        grid-area: help-button-zone;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: center;
      }
    }
    .inner-wrap {
      width: 70%;
      margin: 0 auto;
      padding: 0 30px;
      margin-top: 50px;
      overflow: hidden;
      .dialogue-list{
        .el-col{
          margin-bottom: 15px;
        }
        .listed-dialogue{
          .dialogue-list-single-item-container:hover{
            border-left-color: #0080ff;
            box-shadow: 0 4px 5px rgba(0, 0, 0, 0.1);
          }
          .dialogue-list-single-item-container{
            display: grid;
            grid-template: [row1-start] "info del" [row1-end] / 21fr 3fr;
            border: 1px solid #e4e4ec;
            border-left: 5px solid #d1d1d3;
            box-shadow: 1px 3px 4px rgba(0, 0, 0, 0.08);
            transition: ease 175ms all;
            background: #fff;
            .dialouge-info {
              grid-area: info;
              display: grid;
              grid-template: [row1-start] "id visited switchStatus numTurns" [row1-end] / 6fr 2fr 2fr 2fr;
              background-color: white;
              color: #222;
              padding: 5px;
              transition: ease 250ms all;
              .switch-status{
                grid-area: switchStatus;
                align-self: center;
                /deep/.el-switch__core{
                  display: none!important;
                }
                /deep/.el-switch__label{
                  font-weight: 600;
                  cursor: pointer!important;
                  span[aria-hidden="true"]{
                    color: #10c349;
                  }
                }
              }
              .dialogue-id {
                grid-area: id;
                overflow-x: hidden;
                padding: 10px;
                text-overflow: ellipsis;
                white-space: nowrap;
                cursor: pointer;
              }
              .visited-indicator {
                grid-area: visited;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                color: #10c349;
                font-weight: bold;
                font-family: montserrat;
                text-transform: uppercase;
                font-size: 11px;
                letter-spacing: 1px;
                cursor: pointer;
              }
              .dialogue-num-turns {
                grid-area: numTurns;
                align-self: center;
                overflow-x: hidden;
                // display: flex;
                // justify-content: flex-end;
                // align-items: center;
                text-align: right;
                padding-right: 20px;
                font-weight: bold;
                font-family: montserrat;
                text-transform: uppercase;
                font-size: 11px;
                letter-spacing: 1px;
                text-overflow: ellipsis;
                white-space: nowrap;
              }
            }
            .del-dialogue-button {
              grid-area: del;
              height: 28px;
              line-height: 28px;
              align-self: center;
              padding: 0 15px;
              justify-self: flex-end;
              margin-right: 15px;
            }
          }
        }
      }
      .btn-set{
        margin-bottom: 10px;
        display: grid;
        grid-template: [row1-start] "add-dialog-btn upload-file" [row1-end] / 1fr 1fr;
        .add-dialogue-button{
          grid-area: add-dialog-btn;
        }
        .upload-file{
          grid-area: upload-file;
          display: grid;
          justify-content: flex-end;
          .upload-file-btn:hover{
            opacity: 0.8;
          }
          .upload-file-btn{
            color: #FFF;
            background-color: #409EFF;
            border-color: #409EFF;
            border-radius: 4px;
            font-size: 12px;
            height: 35px;
            line-height: 35px;
            padding: 0 15px;
            cursor: pointer;
          }
        }
        #fileInput{
          display: none;
        }
      }
    }
  }
}
</style>
