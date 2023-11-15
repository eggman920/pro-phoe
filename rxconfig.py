import reflex as rx
from pydynamodb import connect

a = connect(aws_access_key_id="AKIAWSY7AU74O3NS7X6W",
                aws_secret_access_key="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",
                region_name="us-east-1")

config = rx.Config(
    app_name="reflexprod",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)