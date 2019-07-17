# 微信小服务
主要功能是可以挂在服务器上做微信消息服务。  
比如你有一个温度监控服务，发现服务器温度太高，调用本服务的发送消息接口即可向指定微信联系人发送消息。

# 快速使用  
1. 确保你的电脑或服务器有安装 docker 和 docker-compose。  
2. 项目根目录下执行 `docker-compose up --build`  
3. 浏览器访问 [localhost:9910](http://localhost:9910)  
4. 点击登陆，打开手机微信扫码登入即可。  

# 部署
两种方式  
- DOCKER 方式  
  根目录执行 `docker-compose up --build` ，需要后台执行的话加上 `-d` 选项。  

- 手动  
	- backend  
		确保 `requirements.txt` 中的依赖已安装（主要是 flask 和 itchat），运行 `python wechat.py` 即可。  
	- web  
		需要配合 nginx 做部署，同时需配置指向 backend 的反向代理，配置样例查看 [web/nginx/default.conf](web/nginx/default.conf)  

# 运行  
backend 和 web 部署完毕后，浏览器访问 web 所在的地址即可，docker-compose 部署默认地址为[localhost:9910](http://localhost:9910)  

# API  

| 功能     | 请求                                    | 备注 |
| -------- | --------------------------------------- | ---- |
| 发送消息 | {Backend}/api/send/{username}/{message} |      |
| 登陆     | {Backend}/api/login                     |      |
| 登陆检测 | {Backend}/api/login/check               |      |

> docker-compose 配置了 nginx 反代所有 `/api` 开头的请求到 backend， 所以可以直接通过 web 所在的地址访问 backend，比如：[localhost:9910/api/send/特困生/好困啊](http://localhost:9910/api/send/特困生/好困啊)  
> backend 默认端口是 6637

# Ref
Backend：itchat、flask、etc  
Web：Vue、etc  