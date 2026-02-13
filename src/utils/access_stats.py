# -*- coding: utf-8 -*-
"""
访问日志统计分析工具
分析访问日志，统计IP、访问量、热门接口等
"""
import os
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import json


class AccessLogAnalyzer:
    """访问日志分析器"""
    
    def __init__(self, log_base_dir='logs'):
        self.log_base_dir = log_base_dir
        self.ip_pattern = re.compile(r'IP=([^\s]+)')
        self.method_pattern = re.compile(r'Method=([^\s]+)')
        self.path_pattern = re.compile(r'Path=([^\s]+)')
        self.time_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
        
    def get_log_files(self, days=1):
        """获取最近N天的日志文件"""
        log_files = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            log_dir = os.path.join(self.log_base_dir, date)
            access_log = os.path.join(log_dir, 'access.log')
            
            if os.path.exists(access_log):
                log_files.append(access_log)
        
        return log_files
    
    def parse_log_line(self, line):
        """解析单行日志"""
        data = {}
        
        # 提取时间
        time_match = self.time_pattern.search(line)
        if time_match:
            data['time'] = time_match.group(1)
        
        # 提取IP
        ip_match = self.ip_pattern.search(line)
        if ip_match:
            data['ip'] = ip_match.group(1)
        
        # 提取方法
        method_match = self.method_pattern.search(line)
        if method_match:
            data['method'] = method_match.group(1)
        
        # 提取路径
        path_match = self.path_pattern.search(line)
        if path_match:
            data['path'] = path_match.group(1)
        
        return data if data else None
    
    def analyze(self, days=1):
        """分析访问日志"""
        log_files = self.get_log_files(days)
        
        if not log_files:
            return {
                'error': '没有找到访问日志文件',
                'log_dir': self.log_base_dir
            }
        
        # 统计数据
        total_requests = 0
        ip_counter = Counter()
        path_counter = Counter()
        method_counter = Counter()
        hourly_stats = defaultdict(int)
        ip_paths = defaultdict(lambda: Counter())
        
        # 解析日志
        for log_file in log_files:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    data = self.parse_log_line(line)
                    if data:
                        total_requests += 1
                        
                        if 'ip' in data:
                            ip_counter[data['ip']] += 1
                            if 'path' in data:
                                ip_paths[data['ip']][data['path']] += 1
                        
                        if 'path' in data:
                            path_counter[data['path']] += 1
                        
                        if 'method' in data:
                            method_counter[data['method']] += 1
                        
                        if 'time' in data:
                            hour = data['time'].split()[1].split(':')[0]
                            hourly_stats[hour] += 1
        
        # 生成统计报告
        report = {
            'summary': {
                'total_requests': total_requests,
                'unique_ips': len(ip_counter),
                'unique_paths': len(path_counter),
                'analyzed_days': days,
                'log_files': log_files
            },
            'top_ips': [
                {'ip': ip, 'count': count, 'percentage': f"{count/total_requests*100:.2f}%"}
                for ip, count in ip_counter.most_common(20)
            ],
            'top_paths': [
                {'path': path, 'count': count, 'percentage': f"{count/total_requests*100:.2f}%"}
                for path, count in path_counter.most_common(20)
            ],
            'methods': dict(method_counter),
            'hourly_distribution': dict(sorted(hourly_stats.items())),
            'ip_details': {}
        }
        
        # 添加每个IP的详细访问信息
        for ip, count in ip_counter.most_common(10):
            report['ip_details'][ip] = {
                'total_requests': count,
                'top_paths': [
                    {'path': path, 'count': c}
                    for path, c in ip_paths[ip].most_common(10)
                ]
            }
        
        return report
    
    def print_report(self, days=1):
        """打印统计报告"""
        report = self.analyze(days)
        
        if 'error' in report:
            print(f"错误: {report['error']}")
            print(f"日志目录: {report['log_dir']}")
            return
        
        print("\n" + "=" * 80)
        print(f"访问统计报告 (最近 {days} 天)")
        print("=" * 80)
        
        # 总览
        summary = report['summary']
        print(f"\n【总览】")
        print(f"  总请求数: {summary['total_requests']}")
        print(f"  独立IP数: {summary['unique_ips']}")
        print(f"  访问路径数: {summary['unique_paths']}")
        print(f"  分析的日志文件: {len(summary['log_files'])}")
        
        # Top IP
        print(f"\n【访问量最高的IP】")
        for i, item in enumerate(report['top_ips'][:10], 1):
            print(f"  {i:2d}. {item['ip']:20s} - {item['count']:5d} 次 ({item['percentage']})")
        
        # Top 路径
        print(f"\n【最热门的接口】")
        for i, item in enumerate(report['top_paths'][:10], 1):
            print(f"  {i:2d}. {item['path']:40s} - {item['count']:5d} 次 ({item['percentage']})")
        
        # 请求方法分布
        print(f"\n【请求方法分布】")
        for method, count in report['methods'].items():
            percentage = count / summary['total_requests'] * 100
            print(f"  {method:6s}: {count:5d} 次 ({percentage:.2f}%)")
        
        # 小时分布
        print(f"\n【小时访问分布】")
        for hour, count in sorted(report['hourly_distribution'].items()):
            bar = '█' * int(count / max(report['hourly_distribution'].values()) * 50)
            print(f"  {hour}:00 - {count:5d} {bar}")
        
        # IP详情
        print(f"\n【Top IP 详细访问情况】")
        for ip, details in list(report['ip_details'].items())[:5]:
            print(f"\n  IP: {ip} (总计 {details['total_requests']} 次)")
            for path_info in details['top_paths'][:5]:
                print(f"    - {path_info['path']:40s} {path_info['count']:4d} 次")
        
        print("\n" + "=" * 80)
    
    def export_json(self, days=1, output_file='access_stats.json'):
        """导出统计结果为JSON"""
        report = self.analyze(days)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"统计结果已导出到: {output_file}")
        return output_file


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='访问日志统计分析工具')
    parser.add_argument('-d', '--days', type=int, default=1, help='分析最近N天的日志 (默认: 1)')
    parser.add_argument('-o', '--output', type=str, help='导出JSON文件路径')
    parser.add_argument('--log-dir', type=str, default='logs', help='日志目录 (默认: logs)')
    
    args = parser.parse_args()
    
    analyzer = AccessLogAnalyzer(log_base_dir=args.log_dir)
    
    # 打印报告
    analyzer.print_report(days=args.days)
    
    # 导出JSON
    if args.output:
        analyzer.export_json(days=args.days, output_file=args.output)


if __name__ == '__main__':
    main()

