"""Shared auth layout."""
import reflex as rx

from ..components import container


def auth_layout(*args):
    """The shared layout for the login and sign up pages."""
    return rx.container(
        rx.container(height='200px'),
        container(
            
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
            *args,
            width='500px',
            height='auto',
            center_content=True,
            borderRadius='20px',
            boxShadow='9px 9px 50px #ceddf5',
        ),
    )
