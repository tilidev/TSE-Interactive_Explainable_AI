<template>
  <tr class="bg-white hover:bg-gray">
    <td class="py-5 px-10 text-primary">{{ rowData.other.id }}</td>
    <td class="py-5 px-10" v-for="value in rowData.attributes" :key="value">
      {{ value }}
    </td>
    <td
      v-if="rowData.other.NN_recommendation == 'true'"
      class="py-5 px-10 text-positive font-bold"
    >
      <fa-icon icon="check" class=""></fa-icon><span class="ml-2">Approve</span>
    </td>
    <td
      v-else-if="rowData.other.NN_recommendation == 'false'"
      class="py-5 px-10 text-negative font-bold"
    >
      <fa-icon icon="times"></fa-icon><span class="ml-2">Reject</span>
    </td>
    <td
      v-if="rowData.other.NN_confidence < 0.75"
      class="py-5 px-10 text-cc-low font-bold"
    >
      <span class="rounded-lg bg-cc-low text-white px-2 py-1 mr-2"
        >{{ rowData.other.NN_confidence * 100 }}%</span
      ><span>Low</span>
    </td>
    <td
      v-else-if="rowData.other.NN_confidence >= 0.9"
      class="py-5 px-10 text-cc-high font-bold"
    >
      <span class="rounded-lg bg-cc-high text-white px-2 py-1 mr-2"
        >{{ rowData.other.NN_confidence * 100 }}%</span
      ><span>High</span>
    </td>
    <td
      v-else-if="rowData.other.NN_confidence >= 0.75"
      class="py-5 px-10 text-cc-medium font-bold"
    >
      <span class="rounded-lg bg-cc-medium text-white px-2 py-1 mr-2"
        >{{ rowData.other.NN_confidence * 100 }}%</span
      ><span>Medium</span>
    </td>
  </tr>
</template>

<script>
export default {
  props: {
    rowData: Object,
  },
  mounted() {},
};
</script>