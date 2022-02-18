<template>
  <div
    class="fixed overflow-y-auto inset-0 flex justify-center items-center z-50"
  >
    <div class="relative mx-auto w-auto max-w-2xl">
      <div class="bg-white w-100 rounded-lg shadow-md p-4">
        <div class="flex">
          <h4 class="text-lg font-bold">
              Create new experiment
          </h4>
          <button
            @click="this.$emit('close')"
            class="bg-white hover:bg-gray-light px-2 py-0.5 rounded-full"
          >
            <fa-icon icon="times"></fa-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>