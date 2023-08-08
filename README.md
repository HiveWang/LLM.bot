# LLM.bot
## 一、Verctory Database: Milvus
1.install milvus:standalone mode
## 安装

使用 Docker Compose 安装 Milvus 单机版

### **下载YAML文件**

[手动下载](https://github.com/milvus-io/milvus/releases/download/v2.2.12/milvus-standalone-docker-compose.yml) **`milvus-standalone-docker-compose.yml`**并保存**`docker-compose.yml`**，或使用以下命令。

```java
$ wget https://github.com/milvus-io/milvus/releases/download/v2.2.12/milvus-standalone-docker-compose.yml -O docker-compose.yml
```

### **启动 Milvus**

在与该文件相同的目录中**`docker-compose.yml`**，通过运行以下命令启动 Milvus：

```
$ sudo docker-compose up -d
```

```
Creating milvus-etcd  ... done
Creating milvus-minio ... done
Creating milvus-standalone ... done
```

现在检查容器是否已启动并正在运行。

```
$ sudo docker-compose ps
```

Milvus Standalone 启动后，将会运行三个 docker 容器，包括 Milvus Standalone 服务及其两个依赖项。

```
      Name                     Command                  State                            Ports
--------------------------------------------------------------------------------------------------------------------
milvus-etcd         etcd -advertise-client-url ...   Up             2379/tcp, 2380/tcp
milvus-minio        /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp
milvus-standalone   /tini -- milvus run standalone   Up             0.0.0.0:19530->19530/tcp, 0.0.0.0:9091->9091/tcp
```

### 停止 Milvus

要停止 Milvus 独立运行，请运行：

```
sudo docker-compose down
```

要在停止 Milvus 后删除数据，请运行：

```
sudo rm -rf  volumes
```
### Remote access for standalone mode
1.local transport :
ssh -L 19530:0.0.0.0:19530 -p {port} {user}@{milvus host}

## 二、Embedding doc with openAI
https://milvus.io/docs/integrate_with_openai.md#Similarity-Search-with-Milvus-and-OpenAI
