<template>
  <div class="paraphrasingDialogueDetail">
    <div class="dialogue-mark-area">
      <div class="dialogue-id">
        <span>{{ $t('paraphrasingFunction.detail.lblDialogueId') }}</span>
        <span>{{dialogueId}}</span>
      </div>
      <div>
        <ul class="dialogue-areas">
          <li>{{ $t('paraphrasingFunction.detail.lblDomainSeries') }}</li>
          <li>{{dialogueData.domain_sequence}}</li>
        </ul>
      </div>
      <h4 class="table-title">{{ $t('paraphrasingFunction.detail.lblStandardSlot') }}</h4>
      <el-table
        :data="currendStandardTableDatas"
        style="width: 100%">
        <el-table-column v-for="item in standardSlotTableProps" :key="item.prop"
          :prop="item.prop"
          :label="item.label"
          :min-width="item.width">
        </el-table-column>
      </el-table>
      <h4 class="table-title">{{ $t('paraphrasingFunction.detail.lblparaphrasingSlot') }}</h4>
      <el-table
        :data="currendparaphrasingTableDatas"
        style="width: 100%">
        <el-table-column v-for="item in standardSlotTableProps" :key="item.prop"
          :prop="item.prop"
          :label="item.label"
          :min-width="item.width">
          <template slot-scope="scope">
            <p v-if="!item.isInput">{{scope.row[item.prop]}}</p>
            <template v-else>
              <el-input v-if="item.prop ==='slotValue'"
              v-model="scope.row[item.prop]"
              :placeholder="item.label"
              @input="computeSlotPosition(scope.row)"
              @drop.native="dragInput($event, scope.row)"></el-input>
              <el-input v-else-if="item.prop ==='originalValue'" v-model="scope.row[item.prop]"
              @drop.native="disableDrop($event)"
              @input="inputOriginalValue"
              :placeholder="item.label"></el-input>
              <el-input v-else v-model="scope.row[item.prop]"
              @drop.native="disableDrop($event)"
              :placeholder="item.label"></el-input>
            </template>
          </template>
        </el-table-column>
      </el-table>
      <div class="action-btn-box">
        <el-button type="primary" @click="closeDescription">{{ $t('paraphrasingFunction.detail.btnTaskDescription') }}</el-button>
        <el-button type="primary" @click="validateparaphrasingDialogue">{{ $t('paraphrasingFunction.detail.btnValidate') }}</el-button>
        <el-button type="primary" @click="saveparaphrasingDialogue">{{ $t('paraphrasingFunction.detail.btnSave') }}</el-button>
      </div>
    </div>
    <div class="overflow-hide">
      <div class="overflow-header">
        <div class="back-btn">
          <el-button type="primary" @click="goBackAllparaphrasing">{{ $t('paraphrasingFunction.detail.btnBackToMain') }}</el-button>
        </div>
        <div class="annotation-description">
          <p>{{ $t('paraphrasingFunction.detail.lblTaskHint') }}</p>
        </div>
      </div>
      <div v-for="(turn, index) in dialogueData.turn_list" :key="index"
        :class="['dialogue-turn-selected', {'user-string-type-active': (index+1 === dCurrentId)}]"
        @click="update_id(index+1)">
          <div class="turn-header">
              <div class="active-turn-id">
                  <span>{{ $t('paraphrasingFunction.detail.lblDialogueTurn') }} {{index + 1}}</span>
              </div>
              <p class="turn-error-msg">
                <span :class="[turn.para_info.status]">{{turn.para_info.desc}}</span>
                <span :class="[turn.para_info.status]">{{`[${turn.para_info.status}]`}}</span>
              </p>
          </div>
          <div class="dialogue-content-box">
            <div class="dialogue-title">{{turn.role ==="usr" ? $t('paraphrasingFunction.detail.lblTurnUser') : $t('paraphrasingFunction.detail.lblTurnSys')}}</div>
            <div class="user-string-type">
              <div class="user-string-type-name standard-dialogue">{{ $t('paraphrasingFunction.detail.lblStandardDialogue') }}</div>
              <div class="user-string-type-text standard-dialogue">
                <p v-html="turn.src_dialog.lightHeightText">{{turn.src_dialog.lightHeightText}}</p>
              </div>
              <div class="user-string-type-name paraphrasing-dialogue">{{ $t('paraphrasingFunction.detail.lblparaphrasingDialogue') }}</div>
              <div class="user-string-type-text paraphrasing-dialogue">
                <input class="primary-turn-input"
									:placeholder="$t('paraphrasingFunction.detail.lblparaphrasingDialogueHint')"
                  @change="changeDilogueInput"
                  @drop="disableDrop($event)"
                  @dragstart="bindingDrageValue($event, turn.para_dialog)"
                  v-model="turn.para_dialog.text" />
                <div class="voice-input-button-wrapper" v-if="paraphrasingSetting.asrOption">
                  <voice-input-button
                    server=""
                    appId=""
                    APIKey=""
                    @record="(text)=>{showResult(text, turn.para_dialog)}"
                    @record-start="recordStart"
                    @record-stop="recordStop"
                    @record-blank="recordNoResult"
                    @record-failed="recordFailed"
                    @record-ready="recordReady"
                    interactiveMode="touch"
                    color="#c8bcbc"
                    tipPosition="top"
                  >
                    <template slot="no-speak">{{ $t('paraphrasingFunction.detail.lblAsrNoDataHint') }}</template>
                  </voice-input-button>
                </div>
              </div>
            </div>
          </div>
      </div>
    </div>
    <FileFormat :isShow="showFileFormat" @closeModal="closeDescription" :width="40">
      <h4 slot="header">{{ $t('paraphrasingFunction.detail.lblScenarioDescription') }}</h4>
      <p slot="body" v-for="(task,index) in dialogueData.task_list" :key="index"
        style="text-indent: 30px;margin-bottom: 10px;">{{task["TaskDescription"]}}</p>
    </FileFormat>
  </div>
