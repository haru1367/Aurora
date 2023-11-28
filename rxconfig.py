import reflex as rx

# "oracle://hr:hr@163.152.224.145:1521/aurora"
# "sqlite:///reflex.db",
config = rx.Config(
    app_name="aurora",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
