<template>
  <div>
    <info-card :instanceInfo="instanceInfo" :modifiedInstance="modifiedInstance" :modifiable="allowMod"
      :allowWhatIf="expType == 'dice' ? false : allowWhatIf" :resetModificationFunction="resetModificationFunction"
      @apply-modification="applyModification" @generate-explanation="generateExplanation" @reset-instance="reset"
      @new-prediction="passPrediction"></info-card>
    <div class="mt-4 flex p-4 font-bold space-x-4 -mb-4 shadow-md pl-8 bg-white" v-if="allowSwitching">
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
    <dice-explanation v-if="instanceInfo.id != null && expType === 'dice'" :instanceInfo="instanceInfo"
      class="mb-4 mt-8"></dice-explanation>
    <div class="bg-white px-8 py-4 my-8 shadow-md" v-else-if="Object.keys(instanceInfo).length">
      <div class="flex justify-between mb-4">
        <div class="text-lg font-bold flex">
          Factors influencing AI Recommendation
          <div>
            <fa-icon @click="hover = !hover" @mouseover="hover = true" @mouseleave="hover = false" icon="info-circle"
              class="ml-2" />
            <div v-if="hover" class="mt-4 text-sm absolute z-50">
              <div class="
                  p-4
                  max-w-2xl
                  bg-white
                  font-normal
                  text-primary-dark
                  shadow-blurred
                  rounded
                ">
                {{ descriptions[expType] }}
              </div>
            </div>
          </div>
        </div>
        <!-- Modification -->
        <!-- Disable Toggle Fucntionality -->
        <!--
        <div class="flex justify-end space-x-4">
          <div>Toggle detail view</div>
          <Toggle
            v-model="detailed"
            :classes="{
              toggleOn: 'bg-primary border-primary justify-start text-white',
            }"
          />
        </div>
        -->
      </div>
      <div class="flex justify-between">
        <div>
          <div class="text-left mb-2" v-if="whatif">
            Original Loan Application
          </div>
          <tree-map class="-ml-1" :expType="expType" :instance="instanceInfo" :whatif="whatif" :id="'left'"
            :detailView="detailed"></tree-map>
        </div>
        <div v-if="whatif">
          <div class="text-right mb-2">Modified Loan Application</div>
          <tree-map class="-mr-1" :expType="expType" :instance="modifiedInstance" :whatif="whatif" :id="'right'"
            :detailView="detailed"></tree-map>
        </div>
      </div>
      <div>
        <div class="flex my-4">
          <div class="bg-positive-chart h-6 w-6 mr-4"></div>
          <div class="text-positive-chart font-bold">
            Influencing towards approval
          </div>
        </div>
        <div class="flex">
          <div class="bg-negative-chart h-6 w-6 mr-4"></div>
          <div class="text-negative-chart font-bold">
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
// Modification
// Disable Toggle functionality
// import Toggle from "@vueform/toggle";

/**
 * Component for the instance view. Contains the instance info card and the explanation visualization
 */
export default {
  mounted() {
    this.modifiedInstance = Object.assign({}, this.instanceInfo);
  },
  data() {
    return {
      /**
       * True while the user hovers over the info button. In that case the description overlay is shown.
       */
      hover: false,
      /**
       * The instance modified by the user
       */
      modifiedInstance: {},
      /**
       * If detail view is enabled
       */
      detailed: false,
      /**
       * If the instance is modified
       */
      modified: false,
      /**
       * If whatif analysis is enabled
       */
      whatif: false,
      /**
       * Descriptions for the lime and shap explanations
       */
      descriptions: {
        shap: "The SHAP values explain each attribute value’s contribution in percentage points to the difference between the average AI prediction over the entire dataset (Approve, 65% confidence) and the actual prediction for the explained instance. Given an instance with an actual model prediction of “Approve” with 70 % confidence, we expect the SHAP values to add up to 5% - the exact difference to the average model prediction.",
        lime: "The lime values explain each attribute-value's contribution to the local prediction score in percentage points. Lime fits a linear model approximating the AI decision at that point. Therefore the sum of all the lime values plus the local intercept value that has also been fitted add up to the local prediction score. This means that if we would leave the lime value for a certain attribute out when doing the addition, the local prediction score would be changed by the amount of that value.",
      },
      /*
       * Modification
       * New Propops
       * Add prop to reset modification functionality
      * */
      resetModificationFunction: false,
    };
  },
  // Modification
  // Disable Toggle functionality
  // components: { InfoCard, DiceExplanation, TreeMap, Toggle },
  components: { InfoCard, DiceExplanation, TreeMap },
  methods: {
    /**
     * Resets the current instance
     */
    reset() {
      this.modifiedInstance = Object.assign({}, this.instanceInfo);
      this.whatif = false;
      // Modification
      // change prop in child to trigger the reset of modification functionality when experiment navigates to the next loan application
      this.resetModificationFunction = !this.resetModificationFunction;
    },
    /**
     * Generates the explanation for the what if analysis
     * @param {Object} modifiedInstance - Information for the modified instance
     */
    generateExplanation(modifiedInstance) {
      this.modifiedInstance = Object.assign({}, modifiedInstance);
      this.whatif = true;
    },
    /** 
     * Modification
     * Updates modifiedInstance prediction and confidence
     * @param {Object} newPrediction - Prediction of new object
    */
    passPrediction(newPrediction) {
      this.modifiedInstance.NN_confidence = newPrediction.NN_confidence;
      this.modifiedInstance.NN_recommendation = newPrediction.NN_recommendation;
    },
    /**
     * Returns styling classes for the explanation names in the menu
     * @returns {String} - Tailwind classes for styling
     */
    getStyling(explanation) {
      if (explanation == this.expType) {
        return "underline text-positive cursor-pointer";
      }
      return "cursor-pointer";
    },
    /**
     * Applies a new modification to the modified instance
     * @param {Object} modification - The new modification
     */
    applyModification(modification) {
      this.modifiedInstance[modification["attribute"]] = modification["value"];
    },
  },
  watch: {
    instanceInfo(newInstance) {
      this.whatif = false;
      this.modifiedInstance = Object.assign({}, newInstance);
    },
    // Modification
    // Monitor experiment parent component to trigger a reset of the modification functionality
    resetInstance() {
      this.reset();
    },
  },
  inject: ["attributeData"],
  props: {
    /**
     * Object with instance information
     */
    instanceInfo: {
      type: Object,
      required: true,
    },
    /**
     * Specifies if modification is allowed
     */
    allowMod: Boolean,
    /**
     * Specifies if what-if analysis is allowed
     */
    allowWhatIf: Boolean,
    /**
     * The default explanation type
     */
    expType: String,
    /**
     * Specifies if the user can switch between explanation typess
     */
    allowSwitching: Boolean,
    /*
       * Modification
       * New Propops
       * Add prop to reset modification functionality
      * */
    resetInstance: Boolean,
  },
};
</script>

<style>
</style>