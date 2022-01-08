<template>
  <div class="bg-white shadow-md p-4">
    <div>{{ attributeCategories }}</div>
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
  }
};
</script>

<style>
</style>