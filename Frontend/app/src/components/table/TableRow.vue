<template>
  <tr class="bg-gray-light hover:bg-white border-2 border-primary">
    <td class="p-3 text-primary">{{rowData.other.id}}</td>
    <td class="p-3" v-for="value in rowData.attributes" :key="value">{{ value }}</td>
    <td class="p-3" >{{rowData.other.NN_recommendation}}</td>
    <td class="p-3">{{rowData.other.NN_confidence}}</td>
  </tr>
</template>

<script>
export default {
  props: {
    rowData: Object,
  },
  mounted() {

  }
};
</script>