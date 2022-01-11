<template>
  <div class="mx-8">
    <info-card
      :instanceInfo="instanceInfo"
      :attributeData="attributeData"
    ></info-card>
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
  inject: ["apiUrl", "attributeData"],
};
</script>

<style>
</style>