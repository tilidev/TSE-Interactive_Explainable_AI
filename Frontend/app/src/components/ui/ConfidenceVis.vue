<template>
  <div v-if="confidence < 0.75" class="text-cc-low font-bold">
    <span class="rounded-lg bg-cc-low text-white px-2 py-1 mr-2"
      >{{ Math.round(confidence * 100) }}%</span
    ><span>Low</span>
  </div>
  <div v-else-if="confidence >= 0.9" class="text-cc-high font-bold">
    <span class="rounded-lg bg-cc-high text-white px-2 py-1 mr-2"
      >{{ Math.round(confidence * 100) }}%</span
    ><span>High</span>
  </div>
  <div
    v-else-if="confidence >= 0.75"
    class="text-cc-medium font-bold"
  >
    <span class="rounded-lg bg-cc-medium text-white px-2 py-1 mr-2"
      >{{ Math.round(confidence * 100) }}%</span
    ><span>Medium</span>
  </div>
</template>

<script>
export default {
  props: { confidence: Number },
};
</script>

<style>
</style>