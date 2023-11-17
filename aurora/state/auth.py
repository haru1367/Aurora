"""The authentication state."""
import reflex as rx

from .base import State, User


class AuthState(State):
    """The authentication state for sign up and login page."""

    username: str
    password: str
    confirm_password: str

    def signup(self):
        """Sign up a user."""
        with rx.session() as session:
            if self.password != self.confirm_password:
                return rx.window_alert("비밀번호가 일치하지 않습니다.")
            if session.exec(User.select.where(User.username == self.username)).first():
                return rx.window_alert("이미 존재하는 아이디입니다.")
            self.user = User(username=self.username, password=self.password)
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/")

    def login(self):
        """Log in a user."""
        with rx.session() as session:
            user = session.exec(
                User.select.where(User.username == self.username)
            ).first()
            if user and user.password == self.password:
                self.user = user
                return rx.redirect("/")
            else:
                return rx.window_alert("아이디 또는 비밀번호가 일치하지 않습니다.")
