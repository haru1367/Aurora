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
        border="1px solid #000000",
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

# 오른쪽에 표시되는 사이드바
def sidebar(HomeState):
    """The sidebar displayed on the right."""
    return rx.vstack(
        rx.input(
            on_change=HomeState.set_friend,
            placeholder="Search users",  # 사용자 검색을 위한 입력 상자
            width="100%",
            border = "3px solid #000000",
        ),
        rx.foreach(
            HomeState.search_users,
            lambda user: rx.vstack(
                rx.hstack(
                    rx.avatar(name=user.username, size="sm"),  # 검색된 사용자의 아바타 이미지
                    rx.text(user.username),  # 검색된 사용자의 사용자 이름
                    rx.spacer(),
                    rx.button(
                        rx.icon(tag="add"),
                        on_click=lambda: HomeState.follow_user(user.username),  # 사용자를 팔로우하는 버튼
                    ),
                    width="100%",
                ),
                py=2,
                width="100%",
            ),
        ),
        align_items="start",
        gap=4,
        h="100%",
        py=4,
    )

# 피드의 헤더
def feed_header(HomeState):
    """The header of the feed."""
    return rx.hstack(
        rx.heading("Story", size="md"),  # 피드의 제목
        rx.input(on_change=HomeState.set_search, placeholder="Search tweets"),  # 트윗 검색을 위한 입력 상자
        justify="space-between",
        p=4,
        border_bottom="3px solid #000000",
    )

# 새로운 트윗을 작성하는 컴포저
def composer(HomeState):
    """The composer for new tweets."""
    return rx.vstack(
        rx.container(height='5px'),
        rx.vstack(
            rx.hstack(
                rx.avatar(size="md"),  # 사용자의 아바타 이미지
                rx.container(width='30px'),
                rx.text_area(
                    value=HomeState.tweet,
                    w='100%',
                    border=2,
                    placeholder="What's happening?",  # 트윗을 작성하는 입력 상자
                    resize="none",
                    py=4,
                    px=0,
                    _focus={"border": 0, "outline": 0, "boxShadow": "none"},
                    on_change=HomeState.set_tweet,
                ),
                width='95%',
                margin_left = '30px',
            ),
            rx.hstack(
                rx.button(
                    "Select File",
                    border_radius="1em",
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                    box_sizing="border-box",
                    color="white",
                    opacity="0.6",
                    _hover={"opacity": 1},
                    on_click=HomeState.handle_file_selection,
                ),
                rx.button(
                    "Select Cancel",
                    on_click=HomeState.file_select_cancel,
                    border_radius="1em",
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                    box_sizing="border-box",
                    color="white",
                    opacity="0.6",
                    _hover={"opacity": 1},
                ),
                rx.button(
                    "Tweet",
                    on_click= HomeState.post_tweet,
                    border_radius="1em",
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                    box_sizing="border-box",
                    color="white",
                    opacity="0.6",
                    _hover={"opacity": 1},
                    style={"margin-left": "auto"},  # Align to the right
                ),  # 트윗을 게시하는 버튼
                justify_content="flex-end",
                px=4,
                py=2,
                width='100%',
            ),
            rx.responsive_grid(
                rx.foreach(
                    HomeState.img,
                    lambda img: rx.vstack(
                        rx.image(src=img),
                        rx.text(img),
                    ),
                ),
                columns=[2],
                spacing="5px",
            ),
            margin_left='5px',
            width='97%',
            border_radius='20px',
            border="3px solid #000000",
        ),
    )


# 개별 트윗을 표시하는 함수
def tweet(tweet):
    """Display for an individual tweet in the feed."""
    image_tags = rx.cond(
        tweet.image_content,
        rx.foreach(
            tweet.image_content.split(", "),
            lambda image: rx.image(src=f"/{image}", alt="tweet image")
        ),
        rx.box()  # 이미지가 없는 경우 빈 리스트를 반환합니다.
    ),

    return rx.vstack(
        rx.hstack(
            rx.container(width='5px'),
            rx.vstack(
                rx.avatar(name=tweet.author, size="sm"),  # 트윗 작성자의 아바타 이미지
            ),
            rx.box(
                rx.hstack(
                    rx.text("@" + tweet.author, font_weight="bold"),  # 트윗 작성자의 사용자 이름
                    rx.text("["+ tweet.created_at +"]"),
                ),
                rx.text(tweet.content, width="100%"),  # 트윗 내용
                *image_tags,
                width = '100%',
            ),
            py=4,
            gap=1,
            border="3px solid #3498db",
            border_radius='10px',
            width='98%',
        ),
        rx.container(height='5px'),
        margin_left='15px',
        align_items='start',
        width='auto',
    )

# 피드 영역
def feed(HomeState):
    """The feed."""
    return rx.box(
        feed_header(HomeState),
        composer(HomeState),
        rx.container(height='10px'),
        rx.cond(
            HomeState.tweets,
            rx.foreach(
                HomeState.tweets,
                tweet
            ),
            rx.vstack(
                rx.button(
                    rx.icon(
                        tag="repeat",
                        mr=1,
                    ),
                    rx.text("Click to load tweets"),
                    on_click=HomeState.get_tweets,
                ),  # 트윗을 불러오는 버튼
                p=4,
            ),
        ),
        border_x="3px solid #000000",
        h="100%",
    )

# 홈 페이지
def home():
    State.check_login
    return container(
        rx.grid(
            tabs(),
            feed(HomeState),
            sidebar(HomeState),
            grid_template_columns="1fr 4fr 1fr",
            h="100vh",
            gap=4,
        ),
        max_width="1600px",
    )
