INSERT INTO `test_spider`.`city`(`id`, `name`)
VALUE (2, '北京'),
      (3, '测试');

INSERT INTO `test_spider`.`company` (`id`, `city_id`, `shortname`, `fullname`, `finance_stage`, `advantage`,
                                    `size`, `address`, `features`, `introduce`, `process_rate`, `updated_at`)
VALUES (10, '2', '测试', '北京测试公司', '1', '舒适的办公环境,年轻富有活力的团队,美女多','3', '北京海淀区的那个地方','一句话简介', '这是公司介绍', '0', '1494931526'),
(11, '2', '豌豆荚', '北京卓易讯畅科技有限公司', '7', '移动搜索,带薪年假,三餐班车,扁平管理,工作环境舒适,年底双薪,六险一金,绩效奖金', '3', '北京朝阳区首开广场', '中国领先的安卓应用商店，阿里分发平台的核心品牌', '豌豆荚（http://www.wandoujia.com/）是中国 android 用户中最具人气、活跃度最高的「移动内容搜索」，诞生于2009年12月，迄今安装量已超过4.2亿。豌豆荚通过「应用内搜索」技术索引了千万量级的不重复应用、游戏、视频、电子书、主题、电影票、问答、旅游等内容，为用户提供全面准确、直达行动的内容搜索及消费体验。2016年7月，豌豆荚正式并入阿里巴巴移动事业群，成为阿里分发平台的核心品牌。  ', '0', '1494971538');


INSERT INTO `test_spider`.`company_industry` (`id`, `company_id`, `industry_id`, `city_id`)
VALUES ('128060', '11', '24', '2'),
('128061', '10', '25', '3');

INSERT INTO `test_spider`.`job` (`id`, `title`, `work_year`, `city_id`, `company_id`, `department`, `salary`, `education`, `description`, `advantage`, `job_nature`, `created_at`, `updated_at`)
VALUES ('4789', 'Android开发工程师', '1', '3', '10', '堆糖技术部招聘', '10k-20k', '3', ' 职位描述：   开发android手机终端产品。   职位要求：   本科或以上学历，一年以上android开发经验；  有扎实的java语言基础，熟悉android sdk及相关开发、调试、优化工具；  开发基础良好，对手机软件性能优化有一定了解；  对软件产品有强烈的责任心，具备良好的沟通能力和优秀的团队协作能力；  参与过开源项目者优先；有个人的技术blog者优先。  能独立开发app，有成功发布app者优先（最好附带作品演示）。  ', '发展空间大，成长快', '0', '1494864000', '1495006329'),
('6814', 'web前端', '1', '2', '11', '多盟技术部招聘', '10k-20k', '3', ' 工作内容：  1、基于html5的手机富媒体广告的制作和开发 2、引领行业的先进的移动广告形态的调研和技术实现 3、web网站前端开发 4、前端框架调优和性能优化 能力要求：  1、热爱前端技术，坚信前端技术是用户体验非常关键的一环 2、精通html5系相关技术，如果有手机端html5开发和适配经验更佳 3、熟悉或理解后端开发语言（php/python/java等）的工作原理，及与前端配合的工作模式 4、关注领域前沿技术，喜欢尝试新技术，以不断追求对界面和交互的体验改进 ', '国内领先移动广告平台', '0', '1493049600', '1494931484');

INSERT INTO `test_spider`.`job_keyword` (`id`, `job_id`, `keyword_id`, `city_id`)
VALUES ('5637', '4789', '100', '3'),
('5638', '6814', '101', '2'),
('5639', '6814', '100', '2');

INSERT INTO `test_spider`.`keyword` (`id`, `name`)
VALUES ('100', 'python'),
('101', 'java');
