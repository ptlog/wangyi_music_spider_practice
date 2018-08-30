import json
import time

from threading import Thread
from queue import  Queue
from selenium import webdriver


class Song_Info(object):
    '''获取歌曲信息类'''
    def __init__(self, file_name):
        self.file_name = file_name

        self.song_url_dict_queue = Queue()
        self.url_queue = Queue()
        self.song_info_dict_queue = Queue()
        self.info_queue = Queue()


    def get_songs_list(self):
        '''读取文件，获取url'''
        with open(self.file_name+'.txt') as f:
            song_list = json.load(f)  # class list

        # 遍历,获取每个playlist页面的url列表的字典
        # eg:{'url_list':[],'类型':'华语'}
        for item in song_list:
            # 把item放入队列
            self.song_url_dict_queue.put(item)
            # time.sleep(0.5)
        self.stop1 = 1

    def get_songs_list_url(self):
        '''获取每页的url列表'''
        while True:
            url_dict = self.song_url_dict_queue.get()
            url_list = url_dict['url_list']
            # 遍历这个列表， 获取每个进入细分的页面
            for url in url_list:
                # 把url放入队列中
                self.url_queue.put(url)
            self.song_url_dict_queue.task_done()

    def parse_url(self):
        '''访问url,获取每首歌曲的信息'''
        driver = webdriver.Chrome()
        while True:
            print('parse_url')
            url = self.url_queue.get()
            driver.get(url)
            # driver.get('https://music.163.com/#/playlist?id=2081261903')
            driver.switch_to_frame("g_iframe")

            # 获取信息

            # 获取标签，也就是类别
            tags_elements_list = driver.find_elements_by_xpath("//div[@class='tags f-cb']/a/i")
            # print(tags_elements_list)
            tags_list = []
            for tag in tags_elements_list:
                tags_list.append(tag.text)
                # print(tag.text)
            # print(tags_list)
            tr_elements_list = driver.find_elements_by_xpath("//table[@class='m-table ']/tbody/tr")
            # 遍历tr标签，获取每首歌曲的信息
            # song_info_list = []
            for tr in tr_elements_list:
                song_info_dict = {}
                b_element = tr.find_element_by_xpath(".//span[@class='txt']//b")
                span_element = tr.find_element_by_xpath(".//span[@class='u-dur ']")
                s_span_element = tr.find_element_by_xpath(".//div[@class='text']/span")
                a_element = tr.find_element_by_xpath(".//div[@class='text']/a")

                song_name = b_element.get_attribute('title')
                song_dur = span_element.text
                singer = s_span_element.get_attribute('title')
                album = a_element.get_attribute('title')
                song_info_dict['专辑'] = album
                song_info_dict['歌手'] = singer
                song_info_dict['时长'] = song_dur
                song_info_dict['歌名'] = song_name
                song_info_dict['类别'] = tags_list

                self.song_info_dict_queue.put(song_info_dict)

            # self.song_info_list_queue.put(song_info_list)
            self.url_queue.task_done()

                # print(song_name)
                # print(song_dur)
                # print(singer)
                # print(album)

    def save(self):
        '''保存文件'''
        while True:
            with open(self.file_name+'_歌曲信息.txt', 'a') as f:
                while True:
                    song_info_dict = self.song_info_dict_queue.get()
                    f.write(json.dumps(song_info_dict, ensure_ascii=False, indent=2))
                    f.write(',\n')




    def run(self):
        '''实现主要逻辑'''
        # # 读取文件
        get_songs_list = Thread(target=self.get_songs_list)
        get_songs_list.start()
        # self.get_songs_list()
        # # 获取url列表
        threads =[]
        for i in range(2):
            get_songs_url = Thread(target=self.get_songs_list_url)
            threads.append(get_songs_url)
        # self.get_songs_list_url()
        # # 访问url
        for i in range(3):
            parse_url = Thread(target=self.parse_url)
            threads.append(parse_url)
        # self.parse_url()
        # 保存
        
        save = Thread(target=self.save)
        threads.append(save)
        for i in threads:
            i.setDaemon(True)
            i.start()

        for q in [self.url_queue, self.song_info_dict_queue, self.info_queue]:
            q.join()

        time.sleep(4)
        # self.save()

if __name__ == '__main__':
    song_info = Song_Info('欧美')
    song_info.run()


