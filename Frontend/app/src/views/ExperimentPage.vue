<template>
  <div>
    <div class="absolute inset-0 bg-background" v-if="!started">
      <default-button class="mt-8" @click="started = true"
        >Start Experiment</default-button
      >
    </div>
    <div v-if="!done">
      <instance-view
        :instanceInfo="instanceInfo"
        :expType="expType"
        :allowMod="allowMod"
        :allowWhatIf="allowWhatIf"
      ></instance-view>
      <div class="text-right space-x-4 justify-end flex">
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
    <div v-if="done">
      <div class="text-3xl font-bold py-2">You're done!</div>
      <div v-if="!surveyLink" class="text-lg">
        Thank you for participating in our experiment
      </div>
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
      done: true,
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