# -*- coding: utf-8 -*-
"""
日志配置模块
按日期组织日志文件，每天创建独立的文件夹
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class DateBasedLogger:
    """基于日期的日志管理器"""
    
    def __init__(self, log_base_dir='logs', max_bytes=10*1024*1024, backup_count=5):
        """
        初始化日志管理器
        
        Args:
            log_base_dir: 日志根目录
            max_bytes: 单个日志文件最大大小（默认10MB）
            backup_count: 日志文件备份数量
        """
        self.log_base_dir = log_base_dir
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.loggers = {}
        
    def _get_log_dir(self):
        """获取当天的日志目录"""
        today = datetime.now().strftime('%Y-%m-%d')
        log_dir = os.path.join(self.log_base_dir, today)
        
        # 创建目录（如果不存在）
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        return log_dir
    
    def get_logger(self, name='app', level=logging.INFO):
        """
        获取日志记录器
        
        Args:
            name: 日志记录器名称（会作为日志文件名）
            level: 日志级别
            
        Returns:
            logging.Logger: 配置好的日志记录器
        """
        # 如果已经创建过该logger，直接返回
        if name in self.loggers:
            return self.loggers[name]
        
        # 创建logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # 清除已有的handlers（避免重复）
        logger.handlers.clear()
        
        # 获取日志目录
        log_dir = self._get_log_dir()
        log_file = os.path.join(log_dir, f'{name}.log')
        
        # 创建文件handler（带日志轮转）
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        # 创建控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # 缓存logger
        self.loggers[name] = logger
        
        return logger


# 创建全局日志管理器实例
_logger_manager = DateBasedLogger()


def get_logger(name='app', level=logging.INFO):
    """
    获取日志记录器的便捷函数
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    return _logger_manager.get_logger(name, level)


# 使用示例
if __name__ == '__main__':
    # 获取不同模块的logger
    app_logger = get_logger('app')
    kg_logger = get_logger('knowledge_graph')
    api_logger = get_logger('api')
    
    # 测试日志输出
    app_logger.info('应用启动')
    app_logger.debug('调试信息')
    app_logger.warning('警告信息')
    app_logger.error('错误信息')
    
    kg_logger.info('知识图谱构建开始')
    api_logger.info('API请求处理')
    
    print(f"\n日志文件已保存到: {_logger_manager._get_log_dir()}")

