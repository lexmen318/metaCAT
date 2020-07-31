<template>
  <div class="annotatingBatchList">
    <ul class="batchItem-list">
      <el-row :gutter="15" justify="center">
        <el-col :span="8" v-for="(batchItem, index) in allBatch" :key="index">
          <li class="batch-list-item">
            <div class="dialogue-id" @click="gotoAllDialogs(batchItem.batch_id)">{{batchItem.batch_id}}</div>
            <div class="metadata_name" >[{{batchItem.metadata_name}}]</div>
            <div class="annotation-progress">
							<div class="progress" :style="{width: batchItem.batch_progress}"></div>
              <p class="progress-text">{{batchItem.batch_progress}}</p>
            </div>
            <div class="batch-description">
              <template>
                <p class="description-text" @click="editDescriptionTextarea($event)" v-if="isShowAddDescription(batchItem.batch_description)">
                  {{batchItem.batch_description}}</p>
                <p class="add-description" @click="addDescription($event)" v-else>{{ $t('annotatingFunction.batch.lblChangeDescription') }}</p>
                <el-input
                  @blur="showDescription($event,batchItem.batch_id)"
                  @change="updataDescription(batchItem.batch_id, batchItem.batch_description)"
                  class="description-textarea"
                  type="textarea"
                  :rows="3"
                  :placeholder="$t('annotatingFunction.batch.lblChangeDescription')"
                  v-model="batchItem.batch_description">
                </el-input>
              </template>
            </div>
          </li>
        </el-col>
      </el-row>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'AnnotatingBatchList',
  data () {
    return {
      allBatch: [],
      textarea: "",
    }
  },
  methods: {
    isShowAddDescription (value){
      var flag = false
      if(value === "" || !value){
        flag = false
      }else{
        flag = true
      }
      return flag
    },
    editDescriptionTextarea (event){
      var target = event.target;
      target.style.display = "none"
      target.nextElementSibling.style.display = "block"
      target.nextElementSibling.firstElementChild.focus()
    },
    showDescription (event, batchId){
      var parentEl = event.currentTarget.parentElement;
      parentEl.previousElementSibling.style.display = "inline-block"
      parentEl.style.display = "none"

    },
    addDescription (event){
      event.target.nextElementSibling.style.display = "block"
      event.target.nextElementSibling.firstElementChild.focus()
      event.target.style.display = "none"
    },
    updataDescription (batchId, batchDesc){
      this.batch_description_post(batchId, batchDesc, "annotating")
      .then(res => {
        // if(res.data.code == 200){
        //   this.$alertMessage({
        //     msg: res.data.msg
        //   })
        // }
      })
    },
		gotoAllDialogs(batchId){
			this.$router.push({
				path:'/home/annotatingDialogueList',
				query: {
					batchId: batchId
				}
			})
		}
  },
  created (){
    this.$Store.state.alreadyVisited = []
    this.batch_list_by_category("annotating")
      .then(res=>{
        this.allBatch = res.data
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.annotatingBatchList{
  overflow: auto;
  height: 100%;
  .batchItem-list{
    padding: 20px 150px;
    .batch-list-item{
      overflow: hidden;
      display: grid;
      grid-template:
          [row-start] "batchId ." 1.5fr [row-end]
          [row-start] "metadataName ." 1.5fr [row-end]
          [row-start] "progress ." 1fr  [row-end]
          [row-start] "decription ." 3fr[row-end] / 21fr 3fr;
      height: 150px;
      padding-left: 15px;
      margin-bottom: 15px;
      background-color: #fff;
      border: 1px solid #e4e4ec;
      box-shadow: 1px 3px 4px rgba(0, 0, 0, 0.08);
      .dialogue-id{
        grid-area: batchId;
        align-self: center;
        cursor: pointer;
        color: #0080ff;
          }
      .metadata_name{
        grid-area: metadataName;
        align-self: center;
        font-weight: bold;
      }
      .annotation-progress{
        grid-area: progress;
        width: 60%;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        .progress{
          height: 10px;
          width: 80%;
          border-radius: 5px;
          background-color: #0080ff;
        }
        .progress-text{
          margin-left: 10px;
        }
      }
      .batch-description{
        grid-area: decription;
        width: 100%;
        .description-text{
          width: 100%;
          word-break: break-all;
          font-size: 14px;
          color: #231f1f;
          cursor: pointer;
        }
        .description-textarea{
          display: none;
        }
        .add-description:hover{
          opacity: 0.8;
        }
        .add-description{
          display: inline-block;
          cursor: pointer;
          color: #0080ff;
          font-size: 14px;
        }
      }
    }
  }
}
</style>
