from sqlalchemy.orm import Session
from typing import List, Optional

from models.incident import IncidentModel, IncidentStatus, IncidentSource
from schemas.incident import IncidentCreate, IncidentUpdate


class IncidentService:
    @staticmethod
    def create_incident(
            database: Session,
            incident: IncidentCreate,
    ) -> IncidentModel:
        source_value = incident.source.value if hasattr(incident.source, 'value') else incident.source

        db_incident = IncidentModel(
            description=incident.description,
            source=source_value,
        )
        database.add(db_incident)
        database.commit()
        database.refresh(db_incident)
        return db_incident

    @staticmethod
    def get_incidents(
            database: Session,
            status: Optional[IncidentStatus] = None,
            skip: int = 0,
            limit: int = 100,
    ) -> List[IncidentModel]:
        query = database.query(IncidentModel)

        if status:
            # Преобразуем Enum в строку для фильтрации
            status_value = status.value if hasattr(status, 'value') else status
            query = query.filter(IncidentModel.status == status_value)

        return query.order_by(
            IncidentModel.created_at.desc()
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_incident_by_id(
            database: Session,
            incident_id: int,
    ) -> Optional[IncidentModel]:
        return database.query(IncidentModel).filter(
            IncidentModel.id == incident_id
        ).first()

    @staticmethod
    def update_incident(
            database: Session,
            incident_id: int,
            incident_update: IncidentUpdate,
    ) -> Optional[IncidentModel]:
        db_incident = database.query(IncidentModel).filter(
            IncidentModel.id == incident_id
        ).first()

        if not db_incident:
            return None

        update_data = incident_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if value and hasattr(value, 'value'):
                setattr(db_incident, field, value.value)
            else:
                setattr(db_incident, field, value)

        database.commit()
        database.refresh(db_incident)
        return db_incident

    @staticmethod
    def delete_incident(
            database: Session,
            incident_id: int,
    ) -> bool:
        incident = database.query(IncidentModel).filter(
            IncidentModel.id == incident_id
        ).first()

        if not incident:
            return False

        database.delete(incident)
        database.commit()
        return True