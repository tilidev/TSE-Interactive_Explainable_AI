<template>
  <div>
    <info-card
      :instanceInfo="instanceInfo"
      :modifiedInstance="modifiedInstance"
      :attributeData="attributeData"
      :modifiable="allowMod"
      :allowWhatIf="allowWhatIf"
      @apply-modification="applyModification"
      @reset-instance="modifiedInstance = Object.assign({}, instanceInfo)"
    ></info-card>
    <div class="mt-4 flex p-4 font-bold space-x-4 -mb-4 shadow-md pl-8 bg-white" v-if="allowSwitching">
      <div :class="getStyling('lime')" @click="this.$emit('switch', 'lime')">
        LIME
      </div>
      <div :class="getStyling('shap')" @click="this.$emit('switch', 'shap')">
        SHAP
      </div>
      <div :class="getStyling('dice')" @click="this.$emit('switch', 'dice')">
        DiCE
      </div>
    </div>
    <dice-explanation
      v-if="instanceInfo.id != null && expType === 'dice'"
      :instanceInfo="instanceInfo"
      class="mb-4 mt-8"
    ></dice-explanation>
    <tree-map
      v-else-if="Object.keys(instanceInfo).length && expType == 'lime'"
      :expType="'lime'"
      :instance="instanceInfo"
      :detailView="true"
      :whatif="false"
    ></tree-map>
    <tree-map
      v-else-if="Object.keys(instanceInfo).length && expType == 'shap'"
      :expType="'shap'"
      :instance="instanceInfo"
      :detailView="true"
      :whatif="false"
    ></tree-map>
  </div>
</template>

<script>
import InfoCard from "../components/InfoCard.vue";
import DiceExplanation from "../components/explanations/DiceExplanation.vue";
import TreeMap from "../components/explanations/TreeMap.vue";

export default {
  data() {
    return {
      modifiedInstance: {},
    };
  },
  components: { InfoCard, DiceExplanation, TreeMap },
  methods: {
    getStyling(explanation) {
      console.log(this.expType);
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