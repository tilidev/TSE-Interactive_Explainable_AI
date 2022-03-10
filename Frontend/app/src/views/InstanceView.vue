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
    <dice-explanation
      v-if="instanceInfo.id != null && expType === 'dice'"
      :instanceInfo="instanceInfo"
      class="mb-4 mt-8"
    ></dice-explanation>
    <tree-map
      v-else-if="Object.keys(instanceInfo).length"
      :expType="expType"
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
  },
};
</script>

<style>
</style>