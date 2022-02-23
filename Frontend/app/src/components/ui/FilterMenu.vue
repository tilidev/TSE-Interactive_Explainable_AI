<template>
  <div
    class="
      absolute
      mt-4
      shadow-md
      opacity-100
      z-50
      shadow-md
      bg-white
      px-6
      py-4
      text-left
      rounded-md
    "
  >
  <h4 class="mb-4 font-bold">{{ attributeData.labels[attribute] }}</h4>
    <div class="" v-if="attributeData.types[attribute] == 'categorical'">
      <div
        class=""
        v-for="value in attributeData.values[attribute]"
        :key="value"
      >
        <input
          type="checkbox"
          :id="value"
          :value="value"
          v-model="selectedValues"
        />
        <label class="capitalize ml-2" :for="value">{{ value }}</label>
      </div>
    </div>
    <div v-if="attributeData.types[attribute] == 'continuous'">
      <slider
        class="mx-2 mt-16 mb-4"
        :min="attributeData.lowerBounds[attribute]"
        :max="attributeData.upperBounds[attribute]"
        v-model="allowedRange"
      ></slider>
    </div>
    <div class="flex space-x-4 mt-4 justify-between">
      <default-button @click="applyChanges">Apply</default-button>
      <clear-button @click="this.$emit('cancel')">Cancel</clear-button>
    </div>
  </div>
</template>

<script>
import DefaultButton from "@/components/buttons/DefaultButton";
import ClearButton from "@/components/buttons/ClearButton";
import Slider from "@vueform/slider";

export default {
  mounted() {
    this.selectedValues = this.currentFilter.values ?? [];
    this.allowedRange = this.currentFilter.lower_bound
      ? [this.currentFilter.lower_bound, this.currentFilter.upper_bound]
      : [
          this.attributeData.lowerBounds[this.attribute],
          this.attributeData.upperBounds[this.attribute],
        ];
  },
  data() {
    return {
      allowedRange: Array,
      selectedValues: Array,
    };
  },
  methods: {
    applyChanges() {
      if (this.attributeData.types[this.attribute] == "categorical") {
        this.$emit("apply", {
          attribute: this.attribute,
          values: this.selectedValues,
        });
        return;
      }
      this.$emit("apply", {
        attribute: this.attribute,
        lower_bound: this.allowedRange[0],
        upper_bound: this.allowedRange[1],
      });
    },
  },
  components: {
    DefaultButton,
    ClearButton,
    Slider,
  },
  props: {
    currentFilter: Object,
    attribute: String,
  },
  inject: ["attributeData"],
};
</script>
