"""Sign up page. Uses auth_layout to render UI shared with the login page."""
import reflex as rx
from aurora.state.auth import AuthState


def signup():
    """The sign up page."""
    return rx.container(
        rx.container(height='150px'),
        rx.vstack(
            rx.container(height='30px'),
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
            rx.container(
                rx.image(
                    src = "/Mosaic.ico",
                    width="100px",
                    height="100px",
                ),
                center_content=True,
            ),
            rx.container(height='10px'),
            rx.container(
                rx.input(placeholder="Username", on_blur=AuthState.set_username, mb=4),
                rx.input(
                    type_="password",
                    placeholder="Password",
                    on_blur=AuthState.set_password,
                    mb=4,
                ),
                rx.input(
                    type_="password",
                    placeholder="Confirm password",
                    on_blur=AuthState.set_confirm_password,
                    mb=4,
                ),
                rx.button(
                    "Sign up",
                    on_click=AuthState.signup,
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
            width='500px',
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
