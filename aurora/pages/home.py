# aurora.state.home 모듈에서 필요한 State 및 HomeState를 가져옵니다.
import reflex as rx
from aurora.state.base import State
from aurora.state.home import HomeState

# 컴포넌트를 가져옵니다.
from ..components import container

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
            rx.box(
                rx.heading("Followers", size="sm"),
                rx.foreach(
                    HomeState.followers,
                    lambda follow: rx.vstack(
                        rx.hstack(
                            rx.avatar(name=follow.follower_username, size="sm"),  # 팔로워의 아바타 이미지
                            rx.text(follow.follower_username),  # 팔로워의 사용자 이름
                        width="100%",
                        ),
                        padding="1em",
                    ),
                ),
                p=4,
                border_radius="md",
                border="1px solid #eaeaea",
            ),
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
        rx.box(
            rx.heading("Following", size="sm"),
            rx.foreach(
                HomeState.following,
                lambda follow: rx.vstack(
                    rx.hstack(
                        rx.avatar(name=follow.followed_username, size="sm"),  # 팔로잉 중인 사용자의 아바타 이미지
                        rx.text(follow.followed_username),  # 팔로잉 중인 사용자의 사용자 이름
                        rx.spacer(),
                        rx.button(
                            rx.icon(tag="minus"),
                            on_click=lambda: HomeState.unfollow_user(follow.followed_username),
                        ),
                    ),
                    padding="1em",
                ),
            ),
            p=4,
            border_radius="md",
            border="1px solid #eaeaea",
            w="100%",
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
        border_bottom="1px solid #ededed",
    )

# 새로운 트윗을 작성하는 컴포저
def composer(HomeState):
    """The composer for new tweets."""
    return rx.grid(
        rx.vstack(
            rx.avatar(size="md"),  # 사용자의 아바타 이미지
            p=4,
        ),
        rx.box(
            rx.text_area(
                value = HomeState.tweet,
                w="100%",
                border=0,
                placeholder="What's happening?",  # 트윗을 작성하는 입력 상자
                resize="none",
                py=4,
                px=0,
                _focus={"border": 0, "outline": 0, "boxShadow": "none"},
                on_change =HomeState.set_tweet,
            ),
            rx.hstack(
                rx.button(
                    "File Select",
                    border_radius="1em",
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                    box_sizing="border-box",
                    color="white",
                    opacity="0.6",
                    _hover={
                        "opacity": 1,
                    },
                ),
                rx.button(
                    "Tweet",
                    on_click=HomeState.post_tweet,
                    border_radius="1em",
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                    box_sizing="border-box",
                    color="white",
                    opacity="0.6",
                    _hover={
                        "opacity": 1,
                    },
                ),  # 트윗을 게시하는 버튼
                justify_content="flex-end",
                border_top="1px solid #ededed",
                px=4,
                py=2,
            ),
        ),
        grid_template_columns="1fr 5fr",
        border_bottom="1px solid #ededed",
    )

# 개별 트윗을 표시하는 함수
def tweet(tweet):
    """Display for an individual tweet in the feed."""
    return rx.grid(
        rx.vstack(
            rx.avatar(name=tweet.author, size="sm"),  # 트윗 작성자의 아바타 이미지
        ),
        rx.box(
            rx.text("@" + tweet.author, font_weight="bold"),  # 트윗 작성자의 사용자 이름
            rx.text(tweet.content, width="100%"),  # 트윗 내용
        ),
        grid_template_columns="1fr 5fr",
        py=4,
        gap=1,
        border_bottom="1px solid #ededed",
    )

# 피드 영역
def feed(HomeState):
    """The feed."""
    return rx.box(
        feed_header(HomeState),
        composer(HomeState),
        rx.cond(
            HomeState.tweets,
            rx.foreach(
                HomeState.tweets,
                tweet,
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
        border_x="1px solid #ededed",
        h="100%",
    )

# 홈 페이지
def home():
    """The home page."""
    return container(
        rx.grid(
            tabs(),
            feed(HomeState),
            sidebar(HomeState),
            grid_template_columns="1fr 3fr 1fr",
            h="100vh",
            gap=4,
        ),
        max_width="1300px",
    )
