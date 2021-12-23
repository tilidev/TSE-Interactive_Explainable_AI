<template>
  <tr class="rounded-md border-gray-light">
    <th class="py-5 px-10 font-bold" v-for="attribute in [...['id'], ...attributes, ...['NN_recommendation', 'NN_confidence']]" :key="attribute">
      <span @click="applySorting(attribute)">
      <fa-icon
        class="align-text-bottom"
        v-if="sort_by == attribute && desc == false"
        icon="sort-up"
        size="xs"
      />
      <fa-icon
        class="align-text-top"
        v-if="sort_by == attribute && desc == true"
        icon="sort-down"
        size="xs"
      />
      {{ labels[attribute]
      }}</span><fa-icon
        @click="hoverText = hoverText ? '' : descriptions[attribute]"
        @mouseover="hoverText = descriptions[attribute]"
        @mouseleave="hoverText = ''"
        icon="info-circle"
        class="ml-2"
      />
      <div
        v-if="hoverText == descriptions[attribute]"
        class="modal fixed inset-0 flex items-center justify-center z-50"
      >
        <div
          class="p-4 bg-white font-regular text-primary-dark shadow rounded-md"
        >
          {{ hoverText }}
        </div>
      </div>
    </th>
  </tr>
</template>

<script>
export default {
  data() {
    return {
      hoverText: "",
    };
  },
  props: {
    labels: Object,
    descriptions: Object,
    sorting: Object,
    attributes: Array,
    sort_by: String,
    desc: Boolean,
  },
  methods: {
    applySorting(attribute) {
      const newSorting = {sort_by : attribute, desc : (this.desc == false && this.sort_by == attribute)? true : false};
      this.$emit('apply-sorting', newSorting);
    }
  }
};
</script>