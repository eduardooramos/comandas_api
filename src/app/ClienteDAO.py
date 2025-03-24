#Eduardo Ramos
from fastapi import APIRouter
from domain.entities.Cliente import Cliente

# Security import
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

# Data persistence import
import db
from infra.orm.ClienteModel import ClienteDB

router = APIRouter(dependencies= [Depends(get_current_active_user)])

# Creating the routes/endpoints: GET, POST, PUT, DELETE

@router.get("/cliente/", tags=["Cliente"])  # List all
async def get_cliente():
    try:
        session = db.Session()

        #  Search all
        dados = session.query(ClienteDB).all()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/cliente/{id}", tags=["Cliente"])  # List one
async def get_cliente(id: int):
    try:
        session = db.Session()

        # Search with a filter
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).all()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/cliente/", tags=["Cliente"]) # Inserts a new 
async def post_cliente(corpo: Cliente):
    try:
        session = db.Session()
        # Creates a new object with the requisition data
        dados = ClienteDB(None, corpo.nome, corpo.cpf, corpo.telefone)
        session.add(dados)
        # session.flush()
        session.commit()

        return {"id": dados.id_cliente}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/cliente/{id}", tags=["Cliente"])  # Edits one
async def put_cliente(id: int, corpo: Cliente):
    try:
        session = db.Session()

        # Search the current data by id
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        # Updates the data based on the request body
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone

        session.add(dados)
        session.commit()

        return {"id": dados.id_cliente}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/cliente/{id}", tags=["Cliente"])   # Deletes one
async def delete_cliente(id: int):
    try:
        session = db.Session()
        # Search the current data by id
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        session.delete(dados)
        session.commit()

        return {"id": dados.id_cliente}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Checks if the entered CPF is already registered, returning the current data if already is
@router.get("/cliente/cpf/{cpf}", tags=["Cliente - Valida CPF"])
async def cpf_cliente(cpf: str):
    try:
        session = db.Session()

        # Search with filter, returning the registered data
        dados = session.query(ClienteDB).filter(ClienteDB.cpf == cpf).all()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close() 