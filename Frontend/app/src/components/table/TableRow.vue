<template>
  <tr class="bg-gray-light hover:bg-white border-2 border-primary shadow">
    <td class="py-5 px-10 text-primary">{{ rowData.other.id }}</td>
    <td class="py-5 px-10" v-for="value in rowData.attributes" :key="value">
      {{ value }}
    </td>
    <td class="py-5 px-10 bg-positive-light font-bold">
      {{ rowData.other.NN_recommendation }}
    </td>
    <td class="py-5 px-10 bg-cc-medium font-bold">
      {{ rowData.other.NN_confidence }}
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