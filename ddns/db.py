from typing import List
from sqlalchemy import String, MetaData, create_engine, select, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from datetime import datetime

from uuid import uuid4

from . import exceptions
from . import utils

import os
import logging


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

    subdomain_record: Mapped[str] = mapped_column(String(200), primary_key=True)
    identifier_token: Mapped[int] = mapped_column(
        String(utils.IDENTIFIER_TOKEN_LENGTH), 
        nullable=False, 
        unique=True
    )
    secret_token: Mapped[str] = mapped_column(
        String(utils.SECRET_TOKEN_LENGTH), 
        nullable=False
    )
    ip_address: Mapped[str] = mapped_column(String(100), default='')
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    last_updated: Mapped[datetime] = mapped_column(
        default=datetime.strptime('1970-01-01', '%Y-%m-%d')
    )

    def __repr__(self) -> str:
        return f'DDNS(subdomain={self.subdomain_record!r}, ip_address={self.ip_address!r})'


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DataHandler(metaclass=SingletonMeta):
    def __init__(self, database_name=os.getenv('DATABASE')):
        self.__engine = create_engine(f'sqlite:///{database_name}.sqlite')
        Base.metadata.create_all(self.__engine)

        logging.info(f'Initialized DB "{database_name}"')

    def __open_session(self) -> Session:
        return Session(self.__engine)
    
    def identifier_token_exists(self, api_token: str) -> bool:
        identifier_token, secret_token = utils.unpack_api_token(api_token)

        with self.__open_session() as session:
            query = session.query(
                DDNS.identifier_token
            ).filter(DDNS.identifier_token == identifier_token)

            return session.query(query.exists()).scalar()
    
    def subdomain_record_exists(self, subdomain_record: str) -> bool:
        with self.__open_session() as session:
            query = session.query(
                DDNS.subdomain_record
            ).filter(DDNS.subdomain_record == subdomain_record)

            return session.query(query.exists()).scalar()

    def create_new_record(
            self, 
            subdomain_record: str, 
            api_token=None
    ) -> str:
        if not api_token:
            api_token = utils.generate_full_token_pair()
        
        logging.debug(f'create_new_record(dns_record="{subdomain_record}", api_token="{api_token}")')

        identifier_token, secret_token = utils.unpack_api_token(api_token)
        hashed_secret_token = utils.hash_token(secret_token)

        if self.subdomain_record_exists(subdomain_record):
            full_domain_name = f'{subdomain_record}.{os.getenv("DOMAIN_NAME")}'
            raise exceptions.DNSRecordAlreadyExistsError(
                f'DNS record "{full_domain_name}" already exists.'
            )
        
        if self.identifier_token_exists(api_token):
            raise exceptions.IdentifierTokenAlreadyExistsError(
                f'Identifier token "{identifier_token}" already taken.'
            )
        
        with self.__open_session() as session:
            ddns = DDNS(
                subdomain_record=subdomain_record,
                identifier_token=identifier_token,
                secret_token=hashed_secret_token
            )

            session.add(ddns)
            session.commit()

            return api_token
        
    def get_bound_subdomain_record(self, api_token: str) -> str:
        identifier_token, secret_token = utils.unpack_api_token(api_token)

        if not self.identifier_token_exists(api_token):
            raise exceptions.IdentifierTokenNotFoundError(
                f'Identifier token "{identifier_token}" doesn\'t exist.'
            )

        with self.__open_session() as session:
            ddns_data = session.execute(
                select(DDNS)
                .filter_by(identifier_token=identifier_token)
            ).scalar_one()

            if utils.compare_hashed_token(
                token=secret_token,
                hashed_token=ddns_data.secret_token
            ):
                return ddns_data.subdomain_record
            else:
                raise exceptions.SecretTokenIncorrectError(
                    f'Token pair "{api_token}" incorrect.'
                )
        
    def get_record_data(self, subdomain_record: str) -> DDNS:
        with self.__open_session() as session:
            ddns_data = session.execute(
                select(DDNS)
                .filter_by(subdomain_record=subdomain_record)
            ).scalar_one()

            return ddns_data
    
    def update_record_ip_address(self, subdomain_record: str, ip_address: str):
        if not self.subdomain_record_exists(subdomain_record):
            full_domain_name = f'{subdomain_record}.{os.getenv("DOMAIN_NAME")}'
            raise exceptions.DNSRecordNotFoundError(
                f'DNS record "{full_domain_name}" doesn\'t exist.'
            )
        
        with self.__open_session() as session:
            ddns_data = session.execute(
                select(DDNS).
                filter_by(subdomain_record=subdomain_record)
            ).scalar_one()

            ddns_data.ip_address = ip_address
            ddns_data.last_updated = datetime.now()

            session.commit()

    def update_record_api_token(self, subdomain_record: str, new_api_token=None) -> str:
        if not new_api_token:
            new_api_token = utils.generate_full_token_pair()
        
        identifier_token, secret_token = utils.unpack_api_token(new_api_token)
        hashed_secret_token = utils.hash_token(secret_token)

        if not self.subdomain_record_exists(subdomain_record):
            full_domain_name = f'{subdomain_record}.{os.getenv("DOMAIN_NAME")}'
            raise exceptions.DNSRecordNotFoundError(
                f'DNS record "{full_domain_name}" doesn\'t exist.'
            )
        
        with self.__open_session() as session:
            ddns_data = session.execute(
                select(DDNS).
                filter_by(subdomain_record=subdomain_record)
            ).scalar_one()

            ddns_data.identifier_token = identifier_token
            ddns_data.secret_token = hashed_secret_token
            ddns_data.last_updated = datetime.now()

            session.commit()
        
        return new_api_token
        