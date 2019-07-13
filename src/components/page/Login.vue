<template>
  <div class="login">
    <div v-if="isLogin">
      <p>已经登录,是否退出?</p>
    </div>
    <QR v-else></QR>
  </div>
</template>

<script>
import QR from "@/components/common/QR.vue";
export default {
  components: {
    QR
  },
  data() {
    return {
      isLogin: false
    };
  }
};
</script>

<style scoped>
</style>