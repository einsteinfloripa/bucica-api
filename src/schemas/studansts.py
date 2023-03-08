from datetime import datetime

from utils.base_schemas import BaseUniqueItem


class StudantItem(BaseUniqueItem):
    name: str = ""
    cpf: str = ""
    email: str = ""
    phone: str = ""
    attendance: datetime = datetime.now()
