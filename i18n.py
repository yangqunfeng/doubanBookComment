# -*- coding: utf-8 -*-
"""
国际化配置
支持中文和英文
"""

TRANSLATIONS = {
    'zh': {
        # 页面标题
        'page_title': '智能图书推荐系统 - 基于知识图谱的可解释推荐',
        'main_title': '智能图书推荐系统',
        'subtitle': '基于知识图谱的可解释推荐引擎',
        
        # 统计信息
        'stat_books': '图书',
        'stat_authors': '作者',
        'stat_publishers': '出版社',
        'stat_relations': '关系',
        
        # 输入区域
        'input_title': '告诉我们你喜欢的书',
        'input_subtitle': '输入你最喜欢的书籍名称，我们将为你推荐相似的好书',
        'input_placeholder': '输入书名，例如：三体、活着、百年孤独...',
        'btn_add': '添加',
        'empty_books': '还没有添加喜欢的书籍',
        
        # 关键词选择
        'keywords_title': '选择感兴趣的关键词',
        'keywords_subtitle': '（可选，不选则使用所有关键词）',
        'loading_keywords': '正在加载关键词...',
        'btn_select_all': '全选',
        'btn_clear_selection': '清空选择',
        
        # 推荐策略
        'strategy_title': '推荐策略',
        'strategy_mixed': '混合推荐',
        'strategy_mixed_desc': '结合知识图谱关系和评论关键词',
        'strategy_kg': '知识图谱',
        'strategy_kg_desc': '基于作者、系列、出版社等关系',
        'strategy_keyword': '内容相似',
        'strategy_keyword_desc': '基于读者评论关键词匹配',
        
        # 关系选择
        'relations_title': '选择关系类型',
        'relation_series': '系列',
        'relation_author': '作者',
        'relation_translator': '译者',
        'relation_publisher': '出版社',
        
        # 按钮
        'btn_recommend': '开始推荐',
        'btn_clear': '清空',
        
        # 推荐结果
        'results_title': '为你推荐',
        'results_subtitle': '基于你的阅读偏好，我们为你精选了以下书籍',
        'loading_text': '正在分析你的阅读偏好...',
        'match_score': '匹配度',
        'reason_title': '推荐理由',
        'view_detail': '查看详情',
        'no_results': '暂时没有找到合适的推荐',
        
        # 页脚
        'footer_text': '基于知识图谱的可解释图书推荐系统',
        'footer_note': '数据来源：豆瓣读书 | 推荐算法：知识图谱 + 图嵌入',
        
        # 消息提示
        'msg_book_added': '已添加',
        'msg_book_removed': '已移除',
        'msg_book_exists': '该书籍已添加',
        'msg_book_not_found': '未找到该书籍',
        'msg_input_book': '请输入书名',
        'msg_select_book': '请至少添加一本喜欢的书籍',
        'msg_select_relation': '请至少选择一种关系类型',
        'msg_recommend_success': '为您推荐了',
        'msg_recommend_books': '本书',
        'msg_keywords_selected': '已全选关键词',
        'msg_keywords_cleared': '已清空选择',
        'msg_cleared': '已清空所有书籍',
        'msg_confirm_clear': '确定要清空所有书籍吗？',
    },
    'en': {
        # Page titles
        'page_title': 'Smart Book Recommendation System - Explainable Recommendations Based on Knowledge Graph',
        'main_title': 'Smart Book Recommendation',
        'subtitle': 'Explainable Recommendation Engine Based on Knowledge Graph',
        
        # Statistics
        'stat_books': 'Books',
        'stat_authors': 'Authors',
        'stat_publishers': 'Publishers',
        'stat_relations': 'Relations',
        
        # Input area
        'input_title': 'Tell Us Your Favorite Books',
        'input_subtitle': 'Enter your favorite book titles, and we will recommend similar great books',
        'input_placeholder': 'Enter book title, e.g.: The Three-Body Problem, To Live, One Hundred Years of Solitude...',
        'btn_add': 'Add',
        'empty_books': 'No favorite books added yet',
        
        # Keywords selection
        'keywords_title': 'Select Keywords of Interest',
        'keywords_subtitle': '(Optional, all keywords will be used if none selected)',
        'loading_keywords': 'Loading keywords...',
        'btn_select_all': 'Select All',
        'btn_clear_selection': 'Clear Selection',
        
        # Recommendation strategy
        'strategy_title': 'Recommendation Strategy',
        'strategy_mixed': 'Mixed',
        'strategy_mixed_desc': 'Combine knowledge graph and comment keywords',
        'strategy_kg': 'Knowledge Graph',
        'strategy_kg_desc': 'Based on author, series, publisher relations',
        'strategy_keyword': 'Content Similarity',
        'strategy_keyword_desc': 'Based on reader comment keyword matching',
        
        # Relations selection
        'relations_title': 'Select Relation Types',
        'relation_series': 'Series',
        'relation_author': 'Author',
        'relation_translator': 'Translator',
        'relation_publisher': 'Publisher',
        
        # Buttons
        'btn_recommend': 'Get Recommendations',
        'btn_clear': 'Clear',
        
        # Recommendation results
        'results_title': 'Recommendations for You',
        'results_subtitle': 'Based on your reading preferences, we have selected the following books',
        'loading_text': 'Analyzing your reading preferences...',
        'match_score': 'Match',
        'reason_title': 'Reasons',
        'view_detail': 'View Details',
        'no_results': 'No suitable recommendations found',
        
        # Footer
        'footer_text': 'Explainable Book Recommendation System Based on Knowledge Graph',
        'footer_note': 'Data Source: Douban Books | Algorithm: Knowledge Graph + Graph Embedding',
        
        # Messages
        'msg_book_added': 'Added',
        'msg_book_removed': 'Removed',
        'msg_book_exists': 'This book has already been added',
        'msg_book_not_found': 'Book not found',
        'msg_input_book': 'Please enter a book title',
        'msg_select_book': 'Please add at least one favorite book',
        'msg_select_relation': 'Please select at least one relation type',
        'msg_recommend_success': 'Recommended',
        'msg_recommend_books': 'books for you',
        'msg_keywords_selected': 'All keywords selected',
        'msg_keywords_cleared': 'Selection cleared',
        'msg_cleared': 'All books cleared',
        'msg_confirm_clear': 'Are you sure you want to clear all books?',
    }
}

def get_text(key, lang='zh'):
    """获取翻译文本"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['zh']).get(key, key)

