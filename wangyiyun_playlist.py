import json
import time
from selenium import webdriver
from queue import  Queue
from threading import  Thread


'''
note:这里只获取了语种的列表链接

'''

class Playlist(object):
    '''获取每个细分类页面中的列表链接'''

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.start_url = 'https://music.163.com/#/discover/playlist/'
        self.driver_queue = Queue()
        self.detail_item_queue = Queue()
        self.playlist_list_queue = Queue()
        self.stop = 0  # javascript:void(0)


    def get_cata_list(self):
        '''提取分类中的数据'''
        # 分组dl元素
        dl_list = self.driver.find_elements_by_xpath("//div[@class='bd']//dl")
        # 把类别都放到列表中去
        cata_list = []
        for dl in dl_list:
            # 类别:语言， 风格， 场景...
            type ={}
            cat_title = dl.find_element_by_xpath("./dt").text
            type['type_name'] = cat_title
            # 详细类别:语言中的具体语言，风格中的具体风格，等等。
            a_list = dl.find_elements_by_xpath("./dd/a")
            detail_cat_list = []
            for a in a_list:
                item = {}
                item['detail_name'] = a.text
                # eg: {'href':'http://...'
                item['href'] = 'https://music.163.com/#/discover/playlist/?cat={}'.format(a.text)
                detail_cat_list.append(item)
            type['type_detail'] = detail_cat_list
            cata_list.append(type)
        print(cata_list)
        return cata_list
        # self.cat_list_queue.put(cat_list)

    def get_detail_cata(self, cata_list):
        '''获取每个具体分类'''
        # for cat in cata_list:
        #     print(cat)
        #     detail_cat_list = cat['type_detail']
        #     print(detail_cat_list)
        #     # time.sleep(2)
        #     return self.get_playlist(detail_cat_list)
        # cata_list = self.cat_list_queue.get()
        detail_cata_dict = cata_list[0]
        self.type_name = detail_cata_dict['type_name']
        detail_cata_list = detail_cata_dict['type_detail']
        # print(detail_cata_list)
        # print(len(detail_cata_list))
        self.len = len(detail_cata_list)
        for detail in detail_cata_list:
            self.detail_item_queue.put(detail)

        # return detail_cata_dict

    def get_playlist_url_list(self):
        ''''''

        # ------driver_queue-----
        driver = self.driver_queue.get()
        # # 遍历分类列表，
        while True:
            # self.type_name = detail_cata_dict['type_name']
            # detail_cata_list = detail_cata_dict['type_detail']
            playlist_list = []
            # name = detail_cata_list[0]['detail_name']
            # print(name)
            # type_dict = {}

            # type_dict['分类'] = name
            # type_dict['分类'] = self.type_name
            # type_dict['type'] = name
            # playlist_list.append(type_dict)
            # print(playlist_list)

            playlist_dict = {}
            item = self.detail_item_queue.get()

            # 获取url
            url = item['href']
            print(url)
            detail_name = item['detail_name']
            print('----get_playlist---')
            # print(detail_name)
            # 访问请求

            # ------driver_queue-----
            # driver = self.driver_queue.get()
            driver.get(url)
            # 获取下一页的元素
            driver.switch_to_frame("g_iframe")
            print('------2')
            next_page_element = driver.find_element_by_xpath(".//*[@id='m-pl-pager']/div/a[11]")
            print('------3')
            # 获取到当前页面中的li组
            li_list = driver.find_elements_by_xpath(".//ul[@id='m-pl-container']/li")

            # print(li_list)
            print('-----4')
            # 获取所有的playlist页面中的url
            playlist_url_list = []
            for li in li_list:
                url = li.find_element_by_xpath(".//a").get_attribute("href")
                playlist_url_list.append(url)

            href = next_page_element.get_attribute('href')
            # self.stop = href

            while href != 'javascript:void(0)':
                # 获取下一页的href
                driver.get(href)
                # 切换到iframe中
                driver.switch_to_frame("g_iframe")

                next_page_element = driver.find_element_by_xpath(".//*[@id='m-pl-pager']/div/a[11]")
                href = next_page_element.get_attribute('href')
                # 获取到当前页面中的li组
                li_list = driver.find_elements_by_xpath(".//ul[@id='m-pl-container']/li")
                # print(li_list)
                # 获取所有的playlist页面中的url
                for li in li_list:
                    url = li.find_element_by_xpath(".//a").get_attribute("href")
                    playlist_url_list.append(url)

                # playlist_url_list.extend(playlist_url_list)

                # time.sleep(random.randint(1, 4))


                playlist_dict['url_list'] = playlist_url_list
                playlist_dict['类型'] = detail_name
                playlist_list.append(playlist_dict)
                # print(playlist_list)
            self.playlist_list_queue.put(playlist_list)

            self.stop += 1
            if self.stop == self.len:
                driver.quit()
            self.detail_item_queue.task_done()

        #返回结果
        # return playlist_url_list


    # def get_playlist_url(self):
    #     ''''''
    #
    #     # ------driver_queue-----
    #     driver = webdriver.Chrome()
    #     # # 遍历分类列表，
    #
    #     # self.type_name = detail_cata_dict['type_name']
    #     # detail_cata_list = detail_cata_dict['type_detail']
    #     playlist_list = []
    #     # name = detail_cata_list[0]['detail_name']
    #     # print(name)
    #     # type_dict = {}
    #
    #     # type_dict['分类'] = name
    #     # type_dict['分类'] = self.type_name
    #     # type_dict['type'] = name
    #     # playlist_list.append(type_dict)
    #     # print(playlist_list)
    #
    #     playlist_dict = {}
    #     # item = self.detail_item_queue.get()
    #
    #     # 获取url
    #     url = 'https://music.163.com/#/discover/playlist/?cat=%E7%B2%A4%E8%AF%AD'
    #     print(url)
    #     detail_name = '粤语'
    #     print('----get_playlist---')
    #     # print(detail_name)
    #     # 访问请求
    #
    #     # ------driver_queue-----
    #     # driver = self.driver_queue.get()
    #     driver.get(url)
    #     # 获取下一页的元素
    #     driver.switch_to_frame("g_iframe")
    #     print('------2')
    #     next_page_element = driver.find_element_by_xpath(".//*[@id='m-pl-pager']/div/a[11]")
    #     print('------3')
    #     # 获取到当前页面中的li组
    #     li_list = driver.find_elements_by_xpath(".//ul[@id='m-pl-container']/li")
    #
    #     # print(li_list)
    #     print('-----4')
    #     # 获取所有的playlist页面中的url
    #     playlist_url_list = []
    #     for li in li_list:
    #         url = li.find_element_by_xpath(".//a").get_attribute("href")
    #         playlist_url_list.append(url)
    #
    #     href = next_page_element.get_attribute('href')
    #     # self.stop = href
    #
    #     while href != 'javascript:void(0)':
    #         # 获取下一页的href
    #         driver.get(href)
    #         # 切换到iframe中
    #         driver.switch_to_frame("g_iframe")
    #
    #         next_page_element = driver.find_element_by_xpath(".//*[@id='m-pl-pager']/div/a[11]")
    #         href = next_page_element.get_attribute('href')
    #         # 获取到当前页面中的li组
    #         li_list = driver.find_elements_by_xpath(".//ul[@id='m-pl-container']/li")
    #         # print(li_list)
    #         # 获取所有的playlist页面中的url
    #         for li in li_list:
    #             url = li.find_element_by_xpath(".//a").get_attribute("href")
    #             playlist_url_list.append(url)
    #
    #         # playlist_url_list.extend(playlist_url_list)
    #
    #         # time.sleep(random.randint(1, 4))
    #
    #
    #         playlist_dict['url_list'] = playlist_url_list
    #         playlist_dict['类型'] = detail_name
    #         playlist_list.append(playlist_dict)
    #         # print(playlist_list)
    #     self.playlist_list_queue.put(playlist_list)
    #     driver.quit()

    def save(self):
        while True:

            playlist_list = self.playlist_list_queue.get()
            print(playlist_list)
            path_name = playlist_list[0]['类型'] + '.txt'
            # type_dict = playlist_list[0]
            # type_name = self.type_name
            with open(path_name, 'w') as f:
                f.write(json.dumps(playlist_list, ensure_ascii=False, indent=2))
                f.write('\n')
            self.playlist_list_queue.task_done()



    def run(self):
        # 1.构造url
        # 2.发送请求
        self.driver.get(self.start_url)
        self.driver.switch_to_frame("g_iframe")
        self.driver.find_element_by_id("cateToggleLink").click()


        # self.get_cata_list()

        # {'type_name': '语种', 'type_detail': [{'detail_name': '华语', 'href':
        # 'https://music.163.com/#/discover/playlist/?cat=华语'}, {'detail_name': '欧美', 'href':
        # 'https://music.163.com/#/discover/playlist/?cat=欧美'}, {'detail_name': '日语', 'href':
        # 'https://music.163.com/#/discover/playlist/?cat=日语'}, {'detail_name': '韩语', 'href':
        # 'https://music.163.com/#/discover/playlist/?cat=韩语'}, {'detail_name': '粤语', 'href':
        # 'https://music.163.com/#/discover/playlist/?cat=粤语'}, {'detail_name': '小语种', 'href':
        # 'https://music.163.com/#/discover/playlist/?cat=小语种'}]},

        cata_list = self.get_cata_list()
        self.driver.quit()
        self.get_detail_cata(cata_list)
        # # 3.数据提取
        threads = []
        for i in range(3):
            driver = webdriver.Chrome()
            self.driver_queue.put(driver)

        for i in range(3):
            get_playlist_url_list = Thread(target=self.get_playlist_url_list)
            threads.append(get_playlist_url_list)
        # playlist_url_list = self.get_playlist_url_list(detail_cata_dict)
        # # 4.保存
        save = Thread(target=self.save)
        threads.append(save)

        for i in threads:
            i.setDaemon(True)
            i.start()

        while True:
            if self.stop == self.len:
                break
        time.sleep(3)

        # self.get_playlist_url()
        # self.save()










if __name__ == '__main__':
    playlist = Playlist()
    playlist.run()
