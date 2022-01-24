<template>
  <div>
    <info-card
      :instanceInfo="instanceInfo"
      :modifiedInstance="modifiedInstance"
      :attributeData="attributeData"
      :modifiable="true"
      @apply-modification="applyModification"
      @reset-instance="modifiedInstance = Object.assign({}, instanceInfo);"
    ></info-card>
    <dice-explanation class="my-4"></dice-explanation>
  </div>
</template>

<script>
import InfoCard from "../components/InfoCard.vue";
import DiceExplanation from "../components/explanations/DIceExplanation.vue"

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
  }
};
</script>

<style>
</style>