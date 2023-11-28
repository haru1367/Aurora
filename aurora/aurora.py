import cx_Oracle
import reflex as rx

from .pages import home, login, signup, findpassword, myprofile, maps, video, websearch, aichat, talk
from .state.base import State

app = rx.App(state=State)

# Reflex 앱 페이지 추가
app.add_page(login)
app.add_page(signup)
app.add_page(findpassword)
app.add_page(myprofile, on_load=State.check_login())
app.add_page(maps, on_load=State.check_login())
app.add_page(video, on_load=State.check_login())
app.add_page(websearch, on_load=State.check_login())
app.add_page(aichat, on_load=State.check_login())
app.add_page(talk, on_load=State.check_login())
app.add_page(home, route="/", on_load=State.check_login())

# Reflex 앱 컴파일
app.compile()
