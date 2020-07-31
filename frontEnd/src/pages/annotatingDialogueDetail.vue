<template>
  <div id="annotatingDialogueDetail" :class="{'hidden-sys': !annotatingSetting.sysAnnotating}">

    <div id="left-annotations">
      <div class="annotation-header sticky" v-if="false">
      {{ $t('annotatingFunction.detail.lblCurrentTurn') }} {{dCurrentId}}
      </div>
      <LeftClassificationContainer
      v-if="dialogueNonEmpty"
      :metadatas="dTurns.metadata"
      :currentTurn="dCurrentTurn"
      :actionCodeOperation="userIntent.usr"
      @update_classification="turn_update"
      ></LeftClassificationContainer>
    </div>
    <div id="dialogue-turns">
      <div id="dialogue-menu">
        <div class="dialogue-menu-btn">
          <el-button type="primary" @click="go_back_to_all_dialogues($event)"> {{ $t('annotatingFunction.detail.btnDialogueList') }} </el-button>
          <el-button type="primary" @click="validateDialogue">{{ $t('annotatingFunction.detail.btnTagValidate') }}</el-button>
        </div>
        <div class="dialogue-name">
         <el-input v-model="dialogueId" class="edit-title-disable"></el-input>
        </div>
        <div class="saved-status">
            <span v-if="allDataSaved" class="is-saved">{{ $t('annotatingFunction.detail.lblChangeSaved') }}</span>
            <span v-else class="is-not-saved">{{ $t('annotatingFunction.detail.lblChangeNotSaved') }}</span>
            <el-button type="primary"  @click="save()">{{ $t('annotatingFunction.detail.btnSave') }}</el-button>
        </div>
      </div>
      <div class="overflow-hide">
        <div v-for="(turn, index) in dTurns.dialogue" :key="index"
          :class="['dialogue-turn-selected', {'user-string-type-active': (index+1 === dCurrentId)}]"
          @click="update_id(index+1)">
            <div class="turn-header">
                <div class="active-turn-id">
                    {{ $t('annotatingFunction.detail.lblDialogueTurn') }} {{index + 1}}
                </div>
                <el-button plain type="danger" class="turn-deleter" @click="delete_this_turn($event)" v-if="index+1 === dCurrentId && annotatingSetting.turnDeleteFlag">删除</el-button>
            </div>
            <div v-for="(turnVal, turnKey, index) of turn" class="user-string-type"
            :key="index">
                <div class="user-string-type-name">
                  {{turnKey}}
                </div>
                <div class="user-string-type-text">
                  <input class="primary-turn-input"
                    :placeholder="$t('annotatingFunction.detail.lblTurnInputHint')"
                    v-model="turnVal.text"
                    @input="allDataSaved = false"
                    @dragend="forbidingDragInput($event)"
                    @dragstart="drag_start($event, turnKey)">
                </div>
                <p v-if="turnVal.turn_info"
                :class="turnVal.turn_info.status">{{turnVal.turn_info.desc}}</p>
            </div>
        </div>
      </div>
      <div id="input-box" v-if="annotatingSetting.turnAddFlag">
        <ul>
          <li class="input-dialog">
            <el-input v-model="newTurnText" :placeholder="$t('annotatingFunction.detail.lblNewTurnText')" title="用户对话内容" id="new-query-entry-box"
            @keyup.enter.native="new_turn($event)"></el-input>
          </li>
          <li class="input-dialog-btn">
						<el-button type="primary" @click="new_turn">{{ $t('annotatingFunction.detail.btnNewTurn') }} </el-button>
          </li>
        </ul>
      </div>
    </div>

    <div id="right-annotations" v-if="annotatingSetting.sysAnnotating">
      <div class="annotation-header sticky" v-if="false">
      {{ $t('annotatingFunction.detail.lblCurrentTurn') }} {{dCurrentId}}
      </div>
      <RightClassificationContainer
      v-if="dialogueNonEmpty"
      :metadatas="dTurns.metadata"
      :currentTurn="dCurrentTurn"
      :actionCodeOperation="userIntent.sys"
      @update_classification="turn_update"
      ></RightClassificationContainer>
    </div>

  </div>
