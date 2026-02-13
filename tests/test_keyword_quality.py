# -*- coding: utf-8 -*-
"""
测试关键词提取质量
"""
import pickle
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import config
from src.core.keyword_recommender import KeywordBasedRecommender

def test_keyword_quality():
    """测试关键词质量"""
    print("加载推荐系统...")
    recommender = KeywordBasedRecommender()
    recommender.load_kg()
    recommender.load_and_analyze_comments()
    
    print("\n" + "="*80)
    print("关键词质量检查")
    print("="*80)
    
    # 随机抽取一些书籍检查关键词
    import random
    sample_books = random.sample(list(recommender.book_keywords.keys()), min(10, len(recommender.book_keywords)))
    
    for book_id in sample_books:
        book = recommender.entities[book_id]
        keywords = recommender.book_keywords.get(book_id, [])
        
        print(f"\n书名: {book['name']}")
        print(f"评分: {recommender.book_ratings.get(book_id, 0)}")
        
        if book_id in recommender.comment_stats:
            stats = recommender.comment_stats[book_id]
            print(f"评论数: {stats['total_comments']}, 好评率: {stats['like_ratio']:.1%}")
        
        print(f"关键词 ({len(keywords)}个):")
        if keywords:
            # 显示前15个关键词
            for i, kw in enumerate(keywords[:15], 1):
                weight = recommender.book_keyword_weights[book_id].get(kw, 0)
                print(f"  {i:2d}. {kw:10s} (权重: {weight:.4f})")
        else:
            print("  无关键词")
    
    # 统计关键词长度分布
    print("\n" + "="*80)
    print("关键词长度分布")
    print("="*80)
    
    length_dist = {}
    for book_id, keywords in recommender.book_keywords.items():
        for kw in keywords:
            length = len(kw)
            length_dist[length] = length_dist.get(length, 0) + 1
    
    for length in sorted(length_dist.keys()):
        count = length_dist[length]
        print(f"长度 {length}: {count:5d} 个关键词")
    
    # 检查是否还有无意义词
    print("\n" + "="*80)
    print("检查常见无意义词")
    print("="*80)
    
    meaningless_words = ['知道', '想要', '作者', '小说', '故事', '喜欢', '觉得', '感觉', '推荐', '不错']
    
    for word in meaningless_words:
        count = 0
        for keywords in recommender.book_keywords.values():
            if word in keywords:
                count += 1
        if count > 0:
            print(f"'{word}' 出现在 {count} 本书的关键词中")
        else:
            print(f"'{word}' ✓ 已被过滤")

if __name__ == '__main__':
    test_keyword_quality()

