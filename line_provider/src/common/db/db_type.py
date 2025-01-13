from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

title_non_nullable = Annotated[str, mapped_column(String(255), nullable=False)]
