import redis
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.dependencies.db_dependencies import create_get_db
from general_operator.dependencies.get_query_dependencies import CommonQuery
from sqlalchemy.orm import sessionmaker, Session

from function.API.API_common_rule import APICommonRuleOperate


class APICommonRuleRouter(APICommonRuleOperate):
    def __init__(self, module, redis_db: redis.Redis, influxdb: InfluxDB,
                 exc, db_session: sessionmaker):
        APICommonRuleOperate.__init__(self, module, redis_db, influxdb, exc)
        self.exc = exc
        self.db_session = db_session
        self.redis_db = redis_db
        self.influxdb = influxdb

    def create(self):
        router = APIRouter(
            prefix="/api/system_log/common_rule",
            tags=["common_rule"],
            dependencies=[],
        )
        create_schemas = self.create_schemas
        multiple_update_schemas = self.multiple_update_schemas

        @router.get("/", response_model=list[self.main_schemas])
        async def get_api_common_rules(common: CommonQuery = Depends(),
                                       db: Session = Depends(create_get_db(self.db_session))):
            if common.pattern == "all":
                common_rules = self.common_rule_operate.read_all_data_from_redis()[common.skip:][:common.limit]
            else:
                id_set = self.common_rule_operate.execute_sql_where_command(db, common.where_command)
                common_rules = self.common_rule_operate.read_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return JSONResponse(content=common_rules)

        @router.post("/", response_model=list[self.main_schemas])
        async def create_api_common_rules(create_data_list: list[create_schemas],
                                          db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=self.create_common_rules(create_data_list, db))

        @router.patch("/", response_model=list[self.main_schemas])
        async def update_api_common_rules(update_data_list: list[multiple_update_schemas],
                                          db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=self.update_common_rules(update_data_list, db))

        @router.delete("/")
        async def delete_api_common_rules(id_set: set[int] = Query(...),
                                          db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                self.delete_common_rules(id_set, db)
                return JSONResponse(content="ok")

        return router
