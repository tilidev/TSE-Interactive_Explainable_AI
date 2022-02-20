<template>
  <div>
    <div class="absolute inset-0 z-40 opacity-25 bg-black"></div>
    <div
      class="
        fixed
        overflow-y-auto
        inset-0
        flex
        justify-center
        items-center
        z-50
      "
    >
      <div class="relative mx-auto w-auto">
        <div class="bg-white w-100 rounded-lg shadow-md p-4">
          <div class="flex mb-8 justify-between">
            <h4 class="text-xl font-bold">
              {{ experimentName }}
            </h4>
            <button
              @click="this.$emit('close')"
              class="bg-white hover:bg-gray-light px-2 py-0.5 rounded-full"
            >
              <fa-icon icon="times"></fa-icon>
            </button>
          </div>
          <div
            class="
              grid grid-cols-auto grid-flow-col
              gap-x-8 gap-y-8
              auto-cols-max auto-rows-auto
            "
          >
            <div class="col-start-1 col-span-2 font-bold">Description</div>
            <div class="col-start-3 col-span-3">
              {{ experimentData.description }}
            </div>
            <div class="col-start-1 col-span-2 font-bold">
              Applications the user is shown
            </div>
            <div class="col-start-3 col-span-3">
              {{ experimentData.loan_ids }}
            </div>
            <div class="col-start-1 col-span-2 font-bold">
              Modification enabled
            </div>
            <div class="col-start-3 col-span-3 capitalize">
              {{ experimentData.ismodify }}
            </div>
            <div class="col-start-1 col-span-2 font-bold">
              What-if analysis enabled
            </div>
            <div class="col-start-3 col-span-3 capitalize">
              {{ experimentData.iswhatif }}
            </div>
            <div
              class="col-start-1 col-span-2 font-bold"
              v-if="experimentData.survey_link"
            >
              Survey link
            </div>
            <a
              class="col-start-3 col-span-3 text-primary-light underline"
              :href="experimentData.survey_link"
              v-if="experimentData.survey_link"
            ></a>
            <div class="col-start-1 col-span-2 font-bold">Experiment link</div>
            <a
              class="col-start-3 col-span-3 text-primary-light underline"
              :href="experimentLink"
              >{{ experimentLink }}</a
            >
            <default-button class="col-start-1 col-span-2"
              >Download results (CSV)</default-button
            >
            <default-button class="col-start-3 col-span-1"
              >Download results (JSON)</default-button
            >
            <default-button
              @click="resetExperiment()"
              :color="'positive'"
              :hoverColor="'positive-dark'"
              class="col-start-4"
              ><fa-icon icon="undo"></fa-icon
            ></default-button>
            <default-button
              @click="deleteExperiment()"
              :color="'negative'"
              :hoverColor="'negative-dark'"
              class="col-start-5"
              ><fa-icon icon="trash"></fa-icon
            ></default-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DefaultButton from "../buttons/DefaultButton.vue";
export default {
  components: { DefaultButton },
  mounted() {
    this.sendExperimentRequest();
  },
  data() {
    return {
      experimentData: {},
    };
  },
  computed: {
    experimentLink() {
      return (
        window.location.href.replace("admin", "") +
        "experiments/" +
        this.experimentName
      );
    },
  },
  methods: {
    resetExperiment() {
      if (
        confirm(
          "This will reset the experiment and permanently delete all recorded answers. \n\nThis action can not be undone. \n\nAre you sure you wish to proceed?"
        )
      ) {
        const axios = require("axios");
        axios.post(
          this.apiUrl +
            "experiment/reset?experiment_name=" +
            this.experimentName
        );
        this.sendExperimentRequest();
      }
    },
    deleteExperiment() {
      if (
        confirm(
          "This will permanently delete the experiment and all recorded answers. \n\nThis action can not be undone. \n\nAre you sure you wish to proceed?"
        )
      ) {
        const axios = require("axios");
        axios.post(
          this.apiUrl +
            "experiment/delete?experiment_name=" +
            this.experimentName
        );
        this.$emit("close");
      }
    },
    sendExperimentRequest() {
      const axios = require("axios");
      axios
        .get(this.apiUrl + "experiment?name=" + this.experimentName)
        .then((response) => {
          this.experimentData = response.data;
          console.log(this.experimentData);
        });
    },
  },
  props: {
    experimentName: String,
  },
  inject: ["apiUrl"],
};
</script>

<style>
</style>