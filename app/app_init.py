from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from general_operator.app.SQL.database import SQLDB
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.app.redis_db.redis_db import RedisDB
from general_operator.function.exception import GeneralOperatorException
from general_operator.routers.General_table_router import GeneralRouter
from redis.client import Redis
import data.rule, data.url
import data.API.API_url
import data.API.API_log
from app.SQL import models
from function.config_manager import ConfigManager
from routers.API.API_log import APILogRouter
from routers.API.API_url import APIUrlRouter

# from fastapi.security.api_key import APIKeyHeader

from version import version


def mount_config(conf_path: str = None):
    ns = ConfigManager.parse_cli_args()
    file = ns.config_path if ns.config_path else conf_path
    config = ConfigManager.read_config(file)
    return config


def create_connection(config):
    redis_db = RedisDB(config.redis.to_dict()).redis_client()
    db = SQLDB(config.sql.to_dict())
    models.Base.metadata.create_all(bind=db.get_engine())
    influxdb = InfluxDB(config.influxdb.to_dict())
    return db, redis_db, influxdb


def create_app(db: SQLDB, redis_db: Redis, influxdb: InfluxDB):
    app = FastAPI(title="system_log", version=version)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    db_session = db.new_db_session()

    app.include_router(APIUrlRouter(data.API.API_url, redis_db, influxdb,
                                    GeneralOperatorException, db_session).create())
    app.include_router(APILogRouter(data.API.API_log, redis_db, influxdb,
                                    GeneralOperatorException, db_session).create())
    app.include_router(GeneralRouter(data.url, redis_db, influxdb,
                                     GeneralOperatorException, db_session).create())
    app.include_router(GeneralRouter(data.rule, redis_db, influxdb,
                                     GeneralOperatorException, db_session).create())

    @app.exception_handler(GeneralOperatorException)
    async def unicorn_exception_handler(request: Request, exc: GeneralOperatorException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": f"{exc.detail}"},
        )

    @app.get("/exception")
    async def test_exception():
        raise GeneralOperatorException(status_code=423, detail="test exception")

    return app
