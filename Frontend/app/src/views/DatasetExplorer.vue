<template>
  <div class="dataset">
    <data-table :data="tableData" />
  </div>
</template>

<script>
import DataTable from "../components/table/DataTable.vue";

export default {
  data() {
    return {
      tableData: {
        sorting: {
          attribute: "id",
          desc: false
        },
        labels: {
          id: "#",
          balance: "Balance",
          duration: "Duration (months)",
          amount: "Amount",
          purpose: "Purpose",
          NN_recommendation: "AI Recommendation",
          NN_confidence: "AI Confidence",
        },
        descriptions: {
          id: "Description",
          balance: "Description",
          duration: "Description",
          amount: "Description",
          purpose: "Description",
          NN_recommendation: "Description",
          NN_confidence: "Description",
        },
        rows: [
          {
            id: "1",
            balance: "Above 200 EUR",
            duration: "48",
            amount: "14000 EUR",
            purpose: "new car",
            NN_recommendation: "Approve",
            NN_confidence: 0.9,
          },
          {
            id: "1",
            balance: "Above 200 EUR",
            duration: "48",
            amount: "14000 EUR",
            purpose: "new car",
            NN_recommendation: "Approve",
            NN_confidence: 0.9,
          },
          {
            id: "1",
            balance: "Above 200 EUR",
            duration: "48",
            amount: "14000 EUR",
            purpose: "new car",
            NN_recommendation: "Approve",
            NN_confidence: 0.9,
          },
        ],
      },
      requestBody: {
        filter: [
        ],
        attributes: ["amount", "duration", "balance", "age", "employment"],
        sort_by: "id",
        limit: 100,
        offset: 0,
      },
    };
  },
  components: { DataTable },
};
</script>
