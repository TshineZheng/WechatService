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

    <div class="qr-error" v-if="qrStage === 1">
      <p>{{qrRequestMsg}}</p>
      <ElButton type="primary" @click="retry">重试</ElButton>
    </div>

    <div class="qr" v-if="qrStage === 2">
      <ElRow type="flex" justify="center">
        <ElCol :span="5">
          <ElCard :body-style="{ padding : '0px'}">
            <img class="image" :src="qrUrl" />
          </ElCard>
          <p>请扫描二维码登录</p>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      qrUrl:
        'https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1563029353&di=c81432783d94bd3e9b37f528a86344f0&src=http://b-ssl.duitang.com/uploads/item/201601/22/20160122003337_ZxyWu.jpeg',
      // 0 请求发送 1 请求错误 2 请求正常返回，已经获取到二维码
      qrStage: 1,
      // 请求信息
      qrRequestMsg: '请求错误'
    }
  },
  methods: {
    retry () {
      // TODO: 发送请求
      this.qrStage = 0
    }
  },
};
</script>

<style scoped>
.image {
  width: 100%;
  display: block;
}
</style>