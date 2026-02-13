# -*- coding: utf-8 -*-
"""
基于评论关键词的深度推荐系统
提取评论中的关键词，进行语义匹配推荐
"""
import pickle
import numpy as np
import networkx as nx
from collections import defaultdict, Counter
import pandas as pd
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import config
import jieba
import jieba.analyse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


class KeywordBasedRecommender:
    """基于评论关键词的推荐器"""
    
    def __init__(self):
        self.entities = {}
        self.entity_types = {}
        self.relations = []
        self.graph = None
        self.book_entities = []
        self.book_ratings = {}
        self.book_neighbors_cache = {}
        self.book_url_to_id = {}
        self.comment_stats = {}
        self.book_popularity = {}
        
        # 关键词相关
        self.book_keywords = {}  # 每本书的关键词
        self.book_keyword_weights = {}  # 关键词权重
        self.all_keywords = set()  # 所有关键词
        self.keyword_to_books = defaultdict(set)  # 关键词到书籍的反向索引
        
        # 加载停用词
        self.stopwords = self._load_stopwords()
        
    def _load_stopwords(self):
        """加载停用词"""
        try:
            with open(config.STOPWORDS_FILE, 'r', encoding='utf-8') as f:
                stopwords = set([line.strip() for line in f])
            
            # 添加额外的无意义词（评论中常见但无特征的词）
            extra_stopwords = {
                # 通用词
                '小说', '书', '作者', '作品', '故事', '内容', '文字', '文章', '书籍',
                '读者', '阅读', '看', '读', '看完', '读完', '看到', '读到',
                # 评价词（太通用）
                '喜欢', '不错', '推荐', '值得', '可以', '还是', '觉得', '感觉',
                '非常', '很', '太', '比较', '有点', '一点', '一些', '一个',
                # 动词（太通用）
                '知道', '想要', '希望', '需要', '应该', '可能', '能够', '必须',
                '开始', '结束', '继续', '发现', '认为', '以为', '觉得',
                # 代词和连词
                '这个', '那个', '这样', '那样', '什么', '怎么', '为什么', '如何',
                '但是', '然后', '所以', '因为', '虽然', '如果', '或者',
                # 时间词（太通用）
                '时候', '时间', '现在', '以前', '之前', '之后', '最后', '开始',
                # 其他
                '东西', '地方', '方面', '问题', '事情', '情况', '方式', '过程'
            }
            stopwords.update(extra_stopwords)
            
            print(f"加载停用词: {len(stopwords)} 个（含{len(extra_stopwords)}个扩展词）")
            return stopwords
        except:
            print("未找到停用词文件，使用默认停用词")
            # 返回基础停用词 + 扩展停用词
            basic_stopwords = set(['的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'])
            extra_stopwords = {
                '小说', '书', '作者', '作品', '故事', '内容', '文字', '书籍',
                '读者', '阅读', '看', '读', '看完', '读完',
                '喜欢', '不错', '推荐', '值得', '可以', '觉得', '感觉',
                '知道', '想要', '希望', '需要', '应该',
                '这个', '那个', '什么', '怎么', '为什么'
            }
            basic_stopwords.update(extra_stopwords)
            return basic_stopwords
    
    def load_kg(self):
        """加载知识图谱"""
        print("正在加载知识图谱...")
        
        try:
            print(f"加载实体文件: {config.KG_ENTITIES_FILE}")
            with open(config.KG_ENTITIES_FILE, 'rb') as f:
                data = pickle.load(f)
                self.entities = data['entities']
                self.entity_types = data['entity_types']
            print(f"✓ 实体加载成功: {len(self.entities)} 个实体")
        except Exception as e:
            print(f"❌ 加载实体文件失败: {str(e)}")
            print(f"文件路径: {config.KG_ENTITIES_FILE}")
            print(f"请检查文件是否完整，或运行 python knowledge_graph_builder.py 重新生成")
            raise
        
        try:
            print(f"加载关系文件: {config.KG_RELATIONS_FILE}")
            with open(config.KG_RELATIONS_FILE, 'rb') as f:
                data = pickle.load(f)
                self.relations = data['relations']
                self.graph = data['graph']
            print(f"✓ 关系加载成功: {len(self.relations)} 条关系")
        except Exception as e:
            print(f"❌ 加载关系文件失败: {str(e)}")
            print(f"文件路径: {config.KG_RELATIONS_FILE}")
            print(f"请检查文件是否完整，或运行 python knowledge_graph_builder.py 重新生成")
            raise
        
        self.book_entities = self.entity_types.get('book', [])
        
        print("构建图书索引和缓存...")
        for book_id in self.book_entities:
            book = self.entities[book_id]
            self.book_ratings[book_id] = float(book.get('rating', 0))
            book_url = book.get('url', '')
            if book_url:
                self.book_url_to_id[book_url] = book_id
            self.book_neighbors_cache[book_id] = self._get_neighbors_by_type(book_id)
        
        print(f"知识图谱加载完成: {len(self.entities)} 个实体, {len(self.relations)} 条关系")
    
    def load_and_analyze_comments(self):
        """加载并深度分析评论 - 提取关键词（支持缓存）"""
        
        # 检查是否有缓存
        cache_file = os.path.join(config.KG_DIR, 'comment_keywords.pkl')
        
        if os.path.exists(cache_file):
            print(f"发现关键词缓存文件，直接加载...")
            try:
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    self.book_keywords = cache_data['book_keywords']
                    self.book_keyword_weights = cache_data['book_keyword_weights']
                    self.all_keywords = cache_data['all_keywords']
                    self.keyword_to_books = cache_data['keyword_to_books']
                    self.comment_stats = cache_data['comment_stats']
                    self.book_popularity = cache_data['book_popularity']
                
                print(f"缓存加载完成:")
                print(f"  - {len(self.book_keywords)} 本书有关键词")
                print(f"  - 共 {len(self.all_keywords)} 个不同关键词")
                return
            except Exception as e:
                print(f"缓存加载失败: {e}，重新提取关键词")
        
        # 没有缓存，开始提取
        try:
            print("正在加载评论数据...")
            comment_data = pd.read_pickle(config.COMMENT_FILE)
            print(f"评论数据加载完成: {len(comment_data)} 条评论")
            
            # 解析评分
            def parse_rating(rating_str):
                if pd.isna(rating_str):
                    return 0
                try:
                    rating_str = str(rating_str)
                    if 'rating' in rating_str:
                        num = rating_str.replace('rating', '').split('-')[0]
                        return int(num)
                    return 0
                except:
                    return 0
            
            comment_data['rating_score'] = comment_data['rating'].apply(parse_rating)
            
            print("提取评论关键词（使用多进程加速）...")
            
            # 按图书分组
            book_groups = list(comment_data.groupby('readBookUrl'))
            print(f"共 {len(book_groups)} 本书需要处理")
            
            # 使用多进程并行处理
            from multiprocessing import Pool, cpu_count
            
            num_processes = max(1, cpu_count() - 1)  # 留一个核心给系统
            print(f"使用 {num_processes} 个进程并行处理...")
            
            # 准备数据
            tasks = []
            for book_url, comments in book_groups:
                if pd.isna(book_url):
                    continue
                book_id = self.book_url_to_id.get(str(book_url))
                if book_id:
                    tasks.append((book_url, comments, book_id, self.stopwords))
            
            # 并行处理
            with Pool(processes=num_processes) as pool:
                results = []
                for i, result in enumerate(pool.imap_unordered(self._process_book_comments, tasks, chunksize=100)):
                    if result:
                        results.append(result)
                    if (i + 1) % 1000 == 0:
                        print(f"  已处理 {i + 1}/{len(tasks)} 本书")
            
            # 整合结果
            print("整合处理结果...")
            for result in results:
                book_id = result['book_id']
                self.book_keywords[book_id] = result['keywords']
                self.book_keyword_weights[book_id] = result['keyword_weights']
                self.comment_stats[book_id] = result['stats']
                self.book_popularity[book_id] = result['popularity']
                
                for kw in result['keywords']:
                    self.all_keywords.add(kw)
                    self.keyword_to_books[kw].add(book_id)
            
            print(f"\n关键词提取完成:")
            print(f"  - {len(self.book_keywords)} 本书有关键词")
            print(f"  - 共提取 {len(self.all_keywords)} 个不同关键词")
            print(f"  - 平均每本书 {np.mean([len(kws) for kws in self.book_keywords.values()]):.1f} 个关键词")
            
            # 保存缓存
            print("保存关键词缓存...")
            os.makedirs(config.KG_DIR, exist_ok=True)
            with open(cache_file, 'wb') as f:
                pickle.dump({
                    'book_keywords': self.book_keywords,
                    'book_keyword_weights': self.book_keyword_weights,
                    'all_keywords': self.all_keywords,
                    'keyword_to_books': dict(self.keyword_to_books),
                    'comment_stats': self.comment_stats,
                    'book_popularity': self.book_popularity
                }, f)
            print(f"缓存已保存到: {cache_file}")
            
        except Exception as e:
            print(f"评论分析失败: {e}")
            import traceback
            traceback.print_exc()
    
    @staticmethod
    def _is_book_feature_keyword(word, weight, word_freq_in_book, total_books_with_word):
        """
        智能判断关键词是否属于图书特征词
        
        判断标准：
        1. 词的TF-IDF权重（区分度）
        2. 词的长度和词性
        3. 词的特异性（不能太常见）
        4. 语义类别（主题、情节、人物、风格等）
        """
        import jieba.posseg as pseg
        
        # 1. 基础过滤：太短或太常见的词
        if len(word) < 2:
            return False
        
        # 2. 权重过滤：权重太低说明不重要
        if weight < 0.01:
            return False
        
        # 3. 词性判断
        pos_tags = list(pseg.cut(word))
        if not pos_tags:
            return False
        
        main_pos = pos_tags[0].flag
        
        # 优先保留的词性（图书特征相关）
        feature_pos = {
            'n',   # 名词（主题、概念）
            'nr',  # 人名（角色）
            'ns',  # 地名（场景）
            'nt',  # 机构名
            'nz',  # 其他专名
            'vn',  # 名动词（行为特征）
            'an',  # 名形词（属性特征）
            'i',   # 成语
            'l',   # 习语
        }
        
        # 4. 语义类别判断（基于词的特征）
        # 主题词：科幻、历史、爱情、悬疑等
        theme_keywords = {
            '科幻', '历史', '爱情', '悬疑', '推理', '奇幻', '武侠', '都市',
            '军事', '战争', '冒险', '魔幻', '玄幻', '修仙', '穿越', '重生',
            '宫斗', '商战', '职场', '校园', '青春', '文学', '哲学', '心理'
        }
        
        # 情节元素：战斗、阴谋、复仇等
        plot_keywords = {
            '战斗', '阴谋', '复仇', '成长', '救赎', '背叛', '牺牲', '冒险',
            '探索', '发现', '秘密', '真相', '命运', '选择', '挑战', '困境'
        }
        
        # 人物特征：主角、反派、英雄等
        character_keywords = {
            '主角', '主人公', '英雄', '反派', '配角', '角色', '人物', '性格',
            '天才', '强者', '弱者', '智者', '勇士', '领袖', '导师'
        }
        
        # 风格特征：幽默、深刻、细腻等
        style_keywords = {
            '幽默', '深刻', '细腻', '宏大', '震撼', '感人', '温暖', '黑暗',
            '轻松', '沉重', '诗意', '哲理', '讽刺', '批判', '浪漫', '现实'
        }
        
        # 世界观：宇宙、文明、社会等
        worldview_keywords = {
            '宇宙', '文明', '社会', '世界', '时代', '历史', '未来', '现代',
            '古代', '王朝', '帝国', '国家', '民族', '种族', '星球', '维度'
        }
        
        # 5. 综合判断
        is_feature = False
        
        # 规则1：属于特征词类别
        if word in theme_keywords or word in plot_keywords or word in character_keywords:
            is_feature = True
        elif word in style_keywords or word in worldview_keywords:
            is_feature = True
        
        # 规则2：词性符合且长度>=3
        elif main_pos in feature_pos and len(word) >= 3:
            is_feature = True
        
        # 规则3：专有名词（人名、地名等）
        elif main_pos in ('nr', 'ns', 'nt', 'nz'):
            is_feature = True
        
        # 规则4：成语和习语
        elif main_pos in ('i', 'l'):
            is_feature = True
        
        # 规则5：高权重的名词（说明很有区分度）
        elif main_pos == 'n' and weight > 0.05 and len(word) >= 2:
            is_feature = True
        
        return is_feature
    
    @staticmethod
    def _process_book_comments(args):
        """处理单本书的评论（用于多进程）"""
        book_url, comments, book_id, stopwords = args
        
        try:
            # 获取高分评论
            high_rating_comments = []
            all_comments = []
            
            for _, row in comments.iterrows():
                comment_text = str(row.get('bookComment', ''))
                if comment_text and comment_text != 'nan':
                    all_comments.append(comment_text)
                    if row['rating_score'] >= 4:
                        high_rating_comments.append(comment_text)
            
            if not all_comments:
                return None
            
            # 合并评论文本
            high_rating_text = ' '.join(high_rating_comments) if high_rating_comments else ' '.join(all_comments)
            
            # 提取关键词（双算法 + 词性过滤）
            tfidf_keywords = jieba.analyse.extract_tags(
                high_rating_text,
                topK=50,
                withWeight=True,
                allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'vn', 'an', 'i', 'l')
            )
            
            textrank_keywords = jieba.analyse.textrank(
                high_rating_text,
                topK=40,
                withWeight=True,
                allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'vn', 'an', 'i', 'l')
            )
            
            # 合并权重
            keyword_dict = {}
            for word, weight in tfidf_keywords:
                keyword_dict[word] = keyword_dict.get(word, 0) + weight
            for word, weight in textrank_keywords:
                keyword_dict[word] = keyword_dict.get(word, 0) + weight * 0.8
            
            # 智能过滤：只保留图书特征词
            filtered_keywords = []
            for word, weight in keyword_dict.items():
                # 基础过滤
                if len(word) < 2 or word in stopwords:
                    continue
                if word.isdigit() or any(c.isdigit() for c in word):
                    continue
                if all(c in '，。！？、；：""''（）【】《》' for c in word):
                    continue
                
                # 智能判断是否为图书特征词
                if KeywordBasedRecommender._is_book_feature_keyword(word, weight, 0, 0):
                    filtered_keywords.append((word, weight))
            
            filtered_keywords.sort(key=lambda x: x[1], reverse=True)
            
            # 统计信息
            total_comments = len(comments)
            high_rating_count = len(high_rating_comments)
            avg_rating = comments['rating_score'].mean()
            
            return {
                'book_id': book_id,
                'keywords': [kw[0] for kw in filtered_keywords],
                'keyword_weights': dict(filtered_keywords),
                'stats': {
                    'total_comments': total_comments,
                    'like_count': high_rating_count,
                    'like_ratio': high_rating_count / total_comments if total_comments > 0 else 0,
                    'avg_rating': avg_rating,
                    'keywords': [kw[0] for kw in filtered_keywords[:10]]
                },
                'popularity': np.log1p(total_comments) * (1 + high_rating_count / total_comments if total_comments > 0 else 0)
            }
            
        except Exception as e:
            return None
    
    def _get_neighbors_by_type(self, book_id):
        """获取图书的邻居，按类型分组"""
        neighbors = {
            'author': [],
            'publisher': [],
            'translator': [],
            'series': []
        }
        
        for neighbor in self.graph.neighbors(book_id):
            neighbor_entity = self.entities.get(neighbor, {})
            entity_type = neighbor_entity.get('type')
            if entity_type in neighbors:
                neighbors[entity_type].append(neighbor)
        
        return neighbors
    
    def get_book_by_name(self, book_name):
        """根据书名查找图书实体"""
        book_name_lower = book_name.lower()
        
        for entity_id in self.book_entities:
            entity = self.entities[entity_id]
            if entity['name'].lower() == book_name_lower:
                return entity_id
        
        for entity_id in self.book_entities:
            entity = self.entities[entity_id]
            if book_name_lower in entity['name'].lower() or entity['name'].lower() in book_name_lower:
                return entity_id
        
        return None
    
    def _calculate_keyword_similarity(self, book_id1, book_id2):
        """计算两本书的关键词相似度"""
        if book_id1 not in self.book_keywords or book_id2 not in self.book_keywords:
            return 0.0
        
        keywords1 = set(self.book_keywords[book_id1])
        keywords2 = set(self.book_keywords[book_id2])
        
        # Jaccard相似度
        intersection = keywords1 & keywords2
        union = keywords1 | keywords2
        
        if not union:
            return 0.0
        
        # 考虑权重的相似度
        weights1 = self.book_keyword_weights.get(book_id1, {})
        weights2 = self.book_keyword_weights.get(book_id2, {})
        
        weighted_sim = 0.0
        for kw in intersection:
            weighted_sim += min(weights1.get(kw, 0), weights2.get(kw, 0))
        
        return weighted_sim
    
    def recommend(self, favorite_books, top_k=20, strategy='mixed', relations=None, selected_keywords=None):
        """
        基于关键词的深度推荐（支持自定义策略）
        
        Args:
            favorite_books: 用户喜欢的书籍名称列表
            top_k: 推荐数量
            strategy: 推荐策略
                - 'mixed': 混合策略（知识图谱 + 关键词）
                - 'kg_only': 仅使用知识图谱关系
                - 'keyword_only': 仅使用关键词匹配
            relations: 指定使用的知识图谱关系，None表示使用全部
                - 可选值: ['series', 'author', 'translator', 'publisher']
                - 例如: ['series', 'author'] 只使用系列和作者关系
            selected_keywords: 用户选择的关键词列表，None表示使用所有关键词
                - 例如: ['科幻', '宇宙', '文明'] 只使用这些关键词进行匹配
            
        Returns:
            推荐结果列表
        """
        # 设置默认关系
        if relations is None:
            relations = ['series', 'author', 'translator', 'publisher']
        
        # 关系权重配置
        relation_weights = {
            'series': 0.4,
            'author': 0.3,
            'translator': 0.2,
            'publisher': 0.15
        }
        
        print(f"\n开始推荐，用户喜欢的书籍: {favorite_books}")
        print(f"推荐策略: {strategy}")
        if strategy in ['mixed', 'kg_only']:
            print(f"使用关系: {', '.join(relations)}")
        
        # 查找用户喜欢的书籍
        favorite_entities = []
        for book_name in favorite_books:
            entity_id = self.get_book_by_name(book_name)
            if entity_id is not None:
                favorite_entities.append(entity_id)
                print(f"找到书籍: {self.entities[entity_id]['name']}")
                # 显示该书的关键词
                if entity_id in self.book_keywords and strategy in ['mixed', 'keyword_only']:
                    keywords = self.book_keywords[entity_id][:10]
                    print(f"  关键词: {', '.join(keywords)}")
            else:
                print(f"未找到书籍: {book_name}")
        
        if not favorite_entities:
            print("未找到任何匹配的书籍")
            return []
        
        # 收集用户喜欢书籍的所有关键词
        favorite_keywords = Counter()
        if strategy in ['mixed', 'keyword_only']:
            for fav_id in favorite_entities:
                if fav_id in self.book_keyword_weights:
                    for kw, weight in self.book_keyword_weights[fav_id].items():
                        favorite_keywords[kw] += weight
            
            # 如果用户指定了关键词，只使用这些关键词
            if selected_keywords:
                print(f"\n用户选择的关键词: {', '.join(selected_keywords)}")
                # 过滤出用户选择的关键词
                filtered_keywords = Counter()
                for kw in selected_keywords:
                    if kw in favorite_keywords:
                        filtered_keywords[kw] = favorite_keywords[kw]
                    else:
                        # 即使不在原关键词中，也给予一定权重
                        filtered_keywords[kw] = 0.5
                favorite_keywords = filtered_keywords
            
            print(f"\n用户偏好关键词（Top 20）: {', '.join([kw for kw, _ in favorite_keywords.most_common(20)])}")
        
        print(f"\n计算推荐得分...")
        candidate_scores = {}
        
        # 构建反向索引（仅构建需要的关系）
        author_books = defaultdict(set)
        series_books = defaultdict(set)
        publisher_books = defaultdict(set)
        translator_books = defaultdict(set)
        
        if strategy in ['mixed', 'kg_only']:
            for book_id in self.book_entities:
                neighbors = self.book_neighbors_cache[book_id]
                if 'author' in relations:
                    for author_id in neighbors['author']:
                        author_books[author_id].add(book_id)
                if 'series' in relations:
                    for series_id in neighbors['series']:
                        series_books[series_id].add(book_id)
                if 'publisher' in relations:
                    for pub_id in neighbors['publisher']:
                        publisher_books[pub_id].add(book_id)
                if 'translator' in relations:
                    for trans_id in neighbors['translator']:
                        translator_books[trans_id].add(book_id)
        
        # 1. 基于关键词的推荐
        if strategy in ['mixed', 'keyword_only']:
            print("基于关键词匹配...")
            for keyword, weight in favorite_keywords.most_common(50):
                for book_id in self.keyword_to_books.get(keyword, []):
                    if book_id not in favorite_entities:
                        if book_id not in candidate_scores:
                            candidate_scores[book_id] = {'score': 0, 'reasons': [], 'matched_keywords': [], 'strategy': strategy}
                        
                        # 关键词匹配得分
                        keyword_score = weight * (0.5 if strategy == 'mixed' else 1.0)
                        candidate_scores[book_id]['score'] += keyword_score
                        candidate_scores[book_id]['matched_keywords'].append(keyword)
        
        # 2. 基于知识图谱的推荐
        if strategy in ['mixed', 'kg_only']:
            print(f"基于知识图谱关系（{', '.join(relations)}）...")
            for fav_id in favorite_entities:
                fav_book = self.entities[fav_id]
                fav_neighbors = self.book_neighbors_cache[fav_id]
                
                # 相同系列
                if 'series' in relations:
                    for series_id in fav_neighbors['series']:
                        series_name = self.entities[series_id]['name']
                        for book_id in series_books[series_id]:
                            if book_id not in favorite_entities:
                                if book_id not in candidate_scores:
                                    candidate_scores[book_id] = {'score': 0, 'reasons': [], 'matched_keywords': [], 'strategy': strategy}
                                candidate_scores[book_id]['score'] += relation_weights['series']
                                candidate_scores[book_id]['reasons'].append(
                                    f"与《{fav_book['name']}》属于同一系列: {series_name}"
                                )
                
                # 相同作者
                if 'author' in relations:
                    for author_id in fav_neighbors['author']:
                        author_name = self.entities[author_id]['name']
                        for book_id in author_books[author_id]:
                            if book_id not in favorite_entities:
                                if book_id not in candidate_scores:
                                    candidate_scores[book_id] = {'score': 0, 'reasons': [], 'matched_keywords': [], 'strategy': strategy}
                                candidate_scores[book_id]['score'] += relation_weights['author']
                                candidate_scores[book_id]['reasons'].append(
                                    f"与《{fav_book['name']}》作者相同: {author_name}"
                                )
                
                # 相同译者
                if 'translator' in relations:
                    for trans_id in fav_neighbors['translator']:
                        trans_name = self.entities[trans_id]['name']
                        for book_id in translator_books[trans_id]:
                            if book_id not in favorite_entities:
                                if book_id not in candidate_scores:
                                    candidate_scores[book_id] = {'score': 0, 'reasons': [], 'matched_keywords': [], 'strategy': strategy}
                                candidate_scores[book_id]['score'] += relation_weights['translator']
                                candidate_scores[book_id]['reasons'].append(
                                    f"与《{fav_book['name']}》译者相同: {trans_name}"
                                )
                
                # 相同出版社
                if 'publisher' in relations:
                    for pub_id in fav_neighbors['publisher']:
                        pub_name = self.entities[pub_id]['name']
                        for book_id in publisher_books[pub_id]:
                            if book_id not in favorite_entities:
                                if book_id not in candidate_scores:
                                    candidate_scores[book_id] = {'score': 0, 'reasons': [], 'matched_keywords': [], 'strategy': strategy}
                                candidate_scores[book_id]['score'] += relation_weights['publisher']
                                candidate_scores[book_id]['reasons'].append(
                                    f"与《{fav_book['name']}》出版社相同: {pub_name}"
                                )
        
        # 3. 添加评分和评论加权
        print("添加评分和热度加权...")
        for book_id in candidate_scores:
            # 豆瓣评分
            rating = self.book_ratings.get(book_id, 0)
            if rating > 0:
                candidate_scores[book_id]['score'] += (rating / 10.0) * 0.15
                if rating >= 8.5:
                    candidate_scores[book_id]['reasons'].append(f"高分图书（豆瓣评分: {rating}）")
            
            # 评论热度
            if book_id in self.comment_stats:
                stats = self.comment_stats[book_id]
                popularity = self.book_popularity.get(book_id, 0)
                candidate_scores[book_id]['score'] += popularity * 0.05
                
                if stats['like_ratio'] > 0.7 and stats['total_comments'] > 50:
                    candidate_scores[book_id]['reasons'].append(
                        f"读者好评率高（{stats['like_count']}/{stats['total_comments']}条4-5星评论）"
                    )
                
                if stats['total_comments'] > 500:
                    candidate_scores[book_id]['reasons'].append(
                        f"热门图书（{stats['total_comments']}条评论）"
                    )
                
                if stats['avg_rating'] >= 4.0:
                    candidate_scores[book_id]['reasons'].append(
                        f"读者评分高（平均{stats['avg_rating']:.1f}星）"
                    )
            
            # 添加关键词匹配理由（根据策略决定是否显示）
            if strategy in ['mixed', 'keyword_only']:
                matched_kws = candidate_scores[book_id]['matched_keywords']
                if len(matched_kws) >= 3:  # 至少匹配3个关键词才考虑显示
                    # 过滤出真正有意义的关键词
                    meaningful_kws = []
                    for kw in matched_kws[:10]:
                        if kw in favorite_keywords and len(kw) >= 2:
                            meaningful_kws.append(kw)
                    
                    # 只有当有足够多的有意义关键词时才显示
                    if len(meaningful_kws) >= 3:
                        kw_reason = f"评论关键词匹配: {', '.join(meaningful_kws[:5])}"
                        # 在kg_only模式下不显示关键词，在其他模式下显示
                        if strategy == 'keyword_only':
                            # keyword_only模式：关键词理由放在最前面
                            candidate_scores[book_id]['reasons'].insert(0, kw_reason)
                        elif strategy == 'mixed':
                            # mixed模式：关键词理由放在知识图谱关系之后
                            candidate_scores[book_id]['reasons'].append(kw_reason)
        
        print(f"找到 {len(candidate_scores)} 本候选书籍")
        
        # 排序并返回Top-K
        sorted_candidates = sorted(
            candidate_scores.items(), 
            key=lambda x: x[1]['score'], 
            reverse=True
        )[:top_k]
        
        # 构建推荐结果
        recommendations = []
        for book_id, info in sorted_candidates:
            book = self.entities[book_id]
            rating = self.book_ratings.get(book_id, 0)
            
            # 去重推荐理由
            unique_reasons = []
            seen = set()
            for reason in info['reasons']:
                if reason not in seen:
                    unique_reasons.append(reason)
                    seen.add(reason)
            
            recommendations.append({
                'book_id': book_id,
                'book_name': book['name'],
                'book_url': book.get('url', ''),
                'rating': rating,
                'score': float(info['score']),
                'reasons': unique_reasons[:5],  # 最多5条理由
                'keywords': self.comment_stats.get(book_id, {}).get('keywords', []),
                'matched_keywords': info['matched_keywords'][:10],
                'comment_stats': self.comment_stats.get(book_id, {}),
                'explanation': self._generate_explanation(book, unique_reasons, rating)
            })
        
        print(f"\n推荐完成，共推荐 {len(recommendations)} 本书")
        return recommendations
    
    def _generate_explanation(self, book, reasons, rating):
        """生成推荐解释"""
        explanation = f"推荐《{book['name']}》"
        
        if rating > 0:
            explanation += f"（豆瓣评分: {rating}）"
        
        explanation += "的理由：\n"
        
        if reasons:
            for i, reason in enumerate(reasons[:5], 1):
                explanation += f"{i}. {reason}\n"
        else:
            explanation += "与您喜欢的书籍相似"
        
        return explanation.strip()


if __name__ == '__main__':
    import time
    
    recommender = KeywordBasedRecommender()
    recommender.load_kg()
    recommender.load_and_analyze_comments()
    
    # 测试推荐
    favorite_books = ['三体']
    
    start_time = time.time()
    recommendations = recommender.recommend(favorite_books, top_k=20)
    end_time = time.time()
    
    print(f"\n推荐耗时: {end_time - start_time:.2f} 秒")
    print("\n" + "="*80)
    print("推荐结果:")
    print("="*80)
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['book_name']}")
        print(f"   得分: {rec['score']:.3f} | 评分: {rec['rating']}")
        if rec['keywords']:
            print(f"   书籍关键词: {', '.join(rec['keywords'])}")
        if rec['matched_keywords']:
            print(f"   匹配关键词: {', '.join(rec['matched_keywords'][:10])}")
        print(f"   推荐理由:")
        for reason in rec['reasons']:
            print(f"     • {reason}")

