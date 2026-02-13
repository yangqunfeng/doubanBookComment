# -*- coding: utf-8 -*-
"""
Flask Web API服务
提供图书推荐的RESTful API
支持中英文双语
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import config
from src.core.keyword_recommender import KeywordBasedRecommender
from src.utils.i18n import get_text, TRANSLATIONS
from src.utils.logger_config import get_logger
from functools import wraps
from datetime import datetime

# 初始化日志
logger = get_logger('app')
access_logger = get_logger('access')  # 专门的访问日志

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化推荐器
recommender = None


def log_access(f):
    """访问日志装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取客户端信息
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip and ',' in ip:
            ip = ip.split(',')[0].strip()
        
        user_agent = request.headers.get('User-Agent', 'Unknown')
        method = request.method
        path = request.path
        query_string = request.query_string.decode('utf-8')
        
        # 记录访问
        access_logger.info(
            f"IP={ip} | Method={method} | Path={path} | "
            f"Query={query_string} | UserAgent={user_agent}"
        )
        
        return f(*args, **kwargs)
    return decorated_function


def init_recommender():
    """初始化推荐器"""
    global recommender
    if recommender is None:
        logger.info("正在初始化基于关键词的推荐系统...")
        recommender = KeywordBasedRecommender()
        recommender.load_kg()
        recommender.load_and_analyze_comments()
        logger.info("推荐系统初始化完成！")


@app.route('/')
@log_access
def index():
    """首页"""
    # 获取语言参数，默认中文
    lang = request.args.get('lang', 'zh')
    if lang not in ['zh', 'en']:
        lang = 'zh'
    return render_template('index.html', lang=lang, translations=TRANSLATIONS[lang])


@app.route('/api/translations/<lang>', methods=['GET'])
def get_translations(lang):
    """获取翻译文本API"""
    if lang not in TRANSLATIONS:
        lang = 'zh'
    
    return jsonify({
        'success': True,
        'data': {
            'lang': lang,
            'translations': TRANSLATIONS[lang]
        }
    })


@app.route('/api/book/<int:book_id>/keywords', methods=['GET'])
def get_book_keywords(book_id):
    """获取书籍的评论关键词"""
    try:
        logger.info(f"获取书籍关键词请求: book_id={book_id}")
        if book_id not in recommender.entities:
            logger.warning(f"书籍不存在: book_id={book_id}")
            return jsonify({
                'success': False,
                'message': '书籍不存在'
            }), 404
        
        entity = recommender.entities[book_id]
        
        # 获取关键词
        keywords = []
        if book_id in recommender.book_keywords:
            keyword_list = recommender.book_keywords[book_id]
            keyword_weights = recommender.book_keyword_weights.get(book_id, {})
            
            # 构建关键词列表（带权重）
            for kw in keyword_list[:30]:  # 最多返回30个
                keywords.append({
                    'word': kw,
                    'weight': keyword_weights.get(kw, 0)
                })
        
        # 获取评论统计
        comment_stats = recommender.comment_stats.get(book_id, {})
        
        return jsonify({
            'success': True,
            'data': {
                'book_id': book_id,
                'book_name': entity['name'],
                'keywords': keywords,
                'total_keywords': len(keywords),
                'comment_stats': {
                    'total_comments': comment_stats.get('total_comments', 0),
                    'avg_rating': comment_stats.get('avg_rating', 0)
                }
            }
        })
    
    except Exception as e:
        logger.error(f"获取书籍关键词出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'获取失败: {str(e)}'
        }), 500


