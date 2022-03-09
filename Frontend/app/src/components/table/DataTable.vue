<template>
    <div v-if="tableRows[0]" class="shadow-md inline-block">
      <table class="table-auto text-primary shadow-lg text-left block">
        <thead class="bg-primary text-white sticky top-0">
          <table-header
            @apply-sorting="applySorting"
            :labels="attributeData.labels"
            :descriptions="attributeData.descriptions"
            :sort_by="optionsData.sort_by"
            :desc="optionsData.desc"

            :attributes="
              Object.keys(tableRows[0])
            "
          />
        </thead>
        <tbody class="divide-gray divide-y top-8">
          <table-row v-for="row in tableRows" :key="row.id" :rowData="row" />
        </tbody>
      </table>
    </div>
    <div v-else-if="!tableRows[0] && optionsData.filter.length"><div class="text-3xl font-bold py-2">Nothing to show</div><div class="text-lg">Try removing filters to see more results</div></div>
</template>

<script>
import TableHeader from "./TableHeader.vue";
import TableRow from "./TableRow.vue";
export default {
  mounted() {},
  props: {
    tableRows: Array,
    attributeData: Object,
    optionsData: Object,
    isFilterApplied: Boolean,
  },
  components: { TableRow, TableHeader },
  methods: {
    applySorting(sorting) {
      this.$emit("apply-sorting", sorting);
    },
  },
};
</script>