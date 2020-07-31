<template>
  <div id="classificationStringAnnotation" v-if="classString[updataType].domains.length > 0">
    <div  v-for="(slotItem, slotKey, index) of classString[updataType].slots" :key="index">
      <template v-if="classString[updataType].domains.includes(slotKey)">
        <div class="classification-annotation">
          <div class="single-annotation-header" @click="showSelectOption(slotKey)">
            <div class="sticky space collapsor"
            :style="{color: countMethod(slotItem)?'blue':''}">
              {{slotKey}}({{countMethod(slotItem)}})
              <i class="el-icon-caret-bottom" v-if="showOption.includes(slotKey)"></i>
              <i class="el-icon-caret-right" v-else></i>
            </div>

            <!-- <div class="info-button-container">
              <el-tooltip class="item" effect="light" content="点击了解详细信息和标注指引" placement="top-start">
                <div @click="showInfoTip($event)" class="info-detail">
                  <i class="el-icon-question"></i>
                </div>
              </el-tooltip>
            </div> -->
          </div>

          <!-- <div v-if="showInfo">
            <hr>
            <div class="text-container">
                {{ classString.info }}
            </div>
            <hr>
          </div> -->
          <template v-if="showOption.includes(slotKey)">
            <div class="action-operation">
              <label>Intent</label>
              <el-select v-model="operation[slotKey]">
                <el-option
                  v-for="item in actionCodeOperation[slotKey]"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </div>
            <div v-for="(item,index) in slotItem"  class="multilabel-string-item-wrapper" :key="index">
              <div class="multilabel-string-checkbox-container">
                <input type="checkbox"
                  class="multilabel-string-checkbox"
                  :id="item.slot_name"
                  :value="item.slot_name"
                  :checked="checkedMethod(item)"
                  disabled />
                <label :for="item.slot_name" class="multilabel-string-label">
                  <span> {{item.slot_name}}</span>
                </label>
                <div class="add-slot-btn-container">
                  <span @click="addSlotInput(item)" class="el-icon-plus"></span>
                </div>
              </div>

              <div v-for="(slotValue, index) in item.slot_items" :key="index"
              class="multilabel-string-slot-value">
                <el-autocomplete
                  v-if="item.slot_type === 'string'"
                  :clearable="true"
                  :maxlength="0"
                  class="multilabel-string-label-value"
                  v-model="slotValue.slot_value"
                  :fetch-suggestions="(a,b)=>{querySearch(a,b,item)}"
                  :placeholder="$t('annotatingFunction.detail.placeholderSlotValue')"
                  @keydown.native="disableDel($event)"
                  @clear="clearSlotValue(slotValue)"
                  @select="selectSlotValue(slotValue, slotKey)"
                  @drop.native="treat_drop($event, slotValue, slotKey)"
                ></el-autocomplete>
                <el-select
                  v-if="item.slot_type === 'enumeration'"
                  :clearable="true"
                  @change="selectEnumeration(slotValue, slotKey)"
                  v-model="slotValue.slot_value" 
									:placeholder="$t('annotatingFunction.detail.placeholderSlotValue')" >
                  <el-option
                    v-for="en in item.slot_value"
                    :key="en"
                    :label="en"
                    :value="en">
                  </el-option>
                </el-select>
                <el-input class="multilabel-string-label-position" 
									:placeholder="$t('annotatingFunction.detail.placeholderSlotPosition')"
                  :maxlength="0"
                  v-model="slotValue.slot_span"
                  :clearable="true"
                  @clear="updataDialogue"
                  @keydown.native="disableDel($event)"
                  @drop.native="disable_drop($event)">
                </el-input>
                <el-autocomplete
                  class="multilabel-string-action-code"
                  :clearable="true"
                  v-model="slotValue.slot_intent"
                  :maxlength="0"
                  :fetch-suggestions="(a,b)=>{queryOptionCode(a,b,item,slotKey)}"
                  :placeholder="$t('annotatingFunction.detail.placeholderSlotIntent')"
                  @clear="updataDialogue"
                  @select="updataDialogue"
                  @keydown.native="disableDel($event)"
                ></el-autocomplete>
                <span class="delete-slots" v-if="index != 0"
                @click="delSlotInput(item, index)"><i class="el-icon-delete"></i></span>
              </div>

            </div>
          </template>
        </div>
      </template>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ClassificationStringAnnotation',
  data () {
    return {
      annotationSlots: {},
      text: '',
      collapsed: true,
      showOption: [],
      showInfo: false,
      operation: {},
    }
  },
  props: ["classString", "confidences", "currentId", "updataType", "responseType", "actionCodeOperation"], //"operation"
  watch: {
    classString:{
      handler: function(newVal, oldVal){
        this.annotationSlots = newVal
      },
      deep: true,
    },
  },
  methods: {
    disableDel (event) {
      if(event.keyCode === 8 || event.keyCode === 46){
        event.preventDefault()
      }
    },
    selectEnumeration (slot, key) {
      if(slot.slot_value){
        slot.slot_intent = this.operation[key]
      }else{
        slot.slot_intent = ""
      }
      this.updataDialogue()
    },
    updataDialogue () {
      this.$emit("update_classification_string", this.annotationSlots)
    },
    queryOptionCode (queryString, cb, item, slotName) {
      let data =[]
      this.actionCodeOperation[slotName].forEach(i => {
        data.push({
          value: i
        })
      })
      cb(data)
    },
    selectSlotValue (slot) {
      slot.slot_span = ""
      this.updataDialogue()
    },
    querySearch (queryString, cb, item) {
      let data =[]
      item.slot_value.forEach(i => {
        data.push({
          value: i
        })
      })
      cb(data)
    },
    addSlotInput (item) {
      item.slot_items.push({
        slot_span: "",
        slot_value: "",
        slot_intent: ""
      })
      this.updataDialogue()
    },
    delSlotInput (item, index) {
      item.slot_items.splice(index, 1)
      this.updataDialogue()
    },
    showSelectOption (name) {
      if(!this.showOption.includes(name)){
        this.showOption.push(name)
      }else{
        let index = this.showOption.indexOf(name)
        this.showOption.splice(index, 1)
      }
    },
    showInfoTip (event) {
      event.stopPropagation()
      this.showInfo = !this.showInfo
    },
    checkedMethod (slotItem) {
      let flag
      slotItem.slot_items.forEach(item => {
        if(item.slot_value){
          flag = true
          return
        }else{
          flag = false
        }
      })
      return flag;
    },
    countMethod (allLabels) {
      let nLabel = 0;
      allLabels.forEach(item => {
        if(this.checkedMethod(item)){
          nLabel++
        }
      })
      return nLabel;
    },
    clearSlotValue (value) {
      for(let key in value){
        value[key] = ""
      }
      this.updataDialogue()
    },
    treat_drop (event, slotVal, key) {
      event.preventDefault();
      let drag_item = event.dataTransfer.getData("Text");
      if (!drag_item)
        return false;

      drag_item = drag_item.split('@');
      let drag_name = drag_item[0];
      if(drag_name != this.updataType){
        return
      }

      if(!slotVal.slot_intent){
        slotVal.slot_intent = this.operation[key]
      }

      let drag_text = drag_item[1];
      let drag_span = drag_item[2];
      slotVal.slot_value = drag_text
      slotVal.slot_span = drag_span
      this.updataDialogue()
    },
    disable_drop (event) {
      event.preventDefault();
      return false;
    },
    setDefaultValue (list) {
      Object.keys(list).forEach(item => {
        this.$set(this.operation, item, list[item][0])
      })
    },
  },
  created() {
    this.annotationSlots = this.classString
    this.setDefaultValue(this.actionCodeOperation)
  }
}
</script>

