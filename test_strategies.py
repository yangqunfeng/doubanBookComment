# -*- coding: utf-8 -*-
"""
测试不同的推荐策略
"""
from keyword_recommender import KeywordBasedRecommender

def test_strategies():
    """测试不同推荐策略"""
    print("初始化推荐系统...")
    recommender = KeywordBasedRecommender()
    recommender.load_kg()
    recommender.load_and_analyze_comments()
    
    favorite_books = ['三体']
    
    print("\n" + "="*80)
    print("测试不同推荐策略")
    print("="*80)
    
    # 1. 仅使用知识图谱 - 所有关系
    print("\n【策略1】仅知识图谱 - 所有关系")
    print("-" * 80)
    recs = recommender.recommend(
        favorite_books, 
        top_k=5,
        strategy='kg_only',
        relations=['series', 'author', 'translator', 'publisher']
    )
    print_recommendations(recs)
    
    # 2. 仅使用知识图谱 - 只用系列和作者
    print("\n【策略2】仅知识图谱 - 只用系列和作者")
    print("-" * 80)
    recs = recommender.recommend(
        favorite_books, 
        top_k=5,
        strategy='kg_only',
        relations=['series', 'author']
    )
    print_recommendations(recs)
    
    # 3. 仅使用知识图谱 - 只用作者
    print("\n【策略3】仅知识图谱 - 只用作者")
    print("-" * 80)
    recs = recommender.recommend(
        favorite_books, 
        top_k=5,
        strategy='kg_only',
        relations=['author']
    )
    print_recommendations(recs)
    
    # 4. 仅使用关键词
    print("\n【策略4】仅关键词匹配")
    print("-" * 80)
    recs = recommender.recommend(
        favorite_books, 
        top_k=5,
        strategy='keyword_only'
    )
    print_recommendations(recs)
    
    # 5. 混合策略
    print("\n【策略5】混合策略（知识图谱 + 关键词）")
    print("-" * 80)
    recs = recommender.recommend(
        favorite_books, 
        top_k=5,
        strategy='mixed',
        relations=['series', 'author']
    )
    print_recommendations(recs)

def print_recommendations(recommendations):
    """打印推荐结果"""
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['book_name']}")
        print(f"   得分: {rec['score']:.3f} | 评分: {rec['rating']}")
        print(f"   推荐理由:")
        for reason in rec['reasons']:
            print(f"     • {reason}")

if __name__ == '__main__':
    test_strategies()

