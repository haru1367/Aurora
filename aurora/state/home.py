"""The state for the home page."""
from datetime import datetime
import reflex as rx
from .base import Follows, State, Tweet, User, GPT
import os,json
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap
import requests, json
from bs4 import BeautifulSoup as bs
import urllib
import re
import urllib.request
import sys
from PyKakao import KoGPT

class HomeState(State):
    """The state for the home page."""
    tweet: str                                                                 # 유저의 게시물 내용을 저장할 변수
    tweets: list[Tweet] = []                                                   # 게시물 내용들을 리스트로 저장
    user_tweets:list[Tweet] = []                                               # 유저의 story저장
    friend: str                                                                # 유저를 검색하기 위한 입력변수
    search: str                                                                # 게시물을 검색하기 위한 입력변수
    img: list[str]                                                             # 이미지 파일 저장변수
    files: list[str] = []  # Add files attribute                               # 이미지 파일 저장변수
    show_right: bool = False
    show_top: bool = False
    show: bool = False
    KAKAO_REST_API_KEY: str                                                    # Kakao Rest API Key 저장 변수
    Google_API_KEY : str                                                       # Google API Key 저장 변수
    Google_SEARCH_ENGINE_ID : str                                              # Google Search Engine Id 키 저장 변수
    Naver_client_id:str                                                        # Naver Client id  키 저장 변수
    Naver_client_secret:str                                                    # Naver Client Secret 키 저장변수
    locations: list[str]                                                       # Map 키워드 검색 입력변수 저장 리스트
    df:pd.DataFrame                                                            # Map 키워드 검색 결과 저장 데이터 프레임
    search_df:pd.DataFrame                                                     # 웹 크롤링 검색 결과 저장 데이터프레임
    tag_search:str                                                             # Map 키워드 입력변수
    map_html:str = "/map.html"                                                 # Map 검색 결과 html 변환 파일
    map_iframe:str = f'<iframe src="{map_html}" width="100%" height="600"></iframe>' # html파일 이미지 태그 변환 
    video_search:str=""                                                        # 비디오 링크 입력 변수
    web_trend :dict                                                            # 실시간 트렌드 순위 저장 딕셔너리
    web_search :str                                                            # 웹 크롤링 검색어 입력 변수
    chat_input:str                                                             # AI Chat 입력변수
    kogpt_response:str                                                         # KoGPT 답변 저장 변수
    gpts: list[GPT] = []                                                       # KoGPT 전체 답변 저장 리스트
    Trash_Link = ["kin", "dcinside", "fmkorea", "ruliweb", "theqoo", "clien", "mlbpark", "instiz", "todayhumor"] # 웹 크롤링 시 제외할 결과목록
    
    # 파일 선택함수
    def handle_file_selection(self):                                          
        root = tk.Tk()                                                        # 파일 선택 대화상자 열기
        root.withdraw()                                                       # 화면에 창을 보이지 않도록 함
        file_paths = filedialog.askopenfilenames()

        # 선택된 파일 경로에 대한 처리
        for file_path in file_paths:
            file_name = os.path.basename(file_path)                           # 파일 이름과 확장자를 추출
            file_extension = os.path.splitext(file_name)[1]
            
            upload_data = open(file_path, "rb").read()                        # 선택한 파일을 저장
            outfile = f".web/public/{file_name}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file_name)

            # Set the files attribute
            self.files.append(file_name)

    
    #파일 업로드 함수
    async def handle_upload(                                                 
        self, files: list[rx.UploadFile]
    ):
        for file in files:
            upload_data = await file.read()
            outfile = f"/{file.filename}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)
    
    #게시물 업로드 함수
    async def post_tweet(self):
        if not self.logged_in:
            return rx.window_alert("Please log in to post a tweet.")                 # 로그인이 되어있지 않을 시 경고 메시지
        if len(self.tweet)==0:
            return rx.window_alert('Please write at least one character!')           # story 추가시 최소 한 글자 입력 경고 메시지
        
        await self.handle_upload(rx.upload_files())                                  # 이미지 추가
        
        with rx.session() as session:                                                # session에 생성한 story 모델 저장
            tweet = Tweet(
                author=self.user.username,                                           # author : 유저 아이디
                content=self.tweet,                                                  # content : 유저 story 입력 내용
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),             # created_at : stroy 작성 시간
                image_content=", ".join(self.files),                                 # image_content : 이미지 파일
            )
            
            session.add(tweet)
            session.commit()
            self.tweet = ""                                                          # session에 저장 후 story내용 초기화
            self.img=[]
            self.files=[]
            
        return self.get_tweets()                                                     # story 게시 즉시 내용 피드에 반영

    #story 내용 불러오는 함수
    def get_tweets(self):
        """Get tweets from the database."""
        with rx.session() as session:
            if self.search:                                                          # story 검색 입력어가 있을경우
                self.tweets = (
                    session.query(Tweet)
                    .filter(Tweet.content.contains(self.search))                     # story 검색 입력단어가 포함된 story를 모두 가져옴
                    .all()[::-1]
                )
            else:
                self.tweets = session.query(Tweet).all()[::-1]                       # session에 저장된 모든 story를 가져옴

    #story 검색 입력어 세팅 함수
    def set_search(self, search):
        """Set the search query."""
        self.search = search
        return self.get_tweets()                                                     # 검색어에 맞는 story내용 불러오기

    #follow 함수
    def follow_user(self, username):
        """Follow a user."""
        with rx.session() as session:
            friend = Follows(
                follower_username=self.user.username, followed_username=username     # Follow모델에 follower_username에 현재 로그인 된 유저이름저장
            )                                                                        # Follow모델에 followed_username에 팔로잉 한 유저의 이름 저장
            session.add(friend)                                                      # session에 friend이름으로 생성된 Follow모델 추가
            session.commit()                                                         # session 저장
    
    #unfollow 함수
    def unfollow_user(self, username):
        """Unfollow a user."""
        with rx.session() as session: 
            follow = (                                                                       # follow한 유저 목록 불러오기
                session.query(Follows)
                .filter_by(follower_username=self.user.username, followed_username=username)
                .first()
            )
            if follow:                                                                       
                session.delete(follow)                                                       # follow가 되어있으면 session에서 삭제
                session.commit()                                                             # session 저장

                # Refresh the followers list after unfollowing
                self.followers = (                                                           # 삭제 후 session에 저장되어있는 follow 목록 불러오기
                    session.query(Follows)                                                   
                    .filter(Follows.followed_username == self.user.username)
                    .all()
                )        
    
    # 팔로잉 목록을 불러오는 함수
    @rx.var                                                                                  # 실시간으로 값의 변화 감지
    def following(self) -> list[Follows]:
        """Get a list of users the current user is following."""
        if self.logged_in:                                                                   # 로그인 되어있을 때
            with rx.session() as session:
                return (
                    session.query(Follows)                                                   # session에 저장되어 있는 follow 목록 불러오기
                    .filter(Follows.follower_username == self.user.username)
                    .all()
                )
        return []

    # 팔로워 목록을 불러오는 함수
    @rx.var
    def followers(self) -> list[Follows]:                                                    
        """Get a list of users following the current user."""
        if self.logged_in:                                                                   # 로그인 되어 있을 시
            with rx.session() as session:
                return (
                    session.query(Follows)                                                   # session에 저장된 follower 목록 불러오기
                    .where(Follows.followed_username == self.user.username)
                    .all()
                )
        return []

    # user를 검색하는 함수
    @rx.var
    def search_users(self) -> list[User]:
        """Get a list of users matching the search query."""
        if self.friend != "":                                                                # user을 검색하는 입력어가 있을 때
            with rx.session() as session:
                current_username = self.user.username if self.user is not None else ""       # 로그인이 되어있을 시
                users = (
                    session.query(User)
                    .filter(
                        User.username.contains(self.friend),                                 # 검색어가 들어있는 유저 목록 검색
                        User.username != current_username,                                   # 현재 접속해있는 유저의 이름은 빼고 검색
                    )
                    .all()
                )
                return users
        return []
    
    def top(self):
        self.show_top = not (self.show_top)

    def right(self):
        self.show_right = not (self.show_right)

    def change(self):
        self.show = not (self.show)

    # KaKao Rest API Key를 받아오는 함수     
    def kakao_api(self): 
        key=''
        with open('kakaoapikey.json','r')as f:                                              # kakaoapikey.json 파일에 있는 key를 가져와 저장 
            key = json.load(f)
        self.KAKAO_REST_API_KEY = key['key']

    # kakao api 검색으로 장소 목록을 받는 함수   
    def elec_location(self,region,page_num):
        self.kakao_api()                                                                    # kakao_api 함수 호출
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        params = {'query': region,'page': page_num}                                         # API 요청을 위한 매개변수 설정, 검색할 지역 및 페이지 번호가 포함됨
        headers = {"Authorization": f'KakaoAK {self.KAKAO_REST_API_KEY}'}                   # 인증을 위한 Kakao API 키를 포함한 헤더 설정

        places = requests.get(url, params=params, headers=headers).json()['documents']      # Kakao API에 검색어와 페이지 번호를 기반으로 지역 정보를 검색하는 GET 요청 수행
                                                                                            # 응답은 JSON 형식으로 변환되며 'documents' 키를 사용하여 관련 정보를 추출함
        return places                                                                       # Kakao API 검색에서 얻은 장소 목록 반환
    
    # 장소목록의 정보를 가져오는 함수
    def elec_info(self,places):
        X = []                                                                              # 경도 정보를 저장하는 리스트
        Y = []                                                                              # 위도 정보를 저장하는 리스트
        stores = []                                                                         # 가게 이름 정보를 저장하는 리스트
        road_address = []                                                                   # 도로명 주소 정보를 저장하는 리스트
        place_url = []                                                                      # 장소 URL 정보를 저장하는 리스트
        ID = []                                                                             # ID 정보를 저장하는 리스트

        for place in places:                                                                # 주어진 장소 목록을 반복하며 각 정보를 해당 리스트에 추가
            X.append(float(place['x']))
            Y.append(float(place['y']))
            stores.append(place['place_name'])
            road_address.append(place['road_address_name'])
            place_url.append(place['place_url'])
            ID.append(place['id'])

        ar = np.array([ID,stores, X, Y, road_address,place_url]).T                          # NumPy 배열을 사용하여 리스트를 전치하여 2D 배열 생성
        df = pd.DataFrame(ar, columns = ['ID','stores', 'X', 'Y','road_address','place_url']) # Pandas DataFrame으로 변환
        return df
    
    #사용자가 입력한 키워드로 정보를 받아와 데이터 프레임 생성
    def keywords(self):
        df = None
        for loca in self.locations:                                                         # self.locations에 있는 각 지역에 대해 반복
            for page in range(1,4):                                                         # 각 지역에 대해 1부터 3까지의 페이지를 검색
                local_name = self.elec_location(loca, page)                                 # elec_location 함수를 사용하여 지역 정보를 가져오기
                local_elec_info = self.elec_info(local_name)                                # elec_info 함수를 사용하여 가져온 지역 정보를 DataFrame으로 변환

                if df is None:                                                              # df가 초기화되지 않은 경우, local_elec_info로 초기화
                    df = local_elec_info
                elif local_elec_info is None:                                               # local_elec_info가 None인 경우, 계속 진행
                    continue
                else:                                                                       # df가 초기화되었고 local_elec_info가 None이 아닌 경우, 두 DataFrame을 연결
                    df = pd.concat([df, local_elec_info],join='outer', ignore_index = True)
        return df
    
    #데이터 프레임을 기준으로 지도를 생성하는 함수
    def make_map(self,dfs):
        m = folium.Map(location=[37.5518911,126.9917937],                                   # 기준 좌표를 사용하여 Folium 지도 생성
                    zoom_start=12)

        minimap = MiniMap()                                                                 # 미니맵 추가하기
        m.add_child(minimap)
        for i in range(len(dfs)):                                                           # DataFrame에 있는 각 행에 대해 Folium Marker 추가
            folium.Marker([dfs['Y'][i],dfs['X'][i]],                                        # 위도와 경도 정보를 사용하여 마커의 위치 설정
                    tooltip=dfs['stores'][i],                                               # 마커에 대한 툴팁으로 가게 이름 사용
                    popup=dfs['place_url'][i],                                              # 마커를 클릭할 때 나타나는 팝업에 장소 URL 사용
                    ).add_to(m)
        return m                                                                            # 최종 지도 반환

        
    def map_search(self):
        if os.path.exists('assets/map2.html'):                                              # 'assets/map2.html' 파일이 이미 존재하는 경우
            return rx.window_alert('Press clear first!')                                    # 'Clear' 버튼을 누르세요!
        if self.tag_search == "":                                                           # 검색어가 입력되지 않은 경우
            return rx.window_alert('Please enter your search term!')                        # 검색어를 입력해주세요!
        self.locations = self.tag_search.split(',')                                         # 입력된 검색어를 쉼표로 분리하여 위치 정보로 사용
        self.df = self.keywords()
        self.df = self.df.drop_duplicates(['ID'])                                           # 중복된 ID를 가진 행 제거
        self.df = self.df.reset_index()                                                     # 인덱스 재설정
        self.make_map(self.df).save('assets/map2.html')                                     # 지도 생성 및 'assets/map2.html'에 저장
        self.map_html ='/map2.html'                                                         # 맵 파일의 상대 경로
        self.map_iframe = f'<iframe src="{self.map_html}" width="100%" height="600"></iframe>' # 맵을 표시하기 위한 iframe 코드

    def map_clear(self):
        if os.path.exists('assets/map2.html'):                                              # 'assets/map2.html' 파일이 이미 존재하는 경우 삭제
            os.remove('assets/map2.html')
        self.locations=[]                                                                   # 위치 정보, 검색어, 데이터프레임 초기화
        self.tag_search =""
        self.df = pd.DataFrame()
        self.map_html='/map.html'                                                           # 초기 맵 파일의 상대 경로
        self.map_iframe = f'<iframe src="{self.map_html}" width="100%" height="600"></iframe>' # 초기 맵을 표시하기 위한 iframe 코드

    # 맵 iframe의 HTML 코드를 반환하는 Getter 메서드.
    @rx.var
    def map_iframe1(self) -> str:
        return self.map_iframe
    
    # 위치 정보 목록을 반환하는 Getter 메서드
    @rx.var
    def clear_map1(self) -> list[str]:
        return self.locations
    
    # 검색어를 반환하는 Getter 메서드
    @rx.var
    def clear_map2(self) -> str:
        return self.tag_search
    
    # 데이터프레임을 반환하는 Getter 메서드.
    @rx.var
    def clear_map3(self) -> pd.DataFrame:
        return self.df
    
    # 맵 HTML 파일 경로를 반환하는 Getter 메서드
    @rx.var
    def clear_map4(self) -> str:
        return self.map_html
    
    # 비디오 링크 입력 변수를 저장하는 함수
    def search_video(self):                                                                # 비디오 링크가 입력되지 않은 경우
        if self.video_search == "":                                                          
            return rx.window_alert('Enter the link to the video..')
        self.video_search = self.video_search                                              # 입력된 비디오 링크를 사용
        
    # 비디오 링크를 표시하는 Getter 메서드
    @rx.var
    def show_video(self) -> str:
        return self.video_search
    
    # 구글 실시간 트렌드를 가져오는 함수
    def google_crawler(self):
        url = 'https://trends.google.com/trends/api/topdailytrends?hl=ko&tz=-540&geo=KR'   # Google 트렌드 데이터를 가져오는 URL
        html = requests.get(url).text                                                      # URL에서 HTML 데이터 가져오기
        data = json.loads(str(html).split('\n')[1])                                        # JSON 형식의 데이터 추출
        result = []
        for i in range(10):                                                                # 상위 10개 트렌드 검색어 추출
            result.append(data['default']['trendingSearches'][i]['title'])
            
        self.web_trend = {i+1:result[i] for i in range(len(result))}                       # 웹 트렌드 딕셔너리에 저장
    
    # 실시간을 변하는 트렌드 값을 반영하는 함수
    @rx.var
    def real_time_trend(self) -> dict:
        return self.web_trend
    
    # Google API 키를 가져오는 함수
    def google_api(self):
        key=''                                                                             # Google API 키를 저장하는 변수 초기화
        with open('googleapikey.json','r')as f:                                            # 'googleapikey.json' 파일에서 API 키 읽어오기
            key = json.load(f)
        self.Google_API_KEY = key['key']                                                   # 클래스 속성에 Google API 키 저장
        
        key1 = ''                                                                          # 검색 엔진 ID를 저장하는 변수 초기화
        with open('googlesearchengine.json','r') as f:                                     # 'googlesearchengine.json' 파일에서 검색 엔진 ID 읽어오기
            key1 = json.load(f)
        self.Google_SEARCH_ENGINE_ID = key1['key']                                         # 클래스 속성에 Google 검색 엔진 ID 저장
    
    # Google API키를 활용한 웹 크롤링 함수
    def Google_API(self,query, wanted_row):
        query= query.replace("|","OR")                                                     # 검색 쿼리에서 "|"을 "OR"로 대체
        query += "-filetype:pdf"                                                           # PDF 파일 제외하도록 쿼리 업데이트
        start_pages=[]

        df_google= pd.DataFrame(columns=['Title','Link','Description'])                    # 검색 결과를 저장할 빈 데이터프레임 생성

        row_count =0                                                                       # 검색 횟수 초기화
        self.google_api()                                                                  # Google API 설정 메서드 호출


        for i in range(1,wanted_row+1000,10):                                              # 검색 결과를 가져올 페이지 시작 지점 설정
            start_pages.append(i)

        for start_page in start_pages:                                                     # 각 페이지에서 검색 결과 가져오기
            url = f"https://www.googleapis.com/customsearch/v1?key={self.Google_API_KEY}&cx={self.Google_SEARCH_ENGINE_ID}&q={query}&start={start_page}"
            data = requests.get(url).json()                                                # Google Custom Search API를 통해 데이터 가져오기
            search_items = data.get("items")
            
            try:                                                                           # 각 검색 결과에서 필요한 정보 추출
                for i, search_item in enumerate(search_items, start=1):

                    link = search_item.get("link")                                         # 페이지 링크 추출
                    if any(trash in link for trash in self.Trash_Link):                    # Trash_Link에 포함된 단어가 링크에 있는 경우 건너뛰기
                        pass
                    else: 
                        title = search_item.get("title")                                   # 페이지 제목 추출

                        description = search_item.get("snippet")                           # 페이지 스니펫 추출
                        
                        df_google.loc[start_page + i] = [title,link,description]           # 결과를 데이터프레임에 추가
                        row_count+=1                                                       # 검색 결과 횟수 증가
                        if (row_count >= wanted_row) or (row_count == 300) :               # 원하는 행 수에 도달하거나 최대 300개의 결과를 수집한 경우 반환
                            return df_google
            except:
                return df_google

        
        return df_google                                                                   # 모든 페이지에서 검색 결과를 수집한 경우 데이터프레임 반환
    
    # Naver API 클라이언트 Id 와  클라이언트 시크릿을 저장하는 함수
    def naver_api(self):
        key=''
        with open('naverclientid.json','r')as f:                                           # 'naverclientid.json' 파일에서 클라이언트 ID 읽어오기
            key = json.load(f)
        self.Naver_client_id = key['key']                                                  # 클래스 속성에 네이버 API 클라이언트 ID 저장
        
        key1 = ''
        with open('Naver_client_secret.json','r') as f:                                    # 'Naver_client_secret.json' 파일에서 클라이언트 시크릿 읽어오기
            key1 = json.load(f)
        self.Google_SEARCH_ENGINE_ID = key1['key']                                         # 클래스 속성에 네이버 API 클라이언트 시크릿 저장
    
    # Naver API 를 활용한 웹 크롤링 함수
    def Naver_API(self,query,wanted_row):
        query = urllib.parse.quote(query)                                                  # 검색 쿼리를 URL 인코딩

        display=100                                                                        # 한 번에 표시할 검색 결과 수, 시작 페이지, 마지막 페이지, 정렬 기준 설정
        start=1
        end=wanted_row+10000
        idx=0
        sort='sim'

        df= pd.DataFrame(columns=['Title','Link','Description'])                           # 결과를 저장할 데이터프레임 생성
        row_count= 0                                                                       # 검색 결과 횟수 초기화
        
        for start_index in range(start,end,display):                                       # 검색 결과를 가져오는 반복문
            url = "https://openapi.naver.com/v1/search/webkr?query="+ query +\
                "&display=" + str(display)+ \
                "&start=" + str(start_index) + \
                "&sort=" + sort
            request = urllib.request.Request(url)                                          # 네이버 검색 API URL 설정
            request.add_header("X-Naver-Client-Id",self.Naver_client_id)                   # HTTP 요청 헤더에 클라이언트 ID와 시크릿 추가
            request.add_header("X-Naver-Client-Secret",self.Naver_client_secret)
            try:                                                                           # HTTP 요청을 통해 응답 받기
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
                if(rescode==200):                                                          # 응답이 성공적인 경우
                    response_body = response.read()
                    items= json.loads(response_body.decode('utf-8'))['items']
                    remove_tag = re.compile('<.*?>')
                    for item_index in range(0,len(items)):                                 # 각 검색 결과에서 필요한 정보 추출
                        link = items[item_index]['link']
                        if any(trash in link for trash in self.Trash_Link):                # Trash_Link에 포함된 단어가 링크에 있는 경우 건너뛰기
                            idx+=1
                            pass
                        else:                                                              # 결과를 데이터프레임에 추가
                            title = re.sub(remove_tag, '', items[item_index]['title'])
                            description = re.sub(remove_tag, '', items[item_index]['description'])
                            df.loc[idx] =[title,link,description]
                            idx+=1                                                         # 검색 결과 횟수 증가
                            row_count+=1
                            if (row_count >= wanted_row) or (row_count == 300):            # 원하는 행 수에 도달하거나 최대 300개의 결과를 수집한 경우 반환
                                return df
                            
            except:
                return df
    
    # Daum API를 활용한 웹 크롤링
    def Daum_API(self,query,wanted_row):
        pages= wanted_row//10                                                              # 요청할 페이지 수 계산
        self.kakao_api()                                                                   # Kakao API 설정 메서드 호출
        method = "GET"                                                                     # HTTP 요청 방식, URL, 헤더 설정
        url = "https://dapi.kakao.com/v2/search/web"
        header = {'authorization': f'KakaoAK {self.KAKAO_REST_API_KEY}'}

        df= pd.DataFrame(columns=['Title','Link','Description'])                           # 결과를 저장할 데이터프레임 생성

        row_count=0                                                                        # 검색 결과 횟수 초기화

        for page in range(1,pages+10):                                                     # 각 페이지에서 검색 결과 가져오기
            params = {'query' : query, 'page' : page}
            request = requests.get( url, params= params, headers=header )
            for i, item in enumerate(request.json()["documents"], start=1):                # 검색 결과에서 필요한 정보 추출
                link = item['url']
                try:
                    written_year=int(item['datetime'][:4])                                 # 게시된 연도 추출
                except:
                    written_year = 2023

                if (any(trash in link for trash in self.Trash_Link) or (written_year <2020)): # Trash_Link에 포함된 단어가 링크에 있거나, 작성 연도가 2020년 이전인 경우 건너뛰기
                    pass
                else:
                    title= item["title"]
                    description = item["contents"]
                    df.loc[10*page+i] =[title,link,description]                            # 결과를 데이터프레임에 추가
                    row_count+=1                                                           # 검색 결과 횟수 증가
                    if (row_count >= wanted_row) or (row_count == 300):                    # 원하는 행 수에 도달하거나 최대 300개의 결과를 수집한 경우 반환
                        remove_tag = re.compile('<.*?>')                                  
                        df['Title'] =df['Title'].apply(lambda x :re.sub(remove_tag, '',x))
                        df['Description'] =df['Description'].apply(lambda x :re.sub(remove_tag, '',x))

                        return df
                    

        remove_tag = re.compile('<.*?>')                                                   # HTML 태그 제거 후 데이터프레임 반환
        df['Title'] =df['Title'].apply(lambda x :re.sub(remove_tag, '',x))
        df['Description'] =df['Description'].apply(lambda x :re.sub(remove_tag, '',x))
        
        return df
    
    # Google, Naver, Daum의 웹 크롤링 결과를 하나로 합치는 함수
    def final(self,query,wanted_row=100):
        # Google
        df_google = self.Google_API(query,wanted_row)
        df_google['search_engine']='Google'
        
        # Naver
        df_naver = self.Naver_API(query,wanted_row)
        df_naver['search_engine']='Naver'
        
        # Daum
        df_daum = self.Daum_API(query,wanted_row)
        df_daum['search_engine']='Daum'
        
        # 데이터프레임 합치기
        df_final= pd.concat([df_google,df_naver,df_daum])
        df_final.reset_index(inplace=True,drop=True)                                       # 인덱스 재설정
        return df_final
    
    # search 버튼을 누를 때 웹 크롤링 동작을 하게 해주는 함수
    def search_all(self):
        self.search_df = self.final(query=self.web_search, wanted_row=100)
    
    # 실시간으로 웹 크롤링 결과를 반영해주는 함수
    @rx.var
    def search_table(self)->pd.DataFrame:
        return self.search_df
    
    # 실시간으로 ai 채팅 결과를 반영해주는 함수
    @rx.var
    def kogpt_answer(self) ->str:
        return self.kogpt_response
    
    # KoGPT api를 활용한 대화 함수
    def kogptapi(self):
        """Post a tweet."""
        if not self.logged_in:                                                            # 로그인되어 있지 않은 경우 알림
            return rx.window_alert("Please log in first")
        if len(self.chat_input)==0:                                                       # 대화 입력이 비어 있는 경우 알림
            return rx.window_alert('Please write at least one character!')
        
        self.kakao_api()                                                                  # Kakao API 설정 메서드 호출
        api = KoGPT(service_key = self.KAKAO_REST_API_KEY)                                # KoGPT API 인스턴스 생성
        prompt = self.chat_input                                                          # 대화 입력을 프롬프트로 사용하여 KoGPT에 요청하여 응답 받기
        max_tokens=300
        self.kogpt_response = api.generate(prompt, max_tokens, temperature = 0.01)['generations'][0]['text']
        
        with rx.session() as session:                                                     # 대화 내용을 데이터베이스에 저장
            gpt = GPT(
                author=self.user.username,
                content=self.chat_input,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            
            session.add(gpt)
            session.commit()
            self.chat_input= ""
            
        with rx.session() as session:                                                     # KoGPT의 응답을 데이터베이스에 저장
            gpt = GPT(
                author = 'KoGPT',
                content=self.kogpt_response,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            session.add(gpt)
            session.commit()
            self.kogpt_response=''
            
        return self.get_gpt()                                                             # 최신 대화 기록 반환
    
    # 데이터베이스에서 KoGPT 대화내역을 가져오는 함수
    def get_gpt(self):
        with rx.session() as session:
            self.gpts = session.query(GPT).all()[::-1]  
    
    #데이터 베이스에 있는 KoGPT 대화 내역을 삭제하는 함수        
    def clear_gpt(self):
        with rx.session() as session:
            session.query(GPT).delete()
            session.commit()
        
        self.gpts=self.get_gpt()
        print(self.gpts)
    
    # 실시간으로 대화내역을 반영하는 함수
    @rx.var
    def saved_gpt(self) -> list[GPT] :
        return self.gpts
    
    #유저가 작성한 트윗만 가져오는 함수
    def get_user_tweet(self):
        with rx.session() as session:
            self.user_tweets = (session.query(Tweet)
            .filter(Tweet.author == self.user.username)
            .all()[::-1]
            )           