"""The authentication state."""
import reflex as rx

from .base import State, User


class AuthState(State):
    """The authentication state for sign up and login page."""

    username: str
    password: str
    confirm_password: str
    
    

    def signup(self):
        #로그인을 위한 유저의 회원가입 정보 저장
        with rx.session() as session:
            if len(self.password)<4:
                return rx.window_alert("비밀번호는 최소 4자리 이상이어야 합니다.")  #비밀번호 최소 4자리이상 입력해야 가입가능하도록 경고 메시지
            if self.password != self.confirm_password:
                return rx.window_alert("비밀번호가 일치하지 않습니다.")             #비밀번호와 비밀번호 확인칸이 일치하지 않을 시 경고 메시지
            if session.exec(User.select.where(User.username == self.username)).first():
                return rx.window_alert("이미 존재하는 아이디입니다.")               #중복된 아이디로 가입이 불가능하도록 경고 메시지
            self.user = User(username=self.username, password=self.password)      #회원 정보를 데이터베이스에 저장
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/")

    def login(self):
        #로그인 기능
        with rx.session() as session:
            user = session.exec(
                User.select.where(User.username == self.username)               #유저가 입력한 아이디와 데이터베이스의 유저네임이 일치할 때
            ).first()
            if user and user.password == self.password:                         #유저가 입력한 비밀번호와 데이터베이스의 비밀번호가 일치할 때
                self.user = user
                return rx.redirect("/")                                         #경로로 이동
            else:
                return rx.window_alert("아이디 또는 비밀번호가 일치하지 않습니다.") #아이디 또는 비밀번호가 일치하지 않을 때
    
    def findpassword(self):
        #비밀번호 찾기기능
        with rx.session() as session:
            user_instance = session.exec(User.select.where(User.username == self.username)).first() #유저의 아이디가 데이터베이스에 저장된 비밀번호가 일치할 때
            if user_instance:
                return rx.window_alert(f'your password : {user_instance.password}') #아이디를 입력하면 유저의 비밀번호를 화면에 리턴
            session.expire_on_commit = False
            return rx.redirect("/")
        

        
    
    