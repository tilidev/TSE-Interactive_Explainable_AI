<template>
  <tr
    class="bg-white hover:bg-gray cursor-pointer"
    @click="
      this.router.push({
        name: 'Application View',
        params: { id: rowData.id },
      })
    "
  >
    <td class="py-5 px-8 text-primary">{{ rowData.id }}</td>
    <td
      class="py-5 px-8"
      v-for="attrName in filteredAttributes"
      :key="attrName"
    >
      {{ rowData[attrName] }}
    </td>
    <td class="py-5 px-7"><recommendation-vis :recommendation="rowData.NN_recommendation" /></td>
    <td
      v-if="rowData.NN_confidence < 0.75"
      class="py-5 px-8 text-cc-low font-bold"
    >
      <span class="rounded-lg bg-cc-low text-white px-2 py-1 mr-2"
        >{{ Math.round(rowData.NN_confidence * 100) }}%</span
      ><span>Low</span>
    </td>
    <td
      v-else-if="rowData.NN_confidence >= 0.9"
      class="py-5 px-8 text-cc-high font-bold"
    >
      <span class="rounded-lg bg-cc-high text-white px-2 py-1 mr-2"
        >{{ Math.round(rowData.NN_confidence * 100) }}%</span
      ><span>High</span>
    </td>
    <td
      v-else-if="rowData.NN_confidence >= 0.75"
      class="py-5 px-8 text-cc-medium font-bold"
    >
      <span class="rounded-lg bg-cc-medium text-white px-2 py-1 mr-2"
        >{{ Math.round(rowData.NN_confidence * 100) }}%</span
      ><span>Medium</span>
    </td>
  </tr>
</template>

<script>
import router from "../../router/index.js";
import RecommendationVis from "../ui/RecommendationVis.vue";

export default {
  components: { RecommendationVis },
  data() {
    return {
      router: router,
    };
  },
  computed: {
    filteredAttributes() {
      const attributeArray = Object.keys(this.rowData);
      return attributeArray.filter((el) => {
        return !(
          el == "id" ||
          el == "NN_recommendation" ||
          el == "NN_confidence"
        );
      });
    },
  },
  props: {
    rowData: Object,
  },
};
</script>