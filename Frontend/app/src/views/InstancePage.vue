<template>
  <div>
    <div class="flex space-x-4 mb-4 -mt-4">
      <navigation-button :type="'dataset'"></navigation-button>
      <navigation-button :type="'admin'"></navigation-button>
    </div>
    <instance-view
      :allowMod="true"
      :allowWhatIf="true"
      :expType="expType"
      @switch="switchExp"
      :allowSwitching="true"
      :instanceInfo="instanceInfo"
    ></instance-view>
  </div>
</template>

<script>
import NavigationButton from "../components/buttons/NavigationButton.vue";
import InstanceView from "../components/instance/InstanceView.vue";
export default {
  mounted() {
    this.sendInstanceRequest();
  },
  data() {
    return {
      id: this.$route.params.id,
      instanceInfo: {},
      expType: "dice",
    };
  },
  components: { InstanceView, NavigationButton },
  methods: {
    switchExp(expType) {
      this.expType = expType;
    },
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