<template>
  <tr class="bg-white hover:bg-gray">
    <td class="py-5 px-10 text-primary">{{rowData.other.id}}</td>
    <td class="py-5 px-10" v-for="value in rowData.attributes" :key="value">{{ value }}</td>
    <td class="py-5 px-10 text-green-500 font-bold text-white" >{{rowData.other.NN_recommendation}}</td>
    <td class="py-5 px-10 text-blue-500 font-bold text-white ">{{rowData.other.NN_confidence}}</td>
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