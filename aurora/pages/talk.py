# aurora.state.home 모듈에서 필요한 State 및 HomeState를 가져옵니다.
import reflex as rx
from aurora.state.base import State
from aurora.state.home import HomeState

# 컴포넌트를 가져옵니다.
from ..components import container


color = "rgb(107,99,246)"
# 탭 버튼을 생성하는 함수
def tab_button(name, href):
    """A tab switcher button."""
    return rx.link(
        rx.icon(tag="star", mr=2),  # 별 모양 아이콘
        name,  # 버튼 텍스트
        display="inline-flex",
        align_items="center",
        py=3,
        px=6,
        href=href,  # 버튼 클릭 시 이동할 경로
        border="1px solid #eaeaea",
        font_weight="semibold",
        border_radius="full",
    )

# 왼쪽에 표시되는 탭 스위처
def tabs():
    """The tab switcher displayed on the left."""
    return rx.box(
        rx.vstack(
            rx.container(
                rx.hstack(
                    rx.icon(tag="moon", mr=2, color='yellow'),  # 달 모양 아이콘
                    rx.text(
                        "Aurora", 
                        style={
                            "fontSize": "25px",
                            "fontWeight": "bolder",
                            "fontFamily": "Open Sans,Sans-serif",
                            "background": "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)",
                            "-webkit-background-clip": "text",
                            "color": "transparent",
                        },
                        center_content=True,
                    ),  # 앱 이름
                ),
            ),
            tab_button("Home", "/"),  # Home 탭 버튼
            tab_button("My Profile","/myprofile"),
            tab_button("Maps","/maps"),
            tab_button("video","/video"),
            tab_button("web search","/websearch"),
            tab_button("ai chat","/aichat"),
            rx.button("Sign out", on_click=State.logout),  # 로그아웃 버튼
            rx.button(
                rx.icon(tag="moon"),
                on_click=rx.toggle_color_mode,
            ),
            rx.container(height='200px'),
            align_items="left",
            gap=4,
        ),
        py=4,
    )

def sidebar():
    """The sidebar displayed on the right."""
    return rx.vstack(
        align_items="start",
        gap=4,
        h="100%",
        py=4,
    )

# 피드의 헤더
def feed_header(HomeState):
    
    """The header of the feed."""
    return rx.hstack(
        rx.heading("Chat", size="md"),  # 피드의 제목
        rx.input(on_blur=HomeState.set_receive_user, placeholder="Please enter the person you would like to send the message to!"),  # 트윗 검색을 위한 입력 상자
        rx.button(
            "select",
            on_click = HomeState.get_messages,
            border_radius="1em",
            box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
            background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
            box_sizing="border-box",
            color="white",
            opacity="0.6",
            _hover={"opacity": 1},
        ),
        justify="space-between",
        p=4,
        border_bottom="3px solid #ededed",
    )

# 피드 영역
def feed(HomeState):
    return rx.box(
        feed_header(HomeState),
        rx.vstack(
            rx.container(height='10px'),
        ),
        border_x="3px solid #ededed",
        h="100%",
    )

# 홈 페이지
def talk():
    State.check_login
    return container(
        rx.grid(
            tabs(),
            feed(HomeState),
            sidebar(),
            grid_template_columns="1fr 4fr 1fr",
            h="100vh",
            gap=4,
        ),
        max_width="1600px",
    )