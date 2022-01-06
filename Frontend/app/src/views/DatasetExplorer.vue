<template>
  <span>
    <div class="fixed right-16 bottom-16 z-50">
    <fa-icon v-if="!isAtPageTop" icon="arrow-circle-up" size="4x" class="text-primary border-primary" @click="scrollUp"/>
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
      apiUrl: "http://localhost:8000/",
      attributeData: {
        descriptions: {},
        labels: {
          amount: "Amount",
          duration: "Duration",
          balance: "Balance",
          age: "Age",
          employment: "Employment",
          NN_recommendation: "AI Recommendation",
          NN_confidence: "AI Confidence",
          id: "#",
        },
        categories: {},
        types: {},
        lowerBounds: {},
        upperBounds: {},
      },
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
      window.scrollTo(0,0);
    },
    sendTableRequest() {
      const axios = require("axios");
      axios.post(this.apiUrl + "table", this.requestBody).then((response) => {
        this.tableRows = response.data;
      });
    },
    loadMoreRows() {
      window.onscroll = () => {
        this.isAtPageTop = (document.documentElement.scrollTop < 150)? true : false;
        const axios = require('axios');
        let bottomOfWindow =
          document.documentElement.scrollTop + window.innerHeight >=
          document.documentElement.offsetHeight - window.innerHeight;
        if (bottomOfWindow) {
          this.requestBody.offset += this.requestBody.limit;
          axios.post("http://localhost:8000/" + "table", this.requestBody).then((response) => {
            this.tableRows = [...this.tableRows, ...response.data]
          });
        }
      };
    },
    sendAttributeRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "attributes/information").then((response) => {
        for (const element of response.data) {
          this.attributeData.descriptions[element.attribute] =
            element.description;
          this.attributeData.categories[element.attribute] = element.category;
          this.attributeData.types[element.attribute] = element.type;
          this.attributeData.lowerBounds[element.attribute] =
            element.lowerBound;
          this.attributeData.upperBounds[element.attribute] =
            element.upperBound;
        }
      });
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
};
</script>
