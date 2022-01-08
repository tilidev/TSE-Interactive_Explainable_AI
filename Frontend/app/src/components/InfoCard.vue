<template>
  <div class="bg-white shadow-md p-8">
    <div class="flex text-left text-text">
      <div
        class="pr-32 flex"
        v-for="(attributes, category) of attributeCategories"
        :key="category"
      >
        <span class="pr-8">
          <h3 class="capitalize font-bold text-lg pb-4">{{ category }}</h3>
          <div v-for="attribute of attributes" :key="attribute" class="text-primary">
            {{ attributeData.labels[attribute] }}:
          </div>
        </span>
        <span
          ><h3 class="invisible pb-4 text-lg">Invisible Title</h3><div v-for="attribute of attributes" :key="attribute">
            {{ instanceInfo[attribute] }}
          </div></span
        >
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