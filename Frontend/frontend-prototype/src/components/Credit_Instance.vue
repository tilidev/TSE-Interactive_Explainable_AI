<template>
  <div>

  </div>
</template>

<script>
import Vue from 'vue';
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios,axios)

export default {
    name: "Credit_Instance"

    mounted(){
      Vue.axios.get()
    }
}
</script>

<style>

</style>