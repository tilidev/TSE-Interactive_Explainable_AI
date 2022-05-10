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
      <div :class="getStyling('lime_orig')" @click="this.$emit('switch', 'lime_orig')">
        LIME Original
      </div>
      <div :class="getStyling('shap')" @click="this.$emit('switch', 'shap')">
        SHAP
      </div>
      <div :class="getStyling('shap_orig')" @click="this.$emit('switch', 'shap_orig')">
        SHAP Original
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
              <div class="p-4 max-w-2xl bg-white font-normal text-primary-dark shadow-blurred rounded">
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
          <!--
          <tree-map class="-ml-1" v-if="instanceInfo.id != null && expType !== 'shap_orig'" :expType="expType"
          :instance="instanceInfo" :whatif="whatif" :id="'left'" :detailView="detailed"></tree-map>
          -->
          <tree-map-lime class="-ml-1" v-if="instanceInfo.id != null && expType === 'lime'" :expType="expType"
            :instance="instanceInfo" :whatif="whatif" :id="'left'"></tree-map-lime>
          <lime-exp class="-ml-1" v-if="instanceInfo.id != null && expType === 'lime_orig'" :expType="expType"
            :instance="instanceInfo" :whatif="whatif" :id="'left'"></lime-exp>
          <tree-map-shap class="-ml-1" v-if="instanceInfo.id != null && expType === 'shap'" :expType="expType"
            :instance="instanceInfo" :whatif="whatif" :id="'left'"></tree-map-shap>
          <shap-exp class="-ml-1" v-if="instanceInfo.id != null && expType === 'shap_orig'" :expType="expType"
            :instance="instanceInfo" :whatif="whatif" :id="'left'"></shap-exp>
        </div>
        <div v-if="whatif">
          <div class="text-right mb-2">Modified Loan Application</div>
          <!--
          <tree-map class="-mr-1" v-if="instanceInfo.id != null && expType !== 'shap_orig'" :expType="expType"
          :instance="modifiedInstance" :whatif="whatif" :id="'right'" :detailView="detailed"></tree-map>
          -->
          <tree-map-lime class="-mr-1" v-if="instanceInfo.id != null && expType === 'lime'" :expType="expType"
            :instance="modifiedInstance" :whatif="whatif" :id="'right'"></tree-map-lime>
          <lime-exp class="-mr-1" v-if="instanceInfo.id != null && expType === 'lime_orig'" :expType="expType"
            :instance="modifiedInstance" :whatif="whatif" :id="'right'"></lime-exp>
          <tree-map-shap class="-mr-1" v-if="instanceInfo.id != null && expType === 'shap'" :expType="expType"
            :instance="modifiedInstance" :whatif="whatif" :id="'right'"></tree-map-shap>
          <shap-exp class="-mr-1" v-if="instanceInfo.id != null && expType === 'shap_orig'" :expType="expType"
            :instance="modifiedInstance" :whatif="whatif" :id="'right'"></shap-exp>
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
//import TreeMap from "./TreeMap.vue";
import TreeMapLime from "./TreeMapLime.vue";
import TreeMapShap from "./TreeMapShap.vue";
import ShapExp from "./ShapExp.vue";
import LimeExp from "./LimeExp.vue";
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
       * Descriptions for the lime, shap and shap_orig explanations
       */
      descriptions: {
        lime: "LIME explanations fit a linear model approximating the AI system's decision recommendation to the loan application. LIME explanations show the influence that each attribute of the loan application has on the AI system's decision recommendation in percentage points. Additionally, the explanation shows the baseline influence, which is the local intercept value of the linear model. Therefore, the sum of all attributes' influence and the baseline influence add up to the confidence value. This means that if we left the influence value for a certain attribute out when doing the addition, the confidence score would be changed by the amount of that influence value.",
        lime_orig: "LIME explanations fit a linear model approximating the AI system's decision recommendation to the loan application. LIME explanations show the influence that each attribute of the loan application has on the AI system's decision recommendation in percentage points. Additionally, the explanation shows the baseline influence, which is the local intercept value of the linear model. Therefore, the sum of all attributes' influence and the baseline influence add up to the confidence value. This means that if we left the influence value for a certain attribute out when doing the addition, the confidence score would be changed by the amount of that influence value.",
        shap: "SHAP explanations show the influence that each attribute of the loan application has on the AI system's decision recommendation in percentage points. The explanation also shows the baseline influence calculated by analyzing how many applications have been approved and rejected historically. For this system, the baseline influence for approval is 65.4% and for rejections is 34.6%. This means that 65.4% of loan applications are approved, and 34.6% are rejected. For example, given an instance for which the model recommends “Approve” with an 80% confidence, the baseline influence contributes 65.4% of the confidence value. The influence of all attributes in the loan application balance in order to contribute to the remaining 14.6% - the difference between the baseline influence and the confidence. This means that attributes influencing towards approval counterbalance attributes influencing towards rejection.",
        shap_orig: "SHAP explanations show the influence that each attribute of the loan application has on the AI system's decision recommendation in percentage points. The explanation also shows the baseline influence calculated by analyzing how many applications have been approved and rejected historically. For this system, the baseline influence for approval is 65.4% and for rejections is 34.6%. This means that 65.4% of loan applications are approved, and 34.6% are rejected. For example, given an instance for which the model recommends “Approve” with an 80% confidence, the baseline influence contributes 65.4% of the confidence value. The influence of all attributes in the loan application balance in order to contribute to the remaining 14.6% - the difference between the baseline influence and the confidence. This means that attributes influencing towards approval counterbalance attributes influencing towards rejection.",
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
  //components: { InfoCard, DiceExplanation, TreeMap, ShapExp },
  components: { InfoCard, DiceExplanation, TreeMapLime, TreeMapShap, ShapExp, LimeExp },
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