# -*- coding: utf-8 -*-
"""
快速启动脚本
用于首次运行系统时的初始化和启动
"""
import os
import sys
import subprocess
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.logger_config import get_logger

# 初始化日志
logger = get_logger('start')


def check_dependencies():
    """检查依赖是否安装"""
    logger.info("=" * 60)
    logger.info("检查依赖...")
    logger.info("=" * 60)
    
    try:
        import flask
        import pandas
        import numpy
        import networkx
        import sklearn
        import jieba
        logger.info("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        logger.error(f"✗ 缺少依赖: {e}")
        logger.info("\n请运行以下命令安装依赖:")
        logger.info("pip install -r requirements.txt")
        return False


def check_data_files():
    """检查数据文件是否存在"""
    logger.info("\n" + "=" * 60)
    logger.info("检查数据文件...")
    logger.info("=" * 60)
    
    files = ['data/raw/newBookInformation', 'data/raw/newCommentdata']
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            logger.info(f"✓ {file} 存在")
        else:
            logger.warning(f"✗ {file} 不存在")
            all_exist = False
    
    if not all_exist:
        logger.warning("\n警告: 部分数据文件不存在")
        logger.info("系统将尝试使用现有数据构建知识图谱")
    
    return all_exist


def build_knowledge_graph():
    """构建知识图谱"""
    logger.info("\n" + "=" * 60)
    logger.info("构建知识图谱...")
    logger.info("=" * 60)
    
    kg_dir = 'data/processed/knowledge_graph'
    entities_file = os.path.join(kg_dir, 'entities.pkl')
    
    if os.path.exists(entities_file):
        logger.info("✓ 知识图谱已存在，跳过构建")
        return True
    
    logger.info("开始构建知识图谱（这可能需要几分钟）...")
    
    try:
        from src.core.knowledge_graph_builder import KnowledgeGraphBuilder
        builder = KnowledgeGraphBuilder()
        builder.build()
        logger.info("✓ 知识图谱构建完成")
        return True
    except Exception as e:
        logger.error(f"✗ 知识图谱构建失败: {e}", exc_info=True)
        return False


def compute_embeddings():
    """计算实体嵌入"""
    logger.info("\n" + "=" * 60)
    logger.info("计算实体嵌入...")
    logger.info("=" * 60)
    
    kg_dir = 'data/processed/knowledge_graph'
    embeddings_file = os.path.join(kg_dir, 'embeddings.pkl')
    
    if os.path.exists(embeddings_file):
        logger.info("✓ 实体嵌入已存在，跳过计算")
        return True
    
    logger.info("开始计算实体嵌入（这可能需要几分钟）...")
    
    try:
        from recommender import KGRecommender
        recommender = KGRecommender()
        recommender.load_kg()
        recommender.compute_embeddings()
        logger.info("✓ 实体嵌入计算完成")
        return True
    except Exception as e:
        logger.error(f"✗ 实体嵌入计算失败: {e}", exc_info=True)
        logger.warning("系统将在没有嵌入的情况下运行（仅使用路径推理）")
        return False


def start_server():
    """启动Web服务"""
    logger.info("\n" + "=" * 60)
    logger.info("启动Web服务...")
    logger.info("=" * 60)
    
    try:
        logger.info("\n服务启动中...")
        logger.info("访问地址: http://localhost:5000")
        logger.info("按 Ctrl+C 停止服务\n")
        
        import app
        app.init_recommender()
        app.app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        logger.info("\n\n服务已停止")
    except Exception as e:
        logger.error(f"\n✗ 服务启动失败: {e}", exc_info=True)


def main():
    """主函数"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 10 + "基于知识图谱的可解释图书推荐系统" + " " * 10 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    logger.info("\n")
    
    # 1. 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 2. 检查数据文件
    check_data_files()
    
    # 3. 构建知识图谱
    if not build_knowledge_graph():
        logger.error("\n知识图谱构建失败，无法继续")
        sys.exit(1)
    
    # 4. 计算实体嵌入
    compute_embeddings()
    
    # 5. 启动服务
    start_server()


if __name__ == '__main__':
    main()

