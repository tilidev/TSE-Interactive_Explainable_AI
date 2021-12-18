<template>
  <div class="flex justify-center">
      <div class="overflow-auto">
        <table class="text-text border-separate w-full">
          <thead class="bg-gray">
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

<style>
table {
  border-spacing: 0 6px;
}
td:first-child {
    border-top-left-radius: 0.375rem; 
    border-bottom-left-radius: 0.375rem;
}
td:last-child{
    border-bottom-right-radius: 0.375rem; 
    border-top-right-radius: 0.375rem; 
}
th:first-child {
    border-top-left-radius: 0.375rem; 
    border-bottom-left-radius: 0.375rem;
}
th:last-child{
    border-bottom-right-radius: 0.375rem; 
    border-top-right-radius: 0.375rem; 
}
</style>