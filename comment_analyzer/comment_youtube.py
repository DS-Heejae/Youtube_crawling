# 분석 패키지
import pandas as pd
import numpy as np

# 데이터 불러오기
import pymongo
import sys


# 자연어 처리

from konlpy.tag import *  
hannanum = Hannanum()
okt = Okt()
kkma = Kkma()
mecab = Mecab()

# 자연어 빈도 워드 크라우드
from collections import Counter 
from wordcloud import WordCloud

# 시각화 관련
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 네트워크 분석
import re
import csv
from apyori import apriori
import networkx as nx

# 몽고DB
import pymongo

#### 유튜브 크롤링

def you_crawal_comment(keyword, key):
    '''
    설명
    유튜브 댓글 크롤링 코드 
    
    변수
    keyword : 검색어 입력
    key : 몽고db 저장
    
    예시
    you_crawal_comment('타다+금지법', key)
    
    참고
    크롬 드라이버 path 변수 추가. 
    지금은 해당 파일에서 직접 수정 해주세요
    
    '''
    import requests
    from bs4 import BeautifulSoup
    import time
    import urllib.request
    from selenium.webdriver import Chrome
    import re  # 정규표현식 패키지
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    import datetime as dt
    import pandas as pd
    import pymongo
    
    
    
    
    
    path = '/home/loveactualry/dev/chromedriver'
    #url = '타다+금지법'
    
    options = Options()
    options.headless = True
    browser = webdriver.Chrome('/home/loveactualry/dev/chromedriver', options=options) #### 경로 잡아주기
    browser.get('https://www.youtube.com/results?search_query={}&sp=EgYIBRABGAE%253D'.format(keyword))
    
    body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출

    num_of_pagedowns = 20
    # 10번 밑으로 내리는 것
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(4)
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
    
    comment_data = pd.DataFrame({'title': [],
                                 'date': [],
                                 'youtube_id': [],
                                 'comment': [],
                                 'like_num': []
                                 })
    
    
    
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(path, options=options)
    
    
    for i in range(1, len(test_url)):
        start_url = test_url[i]
        browser.get(start_url)
        body = browser.find_element_by_tag_name('body')
    
        time.sleep(3)  # 2초간 여유
    
        num_page_down = 8  # 페이지 다운도 적게
        while num_page_down:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)
            num_page_down -= 1
    
            # 최신 댓글 순으로 가져오기 위한 설정
            # 댓글 정렬창 클릭
        #browser.find_element_by_xpath('//*[@id="sort-menu"]').click() 
        #browser.find_element_by_xpath('//*[@id="menu"]/a[2]/paper-item/paper-item-body/div[text()="최근 날짜순"]').click()
    
        # 여러 댓글 가져오도록 스크롤
        num_page_down = 8  # 스크롤 2~3
        while num_page_down:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            num_page_down -= 1
    
            # 파싱
        html_s0 = browser.page_source
        html_s = BeautifulSoup(html_s0, 'html.parser')
    
        # 전체 댓글 가져오기
        comment0 = html_s.find_all(
            'ytd-comment-renderer', {'class': 'style-scope ytd-comment-thread-renderer'})
        
        # 제목 가져오기
        title0 = html_s.find_all(
            'ytd-video-primary-info-renderer')  # 제목 html 코드 가져오기
        title = title0[0].find('h1').text.split('/')[0]  # 제목 find하고 split
        
        # 날짜 가져오기
        date = browser.find_element_by_css_selector(
            '#date > yt-formatted-string').text
    
        # 영상별 댓글 가져오기
        for i in range(len(comment0)):
    
            # 댓글
            comment = comment0[i].find(
                'yt-formatted-string', {'id': 'content-text', 'class': 'style-scope ytd-comment-renderer'}).text
    
            # 좋아요 싫어요
            try:
                aa = comment0[i].find('span', {'id': 'vote-count-left'}).text
    
                like_num = "".join(re.findall('[0-9]', aa)) + "개"
            except:
                like_num = 0
    
            # 작성자 가져오기 정규 표현식으로 깔끔하게 가져오기.
            bb = comment0[i].find('a', {'id': 'author-text'}).find('span').text
            youtube_id = "".join(re.findall('[가-힣0-9a-zA-Z]', bb))
    
            # 한 영상에 대한 데이터 합치기
            insert_data = pd.DataFrame({'title': [title],
                                        'date': [date],
                                        'youtube_id': [youtube_id],
                                        'comment': [comment],
                                        'like_num': [like_num]
                                        })
    
            # 자료 붙여주기
            comment_data = comment_data.append(insert_data)
    
        # index 붙여주기
        comment_data.index = range(len(comment_data))
    
    browser.quit()
    
    client = pymongo.MongoClient(key)
    items = comment_data.to_dict("records")
    comment_result = client.crawling.youtube4
    ids = comment_result.insert(items)
    








