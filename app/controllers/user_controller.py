from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserResponse, UserUpdate, UserCreateModerator
from app.services.user_service import UserService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obter dados do usuário autenticado",
    description="Retorna os dados do usuário atualmente autenticado.",
)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Atualizar dados do usuário autenticado",
    description="Atualiza as informações do usuário atualmente autenticado.",
)
def update_me(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserService.update_user(db, current_user, user_data)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir conta do usuário autenticado",
    description="Exclui permanentemente a conta do usuário atualmente autenticado.",
)
def delete_me(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    UserService.delete_user(db, current_user)
    return


@router.post(
    "/create-moderator",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um usuário moderador",
    description="Cria uma nova conta com privilégios de moderador. Apenas usuários administradores podem realizar essa operação.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def create_moderator(
    user_data: UserCreateModerator,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserService.create_moderator(db, user_data, current_user)
