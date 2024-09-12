from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self) -> str:
        return self.nickname


class Transaction(Base):
    __tablename__ = "transactions"

    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    transaction_type: Mapped[str] = mapped_column(
        String(50), default="simple", nullable=True
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    user = relationship("User", back_populates="transactions", single_parent=True)
