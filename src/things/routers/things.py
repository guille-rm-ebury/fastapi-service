from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.things.dependencies import get_things_service
from src.things.schemas.things import ThingCreate, ThingRead, ThingUpdate
from src.things.services.things import ThingsService

router = APIRouter(prefix="/things", tags=["things"])


@router.get(
    "/",
    response_model=list[ThingRead],
    summary="List all things",
    description="Returns a list of all things ordered by creation date.",
)
async def list_things(service: ThingsService = Depends(get_things_service)):
    return await service.get_all()


@router.get(
    "/{thing_id}",
    response_model=ThingRead,
    summary="Get a thing by ID",
    description="Returns a single thing by its UUID. Returns 404 if not found.",
    responses={404: {"description": "Thing not found"}},
)
async def get_thing(thing_id: UUID, service: ThingsService = Depends(get_things_service)):
    thing = await service.get_by_id(thing_id)
    if not thing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thing not found")
    return thing


@router.post(
    "/",
    response_model=ThingRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a thing",
    description="Creates a new thing with the given name and optional description.",
)
async def create_thing(payload: ThingCreate, service: ThingsService = Depends(get_things_service)):
    return await service.create(payload)


@router.put(
    "/{thing_id}",
    response_model=ThingRead,
    summary="Update a thing",
    description="Partially updates a thing by its UUID. Only provided fields are updated. Returns 404 if not found.",
    responses={404: {"description": "Thing not found"}},
)
async def update_thing(
    thing_id: UUID,
    payload: ThingUpdate,
    service: ThingsService = Depends(get_things_service),
):
    thing = await service.update(thing_id, payload)
    if not thing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thing not found")
    return thing


@router.delete(
    "/{thing_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a thing",
    description="Deletes a thing by its UUID. Returns 404 if not found.",
    responses={404: {"description": "Thing not found"}},
)
async def delete_thing(thing_id: UUID, service: ThingsService = Depends(get_things_service)):
    deleted = await service.delete(thing_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thing not found")
