<template>
  <div>
    <button @click="this.clicked = !this.clicked"
    v-if="this.clicked == false"
      class="
        btn
        bg-gray-light 
        hover:bg-gray
        px-2
        py-1
        rounded-md
        text-sm
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
        text-primary-light
        px-2
        py-1
        rounded-md
        text-sm
        border
        border-primary-light
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