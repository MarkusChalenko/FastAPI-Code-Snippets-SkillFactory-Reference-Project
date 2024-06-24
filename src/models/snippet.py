from datetime import datetime

from sqlalchemy import String, Column, Integer, TIMESTAMP

from .base import Base


class CodeSnippet(Base):
    __tablename__ = "code_snippet"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    language = Column(String(32), nullable=False)
    code = Column(String(2048), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Добавить связь с пользователем
