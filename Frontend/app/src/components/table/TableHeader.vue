<template>
  <tr class="rounded-md shadow">
    <th class="py-5 px-10" v-for="label in labels" :key="label">{{ label }}</th>
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