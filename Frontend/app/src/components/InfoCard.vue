<template>
  <div class="bg-white shadow-md px-8 py-4 text-left">
    <h2 class="font-bold text-lg pb-4">Current Loan Application</h2>
    <div class="grid grid-cols-auto grid-flow-col text-sm">
      <div class="col-span-2 col-start-1 text-lg">Financial</div>
      <div
        class="col-start-1 text-primary-light font-bold"
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
      <div class="col-span-2 col-start-3 text-lg">Personal</div>
      <div
        class="col-start-3 text-primary-light font-bold font-bold" 
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
      <div class="col-span-2 col-start-5 text-lg">
        Loan-specific
      </div>
      <div
        class="col-start-5 text-primary-light font-bold"
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
      <div class="col-span- col-start-7 pb-2 text-lg">
        AI Recommendation
      </div>
      <recommendation-vis
        class="col-start-7 row-span-2"
        :recommendation="instanceInfo.NN_recommendation"
      />
      <confidence-vis
        class="col-start-7"
        :confidence="instanceInfo.NN_confidence"
        :explicit="true"
      />
      <default-button class="col-start-1 mt-4" @click="modificationEnabled=true" v-if="modifiable && !modificationEnabled">Modify</default-button>
      <default-button class="col-start-1 mt-4" @click="modificationEnabled=false" v-if="modificationEnabled">Reset</default-button>
    </div>
  </div>
</template>

<script>
import DefaultButton from './buttons/DefaultButton.vue';
import ConfidenceVis from "./ui/ConfidenceVis.vue";
import RecommendationVis from "./ui/RecommendationVis.vue";

export default {
  data() {
    return {
      modificationEnabled: false,
      isModified: false,
    }
  },
  components: { RecommendationVis, ConfidenceVis, DefaultButton },
  props: { instanceInfo: Object, attributeData: Object, modifiable: Boolean },
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