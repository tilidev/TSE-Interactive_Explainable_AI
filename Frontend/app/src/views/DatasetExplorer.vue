<template>
  <span>
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
    <data-table
      @apply-sorting="applySorting"
      :tableRows="tableRows"
      :attributeData="attributeData"
      :optionsData="requestBody"
    />
  </span>
</template>

<script>
import DataTable from "../components/table/DataTable.vue";

export default {
  data() {
    return {
      isAtPageTop: true,
      tableRows: [],
      requestBody: {
        filter: [],
        attributes: ["balance", "duration", "amount", "employment", "age"],
        sort_by: "id",
        desc: false,
        limit: 100,
        offset: 0,
      },
    };
  },
  mounted() {
    this.sendAttributeRequest();
    this.sendTableRequest();
    this.loadMoreRows();
  },
  methods: {
    scrollUp() {
      window.scrollTo(0, 0);
    },
    sendTableRequest() {
      const axios = require("axios");
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
        if (bottomOfWindow) {
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
      this.sendTableRequest();
    },
    applyFilters(filters) {
      console.log(filters);
    },
    applyCustomization(customization) {
      console.log(customization);
    },
  },
  components: { DataTable },
  inject: ["apiUrl", "attributeData"],
};
</script>
