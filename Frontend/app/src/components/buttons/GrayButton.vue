<template>
  <div>
    <button
      class="
        btn
        bg-gray-light 
        hover:bg-gray 
        text-primary-text
        px-2
        py-0.5
        rounded-md
        text-xs
        font-extralight
        m-4
      "
    >
      <slot />
      </button>
  </div>
</template>

<script>
export default {

  data() {
    return {
       clicked: false
    }
  }
}
</script>