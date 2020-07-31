<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data (){
    return {

    }
  },
  methods: {
    showMsg (){
      this.$alertMessage({
        title: "tip"
      })
    }
  },
  mounted (){
    window.addEventListener("beforeunload", () => {
      //保存stroe中的变量，防止刷新之后重置
      sessionStorage.setItem('alreadyVisited', JSON.stringify(this.$Store.state.alreadyVisited));
      sessionStorage.setItem('userInfo', JSON.stringify(this.$Store.state.userInfo));
    })
  },
  beforeDestroy () {

  }
}
</script>

<style lang="less" scope>
#app {
  .themeImage{
    height: 60px;
    img{
      height: 100%;
    }
  }
}
</style>
