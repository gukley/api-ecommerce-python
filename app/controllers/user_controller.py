from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserResponse, UserUpdate, UserCreateModerator, UserImageUpdate
from app.services.user_service import UserService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User
from app.dependencies.user_image_form import user_image_form
from pydantic import BaseModel
from app.core.security import hash_password # Função para hashear senhas
from app.services.token_service import create_reset_token, verify_reset_token
from app.services.email_service import send_reset_email 


router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,  # Certifique-se que UserResponse inclui admin_id
    summary="Obter dados do usuário autenticado",
    description="Retorna os dados do usuário atualmente autenticado.",
)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    # O campo admin_id será retornado automaticamente se estiver no schema UserResponse
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
    created = UserService.create_moderator(db, user_data, current_user)
    if not created:
        raise HTTPException(status_code=500, detail="Erro ao criar moderador")
    return created

@router.put(
    "/image",
    response_model=UserResponse,
    summary="Atualizar imagem de perfil do usuário",
    description="Atualiza a imagem de perfil do usuário autenticado.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def update_user_image(
    user_image: UserImageUpdate = Depends(user_image_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserService.update_user_image(db, current_user, user_image)

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

@router.post(
    "/me/change-password",
    status_code=status.HTTP_200_OK,
    summary="Alterar senha do usuário autenticado",
    description="Permite ao usuário autenticado alterar sua senha.",
)
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = UserService.change_password(db, current_user, data.current_password, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Senha atual incorreta.")
    return {"detail": "Senha alterada com sucesso!"}

@router.get(
    "/me/summary",
    summary="Resumo do usuário",
    description="Retorna um resumo dos dados do usuário (total pedidos, valor gasto, favoritos, reviews).",
)
def user_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserService.get_user_summary(db, current_user)

@router.get(
    "/moderators",
    response_model=list[UserResponse],
    summary="Listar todos os moderadores",
    description="Retorna uma lista de todos os usuários com papel de moderador.",
)
def list_moderators(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mods = UserService.get_moderators(db)
    return mods if mods else []  # Retorna lista vazia se não houver moderadores

@router.get(
    "/admin/clients",
    summary="Listar todos os clientes com endereços",
    response_model=list[dict],  # Ou crie um schema específico se quiser tipar melhor
    description="Retorna todos os clientes e seus endereços.",
)
def get_admin_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Filtra apenas clientes (role == 'CLIENT' ou equivalente)
    clients = db.query(User).filter(User.role == "CLIENT").all()
    result = []
    for client in clients:
        addresses = []
        for addr in getattr(client, "addresses", []):
            addresses.append({
                "id": addr.id,
                "street": addr.street,
                "number": addr.number,
                "neighborhood": addr.bairro,  # campo bairro
                "city": addr.city,
                "state": addr.state,
                "cep": addr.zip
            })
        result.append({
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "addresses": addresses
        })
    return result

class ForgotPasswordRequest(BaseModel):
    email: str

@router.post(
    "/forgot-password",
    summary="Solicitar recuperação de senha",
    description="Envia um e-mail de recuperação de senha para o usuário.",
)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    token = create_reset_token(user.id)
    send_reset_email(user.email, token)
    return {"detail": "E-mail de recuperação enviado"}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post(
    "/reset-password",
    summary="Resetar senha do usuário",
    description="Permite ao usuário redefinir sua senha usando o token enviado por e-mail.",
)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    user_id = verify_reset_token(data.token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.password = hash_password(data.new_password)
    db.commit()
    return {"detail": "Senha redefinida com sucesso"}

# Observações e sugestões:

# 1. Não há endpoint para deletar/modificar usuários por ID (apenas /me)
#    - Para excluir um moderador (ou qualquer usuário) por ID, adicione um endpoint DELETE /users/{user_id}
#    - O erro 404 ocorre porque esse endpoint não existe.

# Exemplo de endpoint para deletar usuário por ID (apenas para admin):

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir usuário por ID",
    description="Exclui permanentemente um usuário pelo ID. Apenas administradores podem realizar essa operação.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
        404: {"description": "Usuário não encontrado"},
    },
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Corrija para comparar o valor do Enum, não chamar .upper()
    role = getattr(current_user.role, "value", current_user.role)
    if role != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir usuário por ID",
    description="Exclui permanentemente um usuário (moderador, cliente ou outro) pelo ID. Apenas administradores podem realizar essa operação.",
)
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verifica permissão (ADMIN)
    role = getattr(current_user.role, "value", current_user.role)
    if role != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado")

    # Chama o service
    deleted = UserService.delete_user_by_id(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return

