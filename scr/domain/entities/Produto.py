#Eduardo Ramos
from pydantic import BaseModel
from decimal import Decimal

class Produto(BaseModel):
    id_produto: int | None = None  # Pode ser None ao criar um novo produto
    nome: str
    descricao: str
    foto: bytes  # Para armazenar um BLOB
    valor_unitario: Decimal  # Corrigido para o tipo correto
