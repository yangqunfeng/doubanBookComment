# -*- coding: utf-8 -*-
"""
缓存管理工具
"""
import os
import config

def clear_keyword_cache():
    """清除关键词缓存"""
    cache_file = os.path.join(config.KG_DIR, 'comment_keywords.pkl')
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print(f"✓ 已删除关键词缓存: {cache_file}")
    else:
        print("✗ 关键词缓存不存在")

def clear_embeddings_cache():
    """清除嵌入缓存"""
    if os.path.exists(config.KG_EMBEDDINGS_FILE):
        os.remove(config.KG_EMBEDDINGS_FILE)
        print(f"✓ 已删除嵌入缓存: {config.KG_EMBEDDINGS_FILE}")
    else:
        print("✗ 嵌入缓存不存在")

def clear_all_cache():
    """清除所有缓存"""
    print("清除所有缓存...")
    clear_keyword_cache()
    clear_embeddings_cache()
    print("\n所有缓存已清除！")

def show_cache_info():
    """显示缓存信息"""
    print("="*60)
    print("缓存信息")
    print("="*60)
    
    # 关键词缓存
    cache_file = os.path.join(config.KG_DIR, 'comment_keywords.pkl')
    if os.path.exists(cache_file):
        size = os.path.getsize(cache_file) / (1024 * 1024)  # MB
        print(f"✓ 关键词缓存: {cache_file}")
        print(f"  大小: {size:.2f} MB")
    else:
        print("✗ 关键词缓存: 不存在")
    
    # 嵌入缓存
    if os.path.exists(config.KG_EMBEDDINGS_FILE):
        size = os.path.getsize(config.KG_EMBEDDINGS_FILE) / (1024 * 1024)
        print(f"\n✓ 嵌入缓存: {config.KG_EMBEDDINGS_FILE}")
        print(f"  大小: {size:.2f} MB")
    else:
        print("\n✗ 嵌入缓存: 不存在")
    
    print("="*60)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'clear':
            clear_all_cache()
        elif command == 'clear-keywords':
            clear_keyword_cache()
        elif command == 'clear-embeddings':
            clear_embeddings_cache()
        elif command == 'info':
            show_cache_info()
        else:
            print("未知命令")
            print("用法:")
            print("  python cache_manager.py info              # 查看缓存信息")
            print("  python cache_manager.py clear             # 清除所有缓存")
            print("  python cache_manager.py clear-keywords    # 清除关键词缓存")
            print("  python cache_manager.py clear-embeddings  # 清除嵌入缓存")
    else:
        show_cache_info()

