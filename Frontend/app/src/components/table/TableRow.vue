<template>
  <tr class="bg-white">
    <td v-for="value in rowData.attributes" :key="value">{{ value }}</td>
    <td>{{rowData.results.NN_recommendation}}</td>
    <td>{{rowData.results.NN_confidence}}</td>
  </tr>
</template>

<script>
export default {
  props: {
    rowData: Object,
  },
};
</script>