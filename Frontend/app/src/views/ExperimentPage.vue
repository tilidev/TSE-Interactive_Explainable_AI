<template>
  <div>
    <div class="absolute inset-0 bg-background" v-if="!started">
      <default-button class="mt-8" @click="started = true">Start Experiment</default-button>
    </div>
    <div v-if="!done && started">
      <!--
      Modification
      Remove navigation to previous loan application
      -->
      <!--
      <div v-if="currentIndex" class="flex space-x-2 mb-4 -mt-4 items-center cursor-pointer py-2" @click="goBack()">
        <fa-icon size="xl" icon="arrow-left"></fa-icon>
        <div>Back to previous loan application</div>
      </div>
      -->
      <instance-view v-if="started" :instanceInfo="instanceInfo" :expType="expType" :allowMod="allowMod"
        :allowWhatIf="allowWhatIf" :resetInstance="resetInstance"></instance-view>
      <div class="text-right flex justify-end mt-4">
        <span class="bg-white flex items-center space-x-4 p-4 shadow-md">
          <div class="text-lg font-bold mr-4">
            Would you approve this loan application?
          </div>
          <default-button :color="'positive-chart'" :hoverColor="'positive-chart-dark'" @click="submitDecision(true)">
            Approve</default-button>
          <default-button :color="'negative-chart'" :hoverColor="'negative-chart-dark'" @click="submitDecision(false)">
            Reject</default-button>
        </span>
      </div>
    </div>
    <div v-if="done">
      <div class="text-3xl font-bold py-2">You completed the experiment</div>
      <div v-if="!surveyLink" class="text-lg">Thank you for participating!</div>
      <a v-else :href="surveyLink" class="text-primary-light underline text-lg">Please click here to continue to the
        survey</a>
    </div>
  </div>
</template>

<script>
import DefaultButton from "../components/buttons/DefaultButton.vue";
import InstanceView from "../components/instance/InstanceView.vue";
export default {
  /**
   * Component for the experiment page that allows users to navigate through the given list of instances and approve/reject them.
   */
  mounted() {
    this.sendExperimentRequest();
  },
  data() {
    return {
      /**
       * Indicates if the user has started the experiment.
       */
      started: false,
      /**
       * The explanation type, can be 'lime', 'lime_orig', 'shap', 'shap_orig' or 'dice'
       */
      expType: String,
      /**
       * Indicates if the user is allowed to modify the instance
       */
      allowMod: false,
      /**
       * Indicates if the user is allowed to generate what-if analysis
       */
      allowWhatIf: false,
      /**
       * Indicates if the user is done with the experiment
       */
      done: false,
      /**
       * The current index in the list of instances
       */
      currentIndex: 0,
      /**
       * Array with all instance ids to be shown to the user
       */
      instanceIds: [],
      /**
       * Array with the decision the user has made for each instanc
       */
      results: [],
      /**
       * Object with instance information
       */
      instanceInfo: {},
      /**
       * Survey the experiment page will link to after the user has finished the experiment.
       */
      surveyLink: null,
      /**
       * Unique client id for the experiment participant
       */
      clientId: Number,
      /*
       * Modification
       * New Propops
       * Add prop to reset instance
      * */
      resetInstance: false,
    };
  },
  components: { InstanceView, DefaultButton },
  methods: {
    /**
     * Jumps back to the previous instance to allow the user to change their decision.
     */
    goBack() {
      this.results.pop();
      this.currentIndex--;
      this.sendInstanceRequest();
    },
    /**
     * Called when the user has completed the experiment.
     * Sends the recorded results to the API
     */
    postResults() {
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
    /**
     * Sends an API request to get the experiment information
     */
    sendExperimentRequest() {
      const axios = require("axios");
      axios
        .post(this.apiUrl + "experiment/generate_id", {
          experiment_name: this.$route.params.name,
        })
        .then((response) => {
          this.clientId = response.data.client_id;
        });
      axios
        .get(this.apiUrl + "experiment?name=" + this.$route.params.name)
        .then((response) => {
          this.instanceIds = response.data.loan_ids;
          this.expType = response.data.exp_type;
          this.allowMod = response.data.ismodify;
          this.allowWhatIf = response.data.iswhatif;
          this.surveyLink = response.data.survey_link;
        })
        .then(this.sendInstanceRequest);
    },
    /**
     * Called when the user clicks 'Approve' or 'Reject'.
     * Adds the user's decision on the current instance to the results and jumps to the next instance.
     * @param {String} decision - Can be 'approve' or 'reject'
     */
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
    /**
     * Sends an API request to get the instance information.
     */
    sendInstanceRequest() {
      const axios = require("axios");
      this.resetInstance = false;
      axios
        .get(this.apiUrl + "instance/" + this.instanceIds[this.currentIndex])
        .then((response) => {
          this.instanceInfo = response.data;
          this.resetInstance = true;
        });
    },
  },
  inject: ["apiUrl"],
};
</script>

<style>
</style>