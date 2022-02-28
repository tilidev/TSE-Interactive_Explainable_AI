<template>
  <div>
    <info-card
      :instanceInfo="instanceInfo"
      :modifiedInstance="modifiedInstance"
      :attributeData="attributeData"
      :modifiable="allowMod"
      :allowWhatIf="allowWhatIf"
      @apply-modification="applyModification"
      @reset-instance="modifiedInstance = Object.assign({}, instanceInfo);"
    ></info-card>
    <dice-explanation v-if="instanceInfo.id != null && expType === 'dice'" :instanceInfo="instanceInfo" class="mb-4 mt-8"></dice-explanation>
    <div v-else-if="expType === 'lime'">Placeholder for Lime</div>
    <div v-else-if="expType === 'shap'">Placeholder for SHAP</div>
    
  </div>
</template>

<script>
import InfoCard from "../components/InfoCard.vue";
import DiceExplanation from "../components/explanations/DiceExplanation.vue"

export default {
  data() {
    return {
      modifiedInstance: {},
    };
  },
  components: { InfoCard, DiceExplanation },
  methods: {
    applyModification(modification) {
      this.modifiedInstance[modification["attribute"]] = modification["value"];
    },
  },
  watch: {
    instanceInfo(newInstance) {
      this.modifiedInstance = Object.assign({}, newInstance)
    } 
  },
  inject: ["attributeData"],
  props: {
    instanceInfo : {
      type: Object,
      required: true,
    },
    allowMod : Boolean,
    allowWhatIf : Boolean,
    expType: String,
  }
};
</script>

<style>
</style>