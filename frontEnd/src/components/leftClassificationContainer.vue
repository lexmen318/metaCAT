<template>
  <div class="leftContainer">
    <ClassificationAnnotation
      :classification="metadatas"
      :currentTurn="currentTurn"
      :updataType="'usr'"
      @update_classification="turn_update">
    </ClassificationAnnotation>
    <ClassificationAnnotation
      :classification="metadatas"
      :currentTurn="currentTurn"
      :isDomain="true"
      :updataType="'usr'"
      @update_classification="turn_update">
    </ClassificationAnnotation>
    <ClassificationStringAnnotation
      :classString="currentTurn"
      :actionCodeOperation="actionCodeOperation"
      :updataType="'usr'"
      @update_classification_string="turn_update">
    </ClassificationStringAnnotation>
  </div>
</template>

<script>
import ClassificationAnnotation from './classificationAnnotation'
import ClassificationStringAnnotation from './classificationStringAnnotation'

export default {
  name: 'LeftContainer',
  components: {
    ClassificationAnnotation,
    ClassificationStringAnnotation
  },
  props: ["metadatas", "currentTurn", "actionCodeOperation"],
  data () {
    return {

    }
  },
  methods: {
    turn_update (data) {
      this.$emit("update_classification", data)
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.leftContainer{

}
</style>
