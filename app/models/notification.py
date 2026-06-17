from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    message = Column(String, nullable=False)

    channel = Column(String, nullable=False)

    status = Column(String, nullable=False, default="PENDING")

    created_at = Column(DateTime, default=datetime.utcnow)

    sent_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    recipient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    sender = relationship(
        "User",
        foreign_keys=[sent_by],
        back_populates="sent_notifications"
    )

    recipient = relationship(
        "User",
        foreign_keys=[recipient_id],
        back_populates="received_notifications"
    )