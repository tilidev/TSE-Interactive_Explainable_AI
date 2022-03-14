<template>
  <div v-click-outside="cancel" class="shadow-blurred bg-white px-4 py-2">
    <div class="m-2 font-bold">Original value:</div>
    <div class="m-2 cursor-pointer" @click="applyValue(originalValue)">
      {{ originalValue }}
    </div>
    <hr />
    <div v-if="attributeData.types[attribute] == 'categorical'">
      <div
        class="ml-6 mr-2 my-2 cursor-pointer"
        v-for="value in attributeData.values[attribute]"
        @click="applyValue(value)"
        :key="value"
      >
        <fa-icon
          class="-ml-6 mt-0.5 absolute"
          :class="getValueStyling(value)"
          icon="check"
          v-if="selectedValue == value"
        /><span :class="getValueStyling(value)">{{ value }}</span>
      </div>
    </div>
    <div v-if="attributeData.types[attribute] == 'continuous'">
      <slider
        class="mt-12"
        :min="attributeData.lowerBounds[attribute]"
        :max="attributeData.upperBounds[attribute]"
        v-model="sliderValue"
      ></slider>
      <div class="flex mt-4 mb-1">
        <default-button
          @click="applyValue(sliderValue)"
          class="mr-4"
          :size="'sm'"
          >Apply</default-button
        >
        <clear-button :size="'sm'" @click="this.$emit('cancel')"
          >Cancel</clear-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import Slider from "@vueform/slider";
import vClickOutside from "click-outside-vue3";
import DefaultButton from "@/components/buttons/DefaultButton";
import ClearButton from "../buttons/ClearButton.vue";

export default {
  directives: {
    clickOutside: vClickOutside.directive,
  },
  data() {
    return {
      sliderValue: this.selectedValue,
    };
  },
  components: {
    DefaultButton,
    Slider,
    ClearButton,
  },
  props: { originalValue: String, selectedValue: String, attribute: String },
  inject: ["attributeData"],
  methods: {
    cancel() {
      this.$emit("apply-value", this.originalValue);
    },
    getValueStyling(attribute) {
      if (attribute == this.selectedValue && attribute != this.originalValue) {
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
@import "../../../node_modules/@vueform/slider/themes/tailwind.scss";
</style>
