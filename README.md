## 免责声明
本项目的AI生成代码可能存在以下风险：
- 侵犯第三方知识产权的潜在风险
- 功能缺陷或安全性问题
- 不同司法管辖区对AI作品认定的差异

# 搜索引擎项目
注：完全由DeepseekV3编写，向Bing爬虫实现
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)

一个基于Flask的自定义搜索引擎，可屏蔽指定网站并实现关键词重定向功能。

## ✨ 功能特性

- ✅ 屏蔽百度、360、搜狗等国内搜索引擎
- 🔀 关键词自动重定向（如"steam"跳转官网）
- 🕵️ 随机User-Agent防反爬
- 🎨 简洁美观的搜索界面
- ⚡ 快速响应结果

## 🛠️ 安装指南

### 环境要求
- Python 3.8+
- pip 最新版本

### 安装步骤
```bash
# 克隆仓库
点击右上角"Code"，选择"Download ZIP"，解压

# 安装依赖
pip install flask beautifulsoup4 requests
pip install python-dotenv  # 用于管理环境变量
pip install flake8         # 代码风格检查
pip install black         # 代码格式化工具

#启动爬虫服务
python x.py

#项目结构
custom-search-engine/
├── x.py                 # 主程序
├── requirements.txt     # 依赖列表
└── templates/           # 网页模板
    ├── search.html      # 搜索页
    └── results.html     # 结果页




