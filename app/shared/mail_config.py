from fastapi_mail import ConnectionConfig
import os

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "inkaperu.sac2025@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "dsst wwqj kqpj stiq"),
    MAIL_FROM="inkaperu.sac2025@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",

    MAIL_STARTTLS=True,  # reemplaza a MAIL_TLS
    MAIL_SSL_TLS=False,  # reemplaza a MAIL_SSL

    USE_CREDENTIALS=True,
)