<template>
  <div>
    <button
      class="
        btn
        bg-primary
        hover:bg-primary-dark
        text-white
        px-4
        py-2
        rounded
        text-lg
        font-bold
      "
    >
      <slot />
    </button>
  </div>
</template>

<script>
export default {
};
</script>
