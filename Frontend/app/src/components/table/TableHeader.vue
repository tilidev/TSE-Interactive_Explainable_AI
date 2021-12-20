<template>
  <tr class="rounded-md border-gray-light">
    <th
      class="py-5 pt-5 px-10 font-bold"
      v-for="(label, key) in labels"
      :key="key"
    >
      {{ label
      }}<fa-icon
        @click="hoverText = hoverText ? '' : descriptions[key]"
        @mouseover="hoverText = descriptions[key]"
        @mouseleave="hoverText = ''"
        icon="info-circle"
        class="ml-2"
      />
      <div
        v-if="hoverText == descriptions[key]"
        class="
          modal
          fixed
          inset-0
          flex
          items-center
          justify-center
          z-50
        "
      >
        <div class="p-4 bg-white font-regular text-primary-dark shadow rounded-md">
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
  },
};
</script>