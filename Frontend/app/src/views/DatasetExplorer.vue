<template>
  <div>
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
  components: { DataTable },
};
</script>
