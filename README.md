# pornbot91_py
91视频下载，发送电报




###  特点

尽量异步的方式处理,下载速度大幅提升,实测很快(100M视频,下载+合并用时18秒)

破解91视频的播放限制、理论上可以无限下载

为标题添加中文分词标签，解决电报对中文搜索的问题

重试机制，网络超时重试

向机器人发送链接，可以 `获取视频真实地址` 并 `下载视频`

docker预装环境，方便更换服务，一键启动


### 软件安装



#### 安装 docker
```
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh --mirror Aliyun&&systemctl enable docker&&systemctl start docker

```

#### 安装docker-compose

```yaml
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose &&chmod +x /usr/local/bin/docker-compose
```


### 配置
创建目录 /pybot
```yaml
mkdir /pybot
```
### 编辑docker-compose.yml

```angular2html
      #windows配置环境变量需要重启电脑
      REDIS_HOST: 11.11.22.333
      REDIS_PORT: 16379
      REDIS_PASS: 424243
      API_ID: 21231221
      API_HASH: *************************
      BOT_TOKEN: *****:**************************
      #定时任务发送的群组id(@get_id_bot,可以在这里获取到)
      GROUP_ID: 121231311
```

### 启动项目

```yaml
docker-compose up 
```


### 测试

发送 /start 到机器人

得到回复  `********`
