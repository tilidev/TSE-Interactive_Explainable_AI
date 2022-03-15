<template>
  <div>
    <div
      v-if="!isAtPageTop"
      class="
        fixed
        right-16
        bottom-16
        w-16
        h-16
        rounded-full
        bg-primary
        shadow-float
        cursor-pointer
      "
    >
      <fa-icon
        icon="arrow-up"
        size="2x"
        class="mt-4 text-white text-middle"
        @click="scrollUp"
      />
    </div>
    <div>
      <customize-overlay
        v-if="this.toggleCustomize"
        :currentAttributes="requestBody.attributes"
        @close="toggleCustomize = false"
        @apply="this.applyCustomization"
      />
      <filter-overlay
        v-if="this.toggleFilter"
        @update-filter="updateFilter"
        @close="toggleFilter = false"
        :currentFilters="requestBody.filter"
      />
      <div
        v-if="toggleCustomize || toggleFilter"
        class="absolute inset-0 z-40 opacity-25 bg-black"
      ></div>
    </div>
    <div
      class="flex flex-col mx-8"
      :class="tableRows.length ? 'items-center' : 'items-stretch'"
    >
      <div class="flex flex-col items-stretch">
        <div class="flex space-x-4 mb-4 -mt-4 self-start">
          <navigation-button :type="'admin'"></navigation-button>
        </div>
        <div class="flex justify-between pb-4 items-center">
          <div class="text-2xl font-bold">Dataset Explorer</div>
          <div class="flex flex-row-reverse gap-x-4 justify-start">
            <outline-button @click="toggleCustomize = !toggleCustomize"
              ><fa-icon icon="table" class="mr-2" />Customize</outline-button
            >
            <outline-button @click="toggleFilter = !toggleFilter"
              ><fa-icon icon="filter" class="mr-2" />Filter</outline-button
            >
          </div>
        </div>
        <data-table
          @apply-sorting="applySorting"
          :tableRows="tableRows"
          :optionsData="requestBody"
        />
      </div>
    </div>
  </div>
</template>

<script>
import DataTable from "../components/table/DataTable.vue";
import OutlineButton from "../components/buttons/OutlineButton.vue";
import FilterOverlay from "../components/overlays/FilterOverlay.vue";
import CustomizeOverlay from "../components/overlays/CustomizeOverlay.vue";
import NavigationButton from "../components/buttons/NavigationButton.vue";

export default {
  data() {
    return {
      toggleCustomize: false,
      toggleFilter: false,
      isAtPageTop: true,
      tableRows: [],
      requestBody: {
        filter: [],
        attributes: ["balance", "duration", "amount", "employment", "age"],
        sort_by: "id",
        sort_ascending: true,
        desc: false,
        limit: 100,
        offset: 0,
      },
    };
  },
  mounted() {
    this.sendTableRequest();
    this.loadMoreRows();
  },
  methods: {
    getItemsClass() {
      if (this.tableRows.length) {
        return "items-end";
      }
      return "items-start";
    },
    updateFilter(newFilter) {
      this.requestBody.filter = newFilter;
      this.requestBody.offset = 0;
      this.scrollUp();
      this.sendTableRequest();
    },
    applyCustomization(attributes) {
      this.requestBody.attributes = attributes;
      this.sendTableRequest();
      this.toggleCustomize = false;
    },
    scrollUp() {
      window.scrollTo(0, 0);
    },
    sendTableRequest() {
      const axios = require("axios");
      console.log(this.requestBody);
      axios.post(this.apiUrl + "table", this.requestBody).then((response) => {
        this.tableRows = response.data;
      });
    },
    loadMoreRows() {
      window.onscroll = () => {
        this.isAtPageTop =
          document.documentElement.scrollTop < 150 ? true : false;
        const axios = require("axios");
        let bottomOfWindow =
          document.documentElement.scrollTop + window.innerHeight >=
          document.documentElement.offsetHeight - window.innerHeight;
        if (bottomOfWindow && this.$route.name == "Dataset Explorer") {
          this.requestBody.offset += this.requestBody.limit;
          axios
            .post(this.apiUrl + "table", this.requestBody)
            .then((response) => {
              this.tableRows = [...this.tableRows, ...response.data];
            });
        }
      };
    },
    applySorting(sorting) {
      this.requestBody.sort_by = sorting.sort_by;
      this.requestBody.desc = sorting.desc;
      this.requestBody.sort_ascending = !sorting.desc;
      this.requestBody.offset = 0;
      this.sendTableRequest();
    },
  },
  components: {
    DataTable,
    OutlineButton,
    CustomizeOverlay,
    FilterOverlay,
    NavigationButton,
  },
  inject: ["apiUrl", "attributeData"],
};
</script>