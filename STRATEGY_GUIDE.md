# 自定义推荐策略使用说明

## 功能概述

现在推荐系统支持三种推荐策略，您可以根据需求自由选择：

1. **混合策略 (mixed)** - 结合知识图谱关系和评论关键词
2. **知识图谱策略 (kg_only)** - 仅使用知识图谱关系
3. **关键词策略 (keyword_only)** - 仅使用评论关键词匹配

同时，您还可以指定使用哪些知识图谱关系进行推荐。

---

## 使用方法

### 1. Python代码调用

```python
from keyword_recommender import KeywordBasedRecommender

recommender = KeywordBasedRecommender()
recommender.load_kg()
recommender.load_and_analyze_comments()

# 示例1：仅使用作者关系推荐
recommendations = recommender.recommend(
    favorite_books=['三体'],
    top_k=20,
    strategy='kg_only',
    relations=['author']
)

# 示例2：使用系列和作者关系推荐
recommendations = recommender.recommend(
    favorite_books=['三体'],
    top_k=20,
    strategy='kg_only',
    relations=['series', 'author']
)

# 示例3：仅使用关键词推荐
recommendations = recommender.recommend(
    favorite_books=['三体'],
    top_k=20,
    strategy='keyword_only'
)

# 示例4：混合策略，只用作者和系列关系
recommendations = recommender.recommend(
    favorite_books=['三体'],
    top_k=20,
    strategy='mixed',
    relations=['series', 'author']
)
```

### 2. Web API调用

```bash
# 仅使用作者关系推荐
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "favorite_books": ["三体"],
    "top_k": 20,
    "strategy": "kg_only",
    "relations": ["author"]
  }'

# 使用系列和作者关系推荐
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "favorite_books": ["三体"],
    "top_k": 20,
    "strategy": "kg_only",
    "relations": ["series", "author"]
  }'

# 仅使用关键词推荐
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "favorite_books": ["三体"],
    "top_k": 20,
    "strategy": "keyword_only"
  }'
```

---

## 参数说明

### strategy（推荐策略）

| 值 | 说明 | 推荐理由示例 |
|---|---|---|
| `mixed` | 混合策略（默认） | 知识图谱关系 + 评论关键词 + 评分热度 |
| `kg_only` | 仅知识图谱 | 只显示知识图谱关系 + 评分热度 |
| `keyword_only` | 仅关键词 | 只显示评论关键词匹配 + 评分热度 |

### relations（知识图谱关系）

可选值（可组合使用）：

| 值 | 说明 | 权重 |
|---|---|---|
| `series` | 系列关系 | 0.4 |
| `author` | 作者关系 | 0.3 |
| `translator` | 译者关系 | 0.2 |
| `publisher` | 出版社关系 | 0.15 |

**注意**：
- `relations` 参数仅在 `strategy='kg_only'` 或 `strategy='mixed'` 时有效
- 如果不指定 `relations`，默认使用所有关系
- 可以指定一个或多个关系，例如：`['author']` 或 `['series', 'author']`

---

## 使用场景

### 场景1：找同一作者的其他作品

```python
recommendations = recommender.recommend(
    favorite_books=['三体'],
    strategy='kg_only',
    relations=['author']
)
```

**推荐理由示例**：
- 与《三体》作者相同: 刘慈欣
- 高分图书（豆瓣评分: 8.8）
- 热门图书（1355条评论）

### 场景2：找同一系列的书

```python
recommendations = recommender.recommend(
    favorite_books=['凡人修仙传（1-10）'],
    strategy='kg_only',
    relations=['series']
)
```

**推荐理由示例**：
- 与《凡人修仙传（1-10）》属于同一系列: 凡人修仙传
- 读者评分高（平均4.3星）

### 场景3：找内容相似的书（基于评论关键词）

```python
recommendations = recommender.recommend(
    favorite_books=['三体'],
    strategy='keyword_only'
)
```

**推荐理由示例**：
- 评论关键词匹配: 科幻, 宇宙, 文明, 物理, 想象力
- 高分图书（豆瓣评分: 8.5）
- 热门图书（2000条评论）

### 场景4：综合推荐（作者 + 关键词）

```python
recommendations = recommender.recommend(
    favorite_books=['三体'],
    strategy='mixed',
    relations=['author']
)
```

**推荐理由示例**：
- 与《三体》作者相同: 刘慈欣
- 高分图书（豆瓣评分: 8.8）
- 评论关键词匹配: 科幻, 宇宙, 文明

---

## 测试脚本

运行 `test_strategies.py` 可以测试不同策略的效果：

```bash
python test_strategies.py
```

该脚本会展示5种不同的推荐策略，帮助您理解各策略的差异。

---

## 推荐理由的显示规则

### kg_only 策略
- ✓ 显示知识图谱关系（根据 relations 参数）
- ✓ 显示评分和热度信息
- ✗ 不显示关键词匹配

### keyword_only 策略
- ✗ 不显示知识图谱关系
- ✓ 显示评论关键词匹配（放在最前面）
- ✓ 显示评分和热度信息

### mixed 策略
- ✓ 显示知识图谱关系（根据 relations 参数）
- ✓ 显示评分和热度信息
- ✓ 显示关键词匹配（放在知识图谱关系之后）

---

## 关键词优化说明

新版本对关键词提取进行了优化：

1. **扩展停用词表**：过滤了77个评论中常见但无意义的词
   - 通用词：小说、书、作者、故事、内容等
   - 评价词：喜欢、不错、推荐、值得等
   - 动词：知道、想要、希望、需要等

2. **词性过滤**：只保留名词、专有名词、成语等有特征的词

3. **长度优先**：3字及以上的词优先保留（通常更有特征）

4. **质量控制**：只有当匹配3个以上有意义关键词时才显示

---

## 注意事项

1. **首次运行**：删除缓存后首次运行需要5-10分钟重新提取关键词
2. **缓存位置**：`knowledge_graph/comment_keywords.pkl`
3. **清除缓存**：删除缓存文件后重启服务即可使用新规则
4. **性能**：使用多进程并行处理，速度比之前快5-6倍

---

## 常见问题

**Q: 为什么推荐理由有时是知识图谱关系，有时是关键词？**

A: 这取决于您选择的策略。使用 `strategy='kg_only'` 只显示知识图谱关系，使用 `strategy='keyword_only'` 只显示关键词，使用 `strategy='mixed'` 会同时显示两者。

**Q: 如何只根据作者推荐？**

A: 使用 `strategy='kg_only'` 和 `relations=['author']`。

**Q: 关键词还是有无意义的词怎么办？**

A: 确保已删除缓存文件并重启服务。如果还有问题，可以在停用词表中添加更多词。

**Q: 可以自定义关系权重吗？**

A: 目前权重是固定的（系列0.4、作者0.3、译者0.2、出版社0.15），如需修改请编辑 `keyword_recommender.py` 中的 `relation_weights` 字典。

