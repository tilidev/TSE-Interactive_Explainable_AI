<template>
  <tr class="bg-white hover:bg-gray">
    <td class="py-5 px-10 text-primary">{{ rowData.id }}</td>
    <td class="py-5 px-10" v-for="attrName in filteredAttributes" :key="attrName">
      {{ rowData[attrName
      ] }}
    </td>
    <td
      v-if="rowData.NN_recommendation == true"
      class="py-5 px-10 text-positive font-bold"
    >
      <fa-icon icon="check" class=""></fa-icon><span class="ml-2">Approve</span>
    </td>
    <td
      v-else-if="rowData.NN_recommendation == false"
      class="py-5 px-10 text-negative font-bold"
    >
      <fa-icon icon="times"></fa-icon><span class="ml-2">Reject</span>
    </td>
    <td
      v-if="rowData.NN_confidence < 0.75"
      class="py-5 px-10 text-cc-low font-bold"
    >
      <span class="rounded-lg bg-cc-low text-white px-2 py-1 mr-2"
        >{{ rowData.other.NN_confidence * 100 }}%</span
      ><span>Low</span>
    </td>
    <td
      v-else-if="rowData.NN_confidence >= 0.9"
      class="py-5 px-10 text-cc-high font-bold"
    >
      <span class="rounded-lg bg-cc-high text-white px-2 py-1 mr-2"
        >{{ rowData.NN_confidence * 100 }}%</span
      ><span>High</span>
    </td>
    <td
      v-else-if="rowData.NN_confidence >= 0.75"
      class="py-5 px-10 text-cc-medium font-bold"
    >
      <span class="rounded-lg bg-cc-medium text-white px-2 py-1 mr-2"
        >{{ rowData.NN_confidence * 100 }}%</span
      ><span>Medium</span>
    </td>
  </tr>
</template>

<script>
export default {
  computed: {
    filteredAttributes() {
      const attributeArray = Object.keys(this.rowData);
      return attributeArray.filter((el) => {
        return !(el == 'id' || el == 'NN_recommendation' || el == 'NN_confidence');
      });
    },
  },
  props: {
    rowData: Object,
  },
};
</script>