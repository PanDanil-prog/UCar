from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
import enum

from core.database import Base


class IncidentStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSource(enum.Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"


class IncidentModel(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, default=IncidentStatus.OPEN.value)
    source = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, **kwargs):
        # Преобразуем Enum в строки при инициализации
        if 'source' in kwargs and isinstance(kwargs['source'], IncidentSource):
            kwargs['source'] = kwargs['source'].value
        if 'status' in kwargs and isinstance(kwargs['status'], IncidentStatus):
            kwargs['status'] = kwargs['status'].value
        super().__init__(**kwargs)