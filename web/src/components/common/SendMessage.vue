<template>
  <ElRow type="flex" justify="center">
    <ElCol :span="12">
      <div style="margin: 20px 0;"></div>
      <ElInput v-model="username" placeholder="用户名，可以是备注名" type="text"></ElInput>
      <div style="margin: 20px 0;"></div>
      <ElInput v-model="message" placeholder="信息" type="textarea" :autosize="{ minRows: 3}"></ElInput>
      <div style="margin: 20px 0;"></div>
      <p>通过<span style="color: orange;">ip:port/send/{username}/{message}</span> 可直接发送消息</p>
      <div style="margin: 20px 0;"></div>
      <ElButton type="primary" @click="send">发送</ElButton>
    </ElCol>
  </ElRow>
</template>

<script>
import axios from 'axios'

String.prototype.trim = function () {
  return this.replace(/(^\s*)|(\s*$)/g, "");
}
function isEmpty (str) {
  if (str == null || typeof str == "undefined" || str.trim() == "") {
    return true;
  }
  else {
    return false;
  }
}

export default {
  data () {
    return {
      username: '',
      message: ''
    }
  },
  methods: {
    send () {
      if (isEmpty(this.username) || isEmpty(this.message)) {
        this.$message({
          message: '用户名和消息不得为空',
          type: 'warning'
        });
        return
      }

      axios.post('/api/send/' + this.username + '/' + this.message)
        .then(res => {
          let code = res.data.code
          if (code === 200) {
            this.$message({
              message: '发送成功',
              type: 'success'
            });
            this.message = ''
          } else {
            this.$message({
              message: res.data.msg,
              type: 'error'
            });
          }
        })
        .catch(err => {
          this.$message({
            message: err.message,
            type: 'error'
          });
        })
    }
  },

}
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}
</style>