#Eduardo Ramos
from pydantic import BaseModel

class Cliente(BaseModel):   # The attributes that were set None are optional
    id_cliente: int = None
    nome: str
    cpf: str
    telefone: str