<style lang="less" scope>
#classificationStringAnnotation {
  margin: 0 10px 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e1e1e3;
  /deep/.el-input__inner{
    height: 28px
  }
  /deep/.el-input__icon{
    line-height: 28px;
  }
  .el-icon-circle-close{
    line-height: 30px;
    font-size: 15px;
  }
  .single-annotation-header{
    margin-bottom: 10px;
    display: grid;
    grid-template: [row1-start] "info-header info-btn" [row1-end] / 1fr 0.5fr;
    grid-template-rows: 1fr;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    .sticky{
      grid-area: info-header;
      display: flex;
      align-items: center;
      i{
        font-size: 20px;
        margin-top: 2px;
      }
    }
    .info-button-container{
      grid-area: info-btn;
      display: grid;
      justify-items: flex-end;
      .info-detail{
        font-size: 17px;
        width: 25px;
        cursor: pointer;
        color: #afa7a7;
        text-align: center;
      }
      .info-button{
          width: 50px;
          height: 20px;
        }
    }
  }
  .action-operation{
    margin-bottom: 10px;
  }
  .text-container{
    padding: 10px;
  }
  .multilabel-string-item-wrapper{
    .multilabel-string-checkbox-container{
      display: grid;
      grid-template:
        [row1-start] "checkboxZone labelZone addSlot" 1fr [row1-end] / 0.5fr 3fr 3fr;
      margin-bottom: 10px;
      .multilabel-string-checkbox{
        grid-area: checkboxZone;
      }
      .multilabel-string-label{
        grid-area: labelZone;
      }
      .add-slot-btn-container{
        grid-area: addSlot;
        display:flex;
        justify-content: flex-end;
        padding-right: 20px;
        span{
          display: inline-block;
          padding: 5px 10px;
          cursor: pointer;
        }
      }
      .multilabel-string-action-code{
        grid-area: actionCode;
      }
    }
    .multilabel-string-slot-value{
      display: grid;
      grid-template:
        [row3-start] "labelValue . labelPosition . actionCode delSlot" 1fr [row3-end] / 2fr 5px 1.5fr 5px 2fr 20px;
      align-items: center;
      margin-bottom: 10px;
      .multilabel-string-label-value{
        grid-area: labelValue;
      }
      .multilabel-string-label-position{
        grid-area: labelPosition;
      }
      .multilabel-string-action-code{
        grid-area: actionCode;
      }
      .delete-slots{
        grid-area: delSlot;
        color:#dd6161;
        padding-left: 5px;
        cursor: pointer;
        &:hover{
          opacity: 0.8;
        }
      }
    }
  }
}
</style>
