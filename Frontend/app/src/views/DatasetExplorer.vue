<template>
  <div>
    <div class="flex flex-row-reverse pr-20">
    <outline-button @click="toggleCustomize = !toggleCustomize"
      >Customize</outline-button
    >
    <outline-button @click="toggleFilter = !toggleFilter"
      >Filter</outline-button
    >
    </div>


    <customize-overlay
      v-show="this.toggleCustomize"
      @close="closeCustomizeModal"
    />

    <filter-overlay
      v-show="this.toggleFilter"
      @close="closeFilterModal"
    />
    <div
      v-if="toggleCustomize||toggleFilter"
      class="absolute inset-0 z-40 opacity-25 bg-black"
    ></div>
  </div>
</template>

<script>
import OutlineButton from "../components/buttons/OutlineButton.vue";
import FilterOverlay from '../components/overlays/FilterOverlay.vue';
import CustomizeOverlay from '../components/overlays/CustomizeOverlay.vue';



export default {
  name: "customize",
  data() {
    return {
      toggleCustomize: false,
      toggleFilter: false,
    };
  },
  methods: {
    
    showCustomizeModal() {
      this.toggleCustomize = true;
    },
    closeCustomizeModal() {
      this.toggleCustomize = false;
    },

    showFilterModal() {
      this.toggleFilter = true;
    },
    closeFilterModal() {
      this.toggleFilter = false;
    }
  },
  components: { OutlineButton, FilterOverlay, CustomizeOverlay },
}
</script>


}