## 유튜브 크롤링 댓글 분석 함수 들

def mongo_get_data(address):
    ''' 
    설명
    mongoDB 데이터 가져오기
    
    변수
    address : 주소
    
    
    예시
    mongo_get_data('mongodb://dss:dss@ip.ip.ip.ip:27017/')
    
    참고
    개선사항 : result의 데이터베이스도 변수로 받아올 수 있는 방법 찾기
    '''
    import pymongo
    client = pymongo.MongoClient(address)
    result = client.crawling.youtube3
    comment_result = pd.DataFrame(result.find({}))
    return comment_result



def remove_gae(data, colu, word):
    '''
    설명
    제거하고 싶은 항목과 단어 설정
    
    변수
    data : result data
    colu : 'like_num'
    word : "개"
    
    예시
    num_gae = remove_gae(result,'like_num', '개')
    
    참고
    본 노트북에서는 다음 함수에 b로 다음 과정이 진행되어서 
    num_gae = remove_gae('like_num', '개') 형식으로 실행 해주기 
    '''
    a = data[colu]
    b=[]
    for i in range(0, len(a)):
        c = a[i].replace(word,"")
        b.append(c)
    return b


def sort_like(data, num_gae, obj, num):
    '''
    설명
    댓글 좋아요 내림차순 정렬
    
    변수
    data : result - 데이터
    num_gae : 좋아요 숫자 개수
    obj : 'like_co' - 컬럼명
    num : 1 - 좋아요 개수
    사용 안하는 변수
    colu : 'comment' - 데이터에서 가져오려는 컬럼명  
    
    예시
    comment_sort = sort_like(result, num_gae, 'like_co', 1)
    
    참고
    모든 데이터 프레임 형태를 불러온다.
    그 다음에 댓글만 저장한다.
    comment_sort = list(comment_result_sort['comment'])
    '''
    
    data[obj] = num_gae
    data[obj] = data[obj
                          ].astype(int)
    liek_co_up = data.like_co >= num
    comment_result_sort = data.loc[liek_co_up, :
                                  ].sort_values(by=obj, ascending=False)
    
    #comment_result_sort.head()
    
    # 전체 코멘트 
    #comment_sort = list(comment_result_sort['comment'])
    return comment_result_sort

def write_txt(list,fname,sep):
    ''' 
    설명
    텍스트 파일 쓰기
    
    변수
    list : 리스트형 자료
    fname : 파일명
    sep: 구분자
    
    예시
    write_txt(comment_tada_list,'wtest_samlpe.txt',sep="'")
    
    참고
        
    '''
    file = open(fname,'w')
    vstr = ''
    
    for a in list:
        vstr = vstr + str(a) + sep
    vstr = vstr.rstrip(sep)
    
    file.writelines(vstr)
    
    file.close()
    print('[complete]')







def del_dupl_word(filename):
    '''
    설명
    각 줄별로 동일한 단어가 나올 경우 제거 하고 싶을 때 사용.
    라인별로 읽어야 하기 때문에 open -> readline을 쓴다.
    with를 사용하여 close 명령어 사용하지 않는다.
    
    변수
    filename : 파일명
    
    예시
    duplicate_comment = del_dupl_word('wtest_samlpe.txt')
    
    참고
    시간 함수 추가
    '''
    import time
    
    start_time = time.time()
    with open(filename) as f:
        com_txt = f.readlines()
    
    
    duplicate_comment = []
    
    for i in com_txt:
        duplicate_comment1 = kkma.nouns(i)
        for j in range(0,len(duplicate_comment1)):
            duplicate_comment.append(duplicate_comment1[j])
    print('Fit time : ', time.time() - start_time)
    return(duplicate_comment)


def sel_count_word(data, num):
    '''
    설명
    N 단어 이상의 글자만 선택하기
    
    변수
    data : 리스트형 변수
    num : 글자수(1이상)
    
    예시
    rm_dupl = sel_count_word(duplicate_comment, 2) # 두단어 이상
    rm_one = sel_count_word(duplicate_comment, 1) # 한단어만
    참고
    1과 그 이상으로 if 함수 구분
    이전 함수로 하면 한글자는 집계가 안되어 수정
    '''
    rm_dupl = []
    for i in data:
        if num == 1 and len(i) == 1:
            rm_dupl.append(i)
        elif num > 1 and len(i) >= num:
            rm_dupl.append(i)
    
    return rm_dupl



