<template>
  <div class="qr-root">
    <div class="qr-loading"
         v-if="qrStage === 0"
         v-loading="qrStage === 0"
         element-loading-text="正在请求微信登录二维码"
         element-loading-spinner="el-icon-loading"
         element-loading-background="rgba(0, 0, 0, 0.8)"></div>

    <div class="qr-error"
         v-else-if="qrStage === 1">
      <p class="text">{{qrRequestMsg}}</p>
      <ElButton type="primary"
                @click="retry">重试</ElButton>
    </div>

    <div class="qr"
         v-else>
      <ElRow type="flex"
             justify="center">
        <ElCol :span="5">
          <ElCard :body-style="{ padding : '0px'}">
            <img class="image"
                 :src="qrUrl" />
          </ElCard>

          <p v-if="qrStage === 2"
             class="text">请扫描二维码登录</p>
          <div v-else-if="qrStage === 3">
            <p>二维码失效</p>
            <ElButton type="primary"
                      @click="retry">刷新</ElButton>
          </div>
          <div v-else-if="qrStage === 4">
            <p>请在APP上点击登陆</p>
          </div>
          <div v-else-if="qrStage === 5">
            <p>登陆超时</p>
            <ElButton type="primary"
                      @click="retry">刷新</ElButton>
          </div>
          <div v-else-if="qrStage === 6">
            <p>登陆成功</p>
          </div>
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
      qrUrl: process.env.BASE_URL + '/qr',
      // 0 请求发送 1 请求错误 2 请求正常返回，已经获取到二维码 3 二维码失效 4 二维码被扫 5 二维码被扫超时 6 登陆成功
      qrStage: 0,
      // 请求信息
      qrRequestMsg: '请求错误',
      qrTimestamp: 0,
      timerQR: null,
    }
  },
  methods: {
    login () {
      // 请求登陆
      axios.get('/api/login')
        .then(res => {
          console.debug(res)
          this.checkQRTimer()
        })
        .catch(err => {
          this.qrError(err.message)
        })
    },
    retry () {
      this.qrStage = 0
      this.login()
    },
    qrError (msg) {
      this.qrRequestMsg = msg
      this.qrStage = 1
      this.checkQRTimerClose()
      console.log('获取QR错误：' + msg)
    },
    checkQR () {
      // 检测二维码
      axios.get('/api/qr/check')
        .then(res => {
          console.debug(res)
          if (this.qrTimestamp < res.data.data.qr_time) {
            this.qrTimestamp = res.data.data.qr_time
            // 用这种方式更新 url ，只在 url 最后加入时间，这样 vue 就会认为图片改变了，就会重新获取，而服务器不处理这个时间即可。
            this.qrUrl = process.env.BASE_URL + '/qr?t=' + this.qrTimestamp
            console.debug('更新QR')
          }

          let code = res.data.code
          if (code === 200) {
            //console.log('二维码获取到了')
            this.qrStage = 2
          } else if (code === 201) {
            console.log('还没拿到QR继续等待')
          } else if (code == 202) {
            let wxcode = res.data.data.wechat_error_code
            if (wxcode === 201) {
              console.log('二维码被扫')
              this.qrStage = 4
            }
            else if (wxcode === 400) {
              console.log('二维码确认超时')
              // this.checkQRTimerClose()
              this.qrStage = 5
            } else if (wxcode === 200) {
              this.qrStage = 6
              console.log('登陆成功')
              this.checkQRTimerClose()
            }
            else if (wxcode === 408) {
              console.log('二维码疑似失效')
              this.qrStage = 3
            }
            else {
              this.qrError(res.data.msg + ' 状态码：' + res.data.data.wechat_error_code)
            }
          } else {
            this.qrError(res.data.msg)
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
    this.login()
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