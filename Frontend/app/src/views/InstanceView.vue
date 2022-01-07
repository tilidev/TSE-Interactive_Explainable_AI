<template>
  <div>
    <info-card :instanceInfo="instanceInfo"></info-card>
  </div>
</template>

<script>
import InfoCard from "../components/InfoCard.vue";

export default {
  mounted() {
    this.sendInstanceRequest();
  },
  data() {
    return {
      instanceInfo: {},
      id: this.$route.params.id,
      apiUrl: "http://localhost:8000/",
    };
  },
  components: { InfoCard },
  methods: {
    sendInstanceRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "instance/" + this.id).then((response) => {
        this.instanceInfo = response.data;
      });
    },
  },
};
</script>

<style>
</style>