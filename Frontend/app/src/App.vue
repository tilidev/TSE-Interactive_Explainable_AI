<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/dataset">Dataset Explorer</router-link>
  </div>
  <router-view />
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<script>
export default {
  data() {
    return {
      apiUrl: 'http://localhost:8000/',
      attributeData: {
        descriptions: {},
        labels: {
          amount: "Amount",
          history: "History",
          purpose: "Purpose",
          savings: "Savings",
          available_income: "Available Income",
          residence: "Residence",
          assets: "Assets",
          other_loans: "Other Loans",
          housing: "Housing",
          previous_loans: "Previous Loans",
          job: "Job",
          other_debtors: "Other Debtors",
          people_liable: "People liable",
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
    };
  },
  mounted() {
    this.sendAttributeRequest();
  },
  methods: {
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
  },
  provide() {
    return {
      attributeData: this.attributeData,
      apiUrl: this.apiUrl,
    };
  },
};
</script>
