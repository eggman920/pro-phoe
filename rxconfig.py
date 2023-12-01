import reflex as rx

config = rx.Config(
    app_name="reflexprod",
    api_url="http://34.203.233.228:8000",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
