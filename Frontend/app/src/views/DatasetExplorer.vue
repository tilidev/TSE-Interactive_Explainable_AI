<template>
  <div class="dataset">
    <h1>The table with the loan application data will be displayed here</h1>
    <default-button>Default Button</default-button>
    <clear-button>Clear Button</clear-button>
    <outline-button>Outline Button</outline-button>
  </div>
</template>

<script>
import DefaultButton from "../components/buttons/DefaultButton.vue";
import ClearButton from "../components/buttons/ClearButton.vue";
import OutlineButton from "../components/buttons/OutlineButton.vue"
export default {
  components: { DefaultButton, ClearButton, OutlineButton },
};
</script>