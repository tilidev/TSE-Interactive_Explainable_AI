<template>
  <div>
    <div v-if="recommendation == 'Approve'" class="text-positive font-bold">
      <fa-icon icon="check-circle" size="lg"></fa-icon
      ><span class="ml-2">Approve</span>
    </div>
    <div v-if="recommendation == 'Reject'" class="text-negative font-bold">
      <fa-icon icon="times-circle" size="lg"></fa-icon
      ><span class="ml-2">Reject</span>
    </div>
  </div>
</template>

<script>
export default {
  props: { recommendation: String },
};
</script>