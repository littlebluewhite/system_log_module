from typing import Annotated

import redis
from fastapi import APIRouter, Depends, Query
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.dependencies.db_dependencies import create_get_db
from sqlalchemy.orm import sessionmaker, Session
from starlette.responses import JSONResponse

from function.API.API_log import APILogOperate


class APILogRouter(APILogOperate):
    def __init__(self, module, redis_db:redis.Redis, influxdb: InfluxDB, exc,
                 db_session: sessionmaker):
        self.db_session = db_session
        APILogOperate.__init__(self, module, redis_db, influxdb, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/log",
            tags=["API", "log"],
            dependencies=[],
        )

        main_schemas = self.main_schemas
        create_schemas = self.create_schemas

        @router.get("/", response_model=list[main_schemas])
        async def get_logs(start: Annotated[str, Query()] = ...,
                           stop: Annotated[str | None, Query()] = "",
                           modules: Annotated[list[str] | None, Query()] = None,
                           submodule: Annotated[str | None, Query()] = "",
                           item: Annotated[str | None, Query()] = "",
                           methods: Annotated[list[str] | None, Query()] = None,
                           status_code: Annotated[str | None, Query()] = "",
                           message_code: Annotated[str | None, Query()] = "",
                           account: Annotated[str | None, Query()] = "",
                           ip: Annotated[str | None, Query()] = ""):
            return JSONResponse(content=self.get_logs(start, stop, modules, submodule, item, methods,
                                 status_code, message_code, account, ip))

        @router.post("/")
        async def create_logs(log: create_schemas,
                              db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                self.create_logs(log, db)
                return JSONResponse(content="ok")

        return router
