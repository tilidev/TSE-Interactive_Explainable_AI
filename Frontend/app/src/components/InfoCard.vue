<template>
  <div class="bg-white shadow-md p-8 grid gap-x-4 grid-cols-7 text-left">
    <div class="font-bold col-span-2">Financial</div>
    <div class="font-bold col-span-2">Personal</div>
    <div class="font-bold col-span-2">Loan-specific</div>
    <div class="font-bold col-span-1">AI Recommendation</div>
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