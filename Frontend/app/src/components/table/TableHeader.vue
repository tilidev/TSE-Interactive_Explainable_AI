<template>
  <tr class="rounded-md border-gray-light">
    <th
      class="py-5 px-8 font-bold"
      v-for="attribute in extendedAttributes"
      :key="attribute"
    >
      <span @click="applySorting(attribute)" class="cursor-pointer">
        <fa-icon
          class="align-text-bottom -ml-3"
          v-if="sort_by == attribute && desc == false"
          icon="sort-up"
          size="xs"
        />
        <fa-icon
          class="align-text-top -ml-3"
          v-if="sort_by == attribute && desc == true"
          icon="sort-down"
          size="xs"
        />
        {{ labels[attribute] }}</span
      ><fa-icon
        @click="hoverText = hoverText ? '' : descriptions[attribute]"
        @mouseover="hoverText = descriptions[attribute]"
        @mouseleave="hoverText = ''"
        icon="info-circle"
        class="ml-2"
      />
      <div
        v-if="hoverText == descriptions[attribute]"
        class="mt-8 absolute z-50"
      >
        <div
          class="
            p-4
            bg-white
            font-normal
            text-primary-dark
            shadow-blurred
            rounded
          "
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
  computed: {
    extendedAttributes() {
      return [
        ...["id"],
        ...this.attributes,
        ...["NN_recommendation", "NN_confidence"],
      ];
    },
  },
  methods: {
    applySorting(attribute) {
      const newSorting = {
        sort_by: attribute,
        desc: this.desc == false && this.sort_by == attribute ? true : false,
      };
      this.$emit("apply-sorting", newSorting);
    },
  },
};
</script>