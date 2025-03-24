#Eduardo Ramos
from fastapi import APIRouter
from domain.entities.Funcionario import Funcionario

# Security import
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

# Data persistence import
import db
from infra.orm.FuncionarioModel import FuncionarioDB

router = APIRouter(dependencies= [Depends(get_current_active_user)])

# Creating the routes/endpoints: GET, POST, PUT, DELETE

@router.get("/funcionario/", tags=["Funcionário"])  # List all
async def get_funcionario():
    try:
        session = db.Session()

        #  Search all
        dados = session.query(FuncionarioDB).all()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/{id}", tags=["Funcionário"])  # List one
async def get_funcionario(id: int):
    try:
        session = db.Session()

        # Search with a filter
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).all()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/funcionario/", tags=["Funcionário"]) # Inserts a new 
async def post_funcionario(corpo: Funcionario):
    try:
        session = db.Session()
        # Creates a new object with the requisition data
        dados = FuncionarioDB(None, corpo.nome, corpo.matricula, corpo.cpf, corpo.telefone, corpo.grupo, corpo.senha)
        session.add(dados)
        # session.flush()
        session.commit()

        return {"id": dados.id_funcionario}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/funcionario/{id}", tags=["Funcionário"])  # Edits one
async def put_funcionario(id: int, corpo: Funcionario):
    try:
        session = db.Session()

        # Search the current data by id
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        # Updates the data based on the request body
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        dados.senha = corpo.senha
        dados.matricula = corpo.matricula
        dados.grupo = corpo.grupo

        session.add(dados)
        session.commit()

        return {"id": dados.id_funcionario}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/funcionario/{id}", tags=["Funcionário"])   # Deletes one
async def delete_funcionario(id: int):
    try:
        session = db.Session()
        # Search the current data by id
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        session.delete(dados)
        session.commit()

        return {"id": dados.id_funcionario}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Validates the cpf and password entered by the user
@router.post("/funcionario/login/", tags=["Funcionario - Login"])
async def login_funcionario(corpo: Funcionario):
    try:
        session = db.Session()

        # one(), requires that there's only one result in the result set
        # it's an error if the database returns 0, 2 or more results and an exception will be generated
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == corpo.cpf).filter(FuncionarioDB.senha == corpo.senha).one()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Checks if the entered CPF is already registered, returning the current data if already is
@router.get("/funcionario/cpf/{cpf}", tags=["Funcionário - Valida CPF"])
async def cpf_funcionario(cpf: str):
    try:
        session = db.Session()

        # Search with filter, returning the registered data
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == cpf).all()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close() 