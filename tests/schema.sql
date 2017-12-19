-- CREATE DATABASE `spider` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `job` (
  `id`          INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `title`       VARCHAR(64) NOT NULL COMMENT '职位标题',
  `work_year`   TINYINT  NOT NULL DEFAULT 0 COMMENT '工作年限要求',
  `city_id`     INT UNSIGNED NOT NULL COMMENT '城市',
  `company_id`  INT UNSIGNED NOT NULL COMMENT '公司 id',
  `department`  VARCHAR(64)  NOT NULL DEFAULT '' COMMENT '招聘部门',
  `salary`      VARCHAR(32)  NOT NULL DEFAULT '' COMMENT '薪水',
  `education`   TINYINT  NOT NULL DEFAULT 0 COMMENT '教育背景要求',
  `description` TEXT DEFAULT NULL COMMENT '额外描述',
  `advantage`   VARCHAR(128)  NOT NULL DEFAULT '' COMMENT '职位优势',
  `job_nature`  TINYINT  NOT NULL DEFAULT 0 COMMENT '工作性质',
  `created_at`  INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '职位创建时间',
  `updated_at`  INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '最后更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `company` (
  `id` INT(11) UNSIGNED PRIMARY KEY,
  `city_id` INT(11) UNSIGNED NOT NULL COMMENT '所在城市 id',
  `shortname` VARCHAR(64) NOT NULL COMMENT '公司名称',
  `fullname` VARCHAR(128) NOT NULL COMMENT '公司全称',
  `finance_stage` TINYINT NOT NULL DEFAULT 0 COMMENT '融资阶段',
  `advantage` VARCHAR(128)  NOT NULL DEFAULT '' COMMENT '公司优势',
  `size` TINYINT  NOT NULL DEFAULT 0 COMMENT '公司规模',
  `address` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '公司地址',
  `features` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '公司特点',
  `introduce` TEXT DEFAULT NULL COMMENT '公司简介',
  `process_rate` TINYINT NOT NULL DEFAULT 0  COMMENT '简历处理率',
  `updated_at` INT(11) UNSIGNED NOT NULL DEFAULT 0 COMMENT '最后更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `city` (
  `id` INT(11) UNSIGNED PRIMARY KEY,
  `name` VARCHAR(64) NOT NULL COMMENT '城市名',
  UNIQUE KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `industry` (
  `id` INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(64) NOT NULL COMMENT '行业名称',
  UNIQUE KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `company_industry` (
  `id` INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `company_id` INT(11) UNSIGNED NOT NULL COMMENT '公司 id',
  `industry_id` INT(11) UNSIGNED NOT NULL COMMENT '行业 id',
  `city_id` INT(11) UNSIGNED NOT NULL COMMENT '冗余: 公司所在城市 id',
  UNIQUE KEY(`company_id`, `industry_id`),
  KEY `idx_company_id` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 拉勾预置行业类型
INSERT INTO `industry` (`id`, `name`)
VALUES
(24,'移动互联网'),
(25,'电子商务'),
(26,'社交网络'),
(27,'企业服务'),
(28,'O2O'),
(29,'教育'),
(31,'游戏'),
(32,'旅游'),
(33,'金融'),
(34,'医疗健康'),
(35,'生活服务'),
(38,'信息安全'),
(41,'数据服务'),
(43,'广告营销'),
(45,'文化娱乐'),
(47,'硬件'),
(48,'分类信息'),
(49,'招聘'),
(10594,'其他');
---

CREATE TABLE IF NOT EXISTS `keyword` (
  `id` INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(64) NOT NULL COMMENT '关键词名称',
  UNIQUE KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `job_keyword` (
  `id` INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `job_id` INT(11) NOT NULL COMMENT '工作 id',
  `keyword_id` INT(11) NOT NULL COMMENT '关键词 id',
  `city_id` INT(11) NOT NULL COMMENT '冗余: 公司所在城市 id',
  UNIQUE KEY(`job_id`, `keyword_id`),
  KEY `idx_job_id` (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `jobs_count` (
  `date` INT(11) UNSIGNED COMMENT '日期',
  `keyword_id` INT(11) NOT NULL COMMENT '关键词 id',
  `all_city` INT(11) DEFAULT 0 COMMENT '全国岗位数量',
  `beijing` INT(11) DEFAULT 0 COMMENT '北京岗位数量',
  `guangzhou` INT(11) DEFAULT 0 COMMENT '广州岗位数量',
  `shenzhen` INT(11) DEFAULT 0 COMMENT '深圳岗位数量',
  `shanghai` INT(11) DEFAULT 0 COMMENT '上海岗位数量',
  `hangzhou` INT(11) DEFAULT 0 COMMENT '杭州岗位数量',
  `chengdu` INT(11) DEFAULT 0 COMMENT '成都岗位数量',
  PRIMARY KEY(`date`, `keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
