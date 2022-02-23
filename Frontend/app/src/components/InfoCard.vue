<template>
  <div class="bg-white shadow-md px-8 py-4 text-left">
    <h2 class="font-bold text-lg pb-4">Current Loan Application</h2>
    <div class="flex text-sm justify-between">
      <div
        class="grid grid-cols-auto grid-flow-col gap-x-6"
        v-for="category in Object.keys(attributeCategories)"
        :key="category"
      >
        <div class="col-span-2 col-start-1 text-lg capitalize">
          {{ category }}
        </div>
        <div
          class="col-start-1 text-primary-light font-bold"
          v-for="attribute in attributeCategories[category]"
          :key="attribute"
        >
          {{ attributeData.labels[attribute] }}:
        </div>
        <div
          class="col-start-2 capitalize"
          v-for="attribute in attributeCategories[category]"
          :key="attribute"
        >
          <span :class="getValueStyling(attribute)">
            {{ modifiedInstance[attribute] }}
          </span>
          <fa-icon
            v-if="modificationEnabled && dropdownAttribute != attribute"
            class="ml-2 cursor-pointer"
            icon="caret-down"
            @click="dropdownAttribute = attribute"
          />
          <fa-icon
            v-if="modificationEnabled && dropdownAttribute == attribute"
            class="ml-2 cursor-pointer"
            icon="caret-up"
            @click="dropdownAttribute = ''"
          />
          <dropdown-menu
            class="absolute mt-1"
            v-if="attribute == dropdownAttribute"
            :originalValue="instanceInfo[attribute]"
            :selectedValue="modifiedInstance[attribute]"
            :attribute="attribute"
            @apply-value="applyValue"
            @cancel="dropdownAttribute = ''"
          ></dropdown-menu>
        </div>
      </div>
      <div class="flex flex-col justify-between">
        <div class="flex flex-col space-y-4">
          <div class="text-lg">AI Recommendation</div>
          <div class="flex space-x-4">
            <recommendation-vis
              class=""
              :recommendation="instanceInfo.NN_recommendation"
            />
            <confidence-vis
              class=""
              :confidence="instanceInfo.NN_confidence"
              :explicit="true"
            />
          </div>
        </div>
        <div class="flex flex-col space-y-4" v-if="newPrediction != null">
          <div class="text-lg">New Recommendation</div>
          <div class="flex space-x-4">
            <recommendation-vis
              class=""
              :recommendation="newPrediction.NN_recommendation"
            />
            <confidence-vis
              class=""
              :confidence="newPrediction.NN_confidence"
              :explicit="true"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="flex">
      <default-button
        class="col-start-1 mt-4"
        @click="modificationEnabled = true"
        v-if="modifiable && !modificationEnabled"
        >Modify</default-button
      >
      <default-button
        class="col-start-1 mt-4"
        @click="console.log('Generate Explanation')"
        v-if="modificationEnabled"
        >Generate Explanation</default-button
      >
      <clear-button
        class="col-start-2 mt-4 ml-4"
        @click="resetInstance()"
        v-if="modificationEnabled"
        >Reset</clear-button
      >
    </div>
  </div>
</template>

<script>
import DefaultButton from "./buttons/DefaultButton.vue";
import ConfidenceVis from "./ui/ConfidenceVis.vue";
import DropdownMenu from "./ui/DropdownMenu.vue";
import RecommendationVis from "./ui/RecommendationVis.vue";
import ClearButton from "./buttons/ClearButton.vue";

export default {
  data() {
    return {
      dropdownAttribute: "",
      modificationEnabled: false,
      newPrediction: null,
    };
  },
  components: {
    RecommendationVis,
    ConfidenceVis,
    DefaultButton,
    DropdownMenu,
    ClearButton,
  },
  props: {
    instanceInfo: Object,
    attributeData: Object,
    modifiable: Boolean,
    modifiedInstance: Object,
  },
  methods: {
    sendPredictionRequest() {
      // eslint-disable-next-line no-unused-vars
      const { id, NN_recommendation, NN_confidence, ...reducedInstance } =
        this.modifiedInstance;
      const axios = require("axios");
      axios
        .post(this.apiUrl + "instance/predict", reducedInstance)
        .then((response) => {
          this.newPrediction = response.data;
        });
    },
    resetInstance() {
      this.modificationEnabled = false;
      this.newPrediction = null;
      this.$emit("reset-instance");
    },
    getValueStyling(attribute) {
      if (this.instanceInfo[attribute] != this.modifiedInstance[attribute]) {
        return "text-modified font-bold";
      }
      return "";
    },
    applyValue(value) {
      const modification = { attribute: this.dropdownAttribute, value: value };
      this.dropdownAttribute = "";
      this.$emit("apply-modification", modification);
      this.sendPredictionRequest();
    },
  },
  inject: ["attributeCategories", "apiUrl"],
};
</script>

<style>
</style>