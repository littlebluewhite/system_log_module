import schemas.url
from app.SQL import models

name = "url"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": name + "_module_submodule_item", "key": "module__submodule__item"},
]

sql_model = models.Url
main_schemas = schemas.url.Url
create_schemas = schemas.url.UrlCreate
update_schemas = schemas.url.UrlUpdate
multiple_update_schemas = schemas.url.UrlMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            # {"module": data.rule, "field": "url_id"}
        ],
    "self_field":
        []
}