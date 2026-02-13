# 📚 基于知识图谱的智能图书推荐系统

<div align="center">

**[中文](README.md)** | **[English](README_EN.md)**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

一个基于知识图谱和评论关键词的智能图书推荐系统，提供可解释的推荐理由和多种自定义推荐策略。

### 🌐 在线演示

**👉 [http://47.110.250.188:5000/](http://47.110.250.188:5000/) 👈**

立即体验智能图书推荐系统！

</div>

---

## ✨ 功能特点

- **🎯 三种推荐策略**: 知识图谱推荐、评论关键词匹配、混合推荐
- **🔧 自定义推荐**: 可选择基于作者、系列、出版社、译者的推荐关系
- **🧠 智能关键词**: 自动提取图书评论特征词，支持用户自定义选择
- **💡 可解释性**: 每个推荐都提供清晰的理由和匹配度评分
- **🌍 双语支持**: 完整的中英文界面切换

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 4GB+ RAM

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/your-username/doubanBookComment.git
cd doubanBookComment
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **准备数据**

将原始数据文件放入 `data/raw/` 目录：
- `newBookInformation` - 图书信息
- `newCommentdata` - 评论数据

4. **启动服务**

```bash
python start.py
```

首次运行会自动构建知识图谱（约 30-60 分钟），之后启动仅需几秒。

访问 `http://localhost:5000` 即可使用。

---

## 📖 使用指南

### 基本使用

1. **添加喜欢的图书** - 在搜索框输入书名并添加
2. **选择推荐策略** - 知识图谱/关键词/混合
3. **自定义关键词**（可选）- 选择关注的特征词
4. **查看推荐结果** - 包含评分、理由和匹配度

### API 使用

```bash
POST /api/recommend
Content-Type: application/json

{
    "favorite_books": ["三体"],
    "strategy": "mixed",
    "top_k": 20
}
```

更多 API 文档请查看 `docs/guides/` 目录。

---

## 📊 数据说明

| 数据类型 | 数量 | 说明 |
|---------|------|------|
| 图书信息 | 68万+ | 书名、作者、出版社、评分等 |
| 用户评论 | 367万+ | 评论内容、评分、时间等 |
| 知识图谱实体 | 70万+ | 图书、作者、出版社、译者、系列 |
| 知识图谱关系 | 100万+ | 写作、出版、翻译、系列关系 |

---

## 📁 项目结构

```
doubanBookComment/
├── config/                 # 配置文件
├── data/                   # 数据目录
│   ├── raw/               # 原始数据
│   ├── processed/         # 处理后的数据
│   └── resources/         # 资源文件
├── src/                    # 源代码
│   ├── core/              # 核心业务逻辑
│   └── utils/             # 工具模块
├── static/                 # 静态资源
├── templates/              # HTML模板
├── app.py                  # Flask应用
└── start.py                # 启动脚本
```

---

## 🛠️ 技术栈

- **后端**: Flask + NetworkX + Pandas + Jieba + scikit-learn
- **前端**: JavaScript + CSS3
- **算法**: 知识图谱 + TF-IDF + TextRank

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📜 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

</div>
