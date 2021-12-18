<template>
  <tr class="rounded-md">
    <th class="p-3" v-for="label in labels" :key="label">{{ label }}</th>
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