<template>
  <div>
    <div>id: {{ id }}</div>
    <info-card :instanceInfo="instanceInfo"></info-card>
  </div>
</template>

<script>
import InfoCard from "../components/InfoCard.vue";

export default {
  data() {
    return {
      instanceInfo: {},
      id: this.$route.params.id,
    };
  },
  components: { InfoCard },
};
</script>

<style>
</style>