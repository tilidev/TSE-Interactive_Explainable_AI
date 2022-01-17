<template>
  <div>
    <button @click="this.clicked = !this.clicked"
    v-if="this.clicked == false"
      class="
        btn
        bg-gray-light 
        hover:bg-gray 
        text-primary-text
        px-1
        py-1
        rounded-md
        text-xs
        font-extralight
        m-4
      "
    >
    <slot />
      </button>
    <button @click="this.clicked = !this.clicked"
    v-else-if="this.clicked == true"
      class="
        btn
        bg-gray-light 
        hover:bg-gray 
        text-blue-800
        px-1
        py-1
        rounded-md
        text-xs
        font-extralight
        border
        border-blue-800
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