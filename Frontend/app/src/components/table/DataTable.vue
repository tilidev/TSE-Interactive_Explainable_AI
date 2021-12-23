<template>
  <div class="flex justify-center">
    <div class="overflow-auto shadow-md">
      <table class="table-auto text-primary shadow-lg text-left">
        <thead class="bg-primary text-white">
          <table-header
            @apply-sorting="applySorting"
            :labels="attributeData.labels"
            :descriptions="attributeData.descriptions"
            :sort_by="optionsData.sort_by"
            :desc="optionsData.desc"
            :attributes="optionsData.attributes"
          />
        </thead>
        <tbody class="divide-gray divide-y">
          <table-row v-for="row in tableRows" :key="row.id" :rowData="row" />
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
    tableRows: Array,
    attributeData: Object,
    optionsData: Object,
  },
  components: { TableRow, TableHeader },
  methods: {
    applySorting(sorting) {
      this.$emit("apply-sorting", sorting);
    },
  },
};
</script>