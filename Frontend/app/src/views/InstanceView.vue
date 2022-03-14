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
    <div class="flex flex-row-reverse gap-y-4 pb-4 justify-start">
      <outline-button @click="detailed = !detailed">Detail</outline-button>
    </div>
    <dice-explanation
      v-if="instanceInfo.id != null && expType === 'dice'"
      :instanceInfo="instanceInfo"
      class="mb-4 mt-8"
    ></dice-explanation>
    <tree-map
      v-else-if="Object.keys(instanceInfo).length && this.detailed == false"
      :expType="expType"
      :instance="instanceInfo"
      :detailView="false"
      :whatif="false"
    ></tree-map>
    <tree-map
      v-else-if="Object.keys(instanceInfo).length && this.detailed == true"
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
import OutlineButton from '../components/buttons/OutlineButton.vue';

export default {
  data() {
    return {
      modifiedInstance: {},
      detailed: false
    };
  },
  components: { InfoCard, DiceExplanation, TreeMap, OutlineButton },
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