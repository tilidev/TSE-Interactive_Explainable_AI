<template>
<div>
  <div class="font-bold text-lg mb-4">Please enter the admin password to enter</div>
  <input class="mb-4" v-model="userInput" type="password" placeholder="Password">
  <default-button @click="clickLogin">Login</default-button>
  </div>

</template>

<script>
import DefaultButton from './buttons/DefaultButton.vue';
export default {
  components: { DefaultButton },
  methods: {
    clickLogin() {
      if (this.userInput == this.password) {
        this.$emit("logged-in");
      }
      else {
        alert("Sorry, wrong password");
        this.userInput = ""
      }
    }
  },
  data() {
    return {
      userInput: "",
      password: "ilovekoeri",
    };
  },
};
</script>

<style>
</style>