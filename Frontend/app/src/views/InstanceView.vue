<template>
  <div class="mx-8">
    <info-card
      :instanceInfo="instanceInfo"
      :modifiedInstance="modifiedInstance"
      :attributeData="attributeData"
      :modifiable="true"
      @apply-modification="applyModification"
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
      modifiedInstance: {},
      id: this.$route.params.id,
    };
  },
  components: { InfoCard },
  methods: {
    applyModification(modification) {
      this.modifiedInstance[modification["attribute"]] = modification["value"];
    },
    sendInstanceRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "instance/" + this.id).then((response) => {
        this.instanceInfo = response.data;
        this.modifiedInstance = Object.assign({}, response.data);
      });
    },
  },
  inject: ["apiUrl", "attributeData"],
};
</script>

<style>
</style>