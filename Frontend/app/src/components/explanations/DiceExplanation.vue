<template>
  <div class="text-left px-8 py-4 shadow-md bg-white">
    <h2 class="font-bold text-lg mb-4">Counterfactual Explanations</h2>
    <table
      v-if="counterfactuals.length"
      class="table-auto text-primary shadow-lg text-left"
    >
      <thead class="bg-primary text-white">
        <table-header
          :labels="attributeData.labels"
          :descriptions="attributeData.descriptions"
          :attributes="['id',
            ...Object.keys(counterfactuals[index]),
            'NN_recommendation',
          ]"
        />
      </thead>
      <tbody class="divide-gray divide-y">
        <table-row
          :rowData="
            getBaseRow(counterfactuals[index])
          "
        ></table-row>
        <table-row
          :rowData="{'id': 'Counterfactual Explanation', ...counterfactuals[index]}"
          :highlight="getHighlightSet(counterfactuals[index])"
        />
      </tbody>
    </table>
  </div>
</template>

<script>
import TableHeader from "../table/TableHeader.vue";
import TableRow from "../table/TableRow.vue";
export default {
  inject: ["attributeData", "apiUrl"],
  components: { TableHeader, TableRow },
  mounted() {
    console.log(this.instanceInfo);
    this.sendDiceRequest();
  },
  props: {
    instanceInfo: {
      type: Object,
      required: true,
    },
  },
  methods: {
    sendDiceRequest() {
      const axios = require("axios");
      axios
        .get(
          this.apiUrl + "explanations/dice?instance_id=" + this.instanceInfo.id
        )
        .then((response) => {
          this.counterfactuals = response.data.counterfactuals;
          console.log(this.counterfactuals);
        });
    },
    getBaseRow(cfRow) {
      return {"id":"Original Application", ...Object.fromEntries(Object.entries(this.instanceInfo).filter(([key, value]) => cfRow[key] && value))};
    },
    getHighlightSet(row) {
      const attributeArray = Object.keys(row);
      return new Set(
        attributeArray.filter((el) => {
          return row[el] != this.instanceInfo[el];
        })
      );
    },
  },
  data() {
    return {
      variedAttributes: [],
      filteredRows: [],
      counterfactuals: [],
      index: 0,
    };
  },
};
</script>