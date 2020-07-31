<template>
  <div id="classificationAnnotation">
    <div>
      <div class="classification-annotation">
        <div class="single-annotation-header"  @click="showSelectOption">
          <div class="sticky space collapsor"
          :style="{color: selectedIntend?'blue':''}">
            {{isDomain?"Domain":"General"}}({{selectedIntend}})
            <i class="el-icon-caret-bottom" v-if="showOption"></i>
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

        <!-- <div class="detail-info" v-if="showInfo">
          <hr>
          <div class="text-container">
              {{ classification.info }}
          </div>
          <hr>
        </div> -->

        <div class="checkbox-group" id="classification.name" v-if="showOption">
          <template v-if="isEmpty()">
            <div v-for="(labelName, index) in (isDomain?classification.domain[updataType]:classification.general[updataType])" class="checkbox-wrapper" :key="index"
              style="display: inline-block">
              <input type="checkbox"
                class="checkbox"
                :value="labelName"
                :id="labelName + updataType"
                :checked="checkedMethod(labelName)"
                @input="update_classification(labelName, updataType)">

              <label :for="labelName + updataType" class="classification-label">
                <span :class="{'bold-label': checkedMethod(labelName)}">{{labelName}}</span>
              </label>
            </div>
          </template>
          <p class="no-data" v-else>{{ $t('sysMgmt.tblNoData') }}</p>
        </div>

      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ClassificationAnnotation',
  data () {
    return {
      collapsed: false,
      showOption: true,
      showInfo: false,
      activeTurn: [],
      selectedIntend: 0,
    }
  },
  props: ["classification", "updataType", "currentTurn", "isDomain"],
  watch: {
    currentTurn: {
      handler: function(newVal, oldVal){
        this.activeTurn = newVal
        this.countMethod()
      },
      deep: true,
    }
  },
  methods:{
    isEmpty () {
      let len = 0
      if(this.isDomain){
        len = this.classification.domain[this.updataType].length
      }else{
        len = this.classification.general[this.updataType].length
      }
      return len
    },
    updataDialogue (turns) {
      this.$emit("update_classification", turns)
    },
    showSelectOption () {
      this.showOption = !this.showOption
    },
    showInfoTip (event) {
      event.stopPropagation()
      this.showInfo = !this.showInfo
    },
    update_classification (intentValue, type) {
      var intent
      if(this.isDomain){
        intent = this.activeTurn[type].domains
      }else{
        intent = this.activeTurn[type].general
      }

      if(intent.includes(intentValue)){
        let index = intent.indexOf(intentValue)
        intent.splice(index, 1)
      }else{
        intent.push(intentValue)
      }
      this.countMethod()
      this.updataDialogue(this.activeTurn)
    },
    checkedMethod (labelName, type){
      let flag = false
      var turn = this.currentTurn[this.updataType]
      if(this.isDomain){
        flag = turn.domains.includes(labelName)
      }else{
        flag = turn.general.includes(labelName)
      }
      return flag
    },
    countMethod (){
      let nLabel = 0;
      let turn = this.currentTurn[this.updataType]
      if(this.isDomain){
        nLabel = turn.domains.length
      }else{
        nLabel = turn.general.length
      }
      this.selectedIntend = nLabel;
    },
  },
  created () {
    this.activeTurn = this.currentTurn
    this.countMethod()
  }
}
</script>

<style lang="less" scope>
#classificationAnnotation {
  margin: 0 10px 15px;
  border-bottom: 1px solid #e1e1e3;
  padding-bottom: 15px;
  .classification-annotation{
    .no-data{
      font-size: 14px;
      text-align: center;
      color: #807c7c;
    }
    .single-annotation-header{
      margin-bottom: 10px;
      display: grid;
      grid-template: [row1-start] "info-header info-btn" [row1-end] / 1fr 1fr;
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
    .detail-info{
      margin: 5px 0;
      .text-container{
        padding: 10px;
      }
    }
    .checkbox-group{
      .checkbox-wrapper{
        margin-right: 10px;
        margin-bottom: 5px;
      }
      .checkbox{
        display: none;
      }
      .classification-label::before{
        content: '';
        display: block;
        width: 15px;
        height: 15px;
        border: 1px solid #e1e1e3;
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        background: #fff;
      }
      .classification-label{
        position: relative;
        padding-left: 22px;
        padding-right: 5px;
        font-size: 14px;
      }
      .checkbox:checked + .classification-label:after{
        transform: translateY(-50%) scale(1);
      }
      .classification-label::after{
        content: '';
        display: block;
        width: 7px;
        height: 7px;
        background: #259af7;
        position: absolute;
        left: 5px;
        top: 50%;
        transform: translateY(-50%) scale(0);
        transition: ease 175ms all;
        transform-origin: center center;
      }
    }
  }
}
</style>
