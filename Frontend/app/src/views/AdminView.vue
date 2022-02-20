<template>
  <div class="bg-white shadow-md px-8 py-4 text-left">
    <h2 class="font-bold text-xl">List of Experiments</h2>
    <h4 class="pb-4">Click on an experiment to see details</h4>
    <ul>
      <li
        class="text-primary-light font-bold mb-1 cursor-pointer"
        @click="showExistingOverlay = experiment"
        v-for="experiment in experimentList"
        :key="experiment"
      >
        {{ experiment }}
      </li>
    </ul>
    <default-button
      class="mt-6"
      :color="'positive'"
      :hoverColor="'positive-dark'"
      @click="showNewOverlay = true"
      >Create new experiment</default-button
    >
    <existing-experiment-overlay
      v-if="showExistingOverlay"
      @close="closeOverlay"
      :experimentName="showExistingOverlay"
    ></existing-experiment-overlay>
    <new-experiment-overlay
      v-if="showNewOverlay"
      :existingExperiments="experimentList"
      @close="closeOverlay"
    >
    </new-experiment-overlay>
  </div>
</template>

<script>
import ExistingExperimentOverlay from "../components/admin/ExistingExperimentOverlay.vue";
import NewExperimentOverlay from "../components/admin/NewExperimentOverlay.vue";
import DefaultButton from "../components/buttons/DefaultButton.vue";
export default {
  components: {
    DefaultButton,
    ExistingExperimentOverlay,
    NewExperimentOverlay,
  },
  mounted() {
    this.sendExperimentRequest();
  },
  data() {
    return {
      experimentList: [],
      showExistingOverlay: "",
      showNewOverlay: false,
    };
  },
  methods: {
    closeOverlay() {
      this.showExistingOverlay = "";
      this.showNewOverlay = false;
      this.sendExperimentRequest();
    },
    sendExperimentRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "experiment/all").then((response) => {
        console.log(response.data);
        this.experimentList = response.data;
      });
    },
  },
  inject: ["apiUrl"],
};
</script>

<style>
</style>