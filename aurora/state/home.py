"""The state for the home page."""
from datetime import datetime
import reflex as rx
from .base import Follows, State, Tweet, User
import os,json
import tkinter as tk
from tkinter import filedialog
import requests
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap


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
    REST_API_KEY: str
    locations: list[str]
    df:pd.DataFrame  
    map_html:str
    
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
                created_at=datetime.now().strftime("%m/%d %H"),
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
        with open('../key.json','r')as f:
            key = json.load(f)
        self.REST_API_KEY = key['key']
        
    def elec_location(self,region,page_num):
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        params = {'query': region,'page': page_num}
        headers = {"Authorization": self.REST_API_KEY}

        places = requests.get(url, params=params, headers=headers).json()['documents']
        total = requests.get(url, params=params, headers=headers).json()['meta']['total_count']
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
    
    def keywords(self,location_name):
        df = None
        self.location.extend('성산일출봉 전기충전소','광치기해수욕장 전기충전소')
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

        # 마커 추가하기
        for i in range(len(dfs)):
            folium.Marker([self.df['Y'][i],self.df['X'][i]],
                    tooltip=dfs['stores'][i],
                    popup=dfs['place_url'][i],
                    ).add_to(m)
        return m
    
    def search_map(self):
        self.df = self.keywords(self.locations)
        self.df = self.df.drop_duplicates(['ID'])
        self.df = self.df.reset_index()
        self.make_map(self.df)
        
    def map(self):
        m = folium.Map(location=[37.5518911, 126.9917937], zoom_start=12)