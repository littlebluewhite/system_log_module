from app.SQL import models
from schemas.API import API_url

redis_tables = []

sql_model = models.Url
main_schemas = API_url.APIUrl
create_schemas = API_url.APIUrlCreate
update_schemas = API_url.APIUrlUpdate
multiple_update_schemas = API_url.APIUrlMultipleUpdate

reload_related_redis_tables = {}
