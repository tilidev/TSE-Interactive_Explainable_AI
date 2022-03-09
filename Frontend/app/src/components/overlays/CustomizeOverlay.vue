
<template>
  <transition name="fade">
    <div class="fixed inset-0 flex justify-center items-center z-50">
      <div class="relative mx-auto w-auto">
        <div class="bg-white w-100 rounded-lg shadow-md p-4">
          <div class="flex mb-8 justify-between">
            <h4 class="text-xl font-bold">
              Select up to 5 Attributes to display in the table
            </h4>
            <button
              @click="this.$emit('close')"
              class="bg-white hover:bg-gray-light px-2 py-0.5 rounded-full"
            >
              <fa-icon icon="times"></fa-icon>
            </button>
          </div>
          <div class="flex flex-col space-y-8 mb-8">
            <div
              class="
                font-bold
                flex
                capitalize
                justify-between
                space-x-16
                items-center
              "
              v-for="category in Object.keys(getReducedCategories())"
              :key="category"
            >
              <div>
                {{ category }}
              </div>
              <div class="flex space-x-4">
                <div
                  v-for="attribute of attributeCategories[category]"
                  :key="attribute"
                >
                  <gray-button
                    @click="
                      selectedAttributes = selectedAttributes.filter(
                        (e) => e !== attribute
                      )
                    "
                    :selected="true"
                    v-if="selectedAttributes.includes(attribute)"
                    >{{ attributeData.labels[attribute] }}</gray-button
                  >
                  <gray-button
                    @click="addAttribute(attribute)"
                    :selected="false"
                    v-else
                    >{{ attributeData.labels[attribute] }}</gray-button
                  >
                </div>
              </div>
            </div>
          </div>
          <div class="flex">
            <default-button @click="applyChanges" class="mr-4"
              >Apply Changes</default-button
            >
            <clear-button @click="this.$emit('close')">Cancel</clear-button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import DefaultButton from "../buttons/DefaultButton.vue";
import GrayButton from "../buttons/GrayButton.vue";
import ClearButton from "../buttons/ClearButton.vue";
export default {
  components: { ClearButton, DefaultButton, GrayButton },
  name: "Customize",
  props: {
    currentAttributes: Array,
  },
  data() {
    return {
      selectedAttributes: [...this.currentAttributes],
    };
  },
  inject: ["attributeData", "attributeCategories"],

  methods: {
    getReducedCategories() {
      // eslint-disable-next-line no-unused-vars
      const { other, ...rest } = this.attributeCategories;
      return rest;
    },
    addAttribute(attr) {
      if (this.selectedAttributes.length < 5) {
        this.selectedAttributes.push(attr);
      }
    },
    applyChanges() {
      this.$emit("apply", this.selectedAttributes);
    },
  },
};
</script>

<style scoped>
.fade-enter-from {
  opacity: 0;
}
.fade-enter-to {
  opacity: 1;
}
.fade-enter-active {
  transition: all 1s ease;
}
.fade-leave-from {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
}
.fade-leave-active {
  transition: all 1s ease;
}
</style>


