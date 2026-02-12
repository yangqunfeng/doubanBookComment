# 📚 基于知识图谱的智能图书推荐系统

<div align="center">

**[中文](README.md)** | **[English](README_EN.md)**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

一个基于知识图谱和评论关键词的智能图书推荐系统，提供可解释的推荐理由和多种自定义推荐策略，支持中英文双语界面。

### 🌐 在线演示网站

**👉 [http://47.110.250.188:5000/](http://47.110.250.188:5000/) 👈**

立即体验智能图书推荐系统！

### ⭐ 支持项目

如果这个项目对你有帮助，请访问 [GitHub](https://github.com/yangqunfeng/book-rec-kg-comments) 给我们一个 Star ⭐️

</div>

---

## ✨ 功能特点

- **🎯 三种推荐策略**: 知识图谱推荐、评论关键词匹配、混合推荐
- **🔧 自定义推荐**: 可选择基于作者、系列、出版社、译者的推荐关系
- **🧠 智能关键词**: 自动提取图书评论特征词，支持用户自定义选择
- **💡 可解释性**: 每个推荐都提供清晰的理由和匹配度评分
- **🌍 双语支持**: 完整的中英文界面切换
- **🚀 性能优化**: 多进程加速 + 智能缓存，首次运行后启动仅需 5-10 秒

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 4GB+ RAM（推荐 8GB）

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/yangqunfeng/book-rec-kg-comments.git
cd book-rec-kg-comments
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **构建知识图谱**

```bash
python knowledge_graph_builder.py
```

首次运行会加载 68 万本图书数据和 367 万条评论，构建知识图谱并提取关键词（约 30-60 分钟）。

4. **启动服务**

```bash
python start.py
```

访问 `http://localhost:5000` 即可使用。

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

### 核心技术

- **后端**: Flask + NetworkX + Pandas + Jieba + scikit-learn
- **前端**: 原生 JavaScript + CSS3
- **算法**: 知识图谱 + TF-IDF + TextRank

### 推荐算法

```
混合推荐得分 = 0.5 × 知识图谱得分 + 0.5 × 关键词相似度得分
```

**知识图谱关系权重**:
- 相同作者: 0.30
- 相同系列: 0.40
- 相同出版社: 0.15
- 相同译者: 0.20

---

## 📊 数据说明

| 数据类型 | 数量 | 说明 |
|---------|------|------|
| 图书信息 | 68万+ | 书名、作者、出版社、评分等 |
| 用户评论 | 367万+ | 评论内容、评分、时间等 |
| 知识图谱实体 | 70万+ | 图书、作者、出版社、译者、系列 |
| 知识图谱关系 | 100万+ | 写作、出版、翻译、系列关系 |

数据来源：豆瓣读书（2022年采集）

---

## 📁 项目结构

```
book-rec-kg-comments/
├── app.py                      # Flask 主应用
├── start.py                    # 启动脚本
├── knowledge_graph_builder.py  # 知识图谱构建
├── keyword_recommender.py      # 推荐算法核心
├── requirements.txt            # Python 依赖
├── templates/index.html        # 前端页面
├── static/                     # 静态资源
├── knowledge_graph/            # 知识图谱数据（自动生成）
├── newBookInformation          # 图书信息数据
└── newCommentdata             # 评论数据
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 引用

如果这个项目对您的研究有帮助，欢迎引用：

```bibtex
@mastersthesis{
  title={基于知识图谱的可解释图书推荐研究},
  author={杨群峰},
  school={安徽工程大学},
  year={2024},
  doi={10.27763/d.cnki.gahgc.2023.000087}
}

@article{
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

- 项目主页: [GitHub](https://github.com/yangqunfeng/book-rec-kg-comments)
- 问题反馈: [Issues](https://github.com/yangqunfeng/book-rec-kg-comments/issues)

---

## 📜 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by Yang Qunfeng

</div>
