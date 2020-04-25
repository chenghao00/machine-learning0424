import requests
import re
import bs4


def get_ip(url):
    """获取代理IP"""

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               "Referer": "http://www.xicidaili.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
               }
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    data = soup.table.find_all("td")
    ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  # 匹配IP
    port_compile = re.compile(r'<td>(\d+)</td>')  # 匹配端口
    ip = re.findall(ip_compile, str(data))  # 获取所有IP
    port = re.findall(port_compile, str(data))  # 获取所有端口
    return [":".join(i) for i in zip(ip, port)]  # 组合IP+端口，如：115.112.88.23:8080


if __name__ == '__main__':
    url_list = ["http://www.xicidaili.com/nn/{}".format(i) for i in range(1, 100)]
    for url in url_list:
        print('开始爬取第%d页' % url_list.index(url))
        ip_list = get_ip(url)
        for ip in ip_list:
            print(ip)
