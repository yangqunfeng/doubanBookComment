# -*- coding: utf-8 -*-
"""
检查 pickle 文件完整性
"""
import pickle
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import config

def check_pickle_file(filepath, filename):
    """检查单个 pickle 文件"""
    print(f"\n检查文件: {filename}")
    print(f"路径: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在")
        return False
    
    file_size = os.path.getsize(filepath)
    print(f"文件大小: {file_size / (1024*1024):.2f} MB")
    
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            print(f"✓ 文件完整，可以正常加载")
            print(f"数据类型: {type(data)}")
            if isinstance(data, dict):
                print(f"包含键: {list(data.keys())}")
                for key, value in data.items():
                    if isinstance(value, (list, dict)):
                        print(f"  - {key}: {len(value)} 项")
                    else:
                        print(f"  - {key}: {type(value)}")
            return True
    except Exception as e:
        print(f"❌ 文件损坏: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Pickle 文件完整性检查")
    print("=" * 60)
    
    files_to_check = [
        (config.KG_ENTITIES_FILE, "entities.pkl"),
        (config.KG_RELATIONS_FILE, "relations.pkl"),
        (config.KG_EMBEDDINGS_FILE, "embeddings.pkl"),
    ]
    
    # 检查评论关键词文件（如果存在）
    comment_keywords_file = os.path.join(config.KG_DIR, 'comment_keywords.pkl')
    if os.path.exists(comment_keywords_file):
        files_to_check.append((comment_keywords_file, "comment_keywords.pkl"))
    
    results = {}
    for filepath, filename in files_to_check:
        results[filename] = check_pickle_file(filepath, filename)
    
    print("\n" + "=" * 60)
    print("检查结果汇总:")
    print("=" * 60)
    for filename, status in results.items():
        status_str = "✓ 正常" if status else "❌ 损坏"
        print(f"{filename}: {status_str}")
    
    if all(results.values()):
        print("\n所有文件都正常！")
    else:
        print("\n发现损坏的文件，需要重新生成知识图谱。")
        print("请运行: python knowledge_graph_builder.py")

if __name__ == '__main__':
    main()

