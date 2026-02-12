# -*- coding: utf-8 -*-
"""
快速启动脚本
用于首次运行系统时的初始化和启动
"""
import os
import sys
import subprocess


def check_dependencies():
    """检查依赖是否安装"""
    print("=" * 60)
    print("检查依赖...")
    print("=" * 60)
    
    try:
        import flask
        import pandas
        import numpy
        import networkx
        import sklearn
        import jieba
        print("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False


def check_data_files():
    """检查数据文件是否存在"""
    print("\n" + "=" * 60)
    print("检查数据文件...")
    print("=" * 60)
    
    files = ['newBookInformation', 'newCommentdata']
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file} 存在")
        else:
            print(f"✗ {file} 不存在")
            all_exist = False
    
    if not all_exist:
        print("\n警告: 部分数据文件不存在")
        print("系统将尝试使用现有数据构建知识图谱")
    
    return all_exist


def build_knowledge_graph():
    """构建知识图谱"""
    print("\n" + "=" * 60)
    print("构建知识图谱...")
    print("=" * 60)
    
    kg_dir = 'knowledge_graph'
    entities_file = os.path.join(kg_dir, 'entities.pkl')
    
    if os.path.exists(entities_file):
        print("✓ 知识图谱已存在，跳过构建")
        return True
    
    print("开始构建知识图谱（这可能需要几分钟）...")
    
    try:
        from knowledge_graph_builder import KnowledgeGraphBuilder
        builder = KnowledgeGraphBuilder()
        builder.build()
        print("✓ 知识图谱构建完成")
        return True
    except Exception as e:
        print(f"✗ 知识图谱构建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def compute_embeddings():
    """计算实体嵌入"""
    print("\n" + "=" * 60)
    print("计算实体嵌入...")
    print("=" * 60)
    
    kg_dir = 'knowledge_graph'
    embeddings_file = os.path.join(kg_dir, 'embeddings.pkl')
    
    if os.path.exists(embeddings_file):
        print("✓ 实体嵌入已存在，跳过计算")
        return True
    
    print("开始计算实体嵌入（这可能需要几分钟）...")
    
    try:
        from recommender import KGRecommender
        recommender = KGRecommender()
        recommender.load_kg()
        recommender.compute_embeddings()
        print("✓ 实体嵌入计算完成")
        return True
    except Exception as e:
        print(f"✗ 实体嵌入计算失败: {e}")
        print("系统将在没有嵌入的情况下运行（仅使用路径推理）")
        return False


def start_server():
    """启动Web服务"""
    print("\n" + "=" * 60)
    print("启动Web服务...")
    print("=" * 60)
    
    try:
        print("\n服务启动中...")
        print("访问地址: http://localhost:5000")
        print("按 Ctrl+C 停止服务\n")
        
        import app
        app.init_recommender()
        app.app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n服务已停止")
    except Exception as e:
        print(f"\n✗ 服务启动失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "基于知识图谱的可解释图书推荐系统" + " " * 10 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    # 1. 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 2. 检查数据文件
    check_data_files()
    
    # 3. 构建知识图谱
    if not build_knowledge_graph():
        print("\n知识图谱构建失败，无法继续")
        sys.exit(1)
    
    # 4. 计算实体嵌入
    compute_embeddings()
    
    # 5. 启动服务
    start_server()


if __name__ == '__main__':
    main()

