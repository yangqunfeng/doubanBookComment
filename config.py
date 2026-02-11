# -*- coding: utf-8 -*-
"""
配置文件
"""
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据文件路径
DATA_DIR = BASE_DIR
BOOK_INFO_FILE = os.path.join(DATA_DIR, 'newBookInformation')
COMMENT_FILE = os.path.join(DATA_DIR, 'newCommentdata')
STOPWORDS_FILE = os.path.join(DATA_DIR, 'ChineseStopWords.txt')

# 知识图谱相关配置
KG_DIR = os.path.join(BASE_DIR, 'knowledge_graph')
KG_ENTITIES_FILE = os.path.join(KG_DIR, 'entities.pkl')
KG_RELATIONS_FILE = os.path.join(KG_DIR, 'relations.pkl')
KG_EMBEDDINGS_FILE = os.path.join(KG_DIR, 'embeddings.pkl')

# 模型配置
EMBEDDING_DIM = 128
LEARNING_RATE = 0.001
BATCH_SIZE = 256
EPOCHS = 50

# 推荐配置
TOP_K = 20  # 推荐Top-K本书
MIN_PATH_LENGTH = 2  # 最小推理路径长度
MAX_PATH_LENGTH = 4  # 最大推理路径长度

# Web服务配置
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False  # 关闭调试模式，避免重复加载

