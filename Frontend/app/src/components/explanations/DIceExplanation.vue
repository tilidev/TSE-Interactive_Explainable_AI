<template>
  <div class="px-8 py-4 shadow-md bg-white">
  </div>
</template>

<script>
export default {
  inject: ["attributeData"],
  components: { },
  mounted() {},
  props: {
    instanceInfo: {
      type: Object,
      required: true,
    },
  },
  watch: {
    instanceInfo() {
      for (const attribute of Object.keys(this.instanceInfo)) {
        for (const cf of this.counterfactuals) {
          if (cf[attribute] != this.instanceInfo[attribute]) {
            this.variedAttributes.push(attribute);
            break;
          }
        }
      }
      for (const cf of this.counterfactuals) {
        let row = {};
        for (const attribute of this.variedAttributes) {
          row[attribute] = cf[attribute];
        }
        this.filteredRows.push(row);
      }
    },
  },
  data() {
    return {
      variedAttributes: [],
      filteredRows: [],
      counterfactuals: [
        {
          id: 0,
          balance: "no balance",
          duration: 12,
          history: "paid back previous loans at this bank",
          purpose: "new car",
          amount: 2000,
          savings: "above 1000 EUR",
          employment: "more than 7 years",
          available_income: "less than 20%",
          residence: "more than 7 years",
          assets: "real estate",
          age: 67,
          other_loans: "no additional loans",
          housing: "own",
          previous_loans: "2 or 3",
          job: "skilled",
          other_debtors: "none",
          people_liable: "0 to 2",
          NN_recommendation: "Reject",
          NN_confidence: 0.9382685422897339,
        },
        {
          id: 0,
          balance: "no balance",
          duration: 48,
          history: "paid back previous loans at this bank",
          purpose: "furniture",
          amount: 5000,
          savings: "above 1000 EUR",
          employment: "more than 7 years",
          available_income: "less than 20%",
          residence: "more than 7 years",
          assets: "real estate",
          age: 67,
          other_loans: "no additional loans",
          housing: "own",
          previous_loans: "2 or 3",
          job: "skilled",
          other_debtors: "none",
          people_liable: "0 to 2",
          NN_recommendation: "Approve",
          NN_confidence: 0.9382685422897339,
        },
        {
          id: 0,
          balance: "no account",
          duration: 6,
          history: "delay payment of previous loans",
          purpose: "furniture",
          amount: 1169,
          savings: "above 1000 EUR",
          employment: "more than 7 years",
          available_income: "less than 20%",
          residence: "more than 7 years",
          assets: "real estate",
          age: 67,
          other_loans: "no additional loans",
          housing: "own",
          previous_loans: "2 or 3",
          job: "skilled",
          other_debtors: "none",
          people_liable: "0 to 2",
          NN_recommendation: "Approve",
          NN_confidence: 0.9382685422897339,
        },
        {
          id: 0,
          balance: "no balance",
          duration: 6,
          history: "paid back previous loans at this bank",
          purpose: "old car",
          amount: 1300,
          savings: "above 1000 EUR",
          employment: "more than 7 years",
          available_income: "less than 20%",
          residence: "more than 7 years",
          assets: "real estate",
          age: 67,
          other_loans: "no additional loans",
          housing: "own",
          previous_loans: "2 or 3",
          job: "skilled",
          other_debtors: "none",
          people_liable: "0 to 2",
          NN_recommendation: "Approve",
          NN_confidence: 0.9382685422897339,
        },
      ],
    };
  },
};
</script>