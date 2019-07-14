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
import axios from 'axios'
export default {
  components: {
    QR
  },
  data () {
    return {
      isLogin: false
    };
  },
  created () {
    axios.get('/api/login/check')
      .then(res => {
        this.isLogin = res.data.data.login
        console.log(res)
      })
      .catch(err => {
        console.error(err);
      })
  },
};
</script>

<style scoped>
</style>