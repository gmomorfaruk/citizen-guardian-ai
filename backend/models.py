import uuid
from datetime import datetime
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships to other data
    items: Mapped[list["Item"]] = relationship(back_populates="owner")
    documents: Mapped[list["Document"]] = relationship(back_populates="owner") # <-- ADD THIS


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str | None] = mapped_column(String)
    
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="items")


# --- ADD THIS NEW DOCUMENT MODEL ---
class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    unique_filename: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="documents")