def preprocessing(text):
    '''
    설명
    불용어 제거
    
    변수
    text : 리스트형 
    
    예시
    clean_text = []
    i = 0
    for data in comment_tada_list:
        preprocessed = preprocessing(data)
        clean_text.append(preprocessed)
    
    참고
    stop = stop_word 오류 시 참고
    '''
    # tokenize into words
    hangul = re.compile('[^가-힣a-zA-Z\s]')
    text = hangul.sub('', str(text))
    tokens = kkma.nouns(text) # 명사로 처리.
    
    # 이러면 안되는걸 알지만~~~~~~.............
    stop_word = ['저', '얄', '봉', '만', '새', '돈', '직', '갑', '석', '교', '하', '누', '티', '줄', '책', '뼈', '꿈', '셈', '깡', '불', '지', '냥', '모', '정', '감', '해', '국', '멋', '짓', '로', '규', '엔', '글', '상', '위', '역', '줌', '열', '쇼', '서', '참', 'ㅂ니다', 'ㄷ', '표', '걱', '댓', '증', '습', '님', '흥', '고', '할', '당', '겹', '도', '울', 'ㅉ', '임', '얼', '김', 'ㅅ', '부', '예', '니', '패', '카', '노', '등', '턴', '담', '원', '푼', '씨', '멍', '시', '콜', '억', '월', '컷', '는', '소', '보', '일', '뻐', 'ㅋ', '박', '기', '곳', '징', '읍', '입', '문', '십', '텍', '속', '라', '홀', '적', '짝', '둘', '건', '깃', '행', '듯', '반', '은', 'ㅇ', '뇽', '더', '운', 'ㄲ', '틈', '뿐', '넘', '쟁', '비', '1', '명', '전', '빵', '들', '약', '탕', '대', '겐', '쏫', '피', '호', '식', '5', '놈', '편', '통', '투', '판', '꺼', '승', '디', '8', '세', '짐', '플', '우', 'ㅜ', '달', '꼴', '천', '읏', '번', '묵', '뭐', '영', '군', '사', '꿍', '터', '맘', '렌', '7', 'ㅡ', '심', '민', '단', '아', '잖', '섯', '바', '룰', '길', '업', '설', '균', '최', '득', '히', 'ㅎ', '넬', '함', '나', '걸', '리', '3', '순', '힘', '벙', '폰', '올', '마', '후', '뒤', '공', '죄', '별', '송', '떼', '싱', '백', '싢', '실', '싹', '밑', '채', '남', '웅', '훈', '점', 'ㅆ', 'ㅠ', '수', 'ㆍ', '내', '폼', '쪽', '법', '쌩', '의', '인', '질', '땅', '짱', '코', '손', 'ㅈ', '맗', '동', '년', '철', '거', '자', '알', '간', '다', '야', '오', '똥', '선', '갓', '랩', '레', '때', '날', '욕', '안', '허', '분', '면', '릴', '합', '과', '녹', '끈', '털', '산', '생', '태', '개', '재', '응', '중', '6', '랜', '발', '미', '유', '택', '밥', '꽁', '윈', '눈', '끝', '삼', '근', '진', '잆', '잔', '즈', '배', '어', '여', '벌', '신', '현', '팔', '그', '금', '흠', '연', '겁', '뜻', '키', '쉬', '뻥', '망', '효', '빽', '렉', '형', '앞', '랔', '값', '회', '게', '2', '엽', '악', '요', '너', '젓', '못', '제', '애', '메', '팅', '답', '데', '이', '말', '처', '구', '4', '옆']
    
    # remove stopwords
    stop = stop_word # 노트북의 stoword 변수와 연결되어 있음. stop워드 오류시 여기서 확인
    tokens = [token for token in tokens if token not in stop]
    
    preprocessed_text= ' '.join(tokens)
    return preprocessed_text



def draw_network(data, support):
    '''
    설명
    네트워크 그래프 그려주기
    
    변수
    data : 단어별 댓글 쪼갠 데이터
    min_support : 0.01 이상
    
    예시
    draw_network(test_asso, 0.017)
    
    참고
    pos = nx.kamada_kawai_layout(G) 해당 부분에서 그래프 형태 변경 가능, 
    => 변수 입력 가능하도록 수정 필요
    '''
    
    result = (list(apriori(data, min_support = support)))
    df = pd.DataFrame(result)
    df['length'] = df['items'].apply(lambda x: len(x))
    df = df[(df['length'] ==2) ].sort_values(by='support',ascending=False)
    
    G = nx.Graph()
    #G = nx.path_graph(4)
    ar=(df['items']); 
    G.add_edges_from(ar)
    G.remove_edges_from([('해라', '라'), ('해라', '해'), ('라', '해'), (0, 1), (1, 2), (2, 3) ,('시', '채')])
    pr = nx.pagerank(G)
    nsize = np.array([v for v in pr.values()])
    nsize = 2000 * (nsize - min(nsize)) / (max(nsize) - min(nsize))
    pos = nx.kamada_kawai_layout(G)
    plt.figure(figsize=(16,12))
    plt.axis('off')
    nx.draw_networkx(G, font_family='D2Coding', font_size=16,
                    pos=pos, node_color=list(pr.values()), node_size=nsize,
                    alpha = 0.7, edge_color='.5', cmap=plt.cm.YlGn)











