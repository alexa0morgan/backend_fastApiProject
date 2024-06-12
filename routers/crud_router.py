from fastapi import APIRouter, Depends

from services.auth_service import AuthService


def create_crud_router(
        create_model: type,
        response_model: type,
        update_model: type,
        query_model: type,
        service_type: type,
        ignore_create: bool = False,
        ignore_read: bool = False,
        ignore_update: bool = False,
        ignore_delete: bool = False
):
    router = APIRouter()

    if not ignore_create:
        @router.post("/create", response_model=response_model)
        def create(
                _: AuthService.CurrentAdminUser,
                data: create_model,
                service: service_type = Depends()
        ):
            return service.create(data)

    if not ignore_read:
        @router.get("/", response_model=list[response_model])
        def read(
                _: AuthService.CurrentAdminUser,
                query: query_model = Depends(),
                service: service_type = Depends()
        ):
            return service.read(query)

    if not ignore_update:
        @router.patch("/update/{model_id}", response_model=response_model)
        def update(
                _: AuthService.CurrentAdminUser,
                model_id: int,
                data: update_model,
                service: service_type = Depends()
        ):
            return service.update(model_id, data)

    if not ignore_delete:
        @router.delete("/delete/{model_id}")
        def delete(
                _: AuthService.CurrentAdminUser,
                model_id: int,
                service: service_type = Depends()
        ):
            return service.delete(model_id)

    return router
