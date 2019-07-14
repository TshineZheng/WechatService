<template>
  <div class="qr-root">
    <div
      class="qr-loading"
      v-if="qrStage === 0"
      v-loading="qrStage === 0"
      element-loading-text="正在请求微信登录二维码"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    ></div>

    <div class="qr-error" v-else-if="qrStage === 1">
      <p class="text">{{qrRequestMsg}}</p>
      <ElButton type="primary" @click="retry">重试</ElButton>
    </div>

    <div class="qr" v-else-if="qrStage === 2">
      <ElRow type="flex" justify="center">
        <ElCol :span="5">
          <ElCard :body-style="{ padding : '0px'}">
            <img class="image" :src="qrUrl" />
          </ElCard>
          <p class="text">请扫描二维码登录</p>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      qrUrl:
        process.env.BASE_URL + '/qr',
      // 0 请求发送 1 请求错误 2 请求正常返回，已经获取到二维码
      qrStage: 0,
      // 请求信息
      qrRequestMsg: '请求错误',
      timerQR: null,
    }
  },
  methods: {
    retry () {
      // TODO: 发送请求
      this.qrStage = 0
    },
    qrError (msg) {
      this.qrRequestMsg = msg
      this.qrStage = 1
      console.log('获取QR错误：' + msg)
    },
    checkQR () {
      // 检测二维码
      axios.get('/api/qr/check')
        .then(res => {
          if (res.data === 'exist') {
            this.checkQRTimerClose()
            console.log('qr获取到了')
            this.qrStage = 2
          } else if (res.data === 'not') {
            console.log('还没拿到继续等待')
          } else {
            this.qrError(res.data)
          }
        })
        .catch(err => {
          this.qrError(err.message)
        })
    },
    checkQRTimer () {
      this.checkQRTimerClose()
      this.timerQR = setInterval(this.checkQR, 1000)
    }
    ,
    checkQRTimerClose () {
      if (this.timerQR) {
        clearInterval(this.timerQR)
      }
      this.timerQR = null
    }
  },
  created () {
    // 请求登陆
    axios.get('/api/login')
      .then(res => {
        console.log(res)
        this.checkQRTimer()
      })
      .catch(err => {
        this.qrError(err.message)
      })
  },
  beforeDestroy () {
    this.checkQRTimerClose()
  }
};
</script>

<style scoped>
.image {
  width: 100%;
  display: block;
}
.text {
  font-size: 14px;
}
</style>