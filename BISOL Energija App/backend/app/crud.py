from datetime import datetime
from decimal import Decimal
from typing import List
from sqlmodel import select, Session
from models.models import Customer, TimeSeries


def calculate_total_production_for_customer(time_series: List[TimeSeries]) -> tuple[Decimal, Decimal]:
    
    total_production_kwh = sum(ts.production_kwh for ts in time_series if ts.production_kwh is not None)
    total_production_cost = sum(
        ts.production_kwh * ts.sipx_price.price_eur_kwh
        for ts in time_series
        if ts.production_kwh is not None and ts.sipx_price
    )
    return total_production_kwh, total_production_cost


def calculate_total_consumption_for_customer(time_series: List[TimeSeries]) -> tuple[Decimal, Decimal]:
    
    total_consumption_kwh = sum(ts.consumption_kwh for ts in time_series if ts.consumption_kwh is not None)
    total_consumption_cost = sum(
        ts.consumption_kwh * ts.sipx_price.price_eur_kwh
        for ts in time_series
        if ts.consumption_kwh is not None and ts.sipx_price
    )
    return total_consumption_kwh, total_consumption_cost


def get_customer_by_id(customer_id: int, session: Session) -> Customer:
    
    return session.get(Customer, customer_id)


def get_total_production_for_customer(customer_id: int, session: Session) -> tuple[Decimal, Decimal]:
    
    time_series = find_all_timeseries_for_customer(customer_id, session)
    return calculate_total_production_for_customer(time_series)


def get_total_production_for_customer_in_timespan(customer_id: int, datetime_from: datetime, datetime_to: datetime, session: Session) -> tuple[Decimal, Decimal]:
    
    time_series = session.query(TimeSeries).filter(TimeSeries.customer_id == customer_id, TimeSeries.timestamp >= datetime_from, TimeSeries.timestamp <= datetime_to).all()
    return calculate_total_production_for_customer(time_series)


def get_total_consumption_for_customer(customer_id: int, session: Session) -> tuple[Decimal, Decimal]:
    
    time_series = find_all_timeseries_for_customer(customer_id, session)
    return calculate_total_consumption_for_customer(time_series)


def get_total_consumption_for_customer_in_timespan(customer_id: int, datetime_from: datetime, datetime_to: datetime, session: Session) -> tuple[Decimal, Decimal]:
    
    time_series = session.query(TimeSeries).filter(TimeSeries.customer_id == customer_id, TimeSeries.timestamp >= datetime_from, TimeSeries.timestamp <= datetime_to).all()
    return calculate_total_consumption_for_customer(time_series)


def get_overview_for_customer(customer_id: int, session: Session) -> List[dict]:
    
    time_series = find_all_timeseries_for_customer(customer_id, session)
    return [
        {
            "timestamp": ts.timestamp,
            "consumption_kwh": ts.consumption_kwh,
            "production_kwh": ts.production_kwh,
            "sipx_price": ts.sipx_price.price_eur_kwh if ts.sipx_price else None,
        }
        for ts in time_series
    ]


def get_overview_for_customer_in_timespan(customer_id: int, datetime_from: datetime, datetime_to: datetime, session: Session) -> List[dict]:
    
    time_series = session.query(TimeSeries).filter(TimeSeries.customer_id == customer_id, TimeSeries.timestamp >= datetime_from, TimeSeries.timestamp <= datetime_to).all()
    return [
        {
            "timestamp": ts.timestamp,
            "consumption_kwh": ts.consumption_kwh,
            "production_kwh": ts.production_kwh,
            "sipx_price": ts.sipx_price.price_eur_kwh if ts.sipx_price else None,
        }
        for ts in time_series
    ]

def find_all_timeseries_for_customer(customer_id: int, session: Session):
    
    return session.query(TimeSeries).filter(TimeSeries.customer_id == customer_id).all()

# def calculate_total_production_for_customer(time_series, session: Session) -> tuple[Decimal, Decimal]:
#     total_production_kwh = sum(ts.production_kwh for ts in time_series if ts.production_kwh is not None)
#     total_production_cost = sum(ts.production_kwh * ts.sipx_price.price_eur_kwh for ts in time_series if ts.production_kwh is not None)
#     return total_production_kwh, total_production_cost

