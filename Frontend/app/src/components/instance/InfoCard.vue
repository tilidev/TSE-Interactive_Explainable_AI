<template>
  <div class="bg-white shadow-md px-8 py-4 text-left">
    <h2 class="font-bold text-lg pb-4">Current Loan Application</h2>
    <div class="flex text-sm justify-between">
      <div
        class="grid grid-cols-auto grid-flow-col gap-x-6 grid-rows-8"
        v-for="category in Object.keys(reducedCategories)"
        :key="category"
      >
        <div class="col-span-2 col-start-1 text-lg capitalize -mt-2 mb-1">
          {{ category }}
        </div>
        <div
          class="col-start-1 text-primary-light font-bold"
          v-for="attribute in reducedCategories[category]"
          :key="attribute"
        >
          {{ attributeData.labels[attribute] }}:
        </div>
        <div
          class="col-start-2 capitalize"
          v-for="attribute in reducedCategories[category]"
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
      <div class="flex flex-col justify-start space-y-12">
        <div class="flex flex-col space-y-4 -mt-2">
          <div class="text-lg">
            <span
              v-if="
                newPrediction != null &&
                JSON.stringify(instanceInfo) != JSON.stringify(modifiedInstance)
              "
            >
              Original
            </span>
            AI Recommendation
          </div>
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
        <div
          class="flex flex-col space-y-4"
          v-if="
            newPrediction != null &&
            JSON.stringify(instanceInfo) != JSON.stringify(modifiedInstance)
          "
        >
          <div class="text-lg">New AI Recommendation</div>
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
        class="col-start-1 mt-4 mr-4"
        @click="this.$emit('generate-explanation', modifiedInstance)"
        v-if="JSON.stringify(instanceInfo) != JSON.stringify(modifiedInstance) && allowWhatIf"
        >Generate New Explanation</default-button
      >
      <clear-button
        class="col-start-2 mt-4"
        @click="resetInstance()"
        v-if="JSON.stringify(instanceInfo) != JSON.stringify(modifiedInstance) && allowWhatIf"
        >Reset</clear-button
      >
      <outline-button
        class="col-start-2 mt-4"
        @click="resetInstance()"
        v-else-if="modificationEnabled"
        >Reset</outline-button
      >
    </div>
  </div>
</template>

<script>
import DefaultButton from "../buttons/DefaultButton.vue";
import ConfidenceVis from "../ui/ConfidenceVis.vue";
import DropdownMenu from "../ui/DropdownMenu.vue";
import RecommendationVis from "../ui/RecommendationVis.vue";
import ClearButton from "../buttons/ClearButton.vue";
import OutlineButton from "../buttons/OutlineButton.vue";

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
    OutlineButton,
    DropdownMenu,
    ClearButton,
  },
  props: {
    instanceInfo: Object,
    attributeData: Object,
    modifiable: Boolean,
    modifiedInstance: Object,
    allowWhatIf: Boolean,
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
      this.dropdownAttribute = "";
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
  inject: ["reducedCategories", "apiUrl"],
};
</script>

<style scoped>
.grid-rows-8 {
  grid-template-rows: repeat(8, minmax(0, 1fr));
}
</style>