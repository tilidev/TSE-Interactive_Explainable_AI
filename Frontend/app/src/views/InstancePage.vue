<template>
  <div>
    <div class="flex space-x-4 mb-4 -mt-4">
      <navigation-button :type="'dataset'"></navigation-button>
      <navigation-button :type="'admin'"></navigation-button>
    </div>
    <instance-view
      :allowMod="true"
      :allowWhatIf="true"
      expType="dice"
      :instanceInfo="instanceInfo"
    ></instance-view>
  </div>
</template>

<script>
import NavigationButton from "../components/buttons/NavigationButton.vue";
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
  components: { InstanceView, NavigationButton },
  methods: {
    backToDataset() {
      this.$router.push("/dataset");
    },
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