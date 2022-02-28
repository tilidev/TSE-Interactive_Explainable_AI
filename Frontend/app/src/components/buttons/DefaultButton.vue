<template>
  <div>
    <button
        :class="getStyling()"
    >
      <slot/>
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    getStyling() {
      let paddingClass = "";
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
      return paddingClass + " btn rounded-md font-bold border border-transparent" + " bg-" + this.color + " hover:bg-" + this.hoverColor + " text-"
          + this.textColor + " text-" + this.size;
    }
  },
  props: {
    // The button's main color, needs to be a color defined by tailwind
    color: {
      type: String,
      required: false,
      default: "primary"
    },
    // The button's hover color, needs to be a color defined by tailwind
    hoverColor: {
      type: String,
      required: false,
      default: "primary-dark"
    },
    // The button's text hover color, needs to be a color defined by tailwind
    textColor: {
      type: String,
      required: false,
      default: "white"
    },
    // The button's size, can be sm, base, lg, xl, 2xl, ..., 9xl
    size: {
      type: String,
      required: false,
      default: 'lg'
    }
  }
};
</script>
