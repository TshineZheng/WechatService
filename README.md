# 运行
## DOCKER
根目录执行 `docker-compose up --build` ，需要后台执行加上 `-d` 选项。

## 本地
### backend
确保 `requirements.txt` 中的依赖已安装，运行 `python wechat.py` 即可。

### web
需要配合 nginx 做部署，同时需配置指向 backend 的反向代理，配置样例查看 [web/nginx/default.conf](web/nginx/default.conf)