</template>

<script>
import FileFormat from '../components/FileFormat'
import voiceInputButton from '../utils/voice-input-button-master/dist/voice-input-button'

export default {
  name: 'ParaphrasingDialogueDetail',
  components: {
    FileFormat,
    voiceInputButton,
  },
  data () {
    return {
      paraphrasingSetting:{
          asrOption: false
      },
      dataNotSave: false,
      showFileFormat: false,
      dataTransfer: null,
      dCurrentId: 1,
      standardSlotTableDatas: [],
      paraphrasingSlotTableDatas: [],
      dialogueData: [],
      batchId: "",
      dialogueId: ""
    }
  },
  beforeRouteLeave (to, from, next) {
    if(this.dataNotSave){
      this.$alertMessage({
        title: this.$t('general.lblReminder'),
        leftBtnText: this.$t('paraphrasingFunction.detail.lblLeftBtnText'),
        rigthBtnText: this.$t('paraphrasingFunction.detail.lblRightBtnText'),
        msg: this.$t('paraphrasingFunction.detail.lblBtnMst'),
        confirmCall: () =>{
          let turn_list = this.formatTurnList("all")
          this.updata_paraphrasing_dialogues(this.batchId, this.dialogueId, turn_list)
          .then(res => {
            if(res.data.status.toLowerCase() === "success"){
              next()
            }else{
              next(false)
            }
          })
        },
        cancelCall: () => {
          next()
        }
      })
    }else{
      next()
    }
  },
  watch: {
    dCurrentId (newValue, oldValue){
      let flag = false
      let currentTurn = this.dialogueData.turn_list[oldValue - 1]
      if(!currentTurn.para_dialog.text || (currentTurn.para_info.status != "SUCCESS" && currentTurn.para_info.status != "FINISHED")){
        flag = true
      }

      if(flag){
        let turn_id  = oldValue - 1
        let turn = this.formatTurnList("single",turn_id)
        this.validate_paraphrasing_turn(this.batchId, this.dialogueId, turn)
        .then(res => {
        let error_turn = this.dialogueData.turn_list[turn_id]
        error_turn.para_info.desc = res.data.error
        error_turn.para_info.status = res.data.status
          })
        }
      }
  },
  computed: {

		standardSlotTableProps(){
			return [
        {
          prop: "slot",
          label: this.$t('paraphrasingFunction.detail.lblSlotLabel'),
          width: 20,
        },
        {
          prop: "slotValue",
          label: this.$t('paraphrasingFunction.detail.lblSlotValue'),
          width: 40,
          isInput: true,
        },
        {
          prop: "slotPosition",
          label: this.$t('paraphrasingFunction.detail.lblSlotPosition'),
          width: 20,
          isInput: true,
        },
        {
          prop: "originalValue",
          label: this.$t('paraphrasingFunction.detail.lblOriginalValue'),
          width: 40,
          isInput: true,
        },
      ]
		},
		currendStandardTableDatas() {
      return this.standardSlotTableDatas[this.dCurrentId - 1]
    },
    currendparaphrasingTableDatas() {
      return this.paraphrasingSlotTableDatas[this.dCurrentId - 1]
    },
    dTransformedTurns() {
      return this.dialogueData.turn_list
    }
  },
  methods: {
    showResult (text, model) {
			model.text += text
      console.log(this.$t('asr.lblReceiveResult'), text)
    },
    recordStart () {
      console.log(this.$t('asr.lblRecordStart'))
    },
    recordStop () {
      console.log(this.$t('asr.lblRecordEnd'))
    },
    recordNoResult () {
      console.log(this.$t('asr.lblNoCapture'))
    },
    recordFailed (error) {
      console.log(this.$t('asr.lblRecognizeFailed'), error)
    },
    recordReady () {
      console.log(this.$t('asr.lblRecordReady'))
    },
    changeDilogueInput(value) {
      this.dataNotSave = true
    },
    formatTurnList(type, turnId) {
      let turn_list = {}

      let changeSlotsData = (turn) => {
        let slotsObj = {
            role: turn.role,
            para_dialog: {
              single_slot: {},
              text: turn.para_dialog.text || "",
              batch_slot: {}
            }
          }
          this.paraphrasingSlotTableDatas[turn.turn_id].forEach(slotItem => {
            if(slotItem.slotType === "single"){
              var posArr = slotItem.slotPosition.split("-")
              slotsObj.para_dialog.single_slot[slotItem.slot] = [slotItem.slotValue, (posArr[0] || ""), (posArr[1] || ""), slotItem.originalValue]
            }

            if(slotItem.slotType === "batch"){
              var posArr = slotItem.slotPosition.split("-")
              if(slotsObj.para_dialog.batch_slot[slotItem.slot]){
                slotsObj.para_dialog.batch_slot[slotItem.slot].push([slotItem.slotValue, (posArr[0] || ""), (posArr[1] || ""), slotItem.originalValue])
              }else{
                slotsObj.para_dialog.batch_slot[slotItem.slot] = [ [slotItem.slotValue, (posArr[0] || ""), (posArr[1] || ""), slotItem.originalValue] ]
              }
            }
          })
        return slotsObj
      }

      if(type === "all"){
        this.dialogueData.turn_list.forEach(item => {
          let slotsObj = changeSlotsData(item)
          turn_list[item.turn_id] = slotsObj
        })
      }else{
        this.dialogueData.turn_list.forEach(item => {
          if(item.turn_id === turnId){
            let singleSlotsObj = changeSlotsData(item)
            turn_list[item.turn_id] = singleSlotsObj
            return
          }
        })
      }
      return turn_list
    },
    saveparaphrasingDialogue() {
      this.dataNotSave = false
      let turn_list = this.formatTurnList("all")
      this.updata_paraphrasing_dialogues(this.batchId, this.dialogueId, turn_list)
      .then((res) => {
        if(res.data.status === "SUCCESS"){
          this.init()
        }
      })
    },
    validateparaphrasingDialogue() {
      let turn_list = this.formatTurnList("all")
      this.validate_paraphrasing_dialogues(this.batchId, this.dialogueId, turn_list)
      .then(res => {
        var errorList = res.data.err_turns
        errorList.forEach(errItem => {
          this.dialogueData.turn_list.forEach(turn => {
            if(turn.turn_id === errItem.turn_id){
              turn.para_info.desc = errItem.error
              turn.para_info.status = errItem.status
            }
          })
        })
      })
    },
    getDialogueData() {
      this.standardSlotTableDatas = this.initStandardTableSlots(this.dialogueData)
      this.paraphrasingSlotTableDatas = this.initparaphrasingTableSlots(this.dialogueData)

      this.dialogueData.turn_list.forEach(item => {
        //复制系统对话
        if(item.role === "sys" && !item.para_dialog.text){
          item.para_dialog.text = item.src_dialog.text
        }

        var lightHeightText = item.src_dialog.text,
            textColor = "#0080ff",
            solts = item.src_dialog.single_slot,
            batchSlots = item.src_dialog.batch_slot
        for(let key in solts){
          lightHeightText = lightHeightText.replace(solts[key][0], `<span style='color: ${textColor}'>${solts[key][0]}</span>`)
        }
        for(let key in batchSlots){
          batchSlots[key].forEach(item => {
            lightHeightText = lightHeightText.replace(item[0], `<span style='color: ${textColor}'>${item[0]}</span>`)
          })
        }

        item.src_dialog.lightHeightText = lightHeightText
      })

      return this.dialogueData
    },
    closeDescription(value){
      this.showFileFormat = !this.showFileFormat
    },
    disableDrop(event){
      event.preventDefault()
      return false
    },
    dragInput(event, row) {
      event.preventDefault();
      let dataTransfer = event.dataTransfer.getData("drageText")
      if(dataTransfer){
        var arr = dataTransfer.split("||")
        row.slotValue = arr[0]
        row.slotPosition = arr[1]
      }
    },
    computeSlotPosition(target) {
      this.dataNotSave = true
      if(!target.slotValue){
        target.slotPosition = ""
      }
    },
    inputOriginalValue() {
      this.dataNotSave = true
    },
    bindingDrageValue(event, turn) {
      let paraphrasingText = turn.text
      let start_pos = event.target.selectionStart;
      let end_pos = event.target.selectionEnd;
      if (end_pos <= start_pos)
          return false;
      let value = paraphrasingText.substring(start_pos, end_pos)
      value = value.trimRight();
      end_pos = start_pos + value.length;
      value = value.trimLeft();
      start_pos = end_pos - value.length;
      if (end_pos <= start_pos)
          return false;
      let data_set = `${value}||${start_pos}-${end_pos}`
      event.dataTransfer.setData("drageText", data_set)
    },
    initparaphrasingTableSlots(dialogues) {
      var tabelData = {}
      var list = dialogues.turn_list
      list.forEach(item => {
        tabelData[item.turn_id] = []
        var singleSlots = dialogues.activated ? item.para_dialog.single_slot : item.src_dialog.single_slot
        var batchSlots = dialogues.activated ? item.para_dialog.batch_slot : item.src_dialog.batch_slot
        for(let key in singleSlots){
          let emptySingleSlotObj = {
            slot: key,
            slotValue: "",
            slotPosition: "",
            originalValue: "",
            slotType: "single",
          }
          let singleSlotObj = {
            slot: key,
            slotValue: singleSlots[key][0],
            slotPosition: `${singleSlots[key][1]}-${singleSlots[key][2]}`,
            originalValue: singleSlots[key][3],
            slotType: "single",
          }

          if(dialogues.activated){
            tabelData[item.turn_id].push(singleSlotObj)
          }else{
            // 过滤槽位为0-0的值
            if(singleSlots[key][1] === 0 && singleSlots[key][2] === 0){
              continue
            }else{
              tabelData[item.turn_id].push(emptySingleSlotObj)
            }
          }
        }

        for(let key in batchSlots){
          let arr = batchSlots[key]
          arr.forEach(batchSlotItem => {
            let emptyBatchSlotObj = {
              slot: key,
              slotValue: "",
              slotPosition: "",
              originalValue: "",
              slotType: "batch"
            }
            let batchSlotObj = {
              slot: key,
              slotValue: batchSlotItem[0],
              slotPosition: `${batchSlotItem[1]}-${batchSlotItem[2]}`,
              originalValue: batchSlotItem[3],
              slotType: "batch"
            }
            if(dialogues.activated){
              tabelData[item.turn_id].push(batchSlotObj)
            }else{
              // 过滤槽位为0-0的值
              if(batchSlotItem[1] === 0 && batchSlotItem[2] === 0){
                // continue
              }else{
                tabelData[item.turn_id].push(emptyBatchSlotObj)
              }
            }
          })
        }
      })
      return tabelData
    },
    initStandardTableSlots(dialogues) {
      var tabelData = {}
      var list = dialogues.turn_list
      list.forEach(item => {
        tabelData[item.turn_id] = []
        var slots = item.src_dialog.single_slot
        var batchSlots = item.src_dialog.batch_slot

        for(let key in slots){
          let singleSlotObj = {
            slot: key,
            slotValue: slots[key][0],
            slotPosition: `${slots[key][1]}-${slots[key][2]}`,
            originalValue: slots[key][3],
            slotType: "single"
          }

          tabelData[item.turn_id].push(singleSlotObj)
        }

        for(let key in batchSlots){
          let arr = batchSlots[key]
          arr.forEach(batchSlotItem => {
            let batchSlotObj = {
              slot: key,
              slotValue: batchSlotItem[0],
              slotPosition: `${batchSlotItem[1]}-${batchSlotItem[2]}`,
              originalValue: batchSlotItem[3],
              slotType: "batch"
            }
            tabelData[item.turn_id].push(batchSlotObj)
          })
        }
      })
      return tabelData
    },
    init() {
			this.getSysSettingView().then(res => {
					this.paraphrasingSetting = res.data.paraphrasing
			});

			this.get_paraphrasing_dialogues(this.batchId, this.dialogueId)
      .then(res => {
        this.dialogueData = res.data
        this.getDialogueData()
      })
    },
    update_id (turnIndex) {
      this.dCurrentId = turnIndex
    },
    delete_this_turn (event) {
      this.$alertMessage({
        msg: this.$t('paraphrasingFunction.detail.lblDeleteHint'),
        confirmCall: () => {
          // this.remove_turn()
        },
      })
    },
    change_turn (event) {
      let temp=0;
      if (event.key === "ArrowUp"){
          temp=-1;
      } else if (event.key === "ArrowDown" || event.key === "Enter"){
          temp=1;
      } else if (event.altKey){
          // if (event.key === "s")
            // this.save_dialogue(event);
          // else if (event.key === 'b')
            // this.go_back_to_all_dialogues();
          // return;
      } else {
          return;
      }

      let allTurnsLength = this.dTransformedTurns.length;
      if((this.dCurrentId+temp) <= 0){
        this.dCurrentId = allTurnsLength
      }else if((this.dCurrentId+temp) > allTurnsLength){
        this.dCurrentId = 1
      }else{
        this.dCurrentId += temp
      }
      console.log("当前id", this.dCurrentId)
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
    goBackAllparaphrasing() {
      this.$router.push({
        path:'/home/paraphrasingDialogueList',
				query: {
					batchId: this.batchId
				}
      })
    },
  },
  created() {
    this.batchId = this.$route.query.batchId;
    this.dialogueId = this.$route.query.dialogId;
    this.init()
    this.$nextTick(() => {
      window.addEventListener('keyup', this.change_turn);
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.paraphrasingDialogueDetail{
  display: grid;
  grid-template-columns: 8fr 16fr;
  grid-template-rows: minmax(0,1fr);
  grid-template-areas: "mark dialogueparaphrasing";
  height: 100%;
  .annotation-description{
    p{
      line-height: 20px;
      margin-left: 10px;
      color: #0080ff;
    }
  }
  .dialogue-mark-area{
    overflow-y: auto;
    padding: 20px 10px 45px 20px;
    .dialogue-id{
      margin-bottom: 10px;
      span:nth-child(1){
        font-size: 16px;
        font-weight: 600;
      }
    }
    .action-btn-box{
      position: absolute;
      bottom: 45px;
      z-index: 100;
      .el-button{
        height: 28px;
      }
    }
    .dialogue-areas{
      display: flex;
      border: 2px solid #DCDFE6;
      min-width: 60%;
      margin-bottom: 10px;
      li{
        padding: 5px;
      }
      li:nth-child(1){
        width: 85px;
        border-right: 2px solid #DCDFE6;
      }
    }
    .table-title{
      margin-bottom: 10px;
    }
    .el-table{
      margin-bottom: 20px;
    }
    /deep/.el-input__inner{
      height: 28px;
    }
  }
  .overflow-hide{
    overflow-y: scroll;
    grid-area: dialogueparaphrasing;
    padding: 20px 0;
    .overflow-header{
      margin: 0 15px 15px;
      display: grid;
      grid-template-columns: 1fr 9fr;
      grid-template-areas: "backBtn dialogueId ..";
      align-items: center;
      .back-btn{
        grid-area: backBtn;
      }
    }
    .dialogue-turn-selected{
      max-width: 96%;
      margin: 0 15px 15px;
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
        grid-template-columns: minmax(0,110px)  minmax(0,9fr);
        grid-template-areas: "turnId turnError";
        margin-bottom: 15px;
        height: 28px;
        opacity: 0.5;
        font-weight: 600;
        color: #222;
        overflow: hidden;
        height: auto;
        .active-turn-id{
          grid: turnId;
        }
        .turn-error-msg{
          grid-area: turnError;
          display: flex;
          justify-content: space-between;
          span{
            color: #0080ff;
          }
          .PROCESSING, .FAILED, .failed{
            color: red;
          }
          .success, .SUCCESS, .finished, .FINISHED{
            color: green;
          }
        }
      }
      .dialogue-content-box{
        display: grid;
        grid-template-columns: 85px 22fr;
        grid-template-areas: 'title content';
        justify-content: center;
        align-content: center;
        .dialogue-title{
          grid-area: title;
          text-align: center;
          height: 40px;
          color: #000;
          font-weight: 800;
          line-height: 40px;
          background: #59658a;
          border-radius: 5px;
          padding: 0 15px;
          margin-right: 10px;
          opacity: 0.5;
        }
        .user-string-type {
          border-radius: 3px;
          display: grid;
          grid-template-columns: minmax(0,1fr) minmax(0,9fr);
          grid-template-rows: 1fr 10px 1fr;
          font-weight: 600;
          .standard-dialogue{
            grid-row-start: 1;
            grid-row-end: 2;
          }
          .paraphrasing-dialogue{
            grid-row-start: 3;
            grid-row-end: 4;
            position: relative;
            .voice-input-button-wrapper{
              position: absolute;
              height: 40px;
              width: 40px;
              top: 0;
              right: 0;
            }
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
          }
          .user-string-type-text {
            height: 40px;
            grid-column-start: 2;
            grid-column-end: -1;
            opacity: 0.5;
            p{
              cursor: text;
              box-sizing: border-box;
              padding: 0 15px;
              height: 40px;
              line-height: 40px;
              border: 1px solid #DCDFE6;
              font-size: 16px;
              border-left: none;
              white-space: nowrap;
              overflow-x: scroll;
              overflow-y: hidden;
              &::-webkit-scrollbar {
                display: none;
              }
            }
            input {
              color: #666;
              box-sizing: border-box;
              display: inline-block;
              height: 100%;
              width: 100%;
              justify-self: center;
              margin: 0;
              border-radius: 2px;
              outline: none;
              border: 1px solid #DCDFE6;
              padding: 0 40px 0 15px;
              border-left: none;
              font-size: 16px;
              font-weight: 600;
            }
          }
        }
      }
    }
    .user-string-type-active{
      border-left-color: #0080ff;
      .turn-header{
        opacity: 1;
      }
      .dialogue-content-box{
        .dialogue-title{
          opacity: 1;
        }
        .user-string-type{
          .user-string-type-name{
            opacity: 1;
          }
          .standard-dialog-text{
            opacity: 1;
          }
          .user-string-type-text{
            opacity: 1;
          }
        }
      }
    }
  }
}
</style>
