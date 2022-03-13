
<template>
  <transition name="fade">
    <div class="shadow-blurred fixed inset-0 w-32 flex flex-col justify-stretch bg-white items-stretch z-50">
      <div>

      <div>Hi</div></div>
    </div>
  </transition>
</template>

<script>
export default {};
</script>

<style scoped>
.fade-enter-from {
  opacity: 0;
}
.fade-enter-to {
  opacity: 1;
}
.fade-enter-active {
  transition: all 1s ease;
}
.fade-leave-from {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
}
.fade-leave-active {
  transition: all 1s ease;
}
</style>


