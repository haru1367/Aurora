"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx

from .pages import home, login, signup, findpassword, myprofile, maps, video, websearch, aichat, talk
from .state.base import State

app = rx.App(state=State)
app.add_page(login)
app.add_page(signup)
app.add_page(findpassword)
app.add_page(myprofile, on_load=State.check_login())
app.add_page(maps, on_load=State.check_login())
app.add_page(video, on_load=State.check_login())
app.add_page(websearch, on_load=State.check_login())
app.add_page(aichat, on_load=State.check_login())
app.add_page(talk,on_load=State.check_login())
app.add_page(home, route="/", on_load=State.check_login())
app.compile()
