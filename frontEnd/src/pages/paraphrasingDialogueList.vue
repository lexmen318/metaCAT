<template>
  <div id="paraphrasingDialogueList">
    <div class="all-dialogues-container"
      id="listedDialoguesContainer">
      <div class="dialogue-list-title-container">
        <div class="all-dialogues-list-title">
            <h2>
                {{ Object.keys(allDialogueMetadata).length }} {{ $t('paraphrasingFunction.main.counterHeader') }},
								 {{ finishedTurns }} {{ $t('paraphrasingFunction.main.counterTail') }}
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
        <FileFormat :isShow="showFileFormat" @closeModal='closeFileFormat'></FileFormat>
        <ul class="dialogue-list">
          <el-row :gutter="15" justify="center">
            <el-col :span="12" v-for="(dat, index) in allDialogueMetadata" :key="index">
              <li class="listed-dialogue">
                <div class="dialogue-list-single-item-container">
                  <el-button plain type="danger" v-if="$Store.state.userInfo.user_role == 'SUPER'"
                  class="del-dialogue-button" @click="delete_dialogue(dat)">{{ $t('paraphrasingFunction.main.btnDeleteDialogue') }}</el-button>
                  <div class="dialouge-info">
                    <div class="dialogue-id"  @click="clicked_dialogue(dat,$event)">{{dat.dialogue_id}}</div>
                    <div v-if="dialogue_already_visited(dat.dialogue_id)" class="visited-indicator" @click="clicked_dialogue(dat,$event)">{{ $t('paraphrasingFunction.main.lblVisited') }}</div>
                    <div class="dialogue-finished-turns">{{ $t('paraphrasingFunction.main.lblStatusFinished') }}  {{dat.finished + "/" + dat.turn_len}} {{ $t('paraphrasingFunction.main.lblTurn') }}</div>
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
  name: 'paraphrasingDialogueList',
  components: {
    FileFormat
  },
  data () {
    return {
      allDialogueMetadata: [],
      showFileFormat: false,
      userName : '',
      batchId : '',
    }
  },
  computed: {
    finishedTurns() {
      var num = 0
      console.log("this.allDialogueMetadata",this.allDialogueMetadata)
      for(let key in this.allDialogueMetadata){
        let dialogue = this.allDialogueMetadata[key]
        if(dialogue.turn_len === dialogue.finished){
          num++
        }
      }
      return num
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
    getAllDialogueIdsFromServer(batch_id) {
      // this.annotating_dialogues_metadata(batch_id, "paraphrasing")
      this.get_paraphrasing_dialogues(this.batchId)
        .then( (response) => {
          this.allDialogueMetadata = response.data
        });
    },
    dialogue_already_visited(id) {
      return this.$Store.state.alreadyVisited.includes(id)
    },
    clicked_dialogue(clickedDialogue,event) {
      this.$Store.commit('add_already_visited_list', clickedDialogue.dialogue_id)
      this.$router.push({
        name: "ParaphrasingDialogueDetail",
        query: {
          batchId:this.batchId,
					dialogId: clickedDialogue.dialogue_id
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
        title: this.$t('paraphrasingFunction.main.lblDeleteHint'),
        msg: this.$t('paraphrasingFunction.main.lblDeleteWarning'),
        confirmCall: function(){
          _this.delete_paraphrasing_dialogues(_this.batchId, deletDialog.dialogue_id)
            .then( () => {
                _this.getAllDialogueIdsFromServer(_this.batchId);
            });
          _this.$Store.commit('remove_dialogue_from_visited_list', deletDialog.dialogue_id)
        },
      })
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
#paraphrasingDialogueList{
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
              grid-template: [row1-start] "id visited finishedTurn" [row1-end] / 3fr 1fr 2fr;
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
                text-align: left;
                color: #10c349;
                font-weight: bold;
                font-family: montserrat;
                text-transform: uppercase;
                font-size: 11px;
                letter-spacing: 1px;
                cursor: pointer;
              }
              .dialogue-finished-turns{
                grid-area: finishedTurn;
                align-self: center;
                overflow-x: hidden;
                text-align: right;
                font-weight: bold;
                font-family: montserrat;
                text-transform: uppercase;
                font-size: 11px;
                letter-spacing: 1px;
                text-align: left;
                white-space: nowrap;
              }
              .dialogue-num-turns {
                grid-area: numTurns;
                align-self: center;
                overflow-x: hidden;
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
