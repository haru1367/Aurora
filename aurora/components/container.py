"""A container component."""
import reflex as rx


def container(*children, **props):
    # Enable override of default props.
    props = (
        dict(
        )
        |props
    )
    return rx.container(*children, **props)
