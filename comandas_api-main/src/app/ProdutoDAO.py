#Eduardo Ramos
from fastapi import APIRouter
from domain.entities.Produto import Produto

# Security import
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

# Data persistence import
import db
from infra.orm.ProdutoModel import ProdutoDB

router = APIRouter(dependencies= [Depends(get_current_active_user)])

# Creating the routes/endpoints: GET, POST, PUT, DELETE

@router.get("/produto/", tags=["Produto"])  # List all
async def get_produto():
    try:
        session = db.Session()

        #  Search all
        dados = session.query(ProdutoDB).all()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/produto/{id}", tags=["Produto"])  # List one
async def get_produto(id: int):
    try:
        session = db.Session()

        # Search with a filter
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).all()

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/produto/", tags=["Produto"]) # Inserts a new 
async def post_produto(corpo: Produto):
    try:
        session = db.Session()
        # Creates a new object with the requisition data
        dados = ProdutoDB(None, corpo.nome, corpo.descricao, corpo.foto, corpo.valor_unitario)
        session.add(dados)
        # session.flush()
        session.commit()

        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/produto/{id}", tags=["Produto"])  # Edits one
async def put_produto(id: int, corpo: Produto):
    try:
        session = db.Session()

        # Search the current data by id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        # Updates the data based on the request body
        dados.nome = corpo.nome
        dados.descricao = corpo.descricao
        dados.foto = corpo.foto
        dados.valor_unitario = corpo.valor_unitario

        session.add(dados)
        session.commit()

        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/produto/{id}", tags=["Produto"])   # Deletes one
async def delete_produto(id: int):
    try:
        session = db.Session()
        # Search the current data by id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        session.delete(dados)
        session.commit()

        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()