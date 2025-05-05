# 免责声明
# 本项目的AI生成代码可能存在以下风险：
# - 侵犯第三方知识产权的潜在风险
# - 功能缺陷或安全性问题
# - 不同司法管辖区对AI作品认定的差异

from flask import Flask, request, redirect, render_template, url_for
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
import random
import time
import os

app = Flask(__name__)

# 确保模板文件夹存在
if not os.path.exists('templates'):
    os.makedirs('templates')

# 屏蔽的网站列表
BLOCKED_SITES = [
    'baidu.com',
    '360.cn',
    'so.com',  # 360搜索
    'sogou.com',
    'csdn.net'
]

# 关键词重定向映射
KEYWORD_REDIRECTS = {
    '谷歌浏览器': 'https://chrome.net.cn/help/list_2_2.html',
    'chrome': 'https://chrome.net.cn/help/list_2_2.html',
    'google chrome': 'https://chrome.net.cn/help/list_2_2.html',
    'steam': 'https://store.steampowered.com/'
}

# 随机User-Agent列表
USER_AGENTS = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    
    # Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; rv:89.0) Gecko/20100101 Firefox/89.0',
    
    # Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    
    # Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    
    # 移动设备
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
]

def get_random_user_agent():
    """获取随机User-Agent"""
    return random.choice(USER_AGENTS)

def scrape_bing(query):
    """从Bing HTML结果中抓取数据"""
    url = f"https://www.bing.com/search?q={quote_plus(query)}"
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': 'https://www.bing.com/'
        }
        
        time.sleep(2)  # 增加延迟避免被封
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for li in soup.find_all('li', class_='b_algo'):
            link_tag = li.find('a')
            if not link_tag or 'href' not in link_tag.attrs:
                continue
                
            link = link_tag['href']
            title = li.find('h2').get_text(strip=True) if li.find('h2') else '无标题'
            
            desc = li.find('div', class_='b_caption')
            desc = desc.find('p').get_text(strip=True) if desc and desc.find('p') else '无描述'
            
            if not any(blocked.lower() in link.lower() for blocked in BLOCKED_SITES):
                results.append({
                    'title': title,
                    'url': link,
                    'description': desc
                })
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Bing抓取错误: {e}")
        return []
    except Exception as e:
        print(f"解析Bing结果时出错: {e}")
        return []

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('q', '').strip().lower()
    else:
        query = request.args.get('q', '').strip().lower()
    
    if not query:
        return redirect(url_for('home'))
    
    # 检查关键词重定向
    for keyword, url in KEYWORD_REDIRECTS.items():
        if keyword in query:
            return redirect(url)
    
    search_results = scrape_bing(query)
    return render_template('results.html', query=query, results=search_results)

if __name__ == '__main__':
    app.run(debug=True, port=5500,host='0.0.0.0')  # 使用5500端口