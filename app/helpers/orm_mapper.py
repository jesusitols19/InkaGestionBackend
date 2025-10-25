def to_entity(model, entity_class):
    fields = entity_class.__dataclass_fields__.keys()
    data = {f: getattr(model, f) for f in fields if hasattr(model, f)}
    return entity_class(**data)


def to_model(entity, model_class):
    columns = model_class.__table__.columns.keys()
    data = {c: getattr(entity, c) for c in columns if hasattr(entity, c)}
    return model_class(**data)