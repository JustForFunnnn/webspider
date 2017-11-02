# Lagou Spider

[![Build Status](https://travis-ci.org/GuozhuHe/webspider.png)](https://travis-ci.org/GuozhuHe/webspider)

> 如果感觉项目还不错，给个 Star 吧  `_(:з」∠)_`

--|--
---- | ----
Version | 1.0.1
WebSite | http://www.jobinfo.cc:8000/
Source |  https://github.com/GuozhuHe/webspider
Keywords |  `Python3`, `Tornado`, `Celery`, `Spider`, `Lagou`, `Requests`

爬取到的数据分享链接: https://pan.baidu.com/s/1gfIi5gv 密码: `gikp`

## 关于本系统

本系统是一个主要使用`python3`, `celery`和`requests`来爬取职位数据的爬虫，实现了定时任务，出错重试，日志记录，自动更改`Cookies`等的功能，并使用`ECharts` + `Bootstrap` 来构建前端页面，来展示爬取到的数据。

## 展示页面

![Alt text](job-chart.jpeg)

## Quick Start
> 以下操作均是在 `Linux - Ubuntu` 环境下执行

* 克隆项目

```bash
git clone git@github.com:GuozhuHe/webspider.git
```

* 安装 `MySQL`, `Redis`, `Python3`

```bash
# 安装 redis
apt-get install redis-server

# 后台启动 redis-server
nohup redis-server &

# 安装 python3
apt-get install python3

# 安装 MySQL
apt-get install mysql-server

# 启动 MySQL
sudo service mysql start
```

* 配置数据库和表
```mysql
# 创建数据库
CREATE DATABASE `spider` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# 还需要创建相关表，表的定义语句在 tests/schema.sql 文件中，可自行复制进 MySQL 命令行中执行。
```

* 在项目根目录下构建
```bash
make
# 构建成功后项目的 env/bin 目录下会有可执行脚本
```

* 执行单元测试
```bash
make test
```

* 代码风格检查
```bash
make flake8
```

* 运行 `Web Server`
```bash
env/bin/web
```

* 运行爬虫程序
```bash
# 启动定时任务分发器
env/bin/celery_beat
# 启动爬取 职位数据 的 worker(每个月自动执行一次)
env/bin/celery_lagou_data_worker
# 启动爬取 职位数量 的 worker(每天晚上自动执行一次)
env/bin/celery_jobs_count_worker 
```

* env/bin 目录下其他可执行脚本
```bash
# 直接爬取职位数量
env/bin/crawl_jobs_count        
# 直接爬取职位数据
env/bin/crawl_lagou_data       
# 启动celery监控 
env/bin/celery_flower            
```

* 清除构建信息
```bash
make clean
```

## TODO
* 前后端分离
* 重构数据库访问方式

## 其他常见问题
有问题？联系我解决:
* `E-mail`: `heguozhu@zhihu.com`
* `QQ`: `188003202`
