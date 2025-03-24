#Eduardo Ramos
from pydantic import BaseModel

class Funcionario(BaseModel):   # The attributes that were set None are optional
    id_funcionario: int = None
    nome: str
    matricula: str
    cpf: str
    telefone: str = None
    grupo: int
    senha: str = None