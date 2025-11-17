from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_database
from schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
    IncidentStatus,
)
from services.incident_service import IncidentService


router = APIRouter()


@router.post(
    "/",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать инцидент",
)
async def create_incident(
    incident: IncidentCreate,
    database: Session = Depends(get_database),
):
    """
    Создать новый инцидент

    - **description**: Описание инцидента
    - **source**: Источник инцидента (operator/monitoring/partner)
    """
    return IncidentService.create_incident(database, incident)


@router.get(
    "/",
    response_model=List[IncidentResponse],
    summary="Получить список инцидентов",
)
async def get_incidents(
    status: Optional[IncidentStatus] = Query(None, description="Фильтр по статусу"),
    skip: int = Query(0, ge=0, description="Пропустить записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    database: Session = Depends(get_database),
):
    """
    Получить список инцидентов с возможностью фильтрации по статусу
    """
    return IncidentService.get_incidents(database, status, skip, limit)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
    summary="Получить инцидент по ID",
)
async def get_incident(
    incident_id: int,
    database: Session = Depends(get_database),
):
    """
    Получить инцидент по его ID
    """
    incident = IncidentService.get_incident_by_id(database, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Инцидент не найден",
        )
    return incident


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
    summary="Обновить статус инцидента",
)
async def update_incident_status(
    incident_id: int,
    incident_update: IncidentUpdate,
    database: Session = Depends(get_database),
):
    """
    Обновить статус инцидента по ID

    - **status**: Новый статус инцидента
    - **description**: Новое описание (опционально)
    """
    incident = IncidentService.update_incident(
        database, incident_id, incident_update
    )
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Инцидент не найден",
        )
    return incident


@router.delete(
    "/{incident_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить инцидент",
)
async def delete_incident(
    incident_id: int,
    database: Session = Depends(get_database),
):
    """
    Удалить инцидент по ID
    """
    success = IncidentService.delete_incident(database, incident_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Инцидент не найден",
        )