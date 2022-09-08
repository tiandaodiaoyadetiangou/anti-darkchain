# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from datetime import datetime
from tqdm import tqdm

start = time.time()

with open('url.txt', 'r') as f:  # 读取待检测url记录文件
    urls_list = f.read().split('\n')

with open('word1.txt', 'r', encoding='utf-8') as w:
    re_rules_list = w.read().split('\n')

browser_path = r'C:/Users/lenovo/AppData/Local/Google/Chrome/Application/chromedriver.exe'
browser = webdriver.Chrome(browser_path)

#print(urls_list)
urls = []

for i in urls_list:
    urls.append(i)
    print('已添加：', i)  # 逐个添加url

end = time.time()

for url in tqdm(urls, unit='url'):
    try:
        print('正在尝试：', url)
        browser.get(url)
        time.sleep(1)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滑动窗口等待加载js
        time.sleep(2)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        source_page = browser.page_source  # 获取源码
        rules = []  # 匹配到的标签

        with open(datetime.now().date().isoformat() + '结果.txt', 'a', encoding='utf-8') as f:
            host = True
            for re_rules in re_rules_list:
                # det = re.findall(".*?(%s).*?" %re_rules, source_page)
                if re_rules in source_page:
                    # if det != []:
                    rules.append(re_rules)
                    host = False
            if host == False:
                print(url, '匹配项：', re_rules, file=f)
                print('疑似存在暗链，请人工审查', file=f)

    except:
        print(url, ' 出了点问题导致无法获取到源码')
        time.sleep(1)

browser.close()
