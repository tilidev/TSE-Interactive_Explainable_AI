<template>
  <div>
    <div class="absolute inset-0 bg-background" v-if="!started">
      <default-button class="mt-8" @click="started = true"
        >Start Experiment</default-button
      >
    </div>
    <div v-if="!done">
        <div v-if="currentIndex"
          class="flex space-x-2 mb-4 -mt-4 items-center cursor-pointer py-2"
          @click="goBack()"
        >
          <fa-icon size="xl" icon="arrow-left"></fa-icon>
          <div>Back to last loan application</div>
      </div>
      <instance-view
        :instanceInfo="instanceInfo"
        :expType="expType"
        :allowMod="allowMod"
        :allowWhatIf="allowWhatIf"
      ></instance-view>
      <div class="text-right flex justify-end">
        <span class="bg-white flex items-center space-x-4 p-4 shadow-md">
        <div class="text-lg font-bold mr-4">Do you approve this loan application?</div>
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
        </span>
      </div>
    </div>
    <div v-if="done">
      <div class="text-3xl font-bold py-2">You completed the experiment</div>
      <div v-if="!surveyLink" class="text-lg">Thank you for participating!</div>
      <a v-else :href="surveyLink" class="text-primary-light underline text-lg"
        >Please click here to continue to the survey</a
      >
    </div>
  </div>
</template>

<script>
import DefaultButton from "../components/buttons/DefaultButton.vue";
import InstanceView from "./InstanceView.vue";
export default {
  mounted() {
    this.sendExperimentRequest();
  },
  data() {
    return {
      started: false,
      expType: String,
      allowMod: false,
      allowWhatIf: false,
      done: false,
      currentIndex: 0,
      instanceIds: [],
      results: [],
      instanceInfo: {},
      surveyLink: null,
      clientId: Number,
    };
  },
  components: { InstanceView, DefaultButton },
  methods: {
    goBack() {
      this.results.pop();
      this.currentIndex--;
      this.sendInstanceRequest();
    },
    postResults() {
      console.log(this.results);
      const axios = require("axios");
      let reqBody = {
        experiment_name: this.$route.params.name,
        client_id: this.clientId,
        results: this.results,
      };
      axios
        .post(this.apiUrl + "experiment/results", reqBody)
        .then(() => (this.done = true));
    },
    sendExperimentRequest() {
      const axios = require("axios");
      axios
        .post(this.apiUrl + "experiment/generate_id", {
          experiment_name: this.$route.params.name,
        })
        .then((response) => {
          this.clientId = response.data.client_id;
          console.log(this.clientId);
        });
      axios
        .get(this.apiUrl + "experiment?name=" + this.$route.params.name)
        .then((response) => {
          this.instanceIds = response.data.loan_ids;
          this.expType = response.data.exp_type;
          this.allowMod = response.data.ismodify;
          this.allowWhatIf = response.data.isWhatIf;
          this.surveyLink = response.data.survey_link;
        })
        .then(this.sendInstanceRequest);
    },
    submitDecision(decision) {
      this.results.push({
        loan_id: this.instanceIds[this.currentIndex],
        choice: decision ? "approve" : "reject",
      });
      this.currentIndex++;
      if (this.currentIndex < this.instanceIds.length) {
        this.sendInstanceRequest();
      } else {
        this.postResults();
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