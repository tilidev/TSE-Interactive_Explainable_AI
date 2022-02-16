<template>
  <div>
      <login-screen v-if="!authenticated" @logged-in="authenticated = true"></login-screen>
      <div v-if="authenticated">You're logged in</div>
  </div>
</template>

<script>
import LoginScreen from '../components/LoginScreen.vue'

export default {
    data() {
        return {
            authenticated: false,
        }
    },
    components: {
        LoginScreen
    }
}
</script>

<style>

</style>