from database.enums.enums import UserRole
from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, Uuid, text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_type_id: Mapped[int] = mapped_column(ForeignKey('event_types.id'), nullable=False)
    event_name: Mapped[str | None] = mapped_column(String(64))
    instrument_id: Mapped[int | None] = mapped_column(ForeignKey('instruments.id'))
    reagent_id: Mapped[int | None] = mapped_column(ForeignKey('reagents.id'))
    event_start_date: Mapped[str] = mapped_column(String(64), nullable=False)
    event_end_date: Mapped[str] = mapped_column(String(64), nullable=False)
    time_start: Mapped[str | None] = mapped_column(String(64))
    time_end: Mapped[str | None] = mapped_column(String(64))
    is_there_time: Mapped[bool] = mapped_column(Boolean, default=True)

    event_type: Mapped['EventType'] = relationship('EventType', back_populates='events')
    instrument: Mapped['Instrument'] = relationship('Instrument', back_populates='events')
    reagent: Mapped['Reagent'] = relationship('Reagent', back_populates='events')


class EventType(Base):
    __tablename__ = 'event_types'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)

    events: Mapped[list[Event]] = relationship('Event', back_populates='event_type')


class Reagent(Base):
    __tablename__ = 'reagents'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    instrument_id: Mapped[int] = mapped_column(ForeignKey('instruments.id'), nullable=False)
    run_duration: Mapped[int] = mapped_column(Integer, nullable=False)

    instrument: Mapped['Instrument'] = relationship('Instrument', back_populates='reagents')
    events: Mapped[list[Event]] = relationship('Event', back_populates='reagent')


class Instrument(Base):
    __tablename__ = 'instruments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)

    events: Mapped[list[Event]] = relationship('Event', back_populates='instrument')
    reagents: Mapped[list[Reagent]] = relationship('Reagent', back_populates='instrument')

class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(64))
    username: Mapped[str | None] = mapped_column(String(64))
    user_role: Mapped['UserRole'] = mapped_column(default=UserRole.UNKNOWN, nullable=False)
    