<template>
  <div class="bg-white shadow-md p-8 grid grid-cols-auto grid-flow-col text-left">
    <div class="font-bold col-span-2 col-start-1">Financial</div>
    <div
      class="col-start-1"
      v-for="attribute in attributeCategories.financial"
      :key="attribute"
    >
      {{ attributeData.labels[attribute] }}:
    </div>
    <div
      class="col-start-2 capitalize"
      v-for="attribute in attributeCategories.financial"
      :key="attribute"
    >
      {{ instanceInfo[attribute] }}
    </div>
    <div class="font-bold col-span-2 col-start-3">Personal</div>
    <div
      class="col-start-3"
      v-for="attribute in attributeCategories.personal"
      :key="attribute"
    >
      {{ attributeData.labels[attribute] }}:
    </div>
    <div
      class="col-start-4 capitalize"
      v-for="attribute in attributeCategories.personal"
      :key="attribute"
    >
      {{ instanceInfo[attribute] }}
    </div>
    <div class="font-bold col-span-2 col-start-5">Loan-specific</div>
    <div
      class="col-start-5"
      v-for="attribute in attributeCategories.loan"
      :key="attribute"
    >
      {{ attributeData.labels[attribute] }}:
    </div>
    <div
      class="col-start-6 capitalize"
      v-for="attribute in attributeCategories.loan"
      :key="attribute"
    >
      {{ instanceInfo[attribute] }}
    </div>
    <div class="font-bold col-span- col-start-7">AI Recommendation</div>
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
        other: [],
      };
      for (const attr of Object.keys(this.attributeData.categories)) {
        console.log(attrCat[this.attributeData.categories[attr]]);
        attrCat[this.attributeData.categories[attr]].push(attr);
      }
      return attrCat;
    },
  },
};
</script>

<style>
</style>