</template>

<script>
import RightClassificationContainer from '../components/rightClassificationContainer'
import LeftClassificationContainer from '../components/leftClassificationContainer'

export default {
  name: 'AnnotatingDialogueDetail',
  components: {
    LeftClassificationContainer,
    RightClassificationContainer,
  },
  data (){
    return {
      annotatingSetting:{
         sysAnnotating: true,
         turnDeleteFlag: true,
         turnAddFlag: true
      },
      notSaveToLeave: false,
      editingTitle: false,
      isEditTitle: false,
      changesSaved: true,
      dCurrentId: 1,
      dTurns: [],
      allDataSaved: true,
      dialogueId: '',
			batchId: '',
      newTurnText: '',
      result: "",
    }
  },
  watch: {
    dCurrentId (newVal, oldVal){
      let turn = this.dTurns.dialogue[oldVal - 1]
      let validateTurn = this.handelSaveData({dialogue: [turn]})
      this.validate_turn(this.batchId, this.dialogueId, oldVal, this.dTurns.metadata_name, validateTurn)
      .then(res => {
        turn.sys.turn_info = res.sys
        turn.usr.turn_info = res.usr
      })
    }
  },
  computed:{
    activeDomains () {
      let currentTurn = this.dTurns.dialogue[this.dCurrentId - 1]
      return {
        sys: currentTurn.sys.domains,
        usr: currentTurn.usr.domains
      }
    },
    dCurrentTurn () {
        return this.dTurns.dialogue[this.dCurrentId - 1]
    },
    userIntent () {
      let obj = {
        usr: this.dTurns.metadata.intent.usr,
        sys: this.dTurns.metadata.intent.sys
      }
      return obj
    },
    dialogueNonEmpty () {
      var flag
      if(this.dTurns.dialogue && this.dTurns.dialogue.length > 0){
        flag= true
      }else{
        flag = false
      }
      return flag
    }
  },
  methods: {
    new_turn (event) {
      if (this.newTurnText){
        this.append_new_turn()
      }
    },
    append_new_turn (event) {
      var _this = this;
      this.allDataSaved = false;
      this.annotating_turns(this.newTurnText, this.activeDomains)
        .then((response) => {
          this.newTurnText = ""
          _this.dTurns.dialogue.push(response);
          _this.dCurrentId = _this.dTurns.dialogue.length;
          _this.switchDialogueData(_this.dTurns)
          _this.change_focus_based_on_current_turn_id(_this.dCurrentId)
          _this.focus_on_new_query_box();
        })
    },
    validateDialogue () {
      let turns = this.handelSaveData(this.dTurns)
      this.validate_dialogue(this.batchId, this.dialogueId, this.dTurns.metadata_name, turns)
      .then(res => {
        if(res.status != "SUCCESS"){
          let errorTurns = res.err_turns
          this.dTurns.dialogue.forEach((item, index) => {
            item.sys.turn_info = errorTurns[index].sys.turn_info
            item.usr.turn_info = errorTurns[index].usr.turn_info
          })
        }
      })
    },
    handelSaveData (dailogue) {
      var data = JSON.parse(JSON.stringify(dailogue))
      data.dialogue.forEach(turn => {
        var delSlots = function (turnArr, type) {
          let slots = turnArr[type].slots
          let obj = {}
          turnArr[type].domains.forEach(domainItem => {
            obj[domainItem] = []
            let slotsItems = slots[domainItem]
            slotsItems.forEach(item => {
              let flag = false
              let arr = []
              item.slot_items.forEach(subItem => {
                if(subItem.slot_value){
                  flag = true
                  arr.push(subItem)
                }
              })
              if(flag){
                item.slot_items = arr
                delete item.slot_intent
                delete item.slot_value
                obj[domainItem].push(item)
              }
            })
          })
          turnArr[type].slots = obj
        }
        delSlots(turn, "usr")
        delSlots(turn, "sys")
      })
      return data.dialogue
    },
    save (event) {
      let turns = this.handelSaveData(this.dTurns)
      this.save_dialogue(turns)
    },
    save_dialogue (turns) {
      var _this = this;
      this.put_single_dialogue_async(this.batchId, this.dialogueId, turns)
        .then( (status) => {
          if (status === "success") {
            _this.allDataSaved = true;
            _this.init()
          } else {
            _this.allDataSaved = false;
            _this.$alertMessage({
              msg: "Server error, dialogue not saved!"
            })
          }
        });
    },
    forbidingDragInput (event) {
      return false
    },
    drag_start (event, uniqueName) {
      let start_pos = event.target.selectionStart;
      let end_pos = event.target.selectionEnd;
      if (end_pos <= start_pos)
          return false;
      let drag_text = event.target.value.substring(start_pos, end_pos);
      drag_text = drag_text.trimRight();
      end_pos = start_pos + drag_text.length;
      drag_text = drag_text.trimLeft();
      start_pos = end_pos - drag_text.length;
      if (end_pos <= start_pos)
          return false;
      let drag_span = start_pos + '-' + end_pos;
      let data_set = uniqueName + '@' + drag_text + '@' + drag_span;
      event.dataTransfer.setData("Text", data_set)
    },
    check_if_selected (selectId) {
      return this.dCurrentId === this.selectId;
    },
    update_id (turnIndex) {
      this.dCurrentId = turnIndex
    },
    delete_this_turn (event) {
      this.$alertMessage({
        msg: this.$t('alert.lblConfirmToDeleteTurn'),
        confirmCall: () => {
          this.remove_turn()
        },
      })
    },
    handle_dialogue_id_change (event){
        if (event.target.value !== '') {
            this.allDataSaved = false;
            annotationAppEventBus.$emit('dialogue_id_change', event)
        }
    },
    go_back_to_all_dialogues (event){
      this.$router.push({
        path: "AnnotatingDialogueList",
        query: {
          batchId: this.batchId
        }
      })
    },
    switchDialogueData (data){
      let changeSlot = function (meatdata, dialogData){
        for(let metadataSlotKey in meatdata){
          meatdata[metadataSlotKey].forEach(item => {
            item.slot_items = [{
              slot_value: "",
              slot_span: "",
              slot_intent: ""
            }]
          })

          if(!dialogData[metadataSlotKey]){
            dialogData[metadataSlotKey] = meatdata[metadataSlotKey]
          }else{
            let dialogSoltName = []
            let dialogSlotObj = {}
            dialogData[metadataSlotKey].forEach(dialog => {
              dialogSoltName.push(dialog.slot_name)
              dialogSlotObj[dialog.slot_name] = dialog
            })
            dialogData[metadataSlotKey] = []

            meatdata[metadataSlotKey].forEach(exm => {
              let exmCopy = JSON.parse(JSON.stringify(exm))
              if(!dialogSoltName.includes(exmCopy.slot_name)){
                dialogData[metadataSlotKey].push(exmCopy)
              }else{
                let item = dialogSlotObj[exmCopy.slot_name]
                exmCopy.slot_items = item.slot_items
                dialogData[metadataSlotKey].push(exmCopy)
              }
            })
          }
        }
      }

      data.dialogue.forEach(turn => {
        let sysSlot = turn.sys.slots
        let userSlot = turn.usr.slots
        let metadataUserSlot = data.metadata.usr_slot
        let metadataSysSlot = data.metadata.sys_slot

        changeSlot(metadataSysSlot, sysSlot)
        changeSlot(metadataUserSlot, userSlot)
      })
    },
    init () {
        this.getSysSettingView().then(res => {
            this.annotatingSetting = res.data.annotating
        });

        this.get_single_dialogue_async(this.batchId, this.dialogueId)
        .then( (response) => {
          var data = response
          if(data.status === "failure"){
            this.$alertMessage({
              msg: data.msg
            })
            return
          }
          this.switchDialogueData(data)
          this.dTurns = data
        });
    },
    change_turn (event) {
      let temp=0;
      if (event.key === "ArrowUp"){
          temp=-1;
      }
      else if (event.key === "ArrowDown" || event.key === "Enter"){
          temp=1;
      } else if (event.altKey){
          if (event.key === "s")
            this.save_dialogue(event);
          else if (event.key === 'b')
            this.go_back_to_all_dialogues();
          return;
      } else {
          return;
      }

      let allTurnsLength = this.dTurns.dialogue.length;
      if((this.dCurrentId+temp) <= 0){
        this.dCurrentId = allTurnsLength
      }else if((this.dCurrentId+temp) > allTurnsLength){
        this.dCurrentId = 1
      }else{
        this.dCurrentId += temp
      }

      this.change_focus_based_on_current_turn_id(this.dCurrentId);
    },
    change_focus_based_on_current_turn_id (elIndex) {
      this.$nextTick(() => {
        var currendElIndex = elIndex - 1;
        let turnInputElements = document.querySelectorAll(".overflow-hide")[0].children;
        let currendEl = turnInputElements[currendElIndex];
        document.querySelectorAll(".overflow-hide")[0].scrollTop = currendEl.offsetTop - (document.querySelectorAll(".overflow-hide")[0].clientHeight/2);
      })
    },
    remove_turn () {
      this.allDataSaved = false;
      this.dTurns.splice(this.dCurrentId - 1, 1);
    },
    turn_update (updataClassification){
      this.allDataSaved = false;
      let index = this.dCurrentId - 1
      this.dTurns.dialogue[index] = updataClassification
      this.$set(this.dTurns.dialogue, index, updataClassification)
    },
    focus_on_new_query_box () {
      const toFocus = document.getElementById('new-query-entry-box');
      toFocus.focus()
    },
  },
  created () {
    this.dialogueId = this.$route.query.dialogId;
		this.batchId = this.$route.query.batchId;
  },
  mounted(){
    this.init();
    this.$nextTick(()=>{
      window.addEventListener('keyup', this.change_turn);
      this.focus_on_new_query_box();
    })
  },
  beforeRouteLeave (to, from, next) {
    var  _this = this;
    if(!this.allDataSaved){
      this.$alertMessage({
        leftBtnText: this.$t('alert.lblAbandonChange'),
        rigthBtnText: this.$t('alert.lblSaveChange'),
        msg: this.$t('alert.lblReturnAbandonChange'),
        confirmCall: () =>{
          let turns = this.handelSaveData(this.dTurns)
          this.put_single_dialogue_async(this.batchId, this.dialogueId, turns)
            .then( (status) => {
              if (status === "success") {
                next()
              } else {
                _this.$alertMessage({
                  msg: this.$t('alert.lblErrorNotSaved')
                })
                next(false)
              }
            });
        },
        cancelCall: () => {
          next()
        }
      })
    }else{
      next()
    }
  },
  directives: {
    blur: {
      componentUpdated (el) {
          el.blur();
      }
    }
  },
}
</script>

