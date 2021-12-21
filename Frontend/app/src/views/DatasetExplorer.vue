<template>
  <div>
    <data-table @apply-sorting="applySorting" :data="tableData" />
  </div>
</template>

<script>
import DataTable from "../components/table/DataTable.vue";

export default {
  data() {
    return {
      tableData: {
        sorting: {
          sort_by: "id",
          desc: false,       
        },
        labels: {
          id: "#",
          balance: "Balance",
          duration: "Duration",
          amount: "Amount",
          purpose: "Purpose",
          NN_recommendation: "AI Recommendation",
          NN_confidence: "AI Confidence",
        },
        descriptions: {
          id: "Unique identifier for each loan application",
          balance: "The applicant's account balance",
          duration: "Duration over which the loan has to be paid back",
          amount: "The amount the applicant wants to borrow",
          purpose: "The purpose of the loan",
          NN_recommendation: "Recommendation from the AI",
          NN_confidence: "Specifies how confident the AI is in it's decision",
        },
        rows: [
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "false",
              NN_confidence: 0.6,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.8,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
          {
            attributes: {
              balance: "Above 200 EUR",
              duration: "48 months",
              amount: "1400000 EUR",
              purpose: "new car",
            },
            other: {
              id: 1,
              NN_recommendation: "true",
              NN_confidence: 0.9,
            },
          },
        ],
      },
      requestBody: {
        filter: [],
        attributes: ["amount", "duration", "balance", "age", "employment"],
        sort_by: "id",
        limit: 100,
        offset: 0,
      },
    };
  },
  methods: {
    applySorting(sorting) {
      this.tableData.sorting.sort_by = sorting.sort_by;
      this.tableData.sorting.desc = sorting.desc;
    },
  },
  components: { DataTable },
};
</script>
