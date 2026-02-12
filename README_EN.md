# 📚 Smart Book Recommendation System Based on Knowledge Graph

<div align="center">

**[中文](README.md)** | **[English](README_EN.md)**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

An intelligent book recommendation system based on knowledge graph and comment keywords, providing explainable recommendation reasons and multiple customizable recommendation strategies, supporting bilingual interface in Chinese and English.

### 🌐 Live Demo

**👉 [http://47.110.250.188:5000/](http://47.110.250.188:5000/) 👈**

Experience the smart book recommendation system now!

### ⭐ Support This Project

If this project helps you, please visit [GitHub](https://github.com/yangqunfeng/book-rec-kg-comments) and give us a Star ⭐️

</div>

---

## ✨ Features

- **🎯 Three Recommendation Strategies**: Knowledge graph recommendation, comment keyword matching, and hybrid recommendation
- **🔧 Customizable Recommendations**: Choose recommendation relationships based on author, series, publisher, or translator
- **🧠 Smart Keywords**: Automatically extract book review feature words with user-defined selection support
- **💡 Explainability**: Each recommendation provides clear reasons and matching scores
- **🌍 Bilingual Support**: Complete Chinese/English interface switching
- **🚀 Performance Optimization**: Multi-process acceleration + smart caching, startup takes only 5-10 seconds after first run

---

## 🚀 Quick Start

### Requirements

- Python 3.8+
- 4GB+ RAM (8GB recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yangqunfeng/book-rec-kg-comments.git
cd book-rec-kg-comments
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Build knowledge graph**

```bash
python knowledge_graph_builder.py
```

First run will load 680,000+ books and 3.67 million comments, build knowledge graph and extract keywords (approximately 30-60 minutes).

4. **Start the service**

```bash
python start.py
```

Visit `http://localhost:5000` to use the system.

---

## 📖 User Guide

### Web Interface

#### 1. Add Favorite Books

- Enter book title in the search box, system will provide auto-complete suggestions
- Click "Add" button to add books to the list
- Add multiple books for more accurate recommendations

#### 2. Choose Recommendation Strategy

**Knowledge Graph Recommendation**
- Select relation types: author, series, publisher, translator
- Single or multiple selection supported
- Recommendations based on structured relationships between books

**Comment Keyword Recommendation**
- System automatically extracts feature words from book reviews
- Users can select keywords of interest
- Recommendations based on semantic similarity

**Hybrid Recommendation** (Recommended)
- Combines advantages of knowledge graph and keywords
- Provides more comprehensive recommendation results

#### 3. Customize Keywords (Optional)

- Click "Select Keywords" button
- System displays high-quality keywords extracted from book reviews
- Select feature words you care about
- System will match recommendations based on these keywords

#### 4. View Recommendation Results

Each recommendation includes:
- 📖 Book name and Douban link
- ⭐ Douban rating
- 📊 Match score
- 💡 Detailed recommendation reasons

#### 5. Switch Language

- Click language switch button in the top right corner
- Support Chinese/English switching
- Language preference is automatically saved

### API Usage

#### Get Recommendations

```bash
POST /api/recommend
Content-Type: application/json

{
    "favorite_books": ["The Three-Body Problem", "To Live", "One Hundred Years of Solitude"],
    "strategy": "mixed",
    "relation_types": ["author", "series"],
    "selected_keywords": ["sci-fi", "humanity", "philosophy"],
    "top_k": 20,
    "lang": "en"
}
```

**Parameters**:
- `favorite_books`: List of user's favorite books (required)
- `strategy`: Recommendation strategy, options: `kg_only`, `keyword_only`, `mixed` (default: `mixed`)
- `relation_types`: Knowledge graph relation types, options: `author`, `series`, `publisher`, `translator`
- `selected_keywords`: List of user-selected keywords
- `top_k`: Number of recommendations to return (default: 20)
- `lang`: Language, options: `zh`, `en` (default: `zh`)

**Response Example**:

```json
{
    "success": true,
    "data": {
        "favorite_books": ["The Three-Body Problem"],
        "recommendations": [
            {
                "book_id": 12345,
                "book_name": "Ball Lightning",
                "book_url": "https://book.douban.com/subject/12345/",
                "rating": 8.5,
                "score": 0.92,
                "reasons": [
                    "Same author as 'The Three-Body Problem': Liu Cixin",
                    "Comment keyword match: sci-fi(0.85), physics(0.78)"
                ],
                "explanation": "This book has high similarity with your favorite 'The Three-Body Problem'..."
            }
        ],
        "total": 20,
        "strategy": "mixed"
    }
}
```

#### Search Books

```bash
GET /api/search?q=three-body&limit=10
```

#### Get Book Keywords

```bash
GET /api/book_keywords/12345?lang=en
```

#### Get System Statistics

```bash
GET /api/stats?lang=en
```

---

## 🏗️ Technical Architecture

### Core Technologies

- **Backend**: Flask + NetworkX + Pandas + Jieba + scikit-learn
- **Frontend**: Vanilla JavaScript + CSS3
- **Algorithms**: Knowledge Graph + TF-IDF + TextRank

### Recommendation Algorithm

```
Hybrid Score = 0.5 × Knowledge Graph Score + 0.5 × Keyword Similarity Score
```

**Knowledge Graph Relation Weights**:
- Same author: 0.30
- Same series: 0.40
- Same publisher: 0.15
- Same translator: 0.20

---

## 📊 Data Description

| Data Type | Quantity | Description |
|-----------|----------|-------------|
| Book Information | 680,000+ | Title, author, publisher, rating, etc. |
| User Comments | 3.67M+ | Comment content, rating, time, etc. |
| Knowledge Graph Entities | 700,000+ | Books, authors, publishers, translators, series |
| Knowledge Graph Relations | 1M+ | Writing, publishing, translating, series relations |

Data Source: Douban Books (collected in 2022)

---

## 📁 Project Structure

```
book-rec-kg-comments/
├── app.py                      # Flask main application
├── start.py                    # Startup script
├── knowledge_graph_builder.py  # Knowledge graph builder
├── keyword_recommender.py      # Recommendation algorithm core
├── requirements.txt            # Python dependencies
├── templates/index.html        # Frontend page
├── static/                     # Static resources
├── knowledge_graph/            # Knowledge graph data (auto-generated)
├── newBookInformation          # Book information data
└── newCommentdata             # Comment data
```

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork this project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 Citation

If this project helps your research, please cite:

```bibtex
@mastersthesis{yang2024kg,
  title={Research on Explainable Book Recommendation Based on Knowledge Graph},
  author={Yang Qunfeng},
  school={Anhui Polytechnic University},
  year={2024},
  doi={10.27763/d.cnki.gahgc.2023.000087}
}

@article{yang2022book,
  title={Book Recommendation Method Based on Sentiment Analysis and Concept Dictionary},
  author={Yang Qunfeng and Wang Zhongqun and Huang Subin},
  journal={Journal of Anhui Polytechnic University},
  volume={37},
  number={5},
  pages={59--65},
  year={2022}
}
```

---

## 📧 Contact

- Project Homepage: [GitHub](https://github.com/yangqunfeng/book-rec-kg-comments)
- Issue Tracker: [Issues](https://github.com/yangqunfeng/book-rec-kg-comments/issues)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

<div align="center">

**If this project helps you, please give it a ⭐️ Star!**

Made with ❤️ by Yang Qunfeng

</div>

