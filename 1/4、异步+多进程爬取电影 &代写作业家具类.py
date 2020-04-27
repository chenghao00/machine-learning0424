class HouseItem:

    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return '[%s]占地 %.2f' % (self.name, self.area)


class House:

    def __init__(self, house_type, area):
        self.house_type = house_type
        self.area = area
        self.free_area = area
        self.item_list = []

    def __str__(self):
        return '户型：%s\n总面积:%.2f[剩余：%.2f]\n家具：%s' % (self.house_type, self.area, self.free_area, self.item_list)

    def add_item(self, item):
        print('要添加 %s' % item)
        if item.area > self.free_area:
            print('%s 的面积太大了，无法添加' % item.name)
            return

        self.item_list.append(item.name)
        self.free_area -= item.area

    def del_item(self, item):
        if item.name in self.item_list:
            print('要卖掉 %s' % item)
            self.item_list.remove(item.name)
            self.free_area += item.area
        else:
            print('家里没有%s喔！' % item)


# 创建房子
my_home = House('两室一厅', 60)
print(my_home)
print('*' * 100)

#创建家具
chest = HouseItem('chest', 2)
print(chest)
table = HouseItem('table', 1.5)
print(table)
print('*' * 100)

# 买入
my_home.add_item(chest)
my_home.add_item(table)
print(my_home)
print('*' * 100)

# 卖掉
my_home.del_item(table)
print(my_home)



import asyncio
import aiohttp
import re
import aiofiles

CONCURRENCY = 5

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None
async def scrape_api(url):
    async with semaphore:
        print('正在写入',url)
        async with session.get(url) as response:
            name = re.findall(r'.*?(\d{4}).ts', url, re.S)[0]
            async with aiofiles.open(r'E:\python\项目\草稿\test_html\%s.mp4' % name, 'wb') as f:
                await f.write(await response.read())



async def main():
    global session
    session=aiohttp.ClientSession()
    url_list = ['https://youku.cdn7-okzy.com/20200114/16664_9145d65f/1000k/hls/798274e9ad900%04d.ts' % (i) for i in
                range(200)]

    scrape_index_task=[asyncio.ensure_future(scrape_api(url)) for url in url_list]
    await asyncio.gather(*scrape_index_task)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())