@app.route('/api/recommend', methods=['POST'])
@log_access
def recommend():
    """推荐API"""
    try:
        # 获取请求数据
        data = request.get_json()
        favorite_books = data.get('favorite_books', [])
        top_k = data.get('top_k', config.TOP_K)
        strategy = data.get('strategy', 'mixed')  # 推荐策略
        relations = data.get('relations', None)  # 指定使用的关系
        selected_keywords = data.get('selected_keywords', None)  # 用户选择的关键词
        
        logger.info(f"推荐请求: books={favorite_books}, strategy={strategy}, top_k={top_k}")
        
        if not favorite_books:
            return jsonify({
                'success': False,
                'message': '请至少输入一本喜欢的书籍'
            }), 400
        
        # 验证策略
        valid_strategies = ['mixed', 'kg_only', 'keyword_only']
        if strategy not in valid_strategies:
            return jsonify({
                'success': False,
                'message': f'无效的推荐策略，可选值: {", ".join(valid_strategies)}'
            }), 400
        
        # 验证关系
        if relations is not None:
            valid_relations = ['series', 'author', 'translator', 'publisher']
            for rel in relations:
                if rel not in valid_relations:
                    return jsonify({
                        'success': False,
                        'message': f'无效的关系类型: {rel}，可选值: {", ".join(valid_relations)}'
                    }), 400
        
        # 执行推荐
        recommendations = recommender.recommend(
            favorite_books, 
            top_k=top_k,
            strategy=strategy,
            relations=relations,
            selected_keywords=selected_keywords
        )
        
        return jsonify({
            'success': True,
            'data': {
                'favorite_books': favorite_books,
                'strategy': strategy,
                'relations': relations,
                'selected_keywords': selected_keywords,
                'recommendations': recommendations,
                'total': len(recommendations)
            }
        })
    
    except Exception as e:
        logger.error(f"推荐出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'推荐失败: {str(e)}'
        }), 500


@app.route('/api/search', methods=['GET'])
@log_access
def search_books():
    """搜索书籍API"""
    try:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 10))
        
        logger.info(f"搜索请求: query={query}, limit={limit}")
        
        if not query:
            return jsonify({
                'success': False,
                'message': '请输入搜索关键词'
            }), 400
        
        # 搜索书籍
        results = []
        for entity_id in recommender.book_entities:
            entity = recommender.entities[entity_id]
            if query.lower() in entity['name'].lower():
                results.append({
                    'book_id': entity_id,
                    'book_name': entity['name'],
                    'book_url': entity.get('url', ''),
                    'rating': entity.get('rating', 0)
                })
                if len(results) >= limit:
                    break
        
        return jsonify({
            'success': True,
            'data': {
                'query': query,
                'results': results,
                'total': len(results)
            }
        })
    
    except Exception as e:
        logger.error(f"搜索出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'搜索失败: {str(e)}'
        }), 500


@app.route('/api/book/<int:book_id>', methods=['GET'])
@log_access
def get_book_detail(book_id):
    """获取书籍详情API"""
    try:
        if book_id not in recommender.entities:
            return jsonify({
                'success': False,
                'message': '书籍不存在'
            }), 404
        
        entity = recommender.entities[book_id]
        
        # 获取相关实体
        related = {
            'authors': [],
            'publishers': [],
            'translators': [],
            'series': []
        }
        
        for neighbor in recommender.graph.neighbors(book_id):
            neighbor_entity = recommender.entities.get(neighbor, {})
            entity_type = neighbor_entity.get('type')
            
            if entity_type == 'author':
                related['authors'].append(neighbor_entity['name'])
            elif entity_type == 'publisher':
                related['publishers'].append(neighbor_entity['name'])
            elif entity_type == 'translator':
                related['translators'].append(neighbor_entity['name'])
            elif entity_type == 'series':
                related['series'].append(neighbor_entity['name'])
        
        return jsonify({
            'success': True,
            'data': {
                'book_id': book_id,
                'book_name': entity['name'],
                'book_url': entity.get('url', ''),
                'rating': entity.get('rating', 0),
                'related': related
            }
        })
    
    except Exception as e:
        logger.error(f"获取书籍详情出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'获取失败: {str(e)}'
        }), 500


@app.route('/api/stats', methods=['GET'])
@log_access
def get_stats():
    """获取系统统计信息"""
    try:
        stats = {
            'total_entities': len(recommender.entities),
            'total_relations': len(recommender.relations),
            'books': len(recommender.entity_types.get('book', [])),
            'authors': len(recommender.entity_types.get('author', [])),
            'publishers': len(recommender.entity_types.get('publisher', [])),
            'translators': len(recommender.entity_types.get('translator', [])),
            'series': len(recommender.entity_types.get('series', []))
        }
        
        return jsonify({
            'success': True,
            'data': stats
        })
    
    except Exception as e:
        logger.error(f"获取统计信息出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'获取失败: {str(e)}'
        }), 500


if __name__ == '__main__':
    init_recommender()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG, use_reloader=False)

