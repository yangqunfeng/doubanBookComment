# -*- coding: utf-8 -*-
"""
日志配置模块
按日期将日志存储到独立的文件夹中
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class DateFolderLogger:
    """按日期文件夹组织的日志器"""
    
    def __init__(self, log_base_dir='logs', app_name='book_recommender'):
        """
        初始化日志器
        
        Args:
            log_base_dir: 日志根目录
            app_name: 应用名称，用于日志文件命名
        """
        self.log_base_dir = log_base_dir
        self.app_name = app_name
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _get_log_dir(self):
        """获取当天的日志目录"""
        today = datetime.now().strftime('%Y-%m-%d')
        log_dir = os.path.join(self.log_base_dir, today)
        
        # 创建目录（如果不存在）
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        return log_dir
    
    def _get_log_filename(self, log_type='app'):
        """
        生成日志文件名
        
        Args:
            log_type: 日志类型 ('app' 或 'error')
        
        Returns:
            完整的日志文件路径
        """
        log_dir = self._get_log_dir()
        timestamp = datetime.now().strftime('%H-%M-%S')
        filename = f"{self.app_name}_{log_type}_{timestamp}.log"
        return os.path.join(log_dir, filename)
    
    def _setup_handlers(self):
        """设置日志处理器"""
        # 日志格式
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 1. 应用日志处理器（所有级别）
        app_handler = RotatingFileHandler(
            self._get_log_filename('app'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        app_handler.setLevel(logging.DEBUG)
        app_handler.setFormatter(formatter)
        self.logger.addHandler(app_handler)
        
        # 2. 错误日志处理器（仅ERROR及以上）
        error_handler = RotatingFileHandler(
            self._get_log_filename('error'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
        
        # 3. 控制台处理器（INFO及以上）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """获取日志器实例"""
        return self.logger


# 全局日志器实例
_global_logger = None


def get_logger(name=None):
    """
    获取日志器实例
    
    Args:
        name: 日志器名称，如果为None则使用全局日志器
    
    Returns:
        logging.Logger实例
    """
    global _global_logger
    
    if name:
        # 返回指定名称的日志器
        return logging.getLogger(name)
    
    # 返回全局日志器
    if _global_logger is None:
        _global_logger = DateFolderLogger()
    
    return _global_logger.get_logger()


# 便捷函数
def debug(msg, *args, **kwargs):
    """记录DEBUG级别日志"""
    get_logger().debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """记录INFO级别日志"""
    get_logger().info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """记录WARNING级别日志"""
    get_logger().warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """记录ERROR级别日志"""
    get_logger().error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    """记录CRITICAL级别日志"""
    get_logger().critical(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    """记录异常信息（包含堆栈跟踪）"""
    get_logger().exception(msg, *args, **kwargs)


# 初始化全局日志器
def init_logger(log_base_dir='logs', app_name='book_recommender'):
    """
    初始化全局日志器
    
    Args:
        log_base_dir: 日志根目录
        app_name: 应用名称
    """
    global _global_logger
    _global_logger = DateFolderLogger(log_base_dir, app_name)
    return _global_logger.get_logger()

