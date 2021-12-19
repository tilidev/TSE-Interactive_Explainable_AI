<template>
  <tr class="rounded-md border-gray-light">
    <th class="py-5 pt-5 px-10 font-bold" v-for="label in labels" :key="label">
      {{ label }}
    </th>
  </tr>
</template>

<script>
export default {
  props: {
    labels: Object,
    descriptions: Object,
    sorting: Object,
  },
};
</script>