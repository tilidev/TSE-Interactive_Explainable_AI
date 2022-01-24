<template>
  <div>
    <div class="absolute inset-0 bg-background" v-if="!started">
      <default-button class="mt-8" @click="started = true">Start Experiment</default-button>
    </div>
    <div v-if="!done">
      <instance-view :instanceInfo="instanceInfo"></instance-view>
      <div class="text-right space-x-4 justify-end mx-8 flex">
        <default-button
          :color="'positive'"
          :hoverColor="'positive-dark'"
          @click="submitDecision(true)"
          >Approve</default-button
        >
        <default-button
          :color="'negative'"
          :hoverColor="'negative-dark'"
          @click="submitDecision(false)"
          >Reject</default-button
        >
      </div>
    </div>
    <div v-if="done">You're done</div>
  </div>
</template>

<script>
import DefaultButton from "../components/buttons/DefaultButton.vue";
import InstanceView from "./InstanceView.vue";
export default {
  mounted() {
    this.sendInstanceRequest();
  },
  data() {
    return {
      started: false,
      done: false,
      currentIndex: 0,
      instanceIds: [1, 2, 3, 10],
      results: {},
      instanceInfo: {},
    };
  },
  components: { InstanceView, DefaultButton },
  methods: {
    submitDecision(decision) {
      this.results[this.instanceIds[this.currentIndex]] = decision;
      this.currentIndex++;
      if (this.currentIndex < this.instanceIds.length) {
        this.sendInstanceRequest();
      } else {
        this.done = true;
      }
    },
    sendInstanceRequest() {
      const axios = require("axios");
      axios
        .get(this.apiUrl + "instance/" + this.instanceIds[this.currentIndex])
        .then((response) => {
          this.instanceInfo = response.data;
        });
    },
  },
  inject: ["apiUrl"],
};
</script>

<style>
</style>