<style lang="less" scope>
.hidden-sys{
  grid-template-columns: minmax(0,1.5fr) minmax(0,3fr)!important;
  grid-template-rows: minmax(0,1fr)!important;
}
#annotatingDialogueDetail {
  display: grid;
  grid-template-columns: minmax(0,1fr) minmax(0,2.4fr) minmax(0,1fr);
  grid-template-rows: minmax(0,1fr);
  height: 100%;
  #left-annotations{
    overflow-y: auto;
    padding: 15px 0;
    background: #fff;
  }
  #dialogue-turns{
    display: grid;
    grid-template-rows: 50px 1fr 50px;
    grid-template-columns: 1fr;
    #dialogue-menu{
      display: grid;
      grid-template-rows: 1fr;
      grid-template-columns:  1fr 1fr 0.6fr;;
      justify-items: center;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
      background: #eeee;
      .dialogue-menu-btn{
        width: 100%;
        display: flex;
        justify-content: flex-start;
        .el-button{
          align-self: center;
          justify-self: flex-start;
          margin-left: 15px;
        }
      }
      .dialogue-name{
        align-self: center;
        justify-self: flex-start;
        .el-input__inner{
          height: 28px;
          font-size: 16px;
        }
        .edit-title-disable{
          .el-input__inner{
            border: 0;
            background: #eee;
          }
        }
      }
      .saved-status{
        align-self: center;
        padding-right: 25px;
        justify-self: flex-end;
        .is-saved{
          color: #0080ff;
        }
        .is-not-saved{
          color: #f56c6c
        }
      }
    }
    .overflow-hide{
      overflow-y: scroll;
      padding: 40px 0;
      .dialogue-turn-selected{
        max-width: 96%;
        margin: 0 15px 15px;
        // width: 100%;
        padding: 20px;
        background-color: #ffffff !important;
        color: #666;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border-radius: 1px;
        transition: 0.3s;
        overflow: hidden;
        height: auto;
        border-left-style: solid;
        border-left-width: 5px;
        border-left-color: #d1d1d3;
        cursor: pointer;
        .turn-header{
          display: grid !important;
          grid-template-columns: minmax(0,9fr) minmax(0,0.7fr);
          margin-bottom: 15px;
          height: 28px;
          opacity: 0.5;
          font-weight: 600;
          color: #222;
          .turn-deleter{
            height: 28px;
            justify-self: flex-end;
          }
        }
        .user-string-type {
          background-color: #ffffff !important;
          // height: 60px;
          margin: 0 0 10px;
          border-radius: 3px;
          display: grid !important;
          grid-template-columns: minmax(0,1fr) minmax(0,9fr);
          min-height: 0;
          min-width: 0;
          overflow: hidden;
          cursor: pointer;
          p{
            grid-column-start: 2;
            grid-column-end: -1;
            font-size: 14px;
          }
          .FAILED{
            color: #dd6161;
          }
          .user-string-type-name {
            background-color: #ececee;
            height: 40px;
            grid-column-start: 1;
            grid-column-end: 2;
            text-align: center;
            color: #222;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0.5;
            cursor: pointer;
          }
          .user-string-type-text {
            background-color: #ffffff!important;
            height: 40px;
            margin: 0;
            grid-column-start: 2;
            grid-column-end: -1;
            opacity: 0.5;
            position: relative;
            cursor: pointer;
            input {
              box-sizing: border-box;
              display: inline-block;
              height: 100%;
              width: 100%;
              justify-self: center;
              margin: 0;
              border-radius: 2px;
              outline: none;
              border: 1px solid #e1e1e3;
              padding: 0 40px 0 15px;
              border-left: none;
              font-size: 18px;
            }
          }
        }
      }
      .user-string-type-active{
        border-left-color: #0080ff;
        .turn-header{
          opacity: 1;
        }
        .user-string-type{
          .user-string-type-name{
            opacity: 1;
          }
          .user-string-type-text{
            opacity: 1;
          }
        }
      }
    }
    #input-box{
      background: #eeee;
      ul{
        display: flex;
        align-items: center;
        // justify-content: center;
        height: 100%;
        padding: 0 20px;
        .input-dialog{
          width: 90%;
          .el-input__inner{
            height: 35px;
          }
        }
        .input-dialog-btn{
          margin-left: 15px;
          // button{
          //   height: 33px;
          //   cursor: pointer;
          //   border-radius: 1px;
          //   border-style: hidden;
          //   padding: 0 20px;
          // }
        }
      }
    }
  }
  #right-annotations{
    overflow-y: auto;
    padding: 15px 0;
    background: #fff;
  }
}
</style>
