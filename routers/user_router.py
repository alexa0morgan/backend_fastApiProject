from models.user_model import UserResponse, UserCreate, UserUpdate, UserQuery
from routers.crud_router import create_crud_router
from services.auth_service import AuthService
from services.user_service import UserService

router = create_crud_router(
    create_model=UserCreate,
    response_model=UserResponse,
    update_model=UserUpdate,
    query_model=UserQuery,
    service_type=UserService
)


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: AuthService.CurrentUser):
    return current_user
