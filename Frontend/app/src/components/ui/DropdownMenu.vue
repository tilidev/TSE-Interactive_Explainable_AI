<template>
  <div class="shadow-md bg-white px-4 py-2">
    <div class="m-2">Original value:</div>
    <div class="m-2 cursor-pointer">{{ originalValue }}</div>
    <hr />
    <div v-if="attributeData.types[attribute] == 'categorical'">
      <div
        class="ml-6 mr-2 my-2 cursor-pointer"
        v-for="value in attributeData.values[attribute]"
        @click="applyValue(value)"
        :key="value"
      >
        <fa-icon
          class="text-modified -ml-6 absolute"
          icon="check"
          v-if="selectedValue == value"
        /><span :class="getValueStyling(value)">{{ value }}</span>
      </div>
    </div>
    <div v-if="attributeData.types[attribute] == 'continuous'">
      <slider class="mt-12" :min="attributeData.lowerBounds[attribute]" :max="attributeData.upperBounds[attribute]" v-model="sliderValue"></slider>
      <default-button @click="applyValue(sliderValue)" class="mt-4">Apply</default-button>
    </div>
  </div>
</template>

<script>
import Slider from "@vueform/slider";
import DefaultButton from "@/components/buttons/DefaultButton";

export default {
  data() {
    return {
      sliderValue: this.selectedValue,
    };
  },
  components: {
    DefaultButton,
    Slider,
  },
  props: { originalValue: String, selectedValue: String, attribute: String },
  inject: ["attributeData"],
  methods: {
    getValueStyling(attribute) {
      if (attribute == this.selectedValue) {
        return "text-modified";
      }
      return "";
    },
    applyValue(value) {
      this.$emit("apply-value", value);
    },
  },
};
</script>

<style
src="@vueform/slider/themes/default.css">
</style>