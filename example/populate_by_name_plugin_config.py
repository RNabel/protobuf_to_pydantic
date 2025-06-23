from pydantic import AliasGenerator, BaseModel, ConfigDict

from pydantic.alias_generators import to_camel


class MyBaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_camel,
        ),
        populate_by_name=True,
        ser_json_inf_nan="strings",  # Serialize inf/-inf/nan as "Infinity"/"-Infinity"/"NaN"
    )


base_model_class = MyBaseSchema
