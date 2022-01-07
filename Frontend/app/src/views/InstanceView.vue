<template>
  <div><info-card :instanceInfo="instanceInfo"></info-card></div>
</template>

<script>
import InfoCard from '../components/InfoCard.vue'

export default {
    data() {
        return {
            instanceInfo: {}
        }
    },
  props: { id: Number },
  components: {InfoCard}
};
</script>

<style>
</style>