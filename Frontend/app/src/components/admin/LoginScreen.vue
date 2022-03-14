<template>
  <div>
    <div class="font-bold text-lg mb-4">
      Please enter the admin password to enter
    </div>
    <input
      class="mb-4 rounded border-2 p-2"
      v-model="userInput"
      type="password"
      placeholder="Password"
    />
    <default-button @click="clickLogin">Login</default-button>
  </div>
</template>

<script>
import DefaultButton from "../buttons/DefaultButton.vue";
export default {
  components: { DefaultButton },
  inject: ["apiUrl"],
  methods: {
    clickLogin() {
      const axios = require("axios");
      axios
        .get(this.apiUrl + "authenticate?pwd=" + this.userInput)
        .then(() => this.$emit("logged-in"))
        .catch(() => alert("Sorry, wrong password!"));
    },
  },
  data() {
    return {
      userInput: "",
    };
  },
};
</script>

<style>
</style>