<template>
  <div class="bg-white shadow-md p-4">
    <div class="flex text-left">
      <div class="pr-8"
        v-for="(attributes, category) of attributeCategories"
        :key="category"
      >
        <h3 class="capitalize font-bold">{{ category }}</h3>
        <div v-for="attribute of attributes" :key="attribute"><span>{{attributeData.labels[attribute]}}: </span><span>{{instanceInfo[attribute]}}</span></div>
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