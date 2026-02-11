# 📚 基于知识图谱的智能图书推荐系统

<div align="center">

**中文** | [English](README.md)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

一个基于知识图谱和评论关键词的智能图书推荐系统，提供可解释的推荐理由和多种自定义推荐策略，支持中英文双语界面。

[功能特点](#-功能特点) • [在线演示](#-在线演示) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [技术架构](#-技术架构)

</div>

---

## 📸 系统截图

> **提示**: 部署后请替换为实际截图
> 
> 截图建议：
> 1. 主界面 - 展示搜索框和语言切换功能
> 2. 推荐策略选择 - 展示三种策略的选择界面
> 3. 关键词选择 - 展示智能提取的关键词标签
> 4. 推荐结果 - 展示推荐列表和详细理由
>
> 截图存放位置：在项目根目录创建 `screenshots/` 文件夹，然后更新下方图片链接

### 主界面
![主界面](screenshots/main-interface.png)
*现代化的渐变背景设计，支持中英文切换*

### 推荐策略选择
![推荐策略](screenshots/strategies.png)
*支持知识图谱、评论关键词、混合推荐三种策略*

### 关键词选择
![关键词选择](screenshots/keywords.png)
*智能提取图书评论关键词，用户可自定义选择*

### 推荐结果
![推荐结果](screenshots/results.png)
*详细的推荐理由和匹配度评分*

---

## ✨ 功能特点

### 🎯 智能推荐算法
- **知识图谱推荐**: 基于图书间的关系（作者、出版社、译者、系列）进行推荐
- **评论关键词匹配**: 使用 TF-IDF + TextRank 双算法提取图书特征词
- **混合推荐策略**: 结合知识图谱和关键词的优势，提供更精准的推荐

### 🔧 自定义推荐策略
- **纯知识图谱推荐**: 可选择基于作者、系列、出版社、译者的单一或组合推荐
- **纯关键词推荐**: 基于用户选择的图书特征词进行匹配
- **混合推荐**: 智能融合两种策略的优势

### 🧠 智能关键词识别
- **语义分类**: 自动识别主题、情节、人物、风格、世界观五大类特征词
- **用户自定义**: 支持用户选择自己关注的关键词进行推荐
- **高质量提取**: 77个停用词过滤，确保关键词质量

### 🚀 性能优化
- **多进程加速**: 使用多进程并行提取关键词，速度提升 5-8 倍
- **智能缓存**: 首次运行后缓存结果，后续启动仅需 5-10 秒
- **增量更新**: 支持缓存的增量更新和管理

### 🌍 国际化支持
- **双语界面**: 完整的中英文支持
- **语言切换**: 一键切换语言，自动保存用户偏好
- **SEO 友好**: 正确的 HTML lang 属性设置

### 💡 可解释性
- **推荐理由**: 每个推荐都提供清晰的理由说明
- **匹配度评分**: 量化的推荐置信度
- **关系路径**: 展示图书间的关联关系

---

## 🎬 在线演示

> **在线访问**: [https://your-app-url.com](https://your-app-url.com) *(部署后更新此链接)*

本地运行：

```bash
python start.py
# 访问 http://localhost:5000
```

部署指南请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 4GB+ RAM（推荐 8GB）
- 多核 CPU（用于并行处理）

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/yourusername/doubanBookComment.git
cd doubanBookComment
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **准备数据**

确保以下数据文件存在：
- `newBookInformation`: 图书信息数据
- `newCommentdata`: 评论数据
- `ChineseStopWords.txt`: 中文停用词表

4. **构建知识图谱**

```bash
python knowledge_graph_builder.py
```

首次运行会：
- 加载 68 万本图书数据
- 提取 367 万条评论
- 构建知识图谱关系
- 提取评论关键词（使用多进程加速）
- 保存缓存文件到 `knowledge_graph/` 目录

⏱️ 预计耗时：30-60 分钟（取决于 CPU 核心数）

5. **启动服务**

```bash
python start.py
```

服务将在 `http://localhost:5000` 启动

---

## 📖 使用指南

### Web 界面使用

#### 1. 添加喜欢的图书

- 在搜索框输入书名，系统会提供自动补全建议
- 点击"添加"按钮将图书加入列表
- 可以添加多本图书以获得更精准的推荐

#### 2. 选择推荐策略

**知识图谱推荐**
- 选择关系类型：作者、系列、出版社、译者
- 可以单选或多选
- 基于图书间的结构化关系进行推荐

**评论关键词推荐**
- 系统自动提取图书评论中的特征词
- 用户可以选择关注的关键词
- 基于语义相似度进行推荐

**混合推荐**（推荐）
- 结合知识图谱和关键词的优势
- 提供更全面的推荐结果

#### 3. 自定义关键词（可选）

- 点击"选择关键词"按钮
- 系统展示从图书评论中提取的高质量关键词
- 选择你关注的特征词
- 系统将基于这些关键词进行匹配推荐

#### 4. 查看推荐结果

每个推荐包含：
- 📖 图书名称和豆瓣链接
- ⭐ 豆瓣评分
- 📊 匹配度得分
- 💡 详细的推荐理由

#### 5. 切换语言

- 点击右上角的语言切换按钮
- 支持中文/English 切换
- 语言偏好自动保存

### API 使用

#### 获取推荐

```bash
POST /api/recommend
Content-Type: application/json

{
    "favorite_books": ["三体", "活着", "百年孤独"],
    "strategy": "mixed",
    "relation_types": ["author", "series"],
    "selected_keywords": ["科幻", "人性", "哲学"],
    "top_k": 20,
    "lang": "zh"
}
```

**参数说明**：
- `favorite_books`: 用户喜欢的图书列表（必填）
- `strategy`: 推荐策略，可选 `kg_only`、`keyword_only`、`mixed`（默认 `mixed`）
- `relation_types`: 知识图谱关系类型，可选 `author`、`series`、`publisher`、`translator`
- `selected_keywords`: 用户选择的关键词列表
- `top_k`: 返回推荐数量（默认 20）
- `lang`: 语言，可选 `zh`、`en`（默认 `zh`）

**响应示例**：

```json
{
    "success": true,
    "data": {
        "favorite_books": ["三体"],
        "recommendations": [
            {
                "book_id": 12345,
                "book_name": "球状闪电",
                "book_url": "https://book.douban.com/subject/12345/",
                "rating": 8.5,
                "score": 0.92,
                "reasons": [
                    "与《三体》作者相同: 刘慈欣",
                    "评论关键词匹配: 科幻(0.85), 物理(0.78)"
                ],
                "explanation": "这本书与您喜欢的《三体》有很高的相似度..."
            }
        ],
        "total": 20,
        "strategy": "mixed"
    }
}
```

#### 搜索图书

```bash
GET /api/search?q=三体&limit=10
```

#### 获取图书关键词

```bash
GET /api/book_keywords/12345?lang=zh
```

#### 获取系统统计

```bash
GET /api/stats?lang=zh
```

---

## 🏗️ 技术架构

### 后端技术栈

| 技术 | 用途 |
|------|------|
| **Flask** | Web 框架 |
| **NetworkX** | 知识图谱构建和查询 |
| **Pandas** | 数据处理 |
| **NumPy** | 数值计算 |
| **Jieba** | 中文分词 |
| **scikit-learn** | TF-IDF 特征提取 |
| **Gensim** | TextRank 关键词提取 |

### 前端技术栈

| 技术 | 用途 |
|------|------|
| **原生 JavaScript** | 前端逻辑 |
| **CSS3** | 现代化样式设计 |
| **LocalStorage** | 用户偏好保存 |

### 核心算法

#### 1. 知识图谱构建

```
图书实体 ──写作──> 作者实体
         ├─出版──> 出版社实体
         ├─翻译──> 译者实体
         └─属于──> 系列实体
```

**关系权重**：
- 相同作者：0.30
- 相同系列：0.40
- 相同出版社：0.15
- 相同译者：0.20

#### 2. 评论关键词提取

**双算法融合**：
- **TF-IDF**: 统计词频和逆文档频率
- **TextRank**: 基于图排序的关键词提取

**语义分类**：
- 主题类：科幻、历史、爱情、悬疑...
- 情节类：反转、节奏、伏笔、高潮...
- 人物类：人物、角色、性格、成长...
- 风格类：幽默、深刻、细腻、震撼...
- 世界观类：世界观、设定、架空、未来...

**质量保证**：
- 77 个停用词过滤
- 最小词长度限制
- 词频阈值过滤

#### 3. 推荐算法

**混合推荐策略**：

```python
score = α × kg_score + β × keyword_score

其中：
- kg_score: 知识图谱关系得分
- keyword_score: 关键词相似度得分
- α, β: 可调节权重（默认 0.5, 0.5）
```

---

## 📁 项目结构

```
doubanBookComment/
├── app.py                      # Flask 主应用
├── start.py                    # 启动脚本
├── config.py                   # 配置文件
├── i18n.py                     # 国际化配置
├── knowledge_graph_builder.py  # 知识图谱构建
├── keyword_recommender.py      # 推荐算法核心
├── cache_manager.py            # 缓存管理工具
├── test_keyword_quality.py     # 关键词质量测试
├── test_strategies.py          # 推荐策略测试
├── requirements.txt            # Python 依赖
├── ChineseStopWords.txt        # 中文停用词表
│
├── templates/
│   └── index.html             # 前端页面模板
│
├── static/
│   ├── css/
│   │   └── style.css          # 样式文件
│   └── js/
│       └── app.js             # 前端逻辑
│
├── knowledge_graph/           # 知识图谱数据（自动生成）
│   ├── entities.pkl           # 实体数据
│   ├── relations.pkl          # 关系数据
│   ├── embeddings.pkl         # 实体嵌入
│   └── comment_keywords.pkl   # 评论关键词缓存
│
├── newBookInformation         # 图书信息数据
├── newCommentdata            # 评论数据
│
└── docs/                      # 文档
    ├── CACHE_OPTIMIZATION.md  # 缓存优化说明
    ├── STRATEGY_GUIDE.md      # 推荐策略指南
    ├── WEB_FEATURES.md        # Web 功能说明
    └── I18N_GUIDE.md          # 国际化指南
```

---

## ⚙️ 配置说明

在 `config.py` 中可以自定义配置：

```python
# 推荐配置
TOP_K = 20                    # 默认推荐数量
MIN_SCORE_THRESHOLD = 0.1     # 最低推荐分数阈值

# 关键词提取配置
KEYWORD_TOP_N = 20            # 每本书提取的关键词数量
MIN_KEYWORD_FREQ = 3          # 关键词最小出现频率

# 性能配置
USE_MULTIPROCESSING = True    # 是否使用多进程
MAX_WORKERS = None            # 最大工作进程数（None = CPU核心数-1）

# Web 服务配置
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False
```

---

## 🔧 缓存管理

系统提供了缓存管理工具 `cache_manager.py`：

```bash
# 查看缓存信息
python cache_manager.py info

# 清除所有缓存
python cache_manager.py clear

# 清除特定缓存
python cache_manager.py clear --type keywords

# 重建缓存
python cache_manager.py rebuild
```

---

## 📊 数据说明

### 数据来源

本系统使用豆瓣读书数据集（2022年采集）：

| 数据类型 | 数量 | 说明 |
|---------|------|------|
| 图书信息 | 68万+ | 包含书名、作者、出版社、评分等 |
| 用户评论 | 367万+ | 包含评论内容、评分、时间等 |
| 知识图谱实体 | 70万+ | 图书、作者、出版社、译者、系列 |
| 知识图谱关系 | 100万+ | 写作、出版、翻译、系列关系 |

### 数据格式

**图书信息** (`newBookInformation`):
```python
{
    'bookId': '1234567',
    'bookName': '三体',
    'author': '刘慈欣',
    'publisher': '重庆出版社',
    'rating': '9.3',
    'series': '地球往事三部曲',
    'translator': None
}
```

**评论数据** (`newCommentdata`):
```python
{
    'bookId': '1234567',
    'userId': 'user123',
    'comment': '非常精彩的科幻小说...',
    'rating': 'rating50-5',
    'time': '2022-01-01'
}
```

---

## 🧪 测试

### 关键词质量测试

```bash
python test_keyword_quality.py
```

测试内容：
- 关键词提取质量
- 语义分类准确性
- 停用词过滤效果

### 推荐策略测试

```bash
python test_strategies.py
```

测试场景：
- 纯知识图谱推荐
- 纯关键词推荐
- 混合推荐
- 自定义关系推荐
- 自定义关键词推荐

---

## 🚀 性能优化

### 已实现的优化

1. **多进程并行处理**
   - 关键词提取使用多进程
   - 速度提升 5-8 倍

2. **智能缓存机制**
   - 首次运行后缓存结果
   - 后续启动仅需 5-10 秒

3. **增量更新**
   - 仅处理新增图书
   - 避免重复计算

### 进一步优化建议

- [ ] 使用 Redis 缓存热门推荐结果
- [ ] 使用 Neo4j 图数据库存储知识图谱
- [ ] 使用 Elasticsearch 加速图书搜索
- [ ] 使用 Celery 异步处理推荐任务
- [ ] 添加 CDN 加速静态资源

---

## 📈 未来规划

### 功能扩展

- [ ] 用户系统和个性化推荐
- [ ] 推荐结果反馈机制
- [ ] 知识图谱可视化
- [ ] 推荐理由的图形化展示
- [ ] 移动端适配
- [ ] 社交分享功能

### 算法优化

- [ ] 引入深度学习推荐模型
- [ ] 协同过滤算法
- [ ] 图神经网络（GNN）
- [ ] 强化学习优化推荐策略
- [ ] 多模态推荐（封面图像、简介文本）

### 数据扩展

- [ ] 接入实时豆瓣数据
- [ ] 支持更多图书平台
- [ ] 用户行为数据收集
- [ ] 图书标签和分类体系

---

## 📚 文档

详细文档请查看 `docs/` 目录：

- [缓存优化说明](CACHE_OPTIMIZATION.md)
- [推荐策略指南](STRATEGY_GUIDE.md)
- [Web 功能说明](WEB_FEATURES.md)
- [国际化指南](I18N_GUIDE.md)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 引用

如果这个项目对您的研究有帮助，欢迎引用：

```bibtex
@mastersthesis{yang2024kg,
  title={基于知识图谱的可解释图书推荐研究},
  author={杨群峰},
  school={安徽工程大学},
  year={2024},
  doi={10.27763/d.cnki.gahgc.2023.000087}
}

@article{yang2022book,
  title={基于情感分析和概念词典的图书推荐方法},
  author={杨群峰 and 王忠群 and 皇苏斌},
  journal={安徽工程大学学报},
  volume={37},
  number={5},
  pages={59--65},
  year={2022}
}
```

---

## 📧 联系方式

- 项目主页: [GitHub](https://github.com/yourusername/doubanBookComment) *(替换为你的仓库地址)*
- 问题反馈: [Issues](https://github.com/yourusername/doubanBookComment/issues)
- 邮箱: your.email@example.com *(替换为你的邮箱)*

---

## 📜 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- 感谢豆瓣提供的图书数据
- 感谢所有开源项目的贡献者
- 感谢所有使用和反馈的用户

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by Yang Qunfeng

</div>

