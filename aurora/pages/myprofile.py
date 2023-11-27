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
                    rx.icon(tag="spinner", mr=2, color='green'),  # 달 모양 아이콘
                    rx.text(
                        "Aurora", 
                        style={
                            "fontSize": "25px",
                            "fontWeight": "bolder",
                            "fontFamily": "Open Sans,Sans-serif",
                            "background": "-webkit-linear-gradient(-45deg, #77e67d, #3c8552)",
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
            tab_button("ai_chat","aichat"),
            rx.button(
                rx.icon(tag="moon"),
                on_click=rx.toggle_color_mode,
            ),
            rx.button("Log out", on_click=State.logout),  # 로그아웃 버튼
            rx.container(height='200px'),
            align_items="left",
            gap=4,
        ),
        py=4,
    )

# 오른쪽에 표시되는 사이드바
def sidebar(HomeState):
    """The sidebar displayed on the right."""
    return rx.box(
        rx.vstack(
            rx.container(height='8px'),
            rx.container(
                rx.button(
                    rx.icon(
                        tag="arrow_left", 
                        on_click=HomeState.right
                    ),
                ),
            ),
            rx.drawer(
                rx.drawer_overlay(
                    rx.drawer_content(
                        rx.drawer_header(
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
                        ),
                        rx.drawer_body(
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
                            rx.container(height='8px'),
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
                        ),
                        rx.drawer_footer(
                            rx.button(
                                "Close", on_click=HomeState.right
                            )
                        ),
                        bg="rgba(100, 100, 100, 0.7)",
                    )
                ),
                is_open=HomeState.show_right,
            ),  
        )
    )

# 피드의 헤더
def feed_header(HomeState):
    """The header of the feed."""
    return rx.hstack(
        rx.heading("Story", size="md"),  # 피드의 제목
        rx.input(on_change=HomeState.set_search, placeholder="Search"),  # 트윗 검색을 위한 입력 상자
        justify="space-between",
        p=4,
        border_bottom="3px solid #000000",
    )

def composer(HomeState):
    HomeState.setting_user_id
    HomeState.syn_user_name
    HomeState.syn_user_status_message
    HomeState.syn_user_account_status
    HomeState.getprofile
    return rx.vstack(
        rx.container(height='10px'),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.container(height='10px'),
                    rx.avatar(size="xl"),  # 사용자의 아바타 이미지
                ),
                rx.vstack(
                    rx.text(HomeState.user.username, size = "md", fontSize = "30px", fontWeight = "bold"),
                    rx.text(HomeState.users_name, fontSize = "20px", fontweight='bold'),
                    rx.text(HomeState.users_status_message, fontSize = '15px'),
                    align_items='start',
                ),
                p=4,
                width='100%',
                margin_left='5px',
                align_items='start',
            ),
            rx.hstack(
                rx.hstack(
                    rx.button(
                        "load",
                        on_click = HomeState.getprofile,
                        border_radius="1em",
                        box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                        background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                        box_sizing="border-box",
                        color="white",
                        opacity="0.6",
                        _hover={"opacity": 1},
                    ),
                    rx.button(
                        "Edit Profile",
                        on_click = HomeState.change1,
                        border_radius="1em",
                        box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                        background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                        box_sizing="border-box",
                        color="white",
                        opacity="0.6",
                        _hover={"opacity": 1},
                    ),
                    rx.modal(
                        rx.modal_overlay(
                            rx.modal_content(
                                rx.modal_header("Edit Profile"),
                                rx.modal_body(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.vstack(
                                                rx.text('Nickname '),
                                                rx.container(height='3px'),
                                                rx.text('Message '),
                                                align_items='start',
                                            ),
                                            rx.vstack(
                                                rx.input(on_change=HomeState.set_edit_user_name, placeholder='write nickname'),
                                                rx.input(on_change=HomeState.set_edit_user_status_message, placeholder='write status_message'),
                                                align_items='start',
                                            ),
                                            width='100%',
                                        ),
                                        rx.hstack(
                                            rx.text(
                                                'private account'
                                            ),
                                            rx.switch(
                                                is_checked=HomeState.checked,
                                                on_change=HomeState.change_check,
                                                color_scheme="blue",
                                            ),
                                            justify_content='flex-end',
                                        ),
                                        align_items='start',
                                    ),
                                ),
                                rx.modal_footer(
                                    rx.button(
                                        'Confirm',
                                        on_click=HomeState.change,
                                        border_radius="1em",
                                        box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                                        background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                                        box_sizing="border-box",
                                        color="white",
                                        opacity="0.6",
                                        _hover={"opacity": 1},
                                    )
                                )
                            ),
                        ),
                        is_open=HomeState.show,
                    )
                ),
                rx.container(width='10px'),
                justify_content='flex-end',
                width='100%',
            ),
            rx.container(height='10px'),
            width='100%',
            border='3px solid #eda239',
            border_radius='20px',
        ),
        rx.container(height='10px'),
        width ='97%',
        margin_left='10px',
    )
    
    

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
                rx.avatar(name=tweet.author, size="md"),  # 트윗 작성자의 아바타 이미지
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
        width='97%',
    )

# 피드 영역
def feed(HomeState):
    """The feed."""
    return rx.box(
        feed_header(HomeState),
        composer(HomeState),
        rx.cond(
            HomeState.user_tweets,
            rx.foreach(
                HomeState.user_tweets,
                tweet
            ),
            rx.vstack(
                rx.button(
                    rx.icon(
                        tag="repeat",
                        mr=1,
                    ),
                    rx.text("Click to load tweets"),
                    on_click=HomeState.get_user_tweet,
                ),  # 트윗을 불러오는 버튼
                p=4,
            ),
        ),
        border_x="3px solid #000000",
    )

# 마이 페이지
def myprofile():
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