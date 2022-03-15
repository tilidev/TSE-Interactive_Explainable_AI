<template>
  <tr
    class="bg-white hover:bg-gray cursor-pointer text-sm"
    @click="
      this.router.push({
        name: 'Application View',
        params: { id: rowData.id },
      })
    "
  >
    <td v-if="rowData.id || rowData.id === 0" class="py-5 px-8 text-primary">
      {{ rowData.id }}
    </td>
    <td
      class="py-5 px-8"
      v-for="attrName in filteredAttributes"
      :key="attrName"
    >
      {{ rowData[attrName] }}
    </td>
    <td class="py-5 px-7">
      <recommendation-vis :recommendation="rowData.NN_recommendation" />
    </td>
    <td v-if="rowData.NN_confidence" class="py-5 px-7">
      <confidence-vis :confidence="rowData.NN_confidence" />
    </td>
  </tr>
</template>

<script>
import router from "../../router/index.js";
import RecommendationVis from "../ui/RecommendationVis.vue";
import ConfidenceVis from "../ui/ConfidenceVis.vue";

export default {
  components: { RecommendationVis, ConfidenceVis },
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
    rowData: {
      type: Object,
      required: true,
    },
  },
};
</script>