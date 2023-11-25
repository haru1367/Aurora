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
    tweet: str
    tweets: list[Tweet] = []
    friend: str
    search: str
    img: list[str]
    files: list[str] = []  # Add files attribute
    show_right: bool = False
    show_top: bool = False
    show: bool = False
    KAKAO_REST_API_KEY: str
    Google_API_KEY : str
    Google_SEARCH_ENGINE_ID : str
    Naver_client_id:str
    Naver_client_secret:str
    locations: list[str]
    df:pd.DataFrame
    search_df:pd.DataFrame  
    tag_search:str
    map_html:str = "/map.html"
    map_iframe:str = f'<iframe src="{map_html}" width="100%" height="600"></iframe>'
    map_search_check:bool=False
    video_search:str=""
    web_trend :dict
    web_search :str
    chat_input:str
    kogpt_response:str
    gpts: list[GPT] = []
    Trash_Link = ["kin", "dcinside", "fmkorea", "ruliweb", "theqoo", "clien", "mlbpark", "instiz", "todayhumor"] 
    
    def handle_file_selection(self):
        # 파일 선택 대화상자 열기
        root = tk.Tk()
        root.withdraw()  # 화면에 창을 보이지 않도록 함
        file_paths = filedialog.askopenfilenames()

        # 선택된 파일 경로에 대한 처리
        for file_path in file_paths:
            # 파일 이름과 확장자를 추출
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1]
            
            # 선택한 파일을 저장
            upload_data = open(file_path, "rb").read()
            outfile = f".web/public/{file_name}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file_name)

            # Set the files attribute
            self.files.append(file_name)


    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = f"/{file.filename}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)
    
    async def post_tweet(self):
        """Post a tweet."""
        if not self.logged_in:
            return rx.window_alert("Please log in to post a tweet.")
        if len(self.tweet)==0:
            return rx.window_alert('Please write at least one character!')
        
        await self.handle_upload(rx.upload_files())
        
        with rx.session() as session:
            tweet = Tweet(
                author=self.user.username,
                content=self.tweet,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                image_content=", ".join(self.files),
            )
            
            session.add(tweet)
            session.commit()
            self.tweet = ""
            self.img=[]
            self.files=[]
            
        return self.get_tweets()

    def get_tweets(self):
        """Get tweets from the database."""
        with rx.session() as session:
            if self.search:
                self.tweets = (
                    session.query(Tweet)
                    .filter(Tweet.content.contains(self.search))
                    .all()[::-1]
                )
            else:
                self.tweets = session.query(Tweet).all()[::-1]

    def set_search(self, search):
        """Set the search query."""
        self.search = search
        return self.get_tweets()

    def follow_user(self, username):
        """Follow a user."""
        with rx.session() as session:
            friend = Follows(
                follower_username=self.user.username, followed_username=username
            )
            session.add(friend)
            session.commit()
    
    def unfollow_user(self, username):
        """Unfollow a user."""
        with rx.session() as session:
            follow = (
                session.query(Follows)
                .filter_by(follower_username=self.user.username, followed_username=username)
                .first()
            )
            if follow:
                session.delete(follow)
                session.commit()

                # Refresh the followers list after unfollowing
                self.followers = (
                    session.query(Follows)
                    .filter(Follows.followed_username == self.user.username)
                    .all()
                )        
    
    @rx.var
    def following(self) -> list[Follows]:
        """Get a list of users the current user is following."""
        if self.logged_in:
            with rx.session() as session:
                return (
                    session.query(Follows)
                    .filter(Follows.follower_username == self.user.username)
                    .all()
                )
        return []

    @rx.var
    def followers(self) -> list[Follows]:
        """Get a list of users following the current user."""
        if self.logged_in:
            with rx.session() as session:
                return (
                    session.query(Follows)
                    .where(Follows.followed_username == self.user.username)
                    .all()
                )
        return []

    @rx.var
    def search_users(self) -> list[User]:
        """Get a list of users matching the search query."""
        if self.friend != "":
            with rx.session() as session:
                current_username = self.user.username if self.user is not None else ""
                users = (
                    session.query(User)
                    .filter(
                        User.username.contains(self.friend),
                        User.username != current_username,
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
        
    def kakao_api(self): 
        key=''
        with open('kakaoapikey.json','r')as f:
            key = json.load(f)
        self.KAKAO_REST_API_KEY = key['key']
        
    def elec_location(self,region,page_num):
        self.kakao_api()
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        params = {'query': region,'page': page_num}
        headers = {"Authorization": f'KakaoAK {self.KAKAO_REST_API_KEY}'}

        places = requests.get(url, params=params, headers=headers).json()['documents']
        return places
    
    def elec_info(self,places):
        X = []
        Y = []
        stores = []
        road_address = []
        place_url = []
        ID = []
        for place in places:
            X.append(float(place['x']))
            Y.append(float(place['y']))
            stores.append(place['place_name'])
            road_address.append(place['road_address_name'])
            place_url.append(place['place_url'])
            ID.append(place['id'])

        ar = np.array([ID,stores, X, Y, road_address,place_url]).T
        df = pd.DataFrame(ar, columns = ['ID','stores', 'X', 'Y','road_address','place_url'])
        return df
    
    def keywords(self):
        df = None
        for loca in self.locations:
            for page in range(1,4):
                local_name = self.elec_location(loca, page)
                local_elec_info = self.elec_info(local_name)

                if df is None:
                    df = local_elec_info
                elif local_elec_info is None:
                    continue
                else:
                    df = pd.concat([df, local_elec_info],join='outer', ignore_index = True)
        return df
    
    def make_map(self,dfs):
        # 지도 생성하기
        m = folium.Map(location=[37.5518911,126.9917937],   # 기준좌표: 제주어딘가로 내가 대충 설정
                    zoom_start=12)
        # 미니맵 추가하기
        minimap = MiniMap() 
        m.add_child(minimap)
        for i in range(len(dfs)):
            folium.Marker([dfs['Y'][i],dfs['X'][i]],
                    tooltip=dfs['stores'][i],
                    popup=dfs['place_url'][i],
                    ).add_to(m)
        return m


    # def map(self):
    # m = folium.Map(location=[37.5518911, 126.9917937], zoom_start=12)
    # self.map_html = "/map2.html"
    # self.map_iframe = f'<iframe src="{self.map_html}" width="100%" height="600"></iframe>'
        
    def map_search(self):
        if os.path.exists('assets/map2.html'):
            return rx.window_alert('Press clear first!')
        if self.tag_search == "":
            return rx.window_alert('Please enter your search term!')
        self.locations = self.tag_search.split(',')
        self.df = self.keywords()
        self.df = self.df.drop_duplicates(['ID'])
        self.df = self.df.reset_index()
        self.make_map(self.df).save('assets/map2.html')
        self.map_html ='/map2.html'
        self.map_iframe = f'<iframe src="{self.map_html}" width="100%" height="600"></iframe>'

    def map_clear(self):
        if os.path.exists('assets/map2.html'):
            os.remove('assets/map2.html')
        self.locations=[]
        self.tag_search =""
        self.df = pd.DataFrame()
        self.map_html='/map.html'
        self.map_iframe = f'<iframe src="{self.map_html}" width="100%" height="600"></iframe>'

    @rx.var
    def map_iframe1(self) -> str:
        return self.map_iframe
    
    @rx.var
    def clear_map1(self) -> list[str]:
        return self.locations
    
    @rx.var
    def clear_map2(self) -> str:
        return self.tag_search
    
    @rx.var
    def clear_map3(self) -> pd.DataFrame:
        return self.df
    
    @rx.var
    def clear_map4(self) -> str:
        return self.map_html
    
    def search_video(self):
        if self.video_search == "":
            return rx.window_alert('Enter the link to the video..')
        self.video_search = self.video_search
        
    
    @rx.var
    def show_video(self) -> str:
        return self.video_search
    
    def google_crawler(self):
        url = 'https://trends.google.com/trends/api/topdailytrends?hl=ko&tz=-540&geo=KR'
        html = requests.get(url).text
        data = json.loads(str(html).split('\n')[1])
        result = []
        for i in range(10):
            result.append(data['default']['trendingSearches'][i]['title'])
            
        self.web_trend = {i+1:result[i] for i in range(len(result))}
    
    @rx.var
    def real_time_trend(self) -> dict:
        return self.web_trend
    
    def google_api(self):
        key=''
        with open('googleapikey.json','r')as f:
            key = json.load(f)
        self.Google_API_KEY = key['key']
        
        key1 = ''
        with open('googlesearchengine.json','r') as f:
            key1 = json.load(f)
        self.Google_SEARCH_ENGINE_ID = key1['key']
    
    def Google_API(self,query, wanted_row):
        query= query.replace("|","OR")
        query += "-filetype:pdf"
        start_pages=[]

        df_google= pd.DataFrame(columns=['Title','Link','Description'])

        row_count =0 
        self.google_api()


        for i in range(1,wanted_row+1000,10):
            start_pages.append(i)

        for start_page in start_pages:
            url = f"https://www.googleapis.com/customsearch/v1?key={self.Google_API_KEY}&cx={self.Google_SEARCH_ENGINE_ID}&q={query}&start={start_page}"
            data = requests.get(url).json()
            search_items = data.get("items")
            
            try:
                for i, search_item in enumerate(search_items, start=1):
                    # extract the page url
                    link = search_item.get("link")
                    if any(trash in link for trash in self.Trash_Link):
                        pass
                    else: 
                        # get the page title
                        title = search_item.get("title")
                        # page snippet
                        description = search_item.get("snippet")
                        # print the results
                        df_google.loc[start_page + i] = [title,link,description] 
                        row_count+=1
                        if (row_count >= wanted_row) or (row_count == 300) :
                            return df_google
            except:
                return df_google

        
        return df_google
    
    def naver_api(self):
        key=''
        with open('naverclientid.json','r')as f:
            key = json.load(f)
        self.Naver_client_id = key['key']
        
        key1 = ''
        with open('Naver_client_secret.json','r') as f:
            key1 = json.load(f)
        self.Google_SEARCH_ENGINE_ID = key1['key']
    
    def Naver_API(self,query,wanted_row):
        query = urllib.parse.quote(query)

        display=100
        start=1
        end=wanted_row+10000
        idx=0
        sort='sim'

        df= pd.DataFrame(columns=['Title','Link','Description'])
        row_count= 0 
        
        for start_index in range(start,end,display):
            url = "https://openapi.naver.com/v1/search/webkr?query="+ query +\
                "&display=" + str(display)+ \
                "&start=" + str(start_index) + \
                "&sort=" + sort
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",self.Naver_client_id)
            request.add_header("X-Naver-Client-Secret",self.Naver_client_secret)
            try:
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
                    items= json.loads(response_body.decode('utf-8'))['items']
                    remove_tag = re.compile('<.*?>')
                    for item_index in range(0,len(items)):
                        link = items[item_index]['link']
                        if any(trash in link for trash in self.Trash_Link):
                            idx+=1
                            pass
                        else:
                            title = re.sub(remove_tag, '', items[item_index]['title'])
                            description = re.sub(remove_tag, '', items[item_index]['description'])
                            df.loc[idx] =[title,link,description]
                            idx+=1
                            row_count+=1
                            if (row_count >= wanted_row) or (row_count == 300):
                                return df
                            
            except:
                return df
    
    def Daum_API(self,query,wanted_row):
        pages= wanted_row//10 
        self.kakao_api()
        method = "GET"
        url = "https://dapi.kakao.com/v2/search/web"
        header = {'authorization': f'KakaoAK {self.KAKAO_REST_API_KEY}'}

        df= pd.DataFrame(columns=['Title','Link','Description'])

        row_count=0

        for page in range(1,pages+10):
            params = {'query' : query, 'page' : page}
            request = requests.get( url, params= params, headers=header )
            for i, item in enumerate(request.json()["documents"], start=1):
                link = item['url']
                try:
                    written_year=int(item['datetime'][:4])
                except:
                    written_year = 2023

                if (any(trash in link for trash in self.Trash_Link) or (written_year <2020)):
                    pass
                else:
                    title= item["title"]
                    description = item["contents"]
                    df.loc[10*page+i] =[title,link,description]
                    row_count+=1
                    if (row_count >= wanted_row) or (row_count == 300):
                        remove_tag = re.compile('<.*?>')
                        df['Title'] =df['Title'].apply(lambda x :re.sub(remove_tag, '',x))
                        df['Description'] =df['Description'].apply(lambda x :re.sub(remove_tag, '',x))

                        return df
                    

        remove_tag = re.compile('<.*?>')
        df['Title'] =df['Title'].apply(lambda x :re.sub(remove_tag, '',x))
        df['Description'] =df['Description'].apply(lambda x :re.sub(remove_tag, '',x))
        
        return df
    
    def final(self,query,wanted_row=100):
        df_google = self.Google_API(query,wanted_row)
        df_google['search_engine']='Google'
        df_naver = self.Naver_API(query,wanted_row)
        df_naver['search_engine']='Naver'
        df_daum = self.Daum_API(query,wanted_row)
        df_daum['search_engine']='Daum'
        df_final= pd.concat([df_google,df_naver,df_daum])
        df_final.reset_index(inplace=True,drop=True)
        return df_final
    
    def search_all(self):
        self.search_df = self.final(query=self.web_search, wanted_row=100)
    
    @rx.var
    def search_table(self)->pd.DataFrame:
        return self.search_df
        
    
    # def kogptapi(self):
    #     self.kakao_api()
    #     api = KoGPT(service_key = self.KAKAO_REST_API_KEY)
    #     prompt = self.chat_input
    #     max_tokens=32
    #     self.kogpt_response = api.generate(prompt, max_tokens, temperature = 0.01)['generations'][0]['text']
    #     print(self.kogpt_response)
    
    @rx.var
    def kogpt_answer(self) ->str:
        return self.kogpt_response
    
    def kogptapi(self):
        """Post a tweet."""
        if not self.logged_in:
            return rx.window_alert("Please log in first")
        if len(self.chat_input)==0:
            return rx.window_alert('Please write at least one character!')
        
        self.kakao_api()
        api = KoGPT(service_key = self.KAKAO_REST_API_KEY)
        prompt = self.chat_input
        max_tokens=300
        self.kogpt_response = api.generate(prompt, max_tokens, temperature = 0.01)['generations'][0]['text']
        
        with rx.session() as session:
            gpt = GPT(
                author=self.user.username,
                content=self.chat_input,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            
            session.add(gpt)
            session.commit()
            self.chat_input= ""
            
        with rx.session() as session:
            gpt = GPT(
                author = 'KoGPT',
                content=self.kogpt_response,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            session.add(gpt)
            session.commit()
            self.kogpt_response=''
            
        return self.get_gpt()
    
    def get_gpt(self):
        with rx.session() as session:
            self.gpts = session.query(GPT).all()[::-1]  
            
    def clear_gpt(self):
        with rx.session() as session:
            session.query(GPT).delete()
            session.commit()
        
        self.gpts=self.get_gpt()
        print(self.gpts)
    
    @rx.var
    def saved_gpt(self) -> list[GPT] :
        return self.gpts
              