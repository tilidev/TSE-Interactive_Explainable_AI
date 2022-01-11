<template>
  <div class="bg-white shadow-md p-8">
    <div class="flex text-left text-text">
      <div
        class="pr-28 flex"
        v-for="(attributes, category) of attributeCategories"
        :key="category"
      >
        <span class="pr-8">
          <h3 class="capitalize font-bold text-lg pb-4">{{ category }}</h3>
          <div
            v-for="attribute of attributes"
            :key="attribute"
            class="text-primary"
          >
            {{ attributeData.labels[attribute] }}:
          </div>
        </span>
        <span
          ><h3 class="invisible pb-4 text-lg">Invisible Title</h3>
          <div v-for="attribute of attributes" :key="attribute">
            {{ instanceInfo[attribute] }}
          </div></span
        >
      </div>
      <div class="">
        <h3 class="font-bold text-lg pb-4">AI Recommendation</h3>
        <div
          v-if="instanceInfo.NN_recommendation == true"
          class="pb-4 text-positive font-bold"
        >
          <fa-icon icon="check-circle" size="lg"></fa-icon
          ><span class="ml-2">Approve</span>
        </div>
        <div
          v-else-if="instanceInfo.NN_recommendation == false"
          class="pb-4 text-negative font-bold"
        >
          <fa-icon icon="times-circle" size="lg"></fa-icon
          ><span class="ml-2">Reject</span>
        </div>
        <div
          v-if="instanceInfo.NN_confidence < 0.75"
          class="text-cc-low font-bold"
        >
          <span class="rounded-lg bg-cc-low text-white px-2 py-1 mr-2"
            >{{ instanceInfo.other.NN_confidence * 100 }}%</span
          ><span>Low Confidence</span>
        </div>
        <div
          v-else-if="instanceInfo.NN_confidence >= 0.9"
          class="text-cc-high font-bold"
        >
          <span class="rounded-lg bg-cc-high text-white px-2 py-1 mr-2"
            >{{ instanceInfo.NN_confidence * 100 }}%</span
          ><span>High Confidence</span>
        </div>
        <div
          v-else-if="instanceInfo.NN_confidence >= 0.75"
          class="text-cc-medium font-bold"
        >
          <span class="rounded-lg bg-cc-medium text-white px-2 py-1 mr-2"
            >{{ instanceInfo.NN_confidence * 100 }}%</span
          ><span>Medium Confidence</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: { instanceInfo: Object, attributeData: Object },
  computed: {
    attributeCategories() {
      const attrCat = {
        financial: [],
        personal: [],
        loan: [],
      };
      for (const attr of Object.keys(this.attributeData.categories)) {
        attrCat[this.attributeData.categories[attr]].push(attr);
      }
      return attrCat;
    },
  },
};
</script>

<style>
</style>