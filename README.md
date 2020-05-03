# 유튜브 데이터 크롤링, 댓글 분석 프로젝트
> '타다 금지법(여객자동차 운수사업법 개정안)'의 국회 법제사법위원회 통과에 따른 유튜브 댓글 반응 분석(텍스트 분석)
- 팀원: 이희재, 안효준

![youtubenews](https://user-images.githubusercontent.com/60166667/80870212-fc7f0580-8cdf-11ea-86f8-a084bf0a50d3.jpeg)





## 1. 프로젝트 진행 동기

- 새롭게 떠오른 언론 매체 - 유튜브
  - <시사in> 신뢰도 조사에서 유튜브가 신뢰하는 언론 매체 2위를 차지하였다.(1)
![sisain](https://user-images.githubusercontent.com/60166667/80870497-c17dd180-8ce1-11ea-8dbb-f1b2e404e3e7.jpeg)

  - 유튜브를 통한 뉴스 소비는 전 세계적으로도 증가세를 보이고 있고, 한국은 그중에서도 앞서나가는 편에 속한다. 
  - 영국 옥스퍼드 대학 부설 로이터 저널리즘연구소와 한국언론진흥재단 공동연구로 2019년 6월 공개된 ‘디지털뉴스 리포트 2019’에 따르면 한국인 10명 중 4명은 유튜브로 뉴스를 본다. ‘지난 1주일 동안 유튜브에서 뉴스 관련 동영상을 시청한 적이 있다’라는 질문에 40%가 그렇다고 답했다. 38개 조사 대상국 가운데 4위로, 조사 대상국 전체 평균은 26%였다.(1)
  
  - 네이버와 다음은 텍스트 기사 바탕으로 댓글이 주로 서비스 되고 있는데, 두 사이트의 댓글은 성향에 따라 극단적으로 나눠지는 것으로 파악되고 있다(2).
  
  
- 유튜브 저널리즘의 본격화
 
   ![report](https://user-images.githubusercontent.com/60166667/80869117-647e1d80-8cd9-11ea-8f30-2f8b94a3f6ee.jpg)

   - 시청률조사기업 닐슨이 최근 낸 보고서 ‘2019 뉴스미디어 리포트-유튜브 저널리즘’은 오늘날 영상 기반 미디어환경에서 모바일을 통해 시청하는 유튜브 뉴스가 급성장했다고 진단하며 ‘유튜브 저널리즘’이란 용어를 썼다. 유튜브 저널리즘이 학문적으로 명확히 정의된 것은 아니지만 이미 현상적으로 뉴스수용자들이 유튜브에서 ‘저널리즘’을 소비하고 있다는 판단의 결과로 보인다.

   - 2019.7.25일 기준 주요 유튜브 뉴스 채널 구독자 수는 △YTN뉴스 121만 △JTBC뉴스 108만 △노무현재단 86만 △신의한수 77만 △비디오머그 60만 △SBS뉴스 53만 △펜앤드마이크 정규재TV 48만 △KBS뉴스 45만 △딴지방송국 44만 순으로 집계됐다. 방송뉴스 중 KBS는 콘텐츠가 가장 많고, JTBC는 평균 조회 수가 가장 높다.(3) 


  

- 분석 주제 : '타다 금지법'
  - '혁신' vs '불법' : 타다와 택시의 뜨거운 공방전 
 
  ![illegal](https://user-images.githubusercontent.com/60166667/80869873-c8a2e080-8cdd-11ea-80bc-47d5eb504300.jpg)
  
   - 차량 공유 서비스가 활성화 되면서 '타다'와 '카카오 택시'로 사회에 많은 논란이 있었다. '카카오 택시'는 기존 택시 업계와의 상생 협약을 맺으며 사업을 진행하고 있는 반면, 타다는 업계와의 갈등이 계속되며 2020년 3월 6일 '타다 금지법'이 국회에서 통과 되었다. 
   - 법안 통과 이후에도 '타다' 서비스가 혁신과 불법이라는 극단적인 의견이 대립될 것으로 예상하여,'타다 금지법' 관련 동영상 댓글 수집과 분석을 진행하고자 한다.
 


## 2. 분석 결과

-  단어 빈도 분석: 3/5 ~ 3/31 까지 업로드된 동영상들의 댓글 중, 두 글자 이상의 단어 추출

<img width="740" alt="스크린샷 2020-05-03 오후 8 58 36" src="https://user-images.githubusercontent.com/60166667/80913625-f55c0400-8d80-11ea-9916-f329607e53f0.png">

     
-  워드 클라우드 분석 결과

 ![carword](https://user-images.githubusercontent.com/60166667/80899145-8f9f5600-8d47-11ea-9205-b6d7e615f052.png)

   
-  단어 별 네트워크 분석 결과(지지도 0.017)
  <img width="949" alt="스크린샷 2020-05-03 오후 9 00 09" src="https://user-images.githubusercontent.com/60166667/80913640-158bc300-8d81-11ea-9814-f27c559e6a10.png">

   
- 나이브 베이즈 분류 결과(1: '타다' 편 2: '택시' 편 3: '미분류')

   - 대부분 90% 이상의 정확도로 분류하고 있음.
  <img width="683" alt="스크린샷 2020-05-03 오후 11 46 26" src="https://user-images.githubusercontent.com/60166667/80917187-4fb48f00-8d98-11ea-95b6-76cc04604d4b.png">
  
   - 전체 870개 중, 절반에 해당하는 약 400개의 댓글이 '택시'를 옹호하는 입장임을 알 수 있음. '타다'와 '미분류'는 비등.
<img width="985" alt="스크린샷 2020-05-03 오후 11 58 16" src="https://user-images.githubusercontent.com/60166667/80917469-09602f80-8d9a-11ea-9ca8-3f360895ca35.png">


## 3. 데이터 수집 프로세스 및 구조도

![structure](https://user-images.githubusercontent.com/60166667/77083157-65683200-6a40-11ea-9bb3-07b323c19224.png)

   - 수집 대상 및 기간 
        - item: 개별 동영상들의 제목, 링크, 댓글 남긴 사람 id, 댓글, 좋아요 수
        - 기간: 2020년에 업로드된 '타다 금지법' 관련 동영상 댓글 수집 후, 법안 통과 일자 기준으로 2020.3.6~3.31 기간의 영상 댓글 추출
        
   - 크롤링 방법
        - AWS EC2 환경에서 YouTube '타다 금지법' 영상 댓글 크롤링
        - scrapy 프레임워크 + module 혼합하여 사용

   - 데이터의 저장
        - DB: mongodb 데이터 베이스에 크롤링한 데이터 저장하는 파이프라인 구축
        

## 4. 분석 과정에서 작성한 python 코드 폴더

- Crawling
  - Requirement.txt: 분석에 필요한 패키지
  - scrapycode.ipynb: scrapy를 활용하여 댓글 수집 -> MongoDB에 저장
  - module.py: 크롤링에 사용한 모듈
  
- Comment Analyzer
  - frequency_network_analysis.ipynb : 단어 빈도, 워드 클라우드, 네트워크 분석
  - naive_bayes.ipynb : 나이브 베이즈 분류


## 5. 참고문헌
- (1) 시사IN - '뉴스를 못 믿어서 유튜브를 본다'
- (2) 이준기, 한미애. (2012). 개인의 정치성향이 뉴스 댓글에 대한 신뢰성과 사회적 영향력의 인식에 미치는 영향. 한국전자거래학회지, 17(1), 173-187.
- (3) 미디어오늘 - '유튜브 저널리즘’의 시대가 오고 있다'
