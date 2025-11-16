from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserUpdate, UserCreateModerator, UserImageUpdate
from app.core.security import hash_password
from fastapi import HTTPException


class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return UserRepository.get_user_by_email(db, email)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return UserRepository.get_user_by_id(db, user_id)

    @staticmethod
    def update_user(db: Session, current_user: User, user_data: UserUpdate) -> User:
        # Pydantic v2: model_dump(exclude_unset=True) pega apenas campos enviados
        updates = user_data.model_dump(exclude_unset=True)

        # Se não houver campos para atualizar, devolve o usuário atual (ou levante 400)
        if not updates:
            return current_user

        # Se email for alterado, verificar duplicidade
        if "email" in updates and updates["email"] != current_user.email:
            existing_user = (
                db.query(User).filter(User.email == updates["email"]).first()
            )
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")

        # Se senha foi fornecida, hashear antes de salvar
        if "password" in updates and updates["password"]:
            updates["password"] = hash_password(updates["password"])

        return UserRepository.update_user(db, current_user.id, updates)

    @staticmethod
    def delete_user(db: Session, current_user: User):
        UserRepository.delete_user(db, current_user.id)

    @staticmethod
    def create_moderator(
        db: Session, user_data: UserCreateModerator, current_user: User
    ) -> User:
        if current_user.role.value != UserRole.ADMIN.value:
            raise HTTPException(
                status_code=403, detail="Not authorized to create a moderator"
            )

        existing_user = UserRepository.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data.password = hash_password(user_data.password)
        user = User(**user_data.model_dump(), admin_id=current_user.id)  # Salva o id do admin principal
        return UserRepository.create_user(db, user)

    @staticmethod
    def update_user_image(db: Session, current_user: User, user_image: UserImageUpdate) -> User:
        return UserRepository.update_user_image(db, current_user.id, user_image.image_path)
    
    @staticmethod
    def get_user_summary(db: Session, current_user: User) -> dict:
        # Exemplo: O ideal é consultar pedidos, favoritos, reviews, etc.
        # Aqui, retorna valores de exemplo
        return {
            "totalPedidos": db.query(User).filter(User.id == current_user.id).count(),  # Exemplo genérico
            "valorGasto": 0.0,  # Troque pela soma do valor dos pedidos
            "favoritos": 0,     # Troque pela contagem dos favoritos do usuário
            "reviews": 0        # Troque pela contagem dos reviews do usuário
        }
    
    @staticmethod
    def get_moderators(db: Session):
        return db.query(User).filter(User.role == UserRole.MODERATOR).all()
    
    @staticmethod
    def delete_user_by_id(db: Session, user_id: int) -> bool:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
             return False
         
        UserRepository.delete_user(db, user_id)
        return True     
    
    @staticmethod
    def delete_user_by_id(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True