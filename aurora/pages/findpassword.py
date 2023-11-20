"""Sign up page. Uses auth_layout to render UI shared with the login page."""
import reflex as rx
from aurora.state.auth import AuthState


def findpassword():
    """The findpassword page."""
    return rx.container(
        rx.container(height='150px'),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.container(height='20px'),
                    rx.image(
                        src = "/aurora.ico",
                        width="70px",
                        height="70px",
                    ),
                ),              
                rx.vstack(           
                    rx.container(height='8px'),
                    rx.container(
                        rx.text(
                            "AURORA",
                            style={
                                "fontSize": "40px",
                                "fontWeight": "bolder",
                                "letterSpacing": "3px",
                                "fontFamily": "Open Sans, Sans-serif",
                                "background": "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)",
                                "-webkit-background-clip": "text",
                                "color": "black",
                            },
                            mb=-3,
                        ),
                        rx.text(
                            "Record your shining moments!",
                            style={
                                'background': "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)",
                                'background_clip': "text",  # 텍스트에만 그라데이션 적용
                                'color': "transparent",  # 텍스트 색상을 투명으로 설정
                                'font_weight': "medium",
                            },
                        ),
                    ),

                ),
            ),
            rx.container(height='10px'),
            rx.container(
                rx.input(placeholder="Username", on_blur=AuthState.set_username, mb=4),
                rx.button(
                    "Find Password",
                    on_click=AuthState.findpassword,
                    bg="blue.500",
                    color="white",
                    _hover={"bg": "blue.600"},
                ),
                align_items="left",
                bg="white",
                border="1px solid #eaeaea",
                p=4,
                max_width="400px",
                border_radius="lg",
            ),
            rx.container(height='10px'),
            rx.text(
                "Already have an account? ",
                rx.link("Sign in here.", href="/", color="blue.500"),
                color="gray.600",
            ),
            rx.container(height='20px'),
            width='400px',
            height='auto',
            center_content=True,
            borderRadius='20px',
            boxShadow='9px 9px 100px #79d0ed',
            background="linear-gradient(to bottom, #d7eefc, #ffffff)"
        ),
        center_content=True,
        # justifyContent='center',
        maxWidth='auto',
        maxHeight='auto',
        height='100vh',
        style={
            'background-image':"url('/aurora.jpg')",
            'background-size':'cover',
        }
    )