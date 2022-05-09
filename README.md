#

[![Build Status](https://travis-ci.org/JustForFunnnn/webspider.svg)](https://travis-ci.org/JustForFunnnn/webspider)
[![codecov](https://codecov.io/gh/JustForFunnnn/webspider/branch/master/graph/badge.svg)](https://codecov.io/gh/JustForFunnnn/webspider)
[![Code Health](https://landscape.io/github/JustForFunnnn/webspider/master/landscape.svg?style=flat)](https://landscape.io/github/JustForFunnnn/webspider/master)
[![License](https://img.shields.io/github/license/JustForFunnnn/webspider.svg)](https://github.com/JustForFunnnn/webspider/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/python-3-ff69b4.svg)](https://github.com/JustForFunnnn/webspider)

| --       | --                                         |
| -------- | ------------------------------------------ |
| Version  | 1.0.1                                      |
| WebSite  | http://119.23.223.90:8000                  |
| Source   | https://github.com/JustForFunnnn/webspider |
| Keywords | `Python3`, `Tornado`, `Celery`, `Requests` |

## 项目简介

本项目使用的编程语言是`python3`，数据库用的是`MySQL`, 主要用到的库是`celery`和`requests`，并实现了定时任务，出错重试，日志记录，自动更改`Cookies`等的功能，使用`ECharts` + `Bootstrap` 来构建前端页面。

## 展示页面

![Alt text](job-chart.jpg)

## Quick Start
> 以下操作均是在 `Linux - Ubuntu` 环境下执行

* 克隆项目

```bash
git clone git@github.com:JustForFunnnn/webspider.git
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
# 启动爬取 数据 的 worker
env/bin/celery_lg_data_worker
# 启动爬取 职位数据 的 worker
env/bin/celery_lg_jobs_data_worker
# 启动爬取 职位数量 的 worker
env/bin/celery_lg_jobs_count_worker
```

* env/bin 目录下其他可执行脚本
```bash
# 直接爬取职位数量
env/bin/crawl_lg_jobs_count
# 直接爬取职位数据
env/bin/crawl_lg_data
# 启动celery监控
env/bin/celery_flower
```

* 清除构建信息
```bash
make clean
```
