"""The state for the home page."""
from datetime import datetime

import reflex as rx

from .base import Follows, State, Tweet, User
import os
import tkinter as tk
from tkinter import filedialog



class HomeState(State):
    """The state for the home page."""

    tweet: str
    tweets: list[Tweet] = []

    friend: str
    search: str
    img: list[str]
    files: list[str] = []  # Add files attribute
    
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
