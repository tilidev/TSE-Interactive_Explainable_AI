<template>
  <div>
    <button
        :class="getStyling()"
    >
      <slot />
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    getStyling() {
      let paddingClass = "";
      //TODO: Outsource this to util class to avoid duplicate code
      switch (this.size) {
        case 'sm':
          paddingClass = "px-2 py-1";
          break;
        case 'base':
          paddingClass = "px-4 py-2";
          break;
        case 'lg':
          paddingClass = "px-4 py-2";
          break;
        default:
          paddingClass = "px-6 py-3"
      }
      return paddingClass + " btn rounded-md bg-white font-bold hover:bg-gray-light border border-transparent" + " text-" + this.color
          + " text-" + this.size;
    }
  },
  props: {
    // The button's text color, needs to be a color defined by tailwind
    color: {
      type: String,
      required: false,
      default: "primary"
    },
    // The button's size, can be sm, base, lg, xl, 2xl, ..., 9xl
    size: {
      type: String,
      required: false,
      default: 'lg'
    }
  },
};
</script>