<template>
  <div>
    <div class="flex space-x-4 mb-4 -mt-4 self-start">
      <navigation-button :type="'dataset'"></navigation-button>
    </div>
    <login-screen
      v-if="!authenticated"
      @logged-in="authenticated = true"
    ></login-screen>
    <admin-view v-if="authenticated"></admin-view>
  </div>
</template>

<script>
import LoginScreen from "../components/admin/LoginScreen.vue";
import NavigationButton from "../components/buttons/NavigationButton.vue";
import AdminView from "../components/admin/AdminPanel.vue";

export default {
  data() {
    return {
      authenticated: false,
    };
  },
  components: {
    AdminView,
    LoginScreen,
    NavigationButton,
  },
};
</script>

<style>
</style>