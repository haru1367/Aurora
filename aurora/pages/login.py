"""Login page. Uses auth_layout to render UI shared with the sign up page."""
import reflex as rx
from aurora.state.auth import AuthState


def login():
    return rx.container(
        rx.container(height='200px'), 
        rx.vstack(           
            rx.heading(
                rx.span("Aurora!"),
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
                        align_items="left",
                        bg="white",
                        border="1px solid #eaeaea",
                        p=4,
                        max_width="400px",
                        border_radius="lg",
                    ),
                    rx.text(
                        "Don't have an account yet? ",
                        rx.link("Sign up here.", href="/signup", color="blue.500"),
                        color="gray.600",
                    ),            
                ),
            ),
            width='500px',
            height='auto',
            center_content=True,
            borderRadius='20px',
            boxShadow='9px 9px 50px #ceddf5',
        ),
        center_content=True,
        # justifyContent='center',
        maxWidth='auto',
        maxHeight='auto',
        height='100vh',
        style={
            'background-image': "url('favicon.ico')",
            'background-size': 'cover',
            'background-repeat': 'no-repeat',
        },
    )
