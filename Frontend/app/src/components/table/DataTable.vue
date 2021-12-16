<template>
  <div>
    <table class="w-full table-auto">
      <thead>
        <table-header
          :labels="data.labels"
          :descriptions="data.descriptions"
          :sorting="data.sorting"
        />
      </thead>
      <tbody>
        <table-row v-for="row in data.rows" :key="row.id" :rowData="row" />
      </tbody>
    </table>
  </div>
</template>

<script>
import TableHeader from "./TableHeader.vue";
import TableRow from "./TableRow.vue";
export default {
  props: {
    data: Object,
  },
  components: { TableRow, TableHeader },
};
</script>