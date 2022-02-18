<template>
  <div>
      <login-screen v-if="!authenticated" @logged-in="authenticated = true"></login-screen>
      <admin-view v-if="authenticated"></admin-view>
  </div>
</template>

<script>
import LoginScreen from '../components/admin/LoginScreen.vue'
import AdminView from './AdminView.vue'

export default {
    data() {
        return {
            authenticated: true,
        }
    },
    components: {
        AdminView,
        LoginScreen
    }
}
</script>

<style>

</style>