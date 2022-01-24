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
    <div class=" my-4 px-8 py-4 shadow-md bg-white">Placeholder for explanation</div>
  </div>
</template>

<script>
import InfoCard from "../components/InfoCard.vue";

export default {
  data() {
    return {
      modifiedInstance: {},
    };
  },
  components: { InfoCard },
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