<template>
  <div>
      <login-screen v-if="!authenticated"></login-screen>
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