from general_operator.app.SQL.database import SQLDB
from general_operator.app.influxdb.influxdb import InfluxDB
from redis import Redis
from sqlalchemy.orm import sessionmaker

import data.API.API_log
from function.API.API_log import APILogOperate
from schemas.API.API_log import Log
from server.proto import system_log_pb2, system_log_pb2_grpc

class SystemLogService(system_log_pb2_grpc.SystemLogServiceServicer):
    def __init__(self, db: SQLDB, redis_db: Redis, influxdb: InfluxDB):
        self.db_session: sessionmaker = db.new_db_session()
        self.api_log_operate = APILogOperate(data.API.API_log, redis_db, influxdb, db)
    async def WriteLog(self, request, context):
        log_create = Log(
            timestamp=request.timestamp,
            module=request.module,
            submodule=request.submodule,
            item=request.item,
            method=request.method,
            status_code=request.status_code,
            message_code=request.message_code,
            message=request.message,
            response_size=request.response_size,
            account=request.account,
            ip=request.ip,
            api_url=request.api_url,
            query_params=request.query_params,
            web_path=request.web_path
        )
        print("receive request: ", log_create)
        db = self.db_session()
        with db.begin():
            self.api_log_operate.create_log(log_create, db)
        result = system_log_pb2.LogResponse(
            message="success"
        )
        return result
