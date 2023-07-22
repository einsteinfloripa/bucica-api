from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.models.base_model import Base


class DonorModel(Base):
    __tablename__ = "Dados_Doador"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(name="nome", nullable=False)
    amount: Mapped[float] = mapped_column(name="quantidade", nullable=False)
    indication: Mapped[str] = mapped_column(name="indiacacao", nullable=False)
    created_at: Mapped[datetime] = mapped_column(name="criado_em", nullable=False, server_default=func.now())

