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
        <span :class="getValueStyling(attribute)">
          {{ modifiedInstance[attribute] }}
        </span>
        <fa-icon
          v-if="modificationEnabled && dropdownAttribute != attribute"
          class="ml-2 cursor-pointer"
          icon="caret-down"
          @click="dropdownAttribute = attribute"
        />
        <fa-icon
          v-if="modificationEnabled && dropdownAttribute == attribute"
          class="ml-2 cursor-pointer"
          icon="caret-up"
          @click="dropdownAttribute = ''"
        />
        <dropdown-menu
          class="absolute mt-1"
          v-if="attribute == dropdownAttribute"
          :originalValue="instanceInfo[attribute]"
          :selectedValue="modifiedInstance[attribute]"
          :attribute="attribute"
          @apply-value="applyValue"
          @cancel="dropdownAttribute = ''"
        ></dropdown-menu>
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
        <span :class="getValueStyling(attribute)">
          {{ modifiedInstance[attribute] }}
        </span>
        <fa-icon
          v-if="modificationEnabled && dropdownAttribute != attribute"
          class="ml-2 cursor-pointer"
          icon="caret-down"
          @click="dropdownAttribute = attribute"
        />
        <fa-icon
          v-if="modificationEnabled && dropdownAttribute == attribute"
          class="ml-2 cursor-pointer"
          icon="caret-up"
          @click="dropdownAttribute = ''"
        />
        <dropdown-menu
          class="absolute mt-1"
          v-if="attribute == dropdownAttribute"
          :originalValue="instanceInfo[attribute]"
          :selectedValue="modifiedInstance[attribute]"
          :attribute="attribute"
          @apply-value="applyValue"
          @cancel="dropdownAttribute = ''"
        ></dropdown-menu>
      </div>
      <div class="col-span-2 col-start-5 text-lg">Loan-specific</div>
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
        <span :class="getValueStyling(attribute)">
          {{ modifiedInstance[attribute] }}
        </span>
        <fa-icon
          v-if="modificationEnabled && dropdownAttribute != attribute"
          class="ml-2 cursor-pointer"
          icon="caret-down"
          @click="dropdownAttribute = attribute"
        />
        <fa-icon
          v-if="modificationEnabled && dropdownAttribute == attribute"
          class="ml-2 cursor-pointer"
          icon="caret-up"
          @click="dropdownAttribute = ''"
        />
        <dropdown-menu
          class="absolute mt-1"
          v-if="attribute == dropdownAttribute"
          :originalValue="instanceInfo[attribute]"
          :selectedValue="modifiedInstance[attribute]"
          :attribute="attribute"
          @apply-value="applyValue"
          @cancel="dropdownAttribute = ''"
        ></dropdown-menu>
      </div>
      <div class="col-span- col-start-7 pb-2 text-lg">AI Recommendation</div>
      <recommendation-vis
        class="col-start-7 row-span-2"
        :recommendation="instanceInfo.NN_recommendation"
      />
      <confidence-vis
        class="col-start-7 row-span-2"
        :confidence="instanceInfo.NN_confidence"
        :explicit="true"
      />
    </div>
    <div class="flex">
      <default-button
        class="col-start-1 mt-4"
        @click="modificationEnabled = true"
        v-if="modifiable && !modificationEnabled"
        >Modify</default-button
      >
      <default-button
        class="col-start-1 mt-4"
        @click="console.log('Generate Explanation')"
        v-if="modificationEnabled"
        >Generate Explanation</default-button
      >
      <clear-button
        class="col-start-2 mt-4 ml-4"
        @click="resetInstance()"
        v-if="modificationEnabled"
        >Reset</clear-button
      >
    </div>
  </div>
</template>

<script>
import DefaultButton from "./buttons/DefaultButton.vue";
import ConfidenceVis from "./ui/ConfidenceVis.vue";
import DropdownMenu from "./ui/DropdownMenu.vue";
import RecommendationVis from "./ui/RecommendationVis.vue";
import ClearButton from "./buttons/ClearButton.vue";

export default {
  data() {
    return {
      dropdownAttribute: "",
      modificationEnabled: false,
    };
  },
  components: {
    RecommendationVis,
    ConfidenceVis,
    DefaultButton,
    DropdownMenu,
    ClearButton,
  },
  props: {
    instanceInfo: Object,
    attributeData: Object,
    modifiable: Boolean,
    modifiedInstance: Object,
  },
  methods: {
    resetInstance() {
      this.modificationEnabled = false;
      this.$emit("reset-instance");
    },
    getValueStyling(attribute) {
      if (this.instanceInfo[attribute] != this.modifiedInstance[attribute]) {
        return "text-modified font-bold";
      }
      return "";
    },
    applyValue(value) {
      const modification = { attribute: this.dropdownAttribute, value: value };
      this.dropdownAttribute = "";
      this.$emit("apply-modification", modification);
    },
  },
  computed: {
    attributeCategories() {
      const attrCat = {
        financial: [],
        personal: [],
        loan: [],
        other: [],
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