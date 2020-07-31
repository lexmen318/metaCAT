<template>
  <div id="FileFormat" v-if="isShow">
    <transition name="modal">
      <div class="modal-mask">
        <div class="modal-wrapper">
          <div class="modal-container" :style="{width: (width + '%')}">

            <div class="modal-header">
              <slot name="header">
                对话文件格式(Dialogue File Format)
              </slot>
            </div>

            <hr>

            <div class="modal-body">
              <slot name="body">
                标注系统支持两种文件格式的上传：txt和JSON文件
                (Files can be uploaded to the annotation system in one of two
                formats: either as a raw .txt file or as a JSON file in the
                correct format).
                <br><br>
                如果上传txt文件，则没有格式的限制，但是你需要做进一步的预处理，才能将内容用于对话
                (If you upload a .txt file, there are no format restrictions and
                you will be taken to a screen to process it into a dialogue).
                <br><br>
                如果上传JSON文件，则必须遵循如下的格式要求
                (If you upload a JSON file, it must be in the correct format. This
                format is as follows):

                <ul>
                    <li>
                        文件第一层为以对话名字作为键值的字典
                        （File is a dict with keys as the names of each dialogue
                        and values as lists）.
                    </li>
                    <li>
                        每一个值(对话)是一个字典的列表，每一个字典包含了若干键值对，用来显示待标注的对话数据
                        (Each value is a list of dictionaries, where each
                        dictionary contains a number of key-value pairs which
                        are used to display the dialogue data for annotation.
                    </li>
                    <li>
                        部分键值对是必填的，以便于正确的显示对话
                        (Some key-value pairs are compulsory in order to correctly
                        display the dialogue).
                    </li>
                    <li>
                        必填的键值对可查看server/annotator_config.py文件中相关定义
                        (The key-value pairs which are compulsory are defined in
                        the annotator_config.py file in the "server" folder).
                    </li>
                    <li>
                        缺省情况下，每一轮中唯一必填的键值对是“用户”以及对应的用户输入信息
                        (By default, the only required key-value pair in each turn
                        is called "usr" and should be the user's query as
                        a string).
                    </li>
                </ul>

              </slot>
            </div>

            <hr>

            <div class="modal-footer">
              <slot name="footer">
                metaCAT
                <button class="modal-default-button" @click="closeMask">
                  OK
                </button>
              </slot>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'FileFormat',
  data (){
    return {

    }
  },
  props: {
    isShow:{
      default: false
    },
    width:{
      default: 60
    }
  },
  methods: {
    closeMask () {
      this.$emit('closeModal', false)
    }
  },
  mounted (){

  }
}
</script>

<style lang="less" scope>
#FileFormat {
  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .5);
    display: table;
    transition: opacity .3s ease;
    .modal-wrapper {
      display: table-cell;
      vertical-align: middle;
      .modal-container {
        margin: 0px auto;
        padding: 50px;
        background-color: #fff;
        border-radius: 2px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
        transition: all .3s ease;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 15px;
        hr {
          display: block;
          unicode-bidi: isolate;
          margin-block-start: 0.5em;
          margin-block-end: 0.5em;
          margin-inline-start: auto;
          margin-inline-end: auto;
          overflow: hidden;
          border-style: inset;
          border-width: 1px;
        }
        .modal-body {
          margin: 20px 0;
          ul{
            padding-left: 40px;
            li{
              padding: 5px;
              list-style: disc;
            }
          }
        }
        .modal-footer {
          font-style: italic;
          color: #777;
          .modal-default-button {
            float: right;
            border-style: hidden;
            border-radius: 1px;
            cursor: pointer;
            background-color: #ddd;
            padding: 3px 20px;
          }
        }
      }
    }
  }
}
</style>
