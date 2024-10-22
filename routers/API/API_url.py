import redis
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.dependencies.db_dependencies import create_get_db
from general_operator.dependencies.get_query_dependencies import CommonQuery
from sqlalchemy.orm import sessionmaker, Session

from function.API.API_url import APIUrlOperate


class APIUrlRouter(APIUrlOperate):
    def __init__(self, module, redis_db: redis.Redis, influxdb: InfluxDB,
                 exc, db_session: sessionmaker):
        APIUrlOperate.__init__(self, module, redis_db, influxdb, exc)
        self.exc = exc
        self.db_session = db_session
        self.redis_db = redis_db
        self.influxdb = influxdb

    def create(self):
        router = APIRouter(
            prefix="/api/url",
            tags=["API", "url"],
            dependencies=[],
        )
        create_schemas = self.create_schemas
        multiple_update_schemas = self.multiple_update_schemas

        @router.get("/", response_model=list[self.main_schemas])
        async def get_api_urls(common: CommonQuery = Depends(),
                               db: Session = Depends(create_get_db(self.db_session))):
            if common.pattern == "all":
                urls = self.url_operate.read_all_data_from_redis()[common.skip:][:common.limit]
            else:
                id_set = self.url_operate.execute_sql_where_command(db, common.where_command)
                urls = self.url_operate.read_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return JSONResponse(content=[self.format_api_url(url) for url in urls])

        @router.post("/", response_model=list[self.main_schemas])
        async def create_api_urls(create_data_list: list[create_schemas],
                                  db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=self.create_urls(create_data_list, db))

        @router.patch("/", response_model=list[self.main_schemas])
        async def update_api_urls(update_data_list: list[multiple_update_schemas],
                                  db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=self.update_urls(update_data_list, db))

        @router.delete("/")
        async def delete_api_urls(id_set: set[int] = Query(...),
                                  db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                self.delete_urls(id_set, db)
                return JSONResponse(content="ok")

        return router
