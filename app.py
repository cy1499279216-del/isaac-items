# -*- coding: utf-8 -*-
"""
《以撒的结合：忏悔》中文道具搜索引擎与图鉴服务
一键启动本地 Web 服务并自动唤起浏览器
"""

import os
import sys
import webbrowser
import http.server
import socketserver
from functools import partial

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

class IsaacHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def log_message(self, format, *args):
        # 简化终端日志输出
        if "GET" in args[0] and ("200" in args[1] or "304" in args[1]):
            return
        super().log_message(format, *args)

def main():
    if not os.path.exists(os.path.join(WEB_DIR, "items_data.json")):
        print("[*] 检测到未构建本地数据集，正在自动构建中...")
        import build_chinese_database
        build_chinese_database.build_database()

    url = f"http://localhost:{PORT}"
    print("=" * 65)
    print(" 《以撒的结合：忏悔》全道具中文图鉴与搜索引擎已启动！")
    print(f" 本地访问地址: {url}")
    print(" 按 Ctrl + C 可停止服务")
    print("=" * 65)

    # 自动在默认浏览器中打开页面
    try:
        webbrowser.open(url)
    except Exception:
        pass

    with socketserver.TCPServer(("", PORT), IsaacHTTPHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] 服务已停止。")

if __name__ == "__main__":
    main()
