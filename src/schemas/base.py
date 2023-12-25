from pydantic import BaseModel, RootModel

__all__ = (
    "CamelJsonModel",
    "CamelJsonOrmModel",
)


def to_camel(string: str) -> str:
    new_str = "".join(word.capitalize() for word in string.split("_"))
    return f"{new_str[0].lower()}{new_str[1:]}"


class CamelJsonModel(BaseModel):
    """Модель с поддержкой сериализаций в camelCase."""

    # Camel config settings.
    class Config:
        arbitrary_types_allowed = True
        # Camelize will give us camelCase field names for external usage (docs, client-side app, etc.)
        # while maintaining snake_case for internal usage.
        alias_generator = to_camel
        # Allow internal usage of snake_case field names.
        populate_by_name = True
        # Extra whitespace? Gross.
        str_strip_whitespace = True


class CamelJsonOrmModel(CamelJsonModel):
    """Модель с поддержкой ORM сериализаций данных."""

    class Config:
        from_attributes = True


class OrmRootModel(RootModel):
    """Модель с поддержкой ORM сериализаций данных."""

    class Config:
        from_attributes = True
