<template>
  <div class="textSplitter">
    <div class="text-splitter-container">
      <div class="fname-info-container">
        <h2 class="fname-info" style="color:black">Source File: {{ sourceFname }}</h2>
      </div>

      <textarea class="text-editor"
        @input="log_change_occured($event)"
        v-model="text">
      </textarea>

      <div class="options-container">
        <h3 class="bold-text" style="color:black">对话分割器</h3>
        <hr>
        <span class="white-text" style="color:black">
          将每一轮对话使用空行分隔开。
          （In the pane, separate utterances so that there is a clear blank line
          between each utterance）.
          <br><br>
          如果存在多个对话，则用三个等号("===")加前后空行将不同对话分隔开。
          （If there are multiple dialogues, separate each one with a triple
          equals sign - "===" - with a blank line on either side.）
          <br><br>
          系统假设(This system assumes that):
          <ul>
            <li>所有对话有两个参与者：用户和系统(There are two participants in the dialogue, the "user" and the "system")</li>
            <li>用户总是第一个发言(The user always asks the first query)</li>
          </ul>
        </span>
      </div>

      <div class="text-buttons-container">
        <el-button @click="cancel_splitting($event)">返回</el-button>
        <el-button type="primary" @click="process_into_dialogue()">完成</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TtextSplitter',
  data () {
    return {
      inputChanged: false,
      sourceFname: "",
      text: 'UNINITIALIZED'
    }
  },
  beforeRouteEnter (to, from, next) {
    if(from.name !== "AllDialogues"){
      next("/home")
    }else{
      next()
    }
  },
  beforeRouteLeave (to, from, next) {
    if(this.inputChanged){
      this.$alertMessage({
        msg: this.$t('alert.lblReturnAbandonChange'),
        confirmCall: function(){
          next()
        },
      })
    }else{
      next()
    }
    this.$Store.commit("clearSourceFile")
  },
  methods: {
    read_text_file (file) {
      let reader = new FileReader();
      reader.onload = (event) => {
        this.text = reader.result
      };
      reader.readAsText(file);
    },
    log_change_occured (event) {
      this.inputChanged = true;
      // this.text = event.target.value
    },
    cancel_splitting (event) {
      this.$router.push({
        path: "/home/allDialogues"
      })
    },
    process_into_dialogue (event) {
      let dialoguesList = this.text.split('===');
      this.post_new_dialogues_from_string_lists_async(dialoguesList)
        .then( (response) => {
          this.inputChanged = false;
        });
    }
  },
  mounted () {
    var file = this.$Store.state.editSourceFile;
    this.sourceFname = file.name;
    this.read_text_file(file);
  },
}
</script>

<style scoped lang="less">
.textSplitter{
  display: grid;
  height: 100%;
  .text-splitter-container {
    overflow-y: scroll;
    display: grid;
    grid-template:
      [row1-start] ". info-bar . . ." 1fr [row1-end]
      [row2-start] ". text-edit . text-options ." 8fr [row2-end]
      [row3-start] ". text-buttons . . ." 50px [row3-end] / 1fr 8fr 1fr 4fr 1fr;
    .fname-info-container {
      font-size: 14px;
      grid-area: info-bar;
      display: flex;
      align-items: center;
    }
    .text-editor {
      grid-area: text-edit;
      display: block;
      font-family: CoreSansNR35Light;
      font-size: 16px;
      padding: 10px;
      resize: none;
      border: none;
    }
    .options-container {
      grid-area: text-options;
      font-size: 16px;
      hr{
        margin: 10px 0;
      }
      ul{
        padding-left: 40px;
        margin-top: 15px;
        li{
          list-style: disc;
        }
      }
    }
    .text-buttons-container {
      grid-area: text-buttons;
      display: flex;
      justify-content: center;
      align-items: center;
      .el-button {
        padding: 0 50px;
        height: 28px;
      }
    }
  }
}
</style>
