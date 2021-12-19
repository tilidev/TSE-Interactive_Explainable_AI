<template>
  <tr class="bg-white hover:bg-gray">
    <td class="py-5 px-10 text-primary">{{rowData.other.id}}</td>
    <td class="py-5 px-10" v-for="value in rowData.attributes" :key="value">{{ value }}</td>
    <td class="py-5 px-10 text-green-500 font-bold" ><fa-icon icon="check" class=""></fa-icon><span class="pl-2">{{rowData.other.NN_recommendation}}</span></td>
    <td class="py-5 px-10 text-blue-500 font-bold "><span class="rounded-lg bg-blue-500 text-white px-2 py-1 mr-2">90%</span><span class="">High</span></td>
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