# def calculate_total_consumption_for_customer(time_series, session: Session) -> tuple[Decimal, Decimal]:
#     total_consumption_kwh = sum(ts.consumption_kwh for ts in time_series if ts.consumption_kwh is not None)
#     total_consumption_cost = sum(ts.consumption_kwh * ts.sipx_price.price_eur_kwh for ts in time_series if ts.consumption_kwh is not None)
#     return total_consumption_kwh, total_consumption_cost

# def get_customer_by_id(customer_id: int, session: Session):
#     return session.query(Customer).filter(Customer.id == customer_id).first()

# def get_total_production_for_customer(customer_id: int, session: Session) -> tuple[Decimal, Decimal]:
#     time_series = find_all_timeseries_for_customer(customer_id, session)
#     total_production_kwh, total_production_cost = calculate_total_production_for_customer(customer_id, time_series, session)
#     return total_production_kwh, total_production_cost

# def get_total_production_for_customer_in_timespan(customer_id: int, datetime_from: datetime, datetime_to: datetime, session: Session) -> tuple[Decimal, Decimal]:
#     time_series = session.query(TimeSeries).filter(TimeSeries.customer_id == customer_id, TimeSeries.timestamp >= datetime_from, TimeSeries.timestamp <= datetime_to).all()
#     # total_production = session.query(TimeSeries.production_kwh).filter(TimeSeries.customer_id == customer_id, TimeSeries.timestamp >= datetime_from, TimeSeries.timestamp <= datetime_to).all()
#     # prices = session.query(TimeSeries.sipx_price.price_eur_kwh).filter(TimeSeries.customer_id == customer_id, TimeSeries.timestamp >= datetime_from, TimeSeries.timestamp <= datetime_to).all()
#     total_production_kwh, total_production_cost = calculate_total_production_for_customer(customer_id, time_series, session)
#     return total_production_kwh, total_production_cost

# def get_total_consumption_for_customer(customer_id: int, session: Session) -> tuple[Decimal, Decimal]:
#     time_series = find_all_timeseries_for_customer(customer_id, session)
#     total_consumption_kwh, total_consumption_cost = calculate_total_consumption_for_customer(customer_id, time_series, session)
#     return total_consumption_kwh, total_consumption_cost

# def get_total_consumption_for_customer_in_timespan(customer_id: int, datetime_from: datetime, datetime_to: datetime, session: Session) -> tuple[Decimal, Decimal]:
#     time_series = session.query(TimeSeries).filter(TimeSeries.customer_id == customer_id, TimeSeries.timestamp >= datetime_from, TimeSeries.timestamp <= datetime_to).all()
#     total_consumption_kwh, total_consumption_cost = calculate_total_consumption_for_customer(customer_id, time_series, session)
#     return total_consumption_kwh, total_consumption_cost
    
# def get_overview_for_customer(customer_id: int, session: Session):
#     ## return a list where you have consumption and production for each timestamp
#     time_series = find_all_timeseries_for_customer(customer_id, session)
#     overview = []
#     for ts in time_series:
#         overview.append({
#             "timestamp": ts.timestamp,
#             "consumption_kwh": ts.consumption_kwh,
#             "production_kwh": ts.production_kwh,
#             "sipx_price": ts.sipx_price.price_eur_kwh
#         })
#     return overview

# def get_overview_for_customer_in_timespan(customer_id: int, datetime_from: datetime, datetime_to: datetime, session: Session):
#     time_series = session.query(TimeSeries).filter(TimeSeries.customer_id == customer_id, TimeSeries.timestamp >= datetime_from, TimeSeries.timestamp <= datetime_to).all()
#     overview = []
#     for ts in time_series:
#         overview.append({
#             "timestamp": ts.timestamp,
#             "consumption_kwh": ts.consumption_kwh,
#             "production_kwh": ts.production_kwh,
#             "sipx_price": ts.sipx_price.price_eur_kwh
#         })
#     return overview

