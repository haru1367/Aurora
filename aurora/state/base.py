"""Base state for aurora example. Schema is inspired by https://drawsql.app/templates/aurora."""
from typing import Optional

from sqlmodel import Field
import reflex as rx

#Follow 모델 생성
class Follows(rx.Model, table=True):
    """A table of Follows. This is a many-to-many join table.

    See https://sqlmodel.tiangolo.com/tutorial/many-to-many/ for more information.
    """

    followed_username: str = Field(primary_key=True) #followed 유저의 이름을 저장하는 영역
    follower_username: str = Field(primary_key=True) #follower 유저의 이름을 저장하는 영역

class Profile(rx.Model, table=True):
    user_id:str=Field()
    user_name: str = Field()
    user_status_message:str=Field()
    user_account_status:bool=Field()

#User 모델 생성
class User(rx.Model, table=True):

    username: str = Field() #유저의 아이디를 저장하는 영역
    password: str = Field() #유저의 비밀번호를 저장하는 영역

#Tweet 모델 생성
class Tweet(rx.Model, table=True):

    content: str = Field() #유저의 게시글 입력 내용을 저장하는 영역
    created_at: str = Field()  #유저의 게시글 입력 시간을 저장하는 영역
    image_content: str = Field() #유저의 이미지 파일 정보를 저장하는 영역
    author: str = Field() #유저의 아이디 저장 영역

#GPT 모델 생성    
class GPT(rx.Model, table=True):
    content: str = Field() #유저의 질문내용, KoGPT의 답변을 저장하는 영역
    author: str = Field() #유저의 아이디, KoGPT를 저장하는 영역
    created_at : str = Field() #질문 시각을 저장하는 영역

#앱의 기본 클래스 생성
class State(rx.State):
    user: Optional[User] = None

    def logout(self):
        """Log out a user."""
        self.reset()
        return rx.redirect("/")

    def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect("/login")

    @rx.var
    def logged_in(self):
        """Check if a user is logged in."""
        return self.user is not None
