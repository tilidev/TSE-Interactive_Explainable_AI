<template>
  <div class="dataset">
    <data-table v-bind:data=tableData ></data-table>
  </div>
</template>

<script>
import DataTable from "../components/table/DataTable.vue"


export default {
  data() {
    return {
      tableData : [{id: "1", }],
      requestBody: {},
    }
  },
  components: { DataTable },
};
</script>
