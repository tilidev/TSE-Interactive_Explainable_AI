<template>
  <div class="mx-8">
    <info-card
      :instanceInfo="instanceInfo"
      :attributeData="attributeData"
    ></info-card>
  </div>
</template>

<script>
import InfoCard from "../components/InfoCard.vue";

export default {
  mounted() {
    this.sendAttributeRequest();
    this.sendInstanceRequest();
  },
  data() {
    return {
      instanceInfo: {},
      id: this.$route.params.id,
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
  components: { InfoCard },
  methods: {
    // TODO: Make attribute data available globally to avoid duplicate code and unnecessary requests
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
    sendInstanceRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "instance/" + this.id).then((response) => {
        this.instanceInfo = response.data;
      });
    },
  },
  inject: ["apiUrl"],
};
</script>

<style>
</style>