from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.tag_schema import TagCreate, TagResponse, TagUpdate
from app.services.tag_service import TagService
from app.dependencies.auth import is_moderator
from app.schemas.product_schema import ProductResponse

router = APIRouter()


@router.get(
    "/",
    response_model=list[TagResponse],
    summary="Obter todas as tags",
    description="Retorna uma lista contendo todas as tags disponíveis no sistema.",
)
def get_tags(db: Session = Depends(get_db)):
    return TagService.get_all_tags(db)


@router.get(
    "/{tag_id}",
    response_model=TagResponse,
    summary="Obter uma tag específica",
    description="Retorna detalhes de uma tag específica com base no seu ID.",
    responses={404: {"description": "Tag não encontrada"}},
)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = TagService.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    return tag


@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova tag",
    description="Cria um novo tag. Requer privilégios de moderador.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return TagService.create_tag(db, tag_data)


@router.put(
    "/{tag_id}",
    response_model=TagResponse,
    summary="Atualizar uma tag",
    description="Atualiza informações de uma tag específica com base no seu ID. Requer privilégios de moderador.",
    responses={
        404: {"description": "Tag não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return TagService.update_tag(db, tag_id, tag_data)


@router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir uma tag",
    description="Exclui um tag específica com base no seu ID. Requer privilégios de moderador.",
    responses={
        404: {"description": "Tag não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    TagService.delete_tag(db, tag_id)

@router.post(
    "/{tag_id}/products/{product_id}",
    response_model=list[ProductResponse],
    summary="Adicionar um produto ao tag",
    description="Adiciona um produto específico ao tag.",
)
def add_product_to_tag(
    tag_id: int,
    product_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return TagService.add_product_to_tag(db, tag_id, product_id)

@router.delete(
    "/{tag_id}/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um produto do tag",
    description="Remove um produto específico do tag.",
)
def remove_product_from_tag(
    tag_id: int,
    product_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return TagService.remove_product_from_tag(db, tag_id, product_id)