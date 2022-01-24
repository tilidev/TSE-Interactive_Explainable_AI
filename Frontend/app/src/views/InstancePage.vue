<template>
<div>
  <instance-view :instanceInfo="instanceInfo"></instance-view>
</div>
</template>

<script>
import InstanceView from "./InstanceView.vue";
export default {
  mounted() {
    this.sendInstanceRequest();
  },
  data() {
    return {
      id: this.$route.params.id,
      instanceInfo: {},
    };
  },
  components: { InstanceView },
  methods: {
    sendInstanceRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "instance/" + this.id).then((response) => {
        this.instanceInfo = response.data;
      });
    },
  },
  inject: ["apiUrl"],
};
</script>

<style>
</style>