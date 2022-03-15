<template>
  <div>
    <info-card
      :instanceInfo="instanceInfo"
      :modifiedInstance="modifiedInstance"
      :attributeData="attributeData"
      :modifiable="allowMod"
      :allowWhatIf="expType == 'dice' ? false : allowWhatIf"
      @apply-modification="applyModification"
      @generate-explanation="generateExplanation"
      @reset-instance="reset"
    ></info-card>
    <div
      class="mt-4 flex p-4 font-bold space-x-4 -mb-4 shadow-md pl-8 bg-white"
      v-if="allowSwitching"
    >
      <div :class="getStyling('dice')" @click="this.$emit('switch', 'dice')">
        DiCE
      </div>
      <div :class="getStyling('lime')" @click="this.$emit('switch', 'lime')">
        LIME
      </div>
      <div :class="getStyling('shap')" @click="this.$emit('switch', 'shap')">
        SHAP
      </div>
    </div>
    <dice-explanation
      v-if="instanceInfo.id != null && expType === 'dice'"
      :instanceInfo="instanceInfo"
      class="mb-4 mt-8"
    ></dice-explanation>
    <div
      class="bg-white px-8 py-4 my-8 shadow-md"
      v-else-if="Object.keys(instanceInfo).length"
    >
      <div class="flex justify-between mb-4">
        <div class="text-lg font-bold flex">
          Factors influencing AI Recommendation
          <div>
            <fa-icon
              @click="hover = !hover"
              @mouseover="hover = true"
              @mouseleave="hover = false"
              icon="info-circle"
              class="ml-2"
            />
            <div v-if="hover" class="mt-8 absolute z-50">
              <div
                class="
                  p-4
                  max-w-2xl
                  bg-white
                  font-normal
                  text-primary-dark
                  shadow-blurred
                  rounded
                "
              >
                {{ descriptions[expType] }}
              </div>
            </div>
          </div>
        </div>
        <div class="flex justify-end space-x-4">
          <div>Toggle detail view</div>
          <Toggle
            v-model="detailed"
            :classes="{
              toggleOn: 'bg-primary border-primary justify-start text-white',
            }"
          />
        </div>
      </div>
      <div class="flex justify-between">
        <div>
          <div class="text-left mb-2" v-if="whatif">
            Original Loan Application
          </div>
          <tree-map
            class="-ml-1"
            :expType="expType"
            :instance="instanceInfo"
            :whatif="whatif"
            :id="'left'"
            :detailView="detailed"
          ></tree-map>
        </div>
        <div v-if="whatif">
          <div class="text-right mb-2">Modified Loan Application</div>
          <tree-map
            class="-mr-1"
            :expType="expType"
            :instance="modifiedInstance"
            :whatif="whatif"
            :id="'right'"
            :detailView="detailed"
          ></tree-map>
        </div>
      </div>
      <div>
        <div class="flex my-4">
          <div class="bg-positive h-6 w-6 mr-4"></div>
          <div class="text-positive-dark font-bold">
            Influencing towards approval
          </div>
        </div>
        <div class="flex">
          <div class="bg-negative h-6 w-6 mr-4"></div>
          <div class="text-negative-dark font-bold">
            Influencing towards rejection
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import InfoCard from "./InfoCard.vue";
import DiceExplanation from "./DiceExplanation.vue";
import TreeMap from "./TreeMap.vue";
import Toggle from "@vueform/toggle";

export default {
  mounted() {
    this.modifiedInstance = Object.assign({}, this.instanceInfo);
  },
  data() {
    return {
      hover: false,
      modifiedInstance: {},
      detailed: false,
      modified: false,
      whatif: false,
      descriptions: {
        shap: "The SHAP values explain each attribute-value’s contribution to the difference between the average model prediction over the entire dataset (Approve, 66% confidence) and the actual prediction for the explained instance. Given an instance with an actual model prediction of “Approve” with 70 % confidence, we expect the SHAP values to add up to 4% - the exact difference to the average model prediction.",
        lime: "The SHAP values explain each attribute-value’s contribution to the difference between the average model prediction over the entire dataset (Approve, 66% confidence) and the actual prediction for the explained instance. Given an instance with an actual model prediction of “Approve” with 70 % confidence, we expect the SHAP values to add up to 4% - the exact difference to the average model prediction.",
      },
    };
  },
  components: { InfoCard, DiceExplanation, TreeMap, Toggle },
  methods: {
    reset() {
      this.modifiedInstance = Object.assign({}, this.instanceInfo);
      this.whatif = false;
    },
    generateExplanation(modifiedInstance) {
      this.modifiedInstance = Object.assign({}, modifiedInstance);
      this.whatif = true;
    },
    getStyling(explanation) {
      if (explanation == this.expType) {
        return "underline text-positive cursor-pointer";
      }
      return "cursor-pointer";
    },
    applyModification(modification) {
      this.modifiedInstance[modification["attribute"]] = modification["value"];
    },
  },
  watch: {
    instanceInfo(newInstance) {
      this.whatif = false;
      this.modifiedInstance = Object.assign({}, newInstance);
    },
  },
  inject: ["attributeData"],
  props: {
    instanceInfo: {
      type: Object,
      required: true,
    },
    allowMod: Boolean,
    allowWhatIf: Boolean,
    expType: String,
    allowSwitching: Boolean,
  },
};
</script>

<style>
</style>