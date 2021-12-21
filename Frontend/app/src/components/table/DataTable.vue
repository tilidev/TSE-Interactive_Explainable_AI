<template>
  <div class="flex justify-center">
    <div class="overflow-auto shadow-md">
      <table class="table-auto text-primary shadow-lg text-left">
        <thead class="bg-primary text-white">
          <table-header
            @apply-sorting="applySorting"
            :labels="data.labels"
            :descriptions="data.descriptions"
            :sorting="data.sorting"
          />
        </thead>
        <tbody class="divide-gray divide-y">
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
  methods: {
    applySorting(sorting) {
      this.$emit('apply-sorting', sorting);
    }
  }
};
</script>