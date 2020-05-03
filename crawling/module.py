#### Youtube Comment crawaler Moulization file#####

# 기존 코드를 합쳐서 모듈화 한 코드
# import youtube_comment_crawal
# import youtube_comment_crawal.total1('검색어')

##### 개선사항
# class 화 히기
## 함수화
# 1. 검색창 선택 주소 가져오기
# 2. 세부 댓글 가져오기
# 3. 몽고 DB 넣기 - init.py 함수로 접속 정보 저장 후 가져오기
# 4. 분석 함수 - Konlpy, wordcloud, netwrok analysis


def total1(url):
        
# 필요 패키지 import
    import requests
    import time
    import scrapy
    import pandas as pd
    import re   
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    import datetime as dt   
    from scrapy.http import TextResponse
    from bs4 import BeautifulSoup
    import pymongo
    # 크롬 드라이브 path, server 용 주소
    path = '/home/ubuntu/chromedriver'
    
    #headless 설정, 서버는 창이 안뜸.    
    options = Options()
    options.headless = True
    browser = webdriver.Chrome('/home/ubuntu/chromedriver', options=options)
    browser.get('https://www.youtube.com/results?search_query={}&sp=CAASBAgEEAE%253D'.format(url))
        
    body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출

    num_of_pagedowns = 10
    # 5번 밑으로 내리는 것
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_of_pagedowns -= 1
        
        # 주소 파싱
    html0 = browser.page_source
    html = BeautifulSoup(html0, 'html.parser')
    
    browser.quit()
    
        ##### 여러가지 video_list1이 있지만 video_list1만 사용한다. 각 영상 주소 추출을 위한 것 #####
    ##### 나머지는 조회수, 추천수, 개시일등 확인 가능 #####
    
    # <ytd-thumbnail class="style-scope ytd-video-renderer" use-hovered-property="">
    # 검색에서 주소 가져오기
    
    # 작동코드 건들지 말 것
    video_list0 = html.find('div', {'id': 'contents'})
    # video_list1 만 실제로 가져옴
    video_list1 = html.find_all(
        'a', {'class': 'yt-simple-endpoint style-scope ytd-video-renderer'})
    #####video_list1
    #video_list1 = html.find_all('div', {'class': 'style-scope ytd-video-renderer'})
    #video_list2 = video_list0.find_all('div', {'id': 'thumbnail'})
    #video_list2 = video_list1.find_all('div', {'class': 'style-scope ytd-video-renderer'})
    # video_list0[1].find('a')['href']
    #title1 = video_list0[1].find('a',{'id':'video-title'}).text
    # title1
    # video_list1[0]['href']
    # //*[@id="metadata-line"]/span[1]/text()
    video_list2 = video_list0.find_all(
        'span', {'class': 'style-scope ytd-video-meta-block'})
    #####video_list2[0]
    
    ##### 메타데이터를 사용하여 조회수 개시일 가져오기 text.split('/')[0] 사용하여 분리 #####
    video_list3 = html.find_all(
        'div', {'class': 'text-wrapper style-scope ytd-video-renderer'})
    ######video_list3[0].find('div', {'id': 'metadata-line'})
    
        # 영상 주소 가져오기. 댓글, 좋아요 가져올 때 필요함
    base_url = 'https://www.youtube.com'
    test_url = []
    for i in range(0, len(video_list1)):
        url2 = base_url+video_list1[i]['href']
        test_url.append(url2)
    
    # 코멘트 데이터 넣기 위한 빈 dataframe
    comment_data = pd.DataFrame({'title': [],
                             'youtube_id': [],
                             'comment': [],
                             'like_num': []
                             })
    
    
    
    options = Options() # 없어도 됨
    options.headless = True # 없어도 됨
    browser = webdriver.Chrome(path, options=options)
    
    
    for i in range(1, len(test_url)):
        start_url = test_url[i]
        browser.get(start_url)
        body = browser.find_element_by_tag_name('body')
    
        time.sleep(2)  # 2초간 여유
    
        num_page_down = 1  # 페이지 다운도 적게
        while num_page_down:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)
            num_page_down -= 1
    
            # 최신 댓글 순으로 가져오기 위한 설정
            # 댓글 정렬창 클릭
        #browser.find_element_by_xpath('//*[@id="sort-menu"]').click() 
        #browser.find_element_by_xpath('//*[@id="menu"]/a[2]/paper-item/paper-item-body/div[text()="최근 날짜순"]').click()
    
        # 여러 댓글 가져오도록 스크롤
        num_page_down = 5  # 스크롤 2~3
        while num_page_down:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)
            num_page_down -= 1
    
            # 파싱
        html_s0 = browser.page_source
        html_s = BeautifulSoup(html_s0, 'html.parser')
    
        # 제목 가져오기
        comment0 = html_s.find_all(
            'ytd-comment-renderer', {'class': 'style-scope ytd-comment-thread-renderer'})
        title0 = html_s.find_all(
            'ytd-video-primary-info-renderer')  # 제목 html 코드 가져오기
        title = title0[0].find('h1').text.split('/')[0]  # 제목 find하고 split
    
        # 영상별 댓글 가져오기
        for i in range(len(comment0)):
    
            # 댓글
            comment = comment0[i].find(
                'yt-formatted-string', {'id': 'content-text', 'class': 'style-scope ytd-comment-renderer'}).text
    
            # 좋아요 싫어요
            try:
                aa = comment0[i].find('span', {'id': 'vote-count-left'}).text
    
                like_num = "".join(re.findall('[0-9]', aa))
            except:
                like_num = 0
    
            # 작성자 가져오기 정규 표현식으로 깔끔하게 가져오기.
            bb = comment0[i].find('a', {'id': 'author-text'}).find('span').text
            youtube_id = "".join(re.findall('[가-힣0-9a-zA-Z]', bb))
    
            # 한 영상에 대한 데이터 합치기
            insert_data = pd.DataFrame({'title': [title],
                                        'youtube_id': [youtube_id],
                                        'comment': [comment],
                                        'like_num': [like_num]
                                        })
    
            # 자료 붙여주기
            comment_data = comment_data.append(insert_data)
    
        # index 붙여주기
        comment_data.index = range(len(comment_data))
    
    browser.quit()
    

    # mongoDB import
    client = pymongo.MongoClient('mongodb://mongodb_info/')
    items = comment_data.to_dict("records")
    comment_result = client.crawling.youtube
    ids = comment_result.insert(items)
    
    
