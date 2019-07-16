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
      <SendMessage></SendMessage>
    </div>
    <div v-else-if="loginState === 3">
      <ElButton v-show="!showQR" type="primary" @click="login">登录</ElButton>
      <QR v-if="showQR"></QR>
    </div>
  </div>
</template>

<script>
import QR from "@/components/common/QR.vue";
import SendMessage from "@/components/common/SendMessage"
import axios from 'axios'

var LoginState = {
  CHECK: 0,
  CHECK_FAILED: 1,
  ONLINE: 2,
  OFFLINE: 3
}

export default {
  components: {
    QR,SendMessage
  },
  data () {
    return {
      // 0 正在检测 1 检测错误 2 已登录 3 未登录
      loginState: LoginState.CHECK,
      msg: '',
      timerLogin: null,
      showQR: false
    };
  },
  created () {
    this.checkLoginTimer()
  },
  methods: {
    login () {
      this.showQR = true
    },
    loginCheck () {
      axios.get('/api/login/check')
        .then(res => {
          let state = res.data.data.login ? LoginState.ONLINE : LoginState.OFFLINE

          // 如果之前的状态不是离线, 新的状态是离线，则切换 QR 组件，当用户点击登录时，通过 v-if 重新执行 QR 组件的登录逻辑
          if (this.loginState != LoginState.OFFLINE && state === LoginState.OFFLINE) {
            this.showQR = false
          }

          this.loginState = state
          console.debug('CheckLogin oldState = ' + this.loginState + ' newState = ' + state)
        })
        .catch(err => {
          this.msg = err.message
          this.loginState = LoginState.CHECK_FAILED
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
      this.loginState = LoginState.CHECK
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