<template>
  <div class="text-left px-8 py-4 shadow-md bg-white">
    <div class="flex justify-between">
      <h2 class="font-bold text-lg mb-4">Counterfactual Explanations</h2>
      <div class="text-lg">
        {{ index + 1 + " of " + counterfactuals.length }}
      </div>
    </div>
    <div class="-mx-4 flex space-x-4 justify-between items-center">
      <div :class="getArrowStyling('left')" @click="handleClick('left')">
        <fa-icon icon="arrow-left" size="2x" />
      </div>
      <div>
        <table
          v-if="counterfactuals.length"
          class="table-auto text-primary shadow-lg text-left"
        >
          <thead class="bg-primary text-white">
            <table-header
              :labels="attributeData.labels"
              :descriptions="attributeData.descriptions"
              :attributes="Object.keys(counterfactuals[index])"
            />
          </thead>
          <tbody class="divide-gray divide-y">
            <table-row
              :rowData="getBaseRow(counterfactuals[index])"
            ></table-row>
            <table-row
              :rowData="counterfactuals[index]"
              :highlight="getHighlightSet(counterfactuals[index])"
            />
          </tbody>
        </table>
        <div>
          <div class="flex mt-8 mb-4">
            <div class="bg-primary h-6 w-6 mr-4"></div>
            Original application
          </div>
          <div class="flex">
            <div class="bg-modified h-6 w-6 mr-4"></div>
            <div class="text-modified font-bold">
              Counterfactual application
            </div>
          </div>
        </div>
      </div>
      <div :class="getArrowStyling('right')" @click="handleClick('right')">
        <fa-icon icon="arrow-right" size="2x" />
      </div>
    </div>
  </div>
</template>

<script>
import TableHeader from "../table/TableHeader.vue";
import TableRow from "../table/TableRow.vue";
/**
 * A component for displaying the DiCE explanation.
 * It shows 5 different tables with the original instance and one counterfactual each time.
 * The user can navigate through these tables with arrow buttons.
 */
export default {
  inject: ["attributeData", "apiUrl"],
  components: { TableHeader, TableRow },
  mounted() {
    this.sendDiceRequest();
  },
  props: {
    /**
     * The instance (loan application) to be used for the explanation.
     */
    instanceInfo: {
      type: Object,
      required: true,
    },
  },
  watch: {
    instanceInfo() {
      this.index = 0;
    },
  },
  methods: {
    handleClick(direction) {
      if (
        (this.index === 0 && direction === "left") ||
        (this.index === this.counterfactuals.length - 1 && direction == "right")
      ) {
        return;
      }
      this.index += direction === "left" ? -1 : 1;
    },
    getArrowStyling(direction) {
      if (
        (this.index === 0 && direction === "left") ||
        (this.index === this.counterfactuals.length - 1 && direction == "right")
      ) {
        return "p-4 flex justify-center items-center rounded-full text-gray";
      }
      return "p-4 flex justify-center items-center rounded-full hover:bg-gray-light cursor-pointer";
    },
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
      return Object.fromEntries(
        Object.entries(this.instanceInfo).filter(
          ([key, value]) => cfRow[key] && value
        )
      );
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