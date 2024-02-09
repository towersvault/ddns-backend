from typing import List
from sqlalchemy import String, MetaData, create_engine, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from datetime import datetime

from uuid import uuid4

from . import exceptions

import os


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s'
    })


class DDNS(Base):
    __tablename__ = 'ddns'

    dns_record: Mapped[str] = mapped_column(String(200), primary_key=True)
    api_token: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    ip_address: Mapped[str] = mapped_column(String(100), default='')
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    last_updated: Mapped[datetime] = mapped_column(
        default=datetime.strptime('1970-01-01', '%Y-%m-%d')
    )

    def __repr__(self) -> str:
        return f'DDNS(dns_record={self.dns_record!r}, ip_address={self.ip_address!r})'


class DataHandler:
    def __init__(self, database=os.getenv('DATABASE')):
        self.__engine = create_engine(f'sqlite:///{database}.sqlite')
        Base.metadata.create_all(self.__engine)

    def __open_session(self) -> Session:
        return Session(self.__engine)
    
    def api_token_exists(self, api_token: str) -> bool:
        with self.__open_session() as session:
            query = session.query(
                DDNS.api_token
            ).filter(DDNS.api_token == api_token)

            return session.query(query.exists()).scalar()
    
    def dns_record_exists(self, dns_record: str) -> bool:
        with self.__open_session() as session:
            query = session.query(
                DDNS.dns_record
            ).filter(DDNS.dns_record == dns_record)

            return session.query(query.exists()).scalar()

    def create_new_record(self, dns_record: str, api_token=str(uuid4())) -> str:
        if self.dns_record_exists(dns_record):
            raise exceptions.DNSRecordAlreadyExistsError(
                f'DNS record "{dns_record}" already exists.'
            )
        
        if self.api_token_exists(api_token):
            raise exceptions.APITokenAlreadyExistsError(
                f'API token "{api_token}" already taken.'
            )
        
        with self.__open_session() as session:
            ddns = DDNS(
                dns_record=dns_record,
                api_token=api_token
            )

            session.add(ddns)
            session.commit()

            return api_token
        
    def get_record_data(self, dns_record: str) -> DDNS:
        with self.__open_session() as session:
            statement = select(
                DDNS
            ).where(
                DDNS.dns_record == dns_record
            )

            return session.scalar(statement)
    
    def update_record(self, api_token: str, ip_address: str):
        if not self.api_token_exists(api_token):
            raise exceptions.APITokenNotFoundError(
                f'API token "{api_token}" doesn\'t exist.'
            )
        
        with self.__open_session() as session:
            ddns_data = session.execute(
                select(DDNS).
                filter_by(api_token=api_token)
            ).scalar_one()

            ddns_data.ip_address = ip_address

            session.commit()
        
