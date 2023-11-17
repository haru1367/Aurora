"""Login page. Uses auth_layout to render UI shared with the sign up page."""
import reflex as rx

from aurora.state.auth import AuthState



def login():
    return rx.container(
        rx.container(height='150px'), 
        rx.vstack(           
            rx.heading(
                rx.text(
                    "Aurora",
                    style={
                        "fontSize": "40px",
                        "fontWeight": "bolder",
                        "letterSpacing": "5px",
                        "fontFamily": "Open Sans,Sans-serif",
                        "background": "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)",
                        "-webkit-background-clip": "text",
                        "color": "transparent",
                    },
                    center_content=True,
                ),
                display="flex",
                flex_direction="column",
                align_items="center",
                text_align="center",
            ),
            rx.text(
                "Create a picture with your story!",
                color="gray.500",
                font_weight="medium",
            ),
            rx.container(
                rx.container(height='30px'),
                rx.image(
                    src="C:/Users/a/Desktop/vscodeGithub/aurora/assets/favicon.ico",
                    alt="star",
                    style={"width": "100px", "height": "100px"},
                ),
                center_content=True,
            ),
            rx.container(
                rx.vstack(
                    rx.container(
                        rx.input(placeholder="Username", on_blur=AuthState.set_username, mb=4),
                        rx.input(
                            type_="password",
                            placeholder="Password",
                            on_blur=AuthState.set_password,
                            mb=4,
                        ),
                        rx.button(
                            "Log in",
                            on_click=AuthState.login,
                            bg="blue.500",
                            color="white",
                            _hover={"bg": "blue.600"},
                        ),
                        center_content=True,
                        align_items="left",
                        bg="white",
                        border="1px solid #eaeaea",
                        p=4,
                        max_width="400px",
                        border_radius="lg",
                    ),
                    rx.container(height='10px'),
                    rx.text(
                        'Forgot your password?   ',
                        rx.link('Find Password!',href="/findpassword",color='green.500'),
                        color="gray.600",
                    ), 
                    rx.text(
                        "Don't have an account yet?   ",
                        rx.link("Sign up here!", href="/signup", color="blue.500"),
                        color="gray.600",
                    ),
                    rx.container(height='50px') ,  
                ),
            ),
            width='500px',
            height='auto',
            center_content=True,
            borderRadius='20px',
            boxShadow='9px 9px 100px #79d0ed',
            bg = "rgb(255 255 255)"
        ),
        center_content=True,
        # justifyContent='center',
        maxWidth='auto',
        maxHeight='auto',
        height='100vh',
        style={
            'background-image':"url('C:/Users/a/Desktop/vscodeGithub/aurora/assets/aurora.jpg')",
            'background-size':'cover',
        }
    )

