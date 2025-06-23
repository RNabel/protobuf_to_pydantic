from pydantic import AliasGenerator, BaseModel, ConfigDict

from pydantic.alias_generators import to_camel


class MyBaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_camel,
        ),
        populate_by_name=True,
    )


base_model_class = MyBaseSchema
