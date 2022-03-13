<template>
  <div
    class="flex space-x-2 items-center cursor-pointer bg-white shadow py-2 px-4"
    @click="this.$router.push(getRoute())"
  >
    <fa-icon size="xl" :icon="type == 'dataset' ? 'table' : 'cog'"></fa-icon>
    <div>{{ type == "dataset" ? "Dataset Explorer" : "Admin Panel" }}</div>
  </div>
</template>

<script>
export default {
  props: { type: String },
  methods: {
    getRoute() {
      return this.type == "dataset" ? "/dataset" : "/admin";
    },
  },
};
</script>