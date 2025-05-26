from enum import Enum

from sqlalchemy import and_, asc, desc
from sqlalchemy.orm import Query

from app.schemas.common import T


class FilterFactory:
    """Convierte un schema de filtro a query SQLAlchemy."""

    class Order(Enum):
        asc = "asc"
        desc = "desc"

    @staticmethod
    def apply(query: Query, model: T, schema) -> Query:
        # Campos textuales
        if getattr(schema, "name", None):
            query = query.filter(model.name.ilike(f"%{schema.name}%"))
        if getattr(schema, "phone", None):
            query = query.filter(model.phone.ilike(f"%{schema.phone}%"))

        # Boolean
        if schema.completed is not None:
            query = query.filter(model.completed == schema.completed)

        # Rangos de fechas
        def range_filter(column, dr):
            if dr:
                if dr.gte:
                    query = query.filter(column >= dr.gte)
                if dr.lte:
                    query = query.filter(column <= dr.lte)
            return query

        query = range_filter(model.create_at, schema.created)
        query = range_filter(model.completed_at, schema.completed_date)

        # Orden
        order_col = getattr(model, schema.order_by, None)
        if order_col is not None:
            query = query.order_by(FilterFactory.ORDER_MAP[schema.order](order_col))

        return query
