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
      <div class="relative mx-auto w-auto max-w-2xl">
        <div class="bg-white w-100 rounded-lg shadow-md p-4">
          <div class="flex mb-8 justify-between">
            <h4 class="text-lg font-bold">
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
              gap-x-8 gap-y-2
              auto-cols-max auto-rows-auto
            "
          >
            <div class="col-start-1 col-span-2 ">Description</div>
            <div class="col-start-3 col-span-3">{{experimentData.description}}</div>
            <div class="col-start-1 col-span-2 ">Applications the user is shown</div>
            <div class="col-start-3 col-span-3">{{experimentData.loan_ids}}</div>
            <div class="col-start-1 col-span-2 ">Modification enabled</div>
            <div class="col-start-3 col-span-3 capitalize">{{experimentData.ismodify}}</div>
            <div class="col-start-1 col-span-2 ">What-if analysis enabled</div>
            <div class="col-start-3 col-span-3 capitalize">{{experimentData.iswhatif}}</div>
            <div class="col-start-1 col-span-2 " v-if="experimentData.survey_link">Survey link</div>
            <a class="col-start-3 col-span-3" :href="experimentData.survey_link" v-if="experimentData.survey_link"></a>
            <div class="col-start-1 col-span-2 ">Experiment link</div>
            <a class="col-start-3 col-span-3 text-primary-light" :href="experimentLink">{{experimentLink}}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    this.sendExperimentRequest();
  },
  data() {
    return {
      experimentData: {},
    }
  },
  computed: {
    experimentLink() {
      return window.location.href.replace("admin", "") + "experiments/" + this.experimentName;
    }
  },
  methods: {
    sendExperimentRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "experiment?name=" + this.experimentName).then((response) => {
        this.experimentData = response.data;
        console.log(this.experimentData);

      });
    },
  },
  props: {
    experimentName: String,
  },
  inject: ["apiUrl"]
};
</script>

<style>
</style>