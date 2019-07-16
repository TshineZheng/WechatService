<template>
  <div class="login">
    <div v-if="loginState === 0">
      <p>正在获取登录状态</p>
    </div>
    <div v-else-if="loginState === 1">
      <p>获取登录状态错误</p>
      <p>{{msg}}</p>
      <ElButton type="primary"
                @click="retryLoginCheck">重试</ElButton>
    </div>
    <div v-else-if="loginState === 2">
      <p>已经登录</p>
      <ElButton type="primary"
                @click="logout">退出登录</ElButton>
    </div>
    <div v-else>
      <QR></QR>
    </div>
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
      // 0 正在检测 1 检测错误 2 已登录 3 未登录
      loginState: 0,
      msg: '',
      timerLogin: null,
    };
  },
  created () {
    this.checkLoginTimer()
  },
  methods: {
    loginCheck () {
      axios.get('/api/login/check')
        .then(res => {
          let state = res.data.data.login ? 2 : 3
          this.loginState = state
          console.debug('CheckLogin oldState = ' + this.loginState + ' newState = ' + state)
        })
        .catch(err => {
          this.msg = err.message
          this.loginState = 1
          this.checkLoginTimerClose()
          console.error(err);
        })
    },
    logout () {
      axios.post('/api/logout')
        .then(res => {
          console.log(res)
        })
        .catch(err => {
          console.error(err);
        })
    },
    retryLoginCheck () {
      this.checkLoginTimer()
    },
    checkLoginTimer () {
      this.loginState = 0
      this.checkLoginTimerClose()
      this.timerLogin = setInterval(this.loginCheck, 1000)
    }
    ,
    checkLoginTimerClose () {
      if (this.timerLogin) {
        clearInterval(this.timerLogin)
      }
      this.timerLogin = null
    }
  },
  beforeDestroy () {
    this.checkLoginTimerClose()
  }
};
</script>

<style scoped>
</style>