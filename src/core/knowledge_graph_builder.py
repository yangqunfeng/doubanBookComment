# -*- coding: utf-8 -*-
"""
知识图谱构建模块
从图书数据构建知识图谱，包含实体和关系
"""
import pandas as pd
import numpy as np
import pickle
import os
import sys
from pathlib import Path
from collections import defaultdict
import networkx as nx
from tqdm import tqdm

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import config


class KnowledgeGraphBuilder:
    """知识图谱构建器"""
    
    def __init__(self):
        self.entities = {}  # 实体字典 {entity_id: entity_info}
        self.relations = []  # 关系列表 [(head, relation, tail)]
        self.entity_types = {
            'book': [],
            'author': [],
            'publisher': [],
            'translator': [],
            'series': [],
            'user': [],
            'word': []
        }
        self.graph = nx.MultiDiGraph()
        
    def load_data(self):
        """加载数据"""
        print("正在加载数据...")
        try:
            self.book_data = pd.read_pickle(config.BOOK_INFO_FILE)
            print(f"成功加载 {len(self.book_data)} 条图书信息")
        except Exception as e:
            print(f"加载图书信息失败: {e}")
            self.book_data = pd.DataFrame()
            
        try:
            self.comment_data = pd.read_pickle(config.COMMENT_FILE)
            print(f"成功加载 {len(self.comment_data)} 条评论数据")
        except Exception as e:
            print(f"加载评论数据失败: {e}")
            self.comment_data = pd.DataFrame()
    
    def build_entities(self):
        """构建实体"""
        print("\n正在构建实体...")
        entity_id = 0
        
        # 构建图书实体
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="处理图书实体"):
                book_url = str(row.get('bookUrl', ''))
                if book_url and book_url != 'nan':
                    self.entities[entity_id] = {
                        'id': entity_id,
                        'type': 'book',
                        'name': str(row.get('bookName', '')),
                        'url': book_url,
                        'rating': row.get('bookScore', 0),
                        'original_data': row.to_dict()
                    }
                    self.entity_types['book'].append(entity_id)
                    self.graph.add_node(entity_id, type='book', name=str(row.get('bookName', '')))
                    entity_id += 1
        
        # 构建作者实体
        author_map = {}
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="处理作者实体"):
                author = str(row.get('author', ''))
                if author and author != 'nan' and author not in author_map:
                    author_map[author] = entity_id
                    self.entities[entity_id] = {
                        'id': entity_id,
                        'type': 'author',
                        'name': author
                    }
                    self.entity_types['author'].append(entity_id)
                    self.graph.add_node(entity_id, type='author', name=author)
                    entity_id += 1
        
        # 构建出版社实体
        publisher_map = {}
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="处理出版社实体"):
                publisher = str(row.get('publisher', ''))
                if publisher and publisher != 'nan' and publisher not in publisher_map:
                    publisher_map[publisher] = entity_id
                    self.entities[entity_id] = {
                        'id': entity_id,
                        'type': 'publisher',
                        'name': publisher
                    }
                    self.entity_types['publisher'].append(entity_id)
                    self.graph.add_node(entity_id, type='publisher', name=publisher)
                    entity_id += 1
        
        # 构建译者实体
        translator_map = {}
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="处理译者实体"):
                translator = str(row.get('translator', ''))
                if translator and translator != 'nan' and translator not in translator_map:
                    translator_map[translator] = entity_id
                    self.entities[entity_id] = {
                        'id': entity_id,
                        'type': 'translator',
                        'name': translator
                    }
                    self.entity_types['translator'].append(entity_id)
                    self.graph.add_node(entity_id, type='translator', name=translator)
                    entity_id += 1
        
        # 构建系列实体
        series_map = {}
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="处理系列实体"):
                series = str(row.get('seriesOfBook', ''))
                if series and series != 'nan' and series not in series_map:
                    series_map[series] = entity_id
                    self.entities[entity_id] = {
                        'id': entity_id,
                        'type': 'series',
                        'name': series
                    }
                    self.entity_types['series'].append(entity_id)
                    self.graph.add_node(entity_id, type='series', name=series)
                    entity_id += 1
        
        self.author_map = author_map
        self.publisher_map = publisher_map
        self.translator_map = translator_map
        self.series_map = series_map
        
        print(f"\n实体构建完成:")
        print(f"  - 图书: {len(self.entity_types['book'])}")
        print(f"  - 作者: {len(self.entity_types['author'])}")
        print(f"  - 出版社: {len(self.entity_types['publisher'])}")
        print(f"  - 译者: {len(self.entity_types['translator'])}")
        print(f"  - 系列: {len(self.entity_types['series'])}")
        print(f"  总计: {len(self.entities)} 个实体")
    
    def build_relations(self):
        """构建关系"""
        print("\n正在构建关系...")
        
        # 创建URL到实体ID的映射
        url_to_entity = {}
        for eid, entity in self.entities.items():
            if entity['type'] == 'book':
                url_to_entity[entity['url']] = eid
        
        # 构建图书-作者关系
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="构建图书-作者关系"):
                book_url = str(row.get('bookUrl', ''))
                author = str(row.get('author', ''))
                if book_url in url_to_entity and author in self.author_map:
                    book_id = url_to_entity[book_url]
                    author_id = self.author_map[author]
                    self.relations.append((book_id, 'written_by', author_id))
                    self.relations.append((author_id, 'write', book_id))
                    self.graph.add_edge(book_id, author_id, relation='written_by')
                    self.graph.add_edge(author_id, book_id, relation='write')
        
        # 构建图书-出版社关系
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="构建图书-出版社关系"):
                book_url = str(row.get('bookUrl', ''))
                publisher = str(row.get('publisher', ''))
                if book_url in url_to_entity and publisher in self.publisher_map:
                    book_id = url_to_entity[book_url]
                    publisher_id = self.publisher_map[publisher]
                    self.relations.append((book_id, 'published_by', publisher_id))
                    self.relations.append((publisher_id, 'publish', book_id))
                    self.graph.add_edge(book_id, publisher_id, relation='published_by')
                    self.graph.add_edge(publisher_id, book_id, relation='publish')
        
        # 构建图书-译者关系
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="构建图书-译者关系"):
                book_url = str(row.get('bookUrl', ''))
                translator = str(row.get('translator', ''))
                if book_url in url_to_entity and translator in self.translator_map:
                    book_id = url_to_entity[book_url]
                    translator_id = self.translator_map[translator]
                    self.relations.append((book_id, 'translated_by', translator_id))
                    self.relations.append((translator_id, 'translate', book_id))
                    self.graph.add_edge(book_id, translator_id, relation='translated_by')
                    self.graph.add_edge(translator_id, book_id, relation='translate')
        
        # 构建图书-系列关系
        if not self.book_data.empty:
            for idx, row in tqdm(self.book_data.iterrows(), total=len(self.book_data), desc="构建图书-系列关系"):
                book_url = str(row.get('bookUrl', ''))
                series = str(row.get('seriesOfBook', ''))
                if book_url in url_to_entity and series in self.series_map:
                    book_id = url_to_entity[book_url]
                    series_id = self.series_map[series]
                    self.relations.append((book_id, 'belongs_to', series_id))
                    self.relations.append((series_id, 'contains', book_id))
                    self.graph.add_edge(book_id, series_id, relation='belongs_to')
                    self.graph.add_edge(series_id, book_id, relation='contains')
        
        print(f"\n关系构建完成: {len(self.relations)} 条关系")
    
    def save(self):
        """保存知识图谱"""
        print("\n正在保存知识图谱...")
        os.makedirs(config.KG_DIR, exist_ok=True)
        
        # 保存实体
        with open(config.KG_ENTITIES_FILE, 'wb') as f:
            pickle.dump({
                'entities': self.entities,
                'entity_types': self.entity_types
            }, f)
        
        # 保存关系
        with open(config.KG_RELATIONS_FILE, 'wb') as f:
            pickle.dump({
                'relations': self.relations,
                'graph': self.graph
            }, f)
        
        print(f"知识图谱已保存到 {config.KG_DIR}")
    
    def build(self):
        """构建完整的知识图谱"""
        self.load_data()
        self.build_entities()
        self.build_relations()
        self.save()
        print("\n知识图谱构建完成！")
        return self.entities, self.relations, self.graph


if __name__ == '__main__':
    builder = KnowledgeGraphBuilder()
    builder.build()

