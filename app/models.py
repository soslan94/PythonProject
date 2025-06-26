import enum
import sqlalchemy
from .db import metadata

class ColorEnum(enum.Enum):
    pink = "pink"
    black = "black"
    white = "white"
    yellow = "yellow"

class SizeEnum(enum.Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"
    xxl = "xxl"

users = sqlalchemy.Table(
    "users", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(120), unique=True, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("full_name", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("phone", sqlalchemy.String(13)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column(
        "last_modified_at", sqlalchemy.DateTime,
        nullable=False, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()
    ),
)

clothes = sqlalchemy.Table(
    "clothes", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("color", sqlalchemy.Enum(ColorEnum), nullable=False),
    sqlalchemy.Column("size", sqlalchemy.Enum(SizeEnum), nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(255)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column(
        "last_modified_at", sqlalchemy.DateTime,
        nullable=False, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()
    ),
)