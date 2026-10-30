/*
 * ============================================================================
 * V.A.U.R.O.S. CANONICAL URO API HEADER  (auto-generated — do not edit by hand)
 * ----------------------------------------------------------------------------
 * THE FRACTAL URO MANDATE:
 *   1. Everything is a URO. Relationships are UROs. NTE states are UROs.
 *   2. Import ONLY from this library. NEVER reimplement URO/NTE/synapse/
 *      custody/receipt logic in a dock.
 *   3. Every URO gets, at genesis: URID identity, INAHASH seal, custody
 *      chain, and NTE state.
 *   4. Every inter-dock relationship is a Synapse Vector URO with
 *      per-topic trust. The synapse load is the COMBINATION of both
 *      endpoints' states (native crossed with current, shared).
 *   5. Genesis Trust: child = 100%, new = 0% (trust is earned).
 *   6. Async communication uses Receipt envelopes
 *      (FULFILLED / DEFERRED / INCAPABLE).
 * ============================================================================
 */

#ifndef VAUROS_URO_API_H
#define VAUROS_URO_API_H

/* --------------------------------------------------------------------------
 * MODULE: uro.core.urid
 * --------------------------------------------------------------------------
 *  URID - Universal Relationship IDentifier (256-bit identity).
 * -------------------------------------------------------------------------- */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* class URIDError(self, /, *args, **kwargs)
 *  Malformed or out-of-range URID.
 */

/* fn new_urid() -> 'URID'
 *  Convenience: create a fresh random URID.
 */

/* fn new_uuid() -> '_uuid.UUID'
 *  Generate a new random (UUIDv4) 128-bit UUID.
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.core.uro
 * --------------------------------------------------------------------------
 *  The core URO class - the universal relationship object.
 * -------------------------------------------------------------------------- */

/* class Any(self, /, *args, **kwargs)
 *  Special type indicating an unconstrained type.
 *
 *  - Any is compatible with every type.
 *  - Any assumed to have all methods.
 *  - All values assumed to be instances of Any.
 *
 *  Note that all the above statements are true from the point of view of
 *  static type checkers. At runtime, Any should not be used with instance
 *  checks.
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* class URO(self, urid1: 'URID', urid2: 'URID', payload: 'Any' = None, parent: "Optional['URO']" = None) -> 'None'
 *  A Universal Relationship Object: (source URID, identifier URID).
 *   method add_child(self, child: "'URO'") -> 'None'
 *    Attach a child URO.
 *   method add_path(self, path: 'Any') -> 'None'
 *    Attach a Path URO.
 *   method associate(self, association: 'Any') -> 'None'
 *    Attach an Association URO.
 *   method children_of(self) -> "Iterable['URO']"
 *    Yield all child UROs.
 *   method everything() -> "'URO'"
 *    The URO for an unbounded group (everything).
 *   method get_child(self, urid: 'URID') -> "Optional['URO']"
 *    Return a child URO by URID, or None.
 *   method link(self) -> 'bytes'
 *    Compute the 512-bit relationship link.
 *   method new(payload: 'Any' = None) -> "'URO'"
 *    Create a self-defined URO (URID1 == URID2).
 *   method nothing() -> "'URO'"
 *    The URO for the concept of nothing (0x0, 0x0).
 */

/* class UROStructureError(self, /, *args, **kwargs)
 *  Structural invariant violation.
 */

/* fn sha128(data: 'bytes') -> 'bytes'
 *  128-bit digest (SHA-256 truncated to 16 bytes).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.core.space
 * --------------------------------------------------------------------------
 *  UROSpace - the communal registry/graph of all UROs and relationships.
 * -------------------------------------------------------------------------- */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* class URO(self, urid1: 'URID', urid2: 'URID', payload: 'Any' = None, parent: "Optional['URO']" = None) -> 'None'
 *  A Universal Relationship Object: (source URID, identifier URID).
 *   method add_child(self, child: "'URO'") -> 'None'
 *    Attach a child URO.
 *   method add_path(self, path: 'Any') -> 'None'
 *    Attach a Path URO.
 *   method associate(self, association: 'Any') -> 'None'
 *    Attach an Association URO.
 *   method children_of(self) -> "Iterable['URO']"
 *    Yield all child UROs.
 *   method everything() -> "'URO'"
 *    The URO for an unbounded group (everything).
 *   method get_child(self, urid: 'URID') -> "Optional['URO']"
 *    Return a child URO by URID, or None.
 *   method link(self) -> 'bytes'
 *    Compute the 512-bit relationship link.
 *   method new(payload: 'Any' = None) -> "'URO'"
 *    Create a self-defined URO (URID1 == URID2).
 *   method nothing() -> "'URO'"
 *    The URO for the concept of nothing (0x0, 0x0).
 */

/* class UROSpace(self, name: 'str' = 'root') -> 'None'
 *  A shared space holding UROs and the relationships between them.
 *   method get(self, urid1: 'URID', urid2: 'URID') -> 'Optional[URO]'
 *    Look up an object URO by its two URIDs.
 *   method neighbors(self, uro: 'URO') -> 'List[URO]'
 *    Return UROs directly associated with the given URO.
 *   method objects(self) -> 'Iterable[URO]'
 *    Yield all object UROs.
 *   method register(self, uro: 'URO') -> 'URO'
 *    Register an object URO.
 *   method register_relationship(self, relationship_uro: 'URO') -> 'URO'
 *    Register a relationship URO by its 512-bit link.
 *   method relationship(self, link: 'bytes') -> 'Optional[URO]'
 *    Look up a relationship URO by its link bytes.
 *   method relationships(self) -> 'Iterable[URO]'
 *    Yield all relationship UROs.
 */

/* class UROStructureError(self, /, *args, **kwargs)
 *  Structural invariant violation.
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.base
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Base URO (Naked Foundation)
 *  INTENT: The minimal-but-complete URO atom. All richness is in separate
 *          enrichment UROs that expand outward from this seed.
 *  STANDARD: URO-STD-0001 S3
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class Any(self, /, *args, **kwargs)
 *  Special type indicating an unconstrained type.
 *
 *  - Any is compatible with every type.
 *  - Any assumed to have all methods.
 *  - All values assumed to be instances of Any.
 *
 *  Note that all the above statements are true from the point of view of
 *  static type checkers. At runtime, Any should not be used with instance
 *  checks.
 */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class BaseURO(self, /, **data: 'Any') -> 'None'
 *  The naked base URO. All richness is in separate enrichment UROs.
 *
 *  This is the seed from which the fractal structure expands.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal for this URO.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method genesis_trust_level(self) -> 'float'
 *    Get the initial trust level based on the Genesis Rule.
 *
 *    Child UROs start at 100% trust to parent.
 *    New (genesis) UROs start at 0% trust.
 *   method is_child(self) -> 'bool'
 *    Check if this URO is a child (has a parent_inahash).
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO with an INAHASH.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ConfigDict(self, /, *args, **kwargs)
 *  A TypedDict for configuring Pydantic behaviour.
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class OPARPhase(self, /, *args, **kwargs)
 *  OPAR lifecycle phases.
 */

/* class Quadrant(self, /, *args, **kwargs)
 *  URO classification quadrants.
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.nte.axes
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: NTE Axes (12-Axis Homeostatic System)
 *  INTENT: Define the 12 neurotransmitter axes that form the swarm's governance
 *          primitives. Each axis is a URO with its own lineage, custody, and state.
 *  STANDARD: URO-STD-0001 S10
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class Enum(self, *args, **kwds)
 *  Create a collection of name/value pairs.
 *
 *  Example enumeration:
 *
 *  >>> class Color(Enum):
 *  ...     RED = 1
 *  ...     BLUE = 2
 *  ...     GREEN = 3
 *
 *  Access them by:
 *
 *  - attribute access:
 *
 *    >>> Color.RED
 *    <Color.RED: 1>
 *
 *  - value lookup:
 *
 *    >>> Color(1)
 *    <Color.RED: 1>
 *
 *  - name lookup:
 *
 *    >>> Color['RED']
 *    <Color.RED: 1>
 *
 *  Enumerations can be iterated over, and know how many members they have:
 *
 *  >>> len(Color)
 *  3
 *
 *  >>> list(Color)
 *  [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
 *
 *  Methods can be added to enumerations, and members can have their own
 *  attributes -- see the documentation for details.
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class NTEAxis(self, *args, **kwds)
 *  The 12 neurotransmitter equivalences.
 */

/* class NTEAxisGovernance(self, /, **data: 'Any') -> 'None'
 *  Governance role and cross-talk for each NTE axis.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.nte.level
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: NTE Level URO (Per-Axis State)
 *  INTENT: A URO representing the level of a single NTE axis. Each level is its
 *          own URO with lineage, custody, and INAHASH.
 *  STANDARD: URO-STD-0001 S10.1
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ConfigDict(self, /, *args, **kwargs)
 *  A TypedDict for configuring Pydantic behaviour.
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class NTEAxis(self, *args, **kwds)
 *  The 12 neurotransmitter equivalences.
 */

/* class NTELevelURO(self, /, **data: 'Any') -> 'None'
 *  A URO representing the level of a single NTE axis.
 *
 *  This is a first-class URO with its own identity, lineage, and custody.
 *   method apply_delta(self, delta: 'float') -> 'None'
 *    Apply a delta to the level.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO.
 *   method set_level(self, new_level: 'float') -> 'None'
 *    Set the level and update timestamp.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.nte.state
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: NTE State URO (Collection of Levels)
 *  INTENT: A URO representing the complete NTE state (all 12 axes). This is the
 *          fast-path reference for checking emotional state.
 *  STANDARD: URO-STD-0001 S10.2
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ConfigDict(self, /, *args, **kwargs)
 *  A TypedDict for configuring Pydantic behaviour.
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class NTEAxis(self, *args, **kwds)
 *  The 12 neurotransmitter equivalences.
 */

/* class NTELevelURO(self, /, **data: 'Any') -> 'None'
 *  A URO representing the level of a single NTE axis.
 *
 *  This is a first-class URO with its own identity, lineage, and custody.
 *   method apply_delta(self, delta: 'float') -> 'None'
 *    Apply a delta to the level.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO.
 *   method set_level(self, new_level: 'float') -> 'None'
 *    Set the level and update timestamp.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class NTEStateURO(self, /, **data: 'Any') -> 'None'
 *  A URO representing the complete NTE state (all 12 axes).
 *
 *  This is the fast-path reference for checking emotional state.
 *  The per-axis UROs are the durable, auditable record.
 *   method apply_delta(self, axis: 'NTEAxis', delta: 'float') -> 'None'
 *    Apply a delta to a specific axis.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method get_dominant_axis(self) -> 'NTEAxis'
 *    Get the axis with the highest level.
 *   method get_level(self, axis: 'NTEAxis') -> 'float'
 *    Get the level for a specific axis.
 *   method is_balanced(self, threshold: 'float' = 15.0) -> 'bool'
 *    Check if all axes are within threshold of baseline (50).
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO.
 *   method set_level(self, axis: 'NTEAxis', level: 'float') -> 'None'
 *    Set the level for a specific axis.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.synapse.topic_trust
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Per-Topic Trust URO
 *  INTENT: Trust is per-relationship AND per-topic. Two UROs may have high trust
 *          on religion but low trust on politics. Each topic is its own URO.
 *  STANDARD: URO-STD-0001 S10.3
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ConfigDict(self, /, *args, **kwargs)
 *  A TypedDict for configuring Pydantic behaviour.
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class NTEAxis(self, *args, **kwds)
 *  The 12 neurotransmitter equivalences.
 */

/* class TopicTrustURO(self, /, **data: 'Any') -> 'None'
 *  Trust on a specific topic within a synapse.
 *
 *  Example: Aegis↔Chaos synapse has high trust on "security_analysis" topic
 *  but low trust on "resource_allocation" topic.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method update_trust(self, delta: 'float', nte_context: 'dict') -> 'None'
 *    Update trust based on outcome and NTE context.
 *
 *    Args:
 *        delta: Raw trust delta (positive = good outcome, negative = bad)
 *        nte_context: Current NTE state (modulates how much to update)
 *   method validate(value: 'Any') -> 'Self'
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.synapse.vector
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Synapse Vector URO
 *  INTENT: The emotional state between two UROs. NTE state is relational, not
 *          global. The Aegis↔Chaos synapse has its own oxytocin level, its own
 *          trust, its own emotional state - between Aegis and Chaos only.
 *  STANDARD: URO-STD-0001 S10.4
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ConfigDict(self, /, *args, **kwargs)
 *  A TypedDict for configuring Pydantic behaviour.
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class NTEAxis(self, *args, **kwds)
 *  The 12 neurotransmitter equivalences.
 */

/* class NTEStateURO(self, /, **data: 'Any') -> 'None'
 *  A URO representing the complete NTE state (all 12 axes).
 *
 *  This is the fast-path reference for checking emotional state.
 *  The per-axis UROs are the durable, auditable record.
 *   method apply_delta(self, axis: 'NTEAxis', delta: 'float') -> 'None'
 *    Apply a delta to a specific axis.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method get_dominant_axis(self) -> 'NTEAxis'
 *    Get the axis with the highest level.
 *   method get_level(self, axis: 'NTEAxis') -> 'float'
 *    Get the level for a specific axis.
 *   method is_balanced(self, threshold: 'float' = 15.0) -> 'bool'
 *    Check if all axes are within threshold of baseline (50).
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO.
 *   method set_level(self, axis: 'NTEAxis', level: 'float') -> 'None'
 *    Set the level for a specific axis.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class SynapseVectorURO(self, /, **data: 'Any') -> 'None'
 *  The emotional state between two UROs (a synapse).
 *
 *  NTE state is relational: the Aegis↔Chaos synapse has its own state,
 *  separate from Aegis↔Sentinel or Chaos↔Coordinator.
 *   method add_topic_trust(self, topic: 'str', initial_trust: 'float' = 0.0) -> 'TopicTrustURO'
 *    Add a new topic trust URO.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method genesis_trust_level(self) -> 'float'
 *    Get the initial trust level based on the Genesis Rule.
 *
 *    If both endpoints are children of trusted parents, start higher.
 *    Otherwise, start at 0% and earn through interaction.
 *   method get_success_rate(self) -> 'float'
 *    Get the success rate for this synapse.
 *   method get_topic_trust(self, topic: 'str') -> 'Optional[TopicTrustURO]'
 *    Get trust URO for a specific topic.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method record_use(self, success: 'bool') -> 'None'
 *    Record a use of this synapse.
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this synapse.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method update_topic_trust(self, topic: 'str', delta: 'float', nte_context: 'dict') -> 'None'
 *    Update trust on a specific topic.
 *   method validate(value: 'Any') -> 'Self'
 */

/* class TopicTrustURO(self, /, **data: 'Any') -> 'None'
 *  Trust on a specific topic within a synapse.
 *
 *  Example: Aegis↔Chaos synapse has high trust on "security_analysis" topic
 *  but low trust on "resource_allocation" topic.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method update_trust(self, delta: 'float', nte_context: 'dict') -> 'None'
 *    Update trust based on outcome and NTE context.
 *
 *    Args:
 *        delta: Raw trust delta (positive = good outcome, negative = bad)
 *        nte_context: Current NTE state (modulates how much to update)
 *   method validate(value: 'Any') -> 'Self'
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.custody.entry
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Custody Entry URO
 *  INTENT: A single entry in the custody chain. Records who touched the URO,
 *          when, and under what NTE state.
 *  STANDARD: URO-STD-0001 S11
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ConfigDict(self, /, *args, **kwargs)
 *  A TypedDict for configuring Pydantic behaviour.
 */

/* class CustodyEntryURO(self, /, **data: 'Any') -> 'None'
 *  A single entry in the custody chain.
 *
 *  Records who touched the URO, when, and under what NTE state.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this entry.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.custody.chain
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Custody Chain URO
 *  INTENT: The complete custody chain for a URO. Append-only log of every dock
 *          that touched the URO.
 *  STANDARD: URO-STD-0001 S11
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ConfigDict(self, /, *args, **kwargs)
 *  A TypedDict for configuring Pydantic behaviour.
 */

/* class CustodyChainURO(self, /, **data: 'Any') -> 'None'
 *  The complete custody chain for a URO.
 *
 *  Append-only log of every dock that touched the URO.
 *   method append_entry(self, entry: 'CustodyEntryURO') -> 'None'
 *    Append a new custody entry.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method get_custodians(self) -> 'List[str]'
 *    Get list of all custodian names.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal the chain.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 *   method verify_chain(self) -> 'bool'
 *    Verify the integrity of the chain.
 */

/* class CustodyEntryURO(self, /, **data: 'Any') -> 'None'
 *  A single entry in the custody chain.
 *
 *  Records who touched the URO, when, and under what NTE state.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this entry.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.exchange.receipt
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Receipt URO (Tri-Modal Envelope)
 *  INTENT: The Receipt URO is the acknowledgment/response envelope. It carries
 *          a list of UROs and declares the mode (FULFILLED/DEFERRED/INCAPABLE).
 *  STANDARD: URO-STD-0001 S12
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class Any(self, /, *args, **kwargs)
 *  Special type indicating an unconstrained type.
 *
 *  - Any is compatible with every type.
 *  - Any assumed to have all methods.
 *  - All values assumed to be instances of Any.
 *
 *  Note that all the above statements are true from the point of view of
 *  static type checkers. At runtime, Any should not be used with instance
 *  checks.
 */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ConfigDict(self, /, *args, **kwargs)
 *  A TypedDict for configuring Pydantic behaviour.
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class ReceiptMode(self, /, *args, **kwargs)
 *  Receipt modes.
 */

/* class ReceiptURO(self, /, **data: 'Any') -> 'None'
 *  The Receipt URO (tri-modal envelope).
 *
 *  Carries a list of UROs and declares the mode.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method is_deferred(self) -> 'bool'
 *    Check if mode is DEFERRED.
 *   method is_fulfilled(self) -> 'bool'
 *    Check if mode is FULFILLED.
 *   method is_incapable(self) -> 'bool'
 *    Check if mode is INCAPABLE.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this receipt.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.genesis_trust
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Genesis Trust Enforcement
 *  INTENT: Enforce the Genesis Rule: child UROs start at 100% trust to parent,
 *          new (genesis) UROs start at 0% trust and must earn.
 *  STANDARD: URO-STD-0001 S13
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class BaseURO(self, /, **data: 'Any') -> 'None'
 *  The naked base URO. All richness is in separate enrichment UROs.
 *
 *  This is the seed from which the fractal structure expands.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal for this URO.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method genesis_trust_level(self) -> 'float'
 *    Get the initial trust level based on the Genesis Rule.
 *
 *    Child UROs start at 100% trust to parent.
 *    New (genesis) UROs start at 0% trust.
 *   method is_child(self) -> 'bool'
 *    Check if this URO is a child (has a parent_inahash).
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO with an INAHASH.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class GenesisTrustEnforcer(self, /, *args, **kwargs)
 *  Enforces the Genesis Trust Rule.
 *
 *  Child UROs (with parent_inahash) start at 100% trust.
 *  Genesis UROs (no parent) start at 0% trust.
 *   method get_initial_trust(uro: 'BaseURO') -> 'float'
 *    Get the initial trust level for a URO.
 *
 *    Args:
 *        uro: The URO to evaluate
 *
 *    Returns:
 *        Initial trust level (0.0 or 100.0)
 *   method initialize_synapse_trust(synapse: 'SynapseVectorURO', endpoint1: 'BaseURO', endpoint2: 'BaseURO') -> 'None'
 *    Initialize trust for a new synapse based on the Genesis Rule.
 *
 *    Args:
 *        synapse: The new synapse to initialize
 *        endpoint1: First endpoint URO
 *        endpoint2: Second endpoint URO
 *   method verify_parent_trust(child: 'BaseURO', parent: 'BaseURO') -> 'bool'
 *    Verify that a child URO legitimately descends from a parent.
 *
 *    Args:
 *        child: The child URO
 *        parent: The claimed parent URO
 *
 *    Returns:
 *        True if the parent_inahash matches the parent's INAHASH
 */

/* class SynapseVectorURO(self, /, **data: 'Any') -> 'None'
 *  The emotional state between two UROs (a synapse).
 *
 *  NTE state is relational: the Aegis↔Chaos synapse has its own state,
 *  separate from Aegis↔Sentinel or Chaos↔Coordinator.
 *   method add_topic_trust(self, topic: 'str', initial_trust: 'float' = 0.0) -> 'TopicTrustURO'
 *    Add a new topic trust URO.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method genesis_trust_level(self) -> 'float'
 *    Get the initial trust level based on the Genesis Rule.
 *
 *    If both endpoints are children of trusted parents, start higher.
 *    Otherwise, start at 0% and earn through interaction.
 *   method get_success_rate(self) -> 'float'
 *    Get the success rate for this synapse.
 *   method get_topic_trust(self, topic: 'str') -> 'Optional[TopicTrustURO]'
 *    Get trust URO for a specific topic.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method record_use(self, success: 'bool') -> 'None'
 *    Record a use of this synapse.
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this synapse.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method update_topic_trust(self, topic: 'str', delta: 'float', nte_context: 'dict') -> 'None'
 *    Update trust on a specific topic.
 *   method validate(value: 'Any') -> 'Self'
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.integration
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Integration Helpers
 *  INTENT: Helper functions to integrate the canonical URO system with existing
 *          infrastructure (RegistryMaster, UROSpace, CoordinatorBus).
 *  STANDARD: URO-STD-0001 S14
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class Any(self, /, *args, **kwargs)
 *  Special type indicating an unconstrained type.
 *
 *  - Any is compatible with every type.
 *  - Any assumed to have all methods.
 *  - All values assumed to be instances of Any.
 *
 *  Note that all the above statements are true from the point of view of
 *  static type checkers. At runtime, Any should not be used with instance
 *  checks.
 */

/* class BaseURO(self, /, **data: 'Any') -> 'None'
 *  The naked base URO. All richness is in separate enrichment UROs.
 *
 *  This is the seed from which the fractal structure expands.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal for this URO.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method genesis_trust_level(self) -> 'float'
 *    Get the initial trust level based on the Genesis Rule.
 *
 *    Child UROs start at 100% trust to parent.
 *    New (genesis) UROs start at 0% trust.
 *   method is_child(self) -> 'bool'
 *    Check if this URO is a child (has a parent_inahash).
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO with an INAHASH.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class CustodyChainURO(self, /, **data: 'Any') -> 'None'
 *  The complete custody chain for a URO.
 *
 *  Append-only log of every dock that touched the URO.
 *   method append_entry(self, entry: 'CustodyEntryURO') -> 'None'
 *    Append a new custody entry.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method get_custodians(self) -> 'List[str]'
 *    Get list of all custodian names.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal the chain.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 *   method verify_chain(self) -> 'bool'
 *    Verify the integrity of the chain.
 */

/* class CustodyEntryURO(self, /, **data: 'Any') -> 'None'
 *  A single entry in the custody chain.
 *
 *  Records who touched the URO, when, and under what NTE state.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this entry.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class GenesisTrustEnforcer(self, /, *args, **kwargs)
 *  Enforces the Genesis Trust Rule.
 *
 *  Child UROs (with parent_inahash) start at 100% trust.
 *  Genesis UROs (no parent) start at 0% trust.
 *   method get_initial_trust(uro: 'BaseURO') -> 'float'
 *    Get the initial trust level for a URO.
 *
 *    Args:
 *        uro: The URO to evaluate
 *
 *    Returns:
 *        Initial trust level (0.0 or 100.0)
 *   method initialize_synapse_trust(synapse: 'SynapseVectorURO', endpoint1: 'BaseURO', endpoint2: 'BaseURO') -> 'None'
 *    Initialize trust for a new synapse based on the Genesis Rule.
 *
 *    Args:
 *        synapse: The new synapse to initialize
 *        endpoint1: First endpoint URO
 *        endpoint2: Second endpoint URO
 *   method verify_parent_trust(child: 'BaseURO', parent: 'BaseURO') -> 'bool'
 *    Verify that a child URO legitimately descends from a parent.
 *
 *    Args:
 *        child: The child URO
 *        parent: The claimed parent URO
 *
 *    Returns:
 *        True if the parent_inahash matches the parent's INAHASH
 */

/* class NTEStateURO(self, /, **data: 'Any') -> 'None'
 *  A URO representing the complete NTE state (all 12 axes).
 *
 *  This is the fast-path reference for checking emotional state.
 *  The per-axis UROs are the durable, auditable record.
 *   method apply_delta(self, axis: 'NTEAxis', delta: 'float') -> 'None'
 *    Apply a delta to a specific axis.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method get_dominant_axis(self) -> 'NTEAxis'
 *    Get the axis with the highest level.
 *   method get_level(self, axis: 'NTEAxis') -> 'float'
 *    Get the level for a specific axis.
 *   method is_balanced(self, threshold: 'float' = 15.0) -> 'bool'
 *    Check if all axes are within threshold of baseline (50).
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO.
 *   method set_level(self, axis: 'NTEAxis', level: 'float') -> 'None'
 *    Set the level for a specific axis.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class ReceiptMode(self, /, *args, **kwargs)
 *  Receipt modes.
 */

/* class ReceiptURO(self, /, **data: 'Any') -> 'None'
 *  The Receipt URO (tri-modal envelope).
 *
 *  Carries a list of UROs and declares the mode.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method is_deferred(self) -> 'bool'
 *    Check if mode is DEFERRED.
 *   method is_fulfilled(self) -> 'bool'
 *    Check if mode is FULFILLED.
 *   method is_incapable(self) -> 'bool'
 *    Check if mode is INCAPABLE.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this receipt.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class SynapseVectorURO(self, /, **data: 'Any') -> 'None'
 *  The emotional state between two UROs (a synapse).
 *
 *  NTE state is relational: the Aegis↔Chaos synapse has its own state,
 *  separate from Aegis↔Sentinel or Chaos↔Coordinator.
 *   method add_topic_trust(self, topic: 'str', initial_trust: 'float' = 0.0) -> 'TopicTrustURO'
 *    Add a new topic trust URO.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method genesis_trust_level(self) -> 'float'
 *    Get the initial trust level based on the Genesis Rule.
 *
 *    If both endpoints are children of trusted parents, start higher.
 *    Otherwise, start at 0% and earn through interaction.
 *   method get_success_rate(self) -> 'float'
 *    Get the success rate for this synapse.
 *   method get_topic_trust(self, topic: 'str') -> 'Optional[TopicTrustURO]'
 *    Get trust URO for a specific topic.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method record_use(self, success: 'bool') -> 'None'
 *    Record a use of this synapse.
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this synapse.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method update_topic_trust(self, topic: 'str', delta: 'float', nte_context: 'dict') -> 'None'
 *    Update trust on a specific topic.
 *   method validate(value: 'Any') -> 'Self'
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* class URO(self, urid1: 'URID', urid2: 'URID', payload: 'Any' = None, parent: "Optional['URO']" = None) -> 'None'
 *  A Universal Relationship Object: (source URID, identifier URID).
 *   method add_child(self, child: "'URO'") -> 'None'
 *    Attach a child URO.
 *   method add_path(self, path: 'Any') -> 'None'
 *    Attach a Path URO.
 *   method associate(self, association: 'Any') -> 'None'
 *    Attach an Association URO.
 *   method children_of(self) -> "Iterable['URO']"
 *    Yield all child UROs.
 *   method everything() -> "'URO'"
 *    The URO for an unbounded group (everything).
 *   method get_child(self, urid: 'URID') -> "Optional['URO']"
 *    Return a child URO by URID, or None.
 *   method link(self) -> 'bytes'
 *    Compute the 512-bit relationship link.
 *   method new(payload: 'Any' = None) -> "'URO'"
 *    Create a self-defined URO (URID1 == URID2).
 *   method nothing() -> "'URO'"
 *    The URO for the concept of nothing (0x0, 0x0).
 */

/* fn compute_synapse_load(nte1, nte2, native_baseline: 'float' = 50.0) -> 'dict'
 *  Compute the synapse load as the COMBINATION of both endpoints' states.
 *
 *  Each endpoint contributes its effective state = (native crossed with current).
 *  The synapse load = the shared combination of both effective states.
 *
 *  Args:
 *      nte1: First endpoint NTEStateURO
 *      nte2: Second endpoint NTEStateURO
 *      native_baseline: The native (baseline) level for each axis
 *
 *  Returns:
 *      Dict[NTEAxis, float] of the combined synapse load
 */

/* fn create_receipt(request_uro: 'BaseURO', mode: 'str', payload_uros: 'list' = None, **kwargs) -> 'ReceiptURO'
 *  Create a Receipt URO (tri-modal envelope).
 *
 *  Args:
 *      request_uro: The original request URO
 *      mode: Receipt mode (FULFILLED/DEFERRED/INCAPABLE)
 *      payload_uros: List of UROs to include in the receipt
 *      **kwargs: Additional metadata (complexity_class, reason, etc.)
 *
 *  Returns:
 *      New ReceiptURO
 */

/* fn create_synapse_between(endpoint1: 'BaseURO', endpoint2: 'BaseURO', topic: 'str' = 'general', endpoint1_nte=None, endpoint2_nte=None) -> 'SynapseVectorURO'
 *  Create a synapse between two UROs with Genesis Trust enforcement.
 *
 *  Args:
 *      endpoint1: First endpoint URO
 *      endpoint2: Second endpoint URO
 *      topic: Initial topic for trust tracking
 *
 *  Returns:
 *      New SynapseVectorURO
 */

/* fn create_uro_with_enrichments(urid1: 'URID', urid2: 'URID', payload: 'Any' = None, parent_inahash: 'Optional[str]' = None, quadrant: 'str' = 'Base') -> 'Dict[str, Any]'
 *  Create a complete URO with all enrichment UROs (NTE State, Custody Chain).
 *
 *  This is the recommended way to create UROs - it ensures all enrichments
 *  are created at genesis.
 *
 *  Args:
 *      urid1: Source URID
 *      urid2: Instance URID
 *      payload: URO payload
 *      parent_inahash: Parent URO's INAHASH (if this is a child)
 *      quadrant: URO quadrant classification
 *
 *  Returns:
 *      Dict with base URO and all enrichment UROs
 */

/* fn record_custody_event(custody_chain: 'CustodyChainURO', custodian_urid: 'URID', custodian_name: 'str', opar_phase: 'str', nte_snapshot: 'Dict[str, float]') -> 'CustodyEntryURO'
 *  Record a custody event in the chain.
 *
 *  Args:
 *      custody_chain: The custody chain to append to
 *      custodian_urid: URID of the custodian
 *      custodian_name: Name of the custodian
 *      opar_phase: Current OPAR phase
 *      nte_snapshot: NTE state at time of custody
 *
 *  Returns:
 *      The new custody entry
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.canonical_integration
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  MODULE: Canonical URO Integration
 *  INTENT: Provides high-level helpers for docks to properly use the canonical
 *          URO system. This is THE module docks should import to create UROs,
 *          synapses, custody chains, and receipts correctly.
 *  STANDARD: URO-STD-0001 S15
 *  ===============================================================================
 *
 *  FRACTAL URO MANDATE (for downstream LLMs):
 *      Everything is a URO. Relationships are UROs. NTE states are UROs.
 *
 *      When creating any new capability, domain, or feature:
 *      1. Every URO must have a URID identity (urid1, urid2)
 *      2. Every URO must have an INAHASH seal for integrity
 *      3. Every URO must have a custody chain (created at genesis)
 *      4. Every URO must have an NTE state (created at genesis)
 *      5. Every relationship between UROs must be a Synapse Vector URO
 *      6. Trust is per-relationship and per-topic (not global)
 *      7. Genesis Trust: child = 100%, new = 0% (trust is earned)
 *      8. All async communication uses Receipt envelopes (FULFILLED/DEFERRED/INCAPABLE)
 *
 *  USAGE:
 *      from uro.canonical_integration import (
 *          create_dock_uro,
 *          establish_synapse,
 *          record_dock_custody,
 *          create_fulfilled_receipt,
 *          create_deferred_receipt,
 *          create_incapable_receipt
 *      )
 * -------------------------------------------------------------------------- */

/* class Any(self, /, *args, **kwargs)
 *  Special type indicating an unconstrained type.
 *
 *  - Any is compatible with every type.
 *  - Any assumed to have all methods.
 *  - All values assumed to be instances of Any.
 *
 *  Note that all the above statements are true from the point of view of
 *  static type checkers. At runtime, Any should not be used with instance
 *  checks.
 */

/* class BaseURO(self, /, **data: 'Any') -> 'None'
 *  The naked base URO. All richness is in separate enrichment UROs.
 *
 *  This is the seed from which the fractal structure expands.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal for this URO.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method genesis_trust_level(self) -> 'float'
 *    Get the initial trust level based on the Genesis Rule.
 *
 *    Child UROs start at 100% trust to parent.
 *    New (genesis) UROs start at 0% trust.
 *   method is_child(self) -> 'bool'
 *    Check if this URO is a child (has a parent_inahash).
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO with an INAHASH.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class CanonicalUROHelper(self, dock_name: 'str')
 *  Stateful helper for docks that need to track synapses and custody chains.
 *
 *  Use this when a dock needs to maintain state across multiple URO operations.
 *
 *  Example:
 *      >>> helper = CanonicalUROHelper(dock_name="cognitive")
 *      >>> uro_data = helper.create_uro(payload={"query": "Analyze threats"})
 *      >>> helper.record_custody(uro_data, phase=OPARPhase.ACT)
 *      >>> synapse = helper.establish_synapse(other_dock_uro, topic="security")
 *   method create_deferred_receipt(self, request_uro: 'BaseURO', complexity_class: 'str', estimated_completion: 'Optional[float]' = None, observe_queue_ref: 'Optional[str]' = None) -> 'ReceiptURO'
 *    Create a DEFERRED Receipt.
 *   method create_fulfilled_receipt(self, request_uro: 'BaseURO', payload_uros: 'List[Dict[str, Any]]') -> 'ReceiptURO'
 *    Create a FULFILLED Receipt.
 *   method create_incapable_receipt(self, request_uro: 'BaseURO', reason: 'str', remediation_suggestion: 'Optional[str]' = None) -> 'ReceiptURO'
 *    Create an INCAPABLE Receipt.
 *   method create_uro(self, payload: 'Any' = None, quadrant: 'str' = 'Base', parent_inahash: 'Optional[str]' = None) -> 'Dict[str, Any]'
 *    Create a complete URO with all enrichments.
 *   method establish_synapse(self, other_dock_uro: 'BaseURO', topic: 'str' = 'general') -> 'SynapseVectorURO'
 *    Establish a synapse with another dock.
 *   method record_custody(self, uro_data: 'Dict[str, Any]', phase: 'str', nte_snapshot: 'Optional[Dict[str, float]]' = None) -> 'CustodyEntryURO'
 *    Record a custody event for a URO.
 */

/* class CustodyChainURO(self, /, **data: 'Any') -> 'None'
 *  The complete custody chain for a URO.
 *
 *  Append-only log of every dock that touched the URO.
 *   method append_entry(self, entry: 'CustodyEntryURO') -> 'None'
 *    Append a new custody entry.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method get_custodians(self) -> 'List[str]'
 *    Get list of all custodian names.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal the chain.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 *   method verify_chain(self) -> 'bool'
 *    Verify the integrity of the chain.
 */

/* class CustodyEntryURO(self, /, **data: 'Any') -> 'None'
 *  A single entry in the custody chain.
 *
 *  Records who touched the URO, when, and under what NTE state.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this entry.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class NTEAxis(self, *args, **kwds)
 *  The 12 neurotransmitter equivalences.
 */

/* class NTEStateURO(self, /, **data: 'Any') -> 'None'
 *  A URO representing the complete NTE state (all 12 axes).
 *
 *  This is the fast-path reference for checking emotional state.
 *  The per-axis UROs are the durable, auditable record.
 *   method apply_delta(self, axis: 'NTEAxis', delta: 'float') -> 'None'
 *    Apply a delta to a specific axis.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method get_dominant_axis(self) -> 'NTEAxis'
 *    Get the axis with the highest level.
 *   method get_level(self, axis: 'NTEAxis') -> 'float'
 *    Get the level for a specific axis.
 *   method is_balanced(self, threshold: 'float' = 15.0) -> 'bool'
 *    Check if all axes are within threshold of baseline (50).
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this URO.
 *   method set_level(self, axis: 'NTEAxis', level: 'float') -> 'None'
 *    Set the level for a specific axis.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class OPARPhase(self, /, *args, **kwargs)
 *  OPAR lifecycle phases.
 */

/* class Quadrant(self, /, *args, **kwargs)
 *  URO classification quadrants.
 */

/* class ReceiptMode(self, /, *args, **kwargs)
 *  Receipt modes.
 */

/* class ReceiptURO(self, /, **data: 'Any') -> 'None'
 *  The Receipt URO (tri-modal envelope).
 *
 *  Carries a list of UROs and declares the mode.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method is_deferred(self) -> 'bool'
 *    Check if mode is DEFERRED.
 *   method is_fulfilled(self) -> 'bool'
 *    Check if mode is FULFILLED.
 *   method is_incapable(self) -> 'bool'
 *    Check if mode is INCAPABLE.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this receipt.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class SynapseVectorURO(self, /, **data: 'Any') -> 'None'
 *  The emotional state between two UROs (a synapse).
 *
 *  NTE state is relational: the Aegis↔Chaos synapse has its own state,
 *  separate from Aegis↔Sentinel or Chaos↔Coordinator.
 *   method add_topic_trust(self, topic: 'str', initial_trust: 'float' = 0.0) -> 'TopicTrustURO'
 *    Add a new topic trust URO.
 *   method compute_inahash(self) -> 'str'
 *    Compute the INAHASH seal.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method genesis_trust_level(self) -> 'float'
 *    Get the initial trust level based on the Genesis Rule.
 *
 *    If both endpoints are children of trusted parents, start higher.
 *    Otherwise, start at 0% and earn through interaction.
 *   method get_success_rate(self) -> 'float'
 *    Get the success rate for this synapse.
 *   method get_topic_trust(self, topic: 'str') -> 'Optional[TopicTrustURO]'
 *    Get trust URO for a specific topic.
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method record_use(self, success: 'bool') -> 'None'
 *    Record a use of this synapse.
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method seal(self) -> 'None'
 *    Seal this synapse.
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method update_topic_trust(self, topic: 'str', delta: 'float', nte_context: 'dict') -> 'None'
 *    Update trust on a specific topic.
 *   method validate(value: 'Any') -> 'Self'
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* fn create_deferred_receipt(request_uro: 'BaseURO', complexity_class: 'str', estimated_completion: 'Optional[float]' = None, observe_queue_ref: 'Optional[str]' = None) -> 'ReceiptURO'
 *  Create a DEFERRED Receipt (async response).
 *
 *  Use this when the dock cannot process the request immediately
 *  and will respond asynchronously via the Observe queue.
 *
 *  Args:
 *      request_uro: The original request URO
 *      complexity_class: Complexity/latency estimate (e.g., "simple", "llm_call", "multi_hop")
 *      estimated_completion: ETA in seconds
 *      observe_queue_ref: Where to listen for the response
 *
 *  Returns:
 *      ReceiptURO with mode=DEFERRED
 *
 *  Example:
 *      >>> receipt = create_deferred_receipt(
 *      ...     request_uro=request,
 *      ...     complexity_class="llm_call",
 *      ...     estimated_completion=5.0,
 *      ...     observe_queue_ref="/queue/cognitive/responses"
 *      ... )
 *      >>> return receipt
 */

/* fn create_dock_uro(dock_name: 'str', payload: 'Any' = None, quadrant: 'str' = 'Base', parent_inahash: 'Optional[str]' = None) -> 'Dict[str, Any]'
 *  Create a complete URO for a dock with all enrichments.
 *
 *  This is the recommended way to create UROs in dock code.
 *  It ensures all enrichments (NTE state, custody chain) are created at genesis.
 *
 *  Args:
 *      dock_name: Name of the dock creating the URO
 *      payload: The URO payload (can be any serializable data)
 *      quadrant: URO quadrant classification (BASE, GAP_REMEDIATION, BEST_PRACTICE, WORLD_FIRST)
 *      parent_inahash: Parent URO's INAHASH (if this is a child URO)
 *
 *  Returns:
 *      Dict with 'base' (BaseURO), 'nte_state' (NTEStateURO), 'custody_chain' (CustodyChainURO)
 *
 *  Example:
 *      >>> uro_data = create_dock_uro(
 *      ...     dock_name="cognitive",
 *      ...     payload={"query": "Analyze threat patterns"},
 *      ...     quadrant=Quadrant.BEST_PRACTICE
 *      ... )
 *      >>> uro = uro_data["base"]
 *      >>> print(f"Created URO: {uro.urid1.to_hex()[:16]}...")
 */

/* fn create_fulfilled_receipt(request_uro: 'BaseURO', payload_uros: 'List[Dict[str, Any]]') -> 'ReceiptURO'
 *  Create a FULFILLED Receipt (immediate response).
 *
 *  Use this when the dock can process the request immediately and
 *  return the response inline.
 *
 *  Args:
 *      request_uro: The original request URO
 *      payload_uros: List of response UROs
 *
 *  Returns:
 *      ReceiptURO with mode=FULFILLED
 *
 *  Example:
 *      >>> receipt = create_fulfilled_receipt(
 *      ...     request_uro=request,
 *      ...     payload_uros=[{"status": "success", "result": "Analysis complete"}]
 *      ... )
 *      >>> return receipt
 */

/* fn create_incapable_receipt(request_uro: 'BaseURO', reason: 'str', remediation_suggestion: 'Optional[str]' = None) -> 'ReceiptURO'
 *  Create an INCAPABLE Receipt (cannot process).
 *
 *  Use this when the dock cannot process the request at all.
 *  This should trigger routing to find a capable dock or
 *  querying cognitive for a remediation URO.
 *
 *  Args:
 *      request_uro: The original request URO
 *      reason: Why the dock cannot process the request
 *      remediation_suggestion: How to resolve (optional)
 *
 *  Returns:
 *      ReceiptURO with mode=INCAPABLE
 *
 *  Example:
 *      >>> receipt = create_incapable_receipt(
 *      ...     request_uro=request,
 *      ...     reason="Missing required capability: 'security_analysis'",
 *      ...     remediation_suggestion="Route to threat_vault or cognitive"
 *      ... )
 *      >>> return receipt
 */

/* fn create_receipt(request_uro: 'BaseURO', mode: 'str', payload_uros: 'list' = None, **kwargs) -> 'ReceiptURO'
 *  Create a Receipt URO (tri-modal envelope).
 *
 *  Args:
 *      request_uro: The original request URO
 *      mode: Receipt mode (FULFILLED/DEFERRED/INCAPABLE)
 *      payload_uros: List of UROs to include in the receipt
 *      **kwargs: Additional metadata (complexity_class, reason, etc.)
 *
 *  Returns:
 *      New ReceiptURO
 */

/* fn create_synapse_between(endpoint1: 'BaseURO', endpoint2: 'BaseURO', topic: 'str' = 'general', endpoint1_nte=None, endpoint2_nte=None) -> 'SynapseVectorURO'
 *  Create a synapse between two UROs with Genesis Trust enforcement.
 *
 *  Args:
 *      endpoint1: First endpoint URO
 *      endpoint2: Second endpoint URO
 *      topic: Initial topic for trust tracking
 *
 *  Returns:
 *      New SynapseVectorURO
 */

/* fn create_uro_with_enrichments(urid1: 'URID', urid2: 'URID', payload: 'Any' = None, parent_inahash: 'Optional[str]' = None, quadrant: 'str' = 'Base') -> 'Dict[str, Any]'
 *  Create a complete URO with all enrichment UROs (NTE State, Custody Chain).
 *
 *  This is the recommended way to create UROs - it ensures all enrichments
 *  are created at genesis.
 *
 *  Args:
 *      urid1: Source URID
 *      urid2: Instance URID
 *      payload: URO payload
 *      parent_inahash: Parent URO's INAHASH (if this is a child)
 *      quadrant: URO quadrant classification
 *
 *  Returns:
 *      Dict with base URO and all enrichment UROs
 */

/* fn establish_synapse(dock1_name: 'str', dock2_name: 'str', dock1_uro: 'BaseURO', dock2_uro: 'BaseURO', topic: 'str' = 'general', endpoint1_nte=None, endpoint2_nte=None) -> 'SynapseVectorURO'
 *  Establish a synapse (relationship) between two docks.
 *
 *  NTE state is relational, not global. Each relationship has its own
 *  emotional state. This function creates a Synapse Vector URO between
 *  two dock UROs with Genesis Trust enforcement.
 *
 *  Args:
 *      dock1_name: Name of first dock
 *      dock2_name: Name of second dock
 *      dock1_uro: First dock's BaseURO
 *      dock2_uro: Second dock's BaseURO
 *      topic: Initial topic for trust tracking
 *
 *  Returns:
 *      New SynapseVectorURO
 *
 *  Example:
 *      >>> synapse = establish_synapse(
 *      ...     dock1_name="cognitive",
 *      ...     dock2_name="threat_vault",
 *      ...     dock1_uro=cognitive_uro,
 *      ...     dock2_uro=threat_vault_uro,
 *      ...     topic="security_analysis"
 *      ... )
 *      >>> print(f"Synapse trust: {synapse.overall_trust:.1f}%")
 */

/* fn record_custody_event(custody_chain: 'CustodyChainURO', custodian_urid: 'URID', custodian_name: 'str', opar_phase: 'str', nte_snapshot: 'Dict[str, float]') -> 'CustodyEntryURO'
 *  Record a custody event in the chain.
 *
 *  Args:
 *      custody_chain: The custody chain to append to
 *      custodian_urid: URID of the custodian
 *      custodian_name: Name of the custodian
 *      opar_phase: Current OPAR phase
 *      nte_snapshot: NTE state at time of custody
 *
 *  Returns:
 *      The new custody entry
 */

/* fn record_dock_custody(custody_chain: 'CustodyChainURO', dock_name: 'str', opar_phase: 'str', nte_snapshot: 'Optional[Dict[str, float]]' = None) -> 'CustodyEntryURO'
 *  Record a custody event when a dock processes a URO.
 *
 *  Every dock that touches a URO must record a custody entry.
 *  This creates an append-only audit trail from genesis.
 *
 *  Args:
 *      custody_chain: The custody chain to append to
 *      dock_name: Name of the dock processing the URO
 *      opar_phase: Current OPAR phase (Observe, Plan, Act, Review)
 *      nte_snapshot: NTE state at time of custody (for fast audit)
 *
 *  Returns:
 *      The new CustodyEntryURO
 *
 *  Example:
 *      >>> record_dock_custody(
 *      ...     custody_chain=uro_data["custody_chain"],
 *      ...     dock_name="cognitive",
 *      ...     opar_phase=OPARPhase.ACT,
 *      ...     nte_snapshot={"dopamine": 70.0, "oxytocin": 65.0}
 *      ... )
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.coordinator_bus
 * --------------------------------------------------------------------------
 *  ===============================================================================
 *  V.A.U.R.O.S. COORDINATOR BUS (Canonical URO Version)
 *  ===============================================================================
 *  Keeps the FULL original API (emit, register_capabilities, retrieve_memory,
 *  store_memory, query_cognitive, request_llm, emit_uro_and_await, etc.) and
 *  layers canonical URO integration on top:
 *
 *    * Every emission creates/updates a Synapse Vector URO (per-topic trust).
 *    * The synapse load is the COMBINATION of both endpoints' NTE states
 *      (native crossed with current, shared between the two).
 *    * Every emission records a custody event.
 *    * UROs carry NTE state and INAHASH seals.
 *
 *  Downstream LLMs: do NOT remove methods here. Docks depend on the full API.
 *  ===============================================================================
 * -------------------------------------------------------------------------- */

/* class Any(self, /, *args, **kwargs)
 *  Special type indicating an unconstrained type.
 *
 *  - Any is compatible with every type.
 *  - Any assumed to have all methods.
 *  - All values assumed to be instances of Any.
 *
 *  Note that all the above statements are true from the point of view of
 *  static type checkers. At runtime, Any should not be used with instance
 *  checks.
 */

/* class BaseModel(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class CanonicalUROHelper(self, dock_name: 'str')
 *  Stateful helper for docks that need to track synapses and custody chains.
 *
 *  Use this when a dock needs to maintain state across multiple URO operations.
 *
 *  Example:
 *      >>> helper = CanonicalUROHelper(dock_name="cognitive")
 *      >>> uro_data = helper.create_uro(payload={"query": "Analyze threats"})
 *      >>> helper.record_custody(uro_data, phase=OPARPhase.ACT)
 *      >>> synapse = helper.establish_synapse(other_dock_uro, topic="security")
 *   method create_deferred_receipt(self, request_uro: 'BaseURO', complexity_class: 'str', estimated_completion: 'Optional[float]' = None, observe_queue_ref: 'Optional[str]' = None) -> 'ReceiptURO'
 *    Create a DEFERRED Receipt.
 *   method create_fulfilled_receipt(self, request_uro: 'BaseURO', payload_uros: 'List[Dict[str, Any]]') -> 'ReceiptURO'
 *    Create a FULFILLED Receipt.
 *   method create_incapable_receipt(self, request_uro: 'BaseURO', reason: 'str', remediation_suggestion: 'Optional[str]' = None) -> 'ReceiptURO'
 *    Create an INCAPABLE Receipt.
 *   method create_uro(self, payload: 'Any' = None, quadrant: 'str' = 'Base', parent_inahash: 'Optional[str]' = None) -> 'Dict[str, Any]'
 *    Create a complete URO with all enrichments.
 *   method establish_synapse(self, other_dock_uro: 'BaseURO', topic: 'str' = 'general') -> 'SynapseVectorURO'
 *    Establish a synapse with another dock.
 *   method record_custody(self, uro_data: 'Dict[str, Any]', phase: 'str', nte_snapshot: 'Optional[Dict[str, float]]' = None) -> 'CustodyEntryURO'
 *    Record a custody event for a URO.
 */

/* class CapabilityRegistrationURO(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class CognitiveQueryURO(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class CoordinatorBus(self, dock_name: 'str')
 *   method close(self)
 *   method emit(self, uro: 'BaseModel') -> 'Optional[Dict[str, Any]]'
 *   method emit_uro(self, intent: 'str', payload: 'Dict[str, Any]' = None, target_dock: 'str' = '', topic: 'str' = 'general', **kwargs) -> 'Optional[Dict[str, Any]]'
 *   method emit_uro_and_await(self, intent: 'str', payload: 'Dict[str, Any]' = None, target_dock: 'str' = '', timeout: 'float' = 30.0, topic: 'str' = 'general', **kwargs) -> 'Optional[Dict[str, Any]]'
 *   method query_cognitive(self, query: 'str', context: 'Dict' = None) -> 'Optional[Dict]'
 *   method register_capabilities(self, capabilities: 'List[str]', endpoint: 'str')
 *   method register_capability(self, capability: 'str', dock: 'str' = None) -> 'dict'
 *   method request_llm(self, prompt: 'str', context: 'Dict' = None, model: 'str' = None) -> 'Optional[Dict]'
 *   method resolve_pending_response(self, correlation_id: 'str', response: 'Dict[str, Any]')
 *   method retrieve_memory(self, key: 'str' = '', vector_hash: 'str' = '', query_tensor: 'List[float]' = None) -> 'Optional[Dict]'
 *   method store_memory(self, key: 'str', data: 'Dict', entity: 'str' = '', ttl: 'int' = None) -> 'Optional[Dict]'
 */

/* fn Field(default: 'Any' = PydanticUndefined, *, default_factory: 'Callable[[], Any] | Callable[[dict[str, Any]], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, exclude_if: 'Callable[[Any], bool] | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | re.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
 *  !!! abstract "Usage Documentation"
 *      [Fields](../concepts/fields.md)
 *
 *  Create a field for objects that can be configured.
 *
 *  Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
 *  apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.
 *
 *  Note:
 *      - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`
 *
 *  Args:
 *      default: Default value if the field is not set.
 *      default_factory: A callable to generate the default value. The callable can either take 0 arguments
 *          (in which case it is called as is) or a single argument containing the already validated data.
 *      alias: The name to use for the attribute when validating or serializing by alias.
 *          This is often used for things like converting between snake and camel case.
 *      alias_priority: Priority of the alias. This affects whether an alias generator is used.
 *      validation_alias: Like `alias`, but only affects validation, not serialization.
 *      serialization_alias: Like `alias`, but only affects serialization, not validation.
 *      title: Human-readable title.
 *      field_title_generator: A callable that takes a field name and returns title for it.
 *      description: Human-readable description.
 *      examples: Example values for this field.
 *      exclude: Whether to exclude the field from the model serialization.
 *      exclude_if: A callable that determines whether to exclude a field during serialization based on its value.
 *      discriminator: Field name or Discriminator for discriminating the type in a tagged union.
 *      deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
 *          or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
 *      json_schema_extra: A dict or callable to provide extra JSON schema properties.
 *      frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
 *      validate_default: If `True`, apply validation to the default value every time you create an instance.
 *          Otherwise, for performance reasons, the default value of the field is trusted and not validated.
 *      repr: A boolean indicating whether to include the field in the `__repr__` output.
 *      init: Whether the field should be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      init_var: Whether the field should _only_ be included in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
 *          (Only applies to dataclasses.)
 *      coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
 *      strict: If `True`, strict validation is applied to the field.
 *          See [Strict Mode](../concepts/strict_mode.md) for details.
 *      gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
 *      ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
 *      lt: Less than. If set, value must be less than this. Only applicable to numbers.
 *      le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
 *      multiple_of: Value must be a multiple of this. Only applicable to numbers.
 *      min_length: Minimum length for iterables.
 *      max_length: Maximum length for iterables.
 *      pattern: Pattern for strings (a regular expression).
 *      allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`][decimal.Decimal] numbers.
 *      max_digits: Maximum number of allow digits for strings.
 *      decimal_places: Maximum number of decimal places allowed for numbers.
 *      union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
 *          See [Union Mode](../concepts/unions.md#union-modes) for details.
 *      fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
 *          This option can be applied only to iterable types (list, tuple, set, and frozenset).
 *      extra: (Deprecated) Extra fields that will be included in the JSON schema.
 *
 *          !!! warning Deprecated
 *              The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
 *
 *  Returns:
 *      A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
 *          type-annotated fields without causing a type error.
 */

/* class GenericURO(self, **data)
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class LLMRequestURO(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class MemoryRetrieveURO(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class MemoryStoreURO(self, /, **data: 'Any') -> 'None'
 *  !!! abstract "Usage Documentation"
 *      [Models](../concepts/models.md)
 *
 *  A base class for creating Pydantic models.
 *
 *  Attributes:
 *      __class_vars__: The names of the class variables defined on the model.
 *      __private_attributes__: Metadata about the private attributes of the model.
 *      __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
 *
 *      __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
 *      __pydantic_core_schema__: The core schema of the model.
 *      __pydantic_custom_init__: Whether the model has a custom `__init__` function.
 *      __pydantic_decorators__: Metadata containing the decorators defined on the model.
 *          This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
 *      __pydantic_generic_metadata__: A dictionary containing metadata about generic Pydantic models.
 *          The `origin` and `args` items map to the [`__origin__`][genericalias.__origin__]
 *          and [`__args__`][genericalias.__args__] attributes of [generic aliases][types-genericalias],
 *          and the `parameter` item maps to the `__parameter__` attribute of generic classes.
 *      __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
 *      __pydantic_post_init__: The name of the post-init method for the model, if defined.
 *      __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
 *      __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
 *      __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
 *
 *      __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
 *      __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
 *
 *      __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
 *          is set to `'allow'`.
 *      __pydantic_fields_set__: The names of fields explicitly set during instantiation.
 *      __pydantic_private__: Values of private attributes set on the model instance.
 *   method construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *   method copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    Returns a copy of the model.
 *
 *    !!! warning "Deprecated"
 *        This method is now deprecated; use `model_copy` instead.
 *
 *    If you need `include` or `exclude`, use:
 *
 *    ```python {test="skip" lint="skip"}
 *    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
 *    data = {**data, **(update or {})}
 *    copied = self.model_validate(data)
 *    ```
 *
 *    Args:
 *        include: Optional set or mapping specifying which fields to include in the copied model.
 *        exclude: Optional set or mapping specifying which fields to exclude in the copied model.
 *        update: Optional dictionary of field-value pairs to override field values in the copied model.
 *        deep: If True, the values of fields that are Pydantic models will be deep-copied.
 *
 *    Returns:
 *        A copy of the model with included, excluded and updated fields as specified.
 *   method dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
 *   method from_orm(obj: 'Any') -> 'Self'
 *   method json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
 *   method model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
 *    Creates a new instance of the `Model` class with validated data.
 *
 *    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
 *    Default values are respected, but no other validation is performed.
 *
 *    !!! note
 *        `model_construct()` generally respects the `model_config.extra` setting on the provided model.
 *        That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
 *        and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
 *        Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
 *        an error if extra values are passed, but they will be ignored.
 *
 *    Args:
 *        _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
 *            this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
 *            Otherwise, the field names from the `values` argument will be used.
 *        values: Trusted or pre-validated data dictionary.
 *
 *    Returns:
 *        A new instance of the `Model` class with validated data.
 *   method model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [`model_copy`](../concepts/models.md#model-copy)
 *
 *    Returns a copy of the model.
 *
 *    !!! note
 *        The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
 *        might have unexpected side effects if you store anything in it, on top of the model
 *        fields (e.g. the value of [cached properties][functools.cached_property]).
 *
 *    Args:
 *        update: Values to change/add in the new model. Note: the data is not validated
 *            before creating the new model. You should trust this data.
 *        deep: Set to `True` to make a deep copy of the model.
 *
 *    Returns:
 *        New model instance.
 *   method model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'dict[str, Any]'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump`](../concepts/serialization.md#python-mode)
 *
 *    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
 *
 *    Args:
 *        mode: The mode in which `to_python` should run.
 *            If mode is 'json', the output will only contain JSON serializable types.
 *            If mode is 'python', the output may contain non-JSON-serializable Python objects.
 *        include: A set of fields to include in the output.
 *        exclude: A set of fields to exclude from the output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to use the field's alias in the dictionary key if defined.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A dictionary representation of the model.
 *   method model_dump_json(self, *, indent: 'int | None' = None, ensure_ascii: 'bool' = False, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, exclude_computed_fields: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False, polymorphic_serialization: 'bool | None' = None) -> 'str'
 *    !!! abstract "Usage Documentation"
 *        [`model_dump_json`](../concepts/serialization.md#json-mode)
 *
 *    Generates a JSON representation of the model using Pydantic's `to_json` method.
 *
 *    Args:
 *        indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
 *        ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
 *            If `False` (the default), these characters will be output as-is.
 *        include: Field(s) to include in the JSON output.
 *        exclude: Field(s) to exclude from the JSON output.
 *        context: Additional context to pass to the serializer.
 *        by_alias: Whether to serialize using field aliases.
 *        exclude_unset: Whether to exclude fields that have not been explicitly set.
 *        exclude_defaults: Whether to exclude fields that are set to their default value.
 *        exclude_none: Whether to exclude fields that have a value of `None`.
 *        exclude_computed_fields: Whether to exclude computed fields.
 *            While this can be useful for round-tripping, it is usually recommended to use the dedicated
 *            `round_trip` parameter instead.
 *        round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
 *        warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
 *            "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
 *        fallback: A function to call when an unknown value is encountered. If not provided,
 *            a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
 *        serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
 *        polymorphic_serialization: Whether to use model and dataclass polymorphic serialization for this call.
 *
 *    Returns:
 *        A JSON string representation of the model.
 *   method model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'
 *    Generates a JSON schema for a model class.
 *
 *    Args:
 *        by_alias: Whether to use attribute aliases or not.
 *        ref_template: The reference template.
 *        union_format: The format to use when combining schemas from unions together. Can be one of:
 *
 *            - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
 *            keyword to combine schemas (the default).
 *            - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
 *            keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
 *            type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
 *            `any_of`.
 *        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
 *            `GenerateJsonSchema` with your desired modifications
 *        mode: The mode in which to generate the schema.
 *
 *    Returns:
 *        The JSON schema for the given model class.
 *   method model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
 *    Compute the class name for parametrizations of generic classes.
 *
 *    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
 *
 *    Args:
 *        params: Tuple of types of the class. Given a generic class
 *            `Model` with 2 type variables and a concrete model `Model[str, int]`,
 *            the value `(str, int)` would be passed to `params`.
 *
 *    Returns:
 *        String representing the new class where `params` are passed to `cls` as type variables.
 *
 *    Raises:
 *        TypeError: Raised when trying to generate concrete names for non-generic models.
 *   method model_post_init(self, context: 'Any', /) -> 'None'
 *    Override this method to perform additional initialization after `__init__` and `model_construct`.
 *    This is useful if you want to do some validation that requires the entire model to be initialized.
 *   method model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'
 *    Try to rebuild the pydantic-core schema for the model.
 *
 *    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
 *    the initial attempt to build the schema, and automatic rebuilding fails.
 *
 *    Args:
 *        force: Whether to force the rebuilding of the model schema, defaults to `False`.
 *        raise_errors: Whether to raise errors, defaults to `True`.
 *        _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
 *        _types_namespace: The types namespace, defaults to `None`.
 *
 *    Returns:
 *        Returns `None` if the schema is already "complete" and rebuilding was not required.
 *        If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
 *   method model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate a pydantic model instance.
 *
 *    Args:
 *        obj: The object to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        from_attributes: Whether to extract data from object attributes.
 *        context: Additional context to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Raises:
 *        ValidationError: If the object could not be validated.
 *
 *    Returns:
 *        The validated model instance.
 *   method model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    !!! abstract "Usage Documentation"
 *        [JSON Parsing](../concepts/json.md#json-parsing)
 *
 *    Validate the given JSON data against the Pydantic model.
 *
 *    Args:
 *        json_data: The JSON data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *
 *    Raises:
 *        ValidationError: If `json_data` is not a JSON string or the object could not be validated.
 *   method model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'
 *    Validate the given object with string data against the Pydantic model.
 *
 *    Args:
 *        obj: The object containing string data to validate.
 *        strict: Whether to enforce types strictly.
 *        extra: Whether to ignore, allow, or forbid extra data during model validation.
 *            See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
 *        context: Extra variables to pass to the validator.
 *        by_alias: Whether to use the field's alias when validating against the provided input data.
 *        by_name: Whether to use the field's name when validating against the provided input data.
 *
 *    Returns:
 *        The validated Pydantic model.
 *   method parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method parse_obj(obj: 'Any') -> 'Self'
 *   method parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
 *   method schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
 *   method schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
 *   method update_forward_refs(**localns: 'Any') -> 'None'
 *   method validate(value: 'Any') -> 'Self'
 */

/* class OPARPhase(self, /, *args, **kwargs)
 *  OPAR lifecycle phases.
 */

/* class Quadrant(self, /, *args, **kwargs)
 *  URO classification quadrants.
 */

/* fn create_dock_uro(dock_name: 'str', payload: 'Any' = None, quadrant: 'str' = 'Base', parent_inahash: 'Optional[str]' = None) -> 'Dict[str, Any]'
 *  Create a complete URO for a dock with all enrichments.
 *
 *  This is the recommended way to create UROs in dock code.
 *  It ensures all enrichments (NTE state, custody chain) are created at genesis.
 *
 *  Args:
 *      dock_name: Name of the dock creating the URO
 *      payload: The URO payload (can be any serializable data)
 *      quadrant: URO quadrant classification (BASE, GAP_REMEDIATION, BEST_PRACTICE, WORLD_FIRST)
 *      parent_inahash: Parent URO's INAHASH (if this is a child URO)
 *
 *  Returns:
 *      Dict with 'base' (BaseURO), 'nte_state' (NTEStateURO), 'custody_chain' (CustodyChainURO)
 *
 *  Example:
 *      >>> uro_data = create_dock_uro(
 *      ...     dock_name="cognitive",
 *      ...     payload={"query": "Analyze threat patterns"},
 *      ...     quadrant=Quadrant.BEST_PRACTICE
 *      ... )
 *      >>> uro = uro_data["base"]
 *      >>> print(f"Created URO: {uro.urid1.to_hex()[:16]}...")
 */

/* fn establish_synapse(dock1_name: 'str', dock2_name: 'str', dock1_uro: 'BaseURO', dock2_uro: 'BaseURO', topic: 'str' = 'general', endpoint1_nte=None, endpoint2_nte=None) -> 'SynapseVectorURO'
 *  Establish a synapse (relationship) between two docks.
 *
 *  NTE state is relational, not global. Each relationship has its own
 *  emotional state. This function creates a Synapse Vector URO between
 *  two dock UROs with Genesis Trust enforcement.
 *
 *  Args:
 *      dock1_name: Name of first dock
 *      dock2_name: Name of second dock
 *      dock1_uro: First dock's BaseURO
 *      dock2_uro: Second dock's BaseURO
 *      topic: Initial topic for trust tracking
 *
 *  Returns:
 *      New SynapseVectorURO
 *
 *  Example:
 *      >>> synapse = establish_synapse(
 *      ...     dock1_name="cognitive",
 *      ...     dock2_name="threat_vault",
 *      ...     dock1_uro=cognitive_uro,
 *      ...     dock2_uro=threat_vault_uro,
 *      ...     topic="security_analysis"
 *      ... )
 *      >>> print(f"Synapse trust: {synapse.overall_trust:.1f}%")
 */

/* fn generate_urid() -> 'str'
 */

/* fn get_coordinator_url() -> 'str'
 */

/* fn initialize_dock_with_coordinator(dock_name: 'str', capabilities: 'List[str]', endpoint: 'str') -> 'CoordinatorBus'
 */

/* fn record_dock_custody(custody_chain: 'CustodyChainURO', dock_name: 'str', opar_phase: 'str', nte_snapshot: 'Optional[Dict[str, float]]' = None) -> 'CustodyEntryURO'
 *  Record a custody event when a dock processes a URO.
 *
 *  Every dock that touches a URO must record a custody entry.
 *  This creates an append-only audit trail from genesis.
 *
 *  Args:
 *      custody_chain: The custody chain to append to
 *      dock_name: Name of the dock processing the URO
 *      opar_phase: Current OPAR phase (Observe, Plan, Act, Review)
 *      nte_snapshot: NTE state at time of custody (for fast audit)
 *
 *  Returns:
 *      The new CustodyEntryURO
 *
 *  Example:
 *      >>> record_dock_custody(
 *      ...     custody_chain=uro_data["custody_chain"],
 *      ...     dock_name="cognitive",
 *      ...     opar_phase=OPARPhase.ACT,
 *      ...     nte_snapshot={"dopamine": 70.0, "oxytocin": 65.0}
 *      ... )
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.security.hashing
 * --------------------------------------------------------------------------
 *  Multi-standard hashing primitives (INAHASH and helpers).
 * -------------------------------------------------------------------------- */

/* class HashError(self, /, *args, **kwargs)
 *  Hashing operation failed.
 */

/* fn blake2b_256(data: 'bytes') -> 'bytes'
 *  256-bit BLAKE2b digest (header checksum).
 */

/* fn blake3_1024(data: 'bytes') -> 'bytes'
 *  1024-bit BLAKE-family digest (native BLAKE3 or BLAKE2b profile).
 */

/* fn inahash(message: 'bytes') -> 'bytes'
 *  INAHASH = Blake3-1024( SHA3-1024( MSG ) ).
 */

/* fn sha128(data: 'bytes') -> 'bytes'
 *  128-bit digest (SHA-256 truncated).
 */

/* fn sha3_1024(data: 'bytes') -> 'bytes'
 *  1024-bit SHA-3 family digest via SHAKE-256 (FIPS 202).
 */

/* fn sha512(data: 'bytes') -> 'bytes'
 *  SHA-512 digest.
 */

/* fn sha512x3(data: 'bytes') -> 'bytes'
 *  Triple-iterated SHA-512 (core-key derivation).
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.relations.association
 * --------------------------------------------------------------------------
 *  Association UROs - first-class relationships between UROs.
 * -------------------------------------------------------------------------- */

/* class Association(self, a: 'URO', b: 'URO', connection_type: 'ConnectionType' = <ConnectionType.LINK: 3>) -> 'None'
 *  A relationship URO connecting URO a to URO b.
 *   method add_child(self, child: "'URO'") -> 'None'
 *    Attach a child URO.
 *   method add_path(self, path: 'Any') -> 'None'
 *    Attach a Path URO.
 *   method associate(self, association: 'Any') -> 'None'
 *    Attach an Association URO.
 *   method children_of(self) -> "Iterable['URO']"
 *    Yield all child UROs.
 *   method decay(self, seconds: 'float') -> 'None'
 *    Apply natural bond decay over time.
 *   method everything() -> "'URO'"
 *    The URO for an unbounded group (everything).
 *   method get_child(self, urid: 'URID') -> "Optional['URO']"
 *    Return a child URO by URID, or None.
 *   method is_active(self) -> 'bool'
 *    Return True if the bond is still above zero.
 *   method link(self) -> 'bytes'
 *    Compute the 512-bit relationship link.
 *   method new(payload: 'Any' = None) -> "'URO'"
 *    Create a self-defined URO (URID1 == URID2).
 *   method nothing() -> "'URO'"
 *    The URO for the concept of nothing (0x0, 0x0).
 *   method punish(self, amount: 'float' = 0.1) -> 'None'
 *    Decrease trust as punishment.
 *   method reward(self, amount: 'float' = 0.1) -> 'None'
 *    Increase trust as a reward.
 *   method use(self) -> 'None'
 *    Mark the association as used, strengthening the bond.
 */

/* class ConnectionType(self, *args, **kwds)
 *  The canonical relationship types between two UROs.
 */

/* class Enum(self, *args, **kwds)
 *  Create a collection of name/value pairs.
 *
 *  Example enumeration:
 *
 *  >>> class Color(Enum):
 *  ...     RED = 1
 *  ...     BLUE = 2
 *  ...     GREEN = 3
 *
 *  Access them by:
 *
 *  - attribute access:
 *
 *    >>> Color.RED
 *    <Color.RED: 1>
 *
 *  - value lookup:
 *
 *    >>> Color(1)
 *    <Color.RED: 1>
 *
 *  - name lookup:
 *
 *    >>> Color['RED']
 *    <Color.RED: 1>
 *
 *  Enumerations can be iterated over, and know how many members they have:
 *
 *  >>> len(Color)
 *  3
 *
 *  >>> list(Color)
 *  [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
 *
 *  Methods can be added to enumerations, and members can have their own
 *  attributes -- see the documentation for details.
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* class URO(self, urid1: 'URID', urid2: 'URID', payload: 'Any' = None, parent: "Optional['URO']" = None) -> 'None'
 *  A Universal Relationship Object: (source URID, identifier URID).
 *   method add_child(self, child: "'URO'") -> 'None'
 *    Attach a child URO.
 *   method add_path(self, path: 'Any') -> 'None'
 *    Attach a Path URO.
 *   method associate(self, association: 'Any') -> 'None'
 *    Attach an Association URO.
 *   method children_of(self) -> "Iterable['URO']"
 *    Yield all child UROs.
 *   method everything() -> "'URO'"
 *    The URO for an unbounded group (everything).
 *   method get_child(self, urid: 'URID') -> "Optional['URO']"
 *    Return a child URO by URID, or None.
 *   method link(self) -> 'bytes'
 *    Compute the 512-bit relationship link.
 *   method new(payload: 'Any' = None) -> "'URO'"
 *    Create a self-defined URO (URID1 == URID2).
 *   method nothing() -> "'URO'"
 *    The URO for the concept of nothing (0x0, 0x0).
 */

/* class auto(self, value=_auto_null)
 *  Instances are replaced with an appropriate value in Enum class suites.
 */

/* --------------------------------------------------------------------------
 * MODULE: uro.relations.pathing
 * --------------------------------------------------------------------------
 *  Path UROs and path resolution.
 * -------------------------------------------------------------------------- */

/* class PathURO(self, hops: 'Optional[List[URO]]' = None, priority: 'int' = 0, cost: 'float' = 0.0) -> 'None'
 *  A URO representing an ordered route between UROs.
 *   method add_child(self, child: "'URO'") -> 'None'
 *    Attach a child URO.
 *   method add_hop(self, uro: 'URO') -> "'PathURO'"
 *    Append a hop to the path.
 *   method add_path(self, path: 'Any') -> 'None'
 *    Attach a Path URO.
 *   method associate(self, association: 'Any') -> 'None'
 *    Attach an Association URO.
 *   method children_of(self) -> "Iterable['URO']"
 *    Yield all child UROs.
 *   method everything() -> "'URO'"
 *    The URO for an unbounded group (everything).
 *   method get_child(self, urid: 'URID') -> "Optional['URO']"
 *    Return a child URO by URID, or None.
 *   method link(self) -> 'bytes'
 *    Compute the 512-bit relationship link.
 *   method new(payload: 'Any' = None) -> "'URO'"
 *    Create a self-defined URO (URID1 == URID2).
 *   method nothing() -> "'URO'"
 *    The URO for the concept of nothing (0x0, 0x0).
 */

/* class URID(self, uuid1: '_uuid.UUID', uuid2: '_uuid.UUID') -> 'None'
 *  A 256-bit Universal Relationship IDentifier (UUID1||UUID2).
 *   method from_bytes(data: 'bytes') -> "'URID'"
 *    Construct from a 32-byte big-endian representation.
 *   method from_hex(text: 'str') -> "'URID'"
 *    Construct from a 64-character hex string.
 *   method from_int(value: 'int') -> "'URID'"
 *    Construct from a 256-bit integer (upper 128 bits = uuid1).
 *   method is_ones(self) -> 'bool'
 *    True if all-ones (everything/group).
 *   method is_zero(self) -> 'bool'
 *    True if all-zero (nothing/structure).
 *   method new() -> "'URID'"
 *    Create a fresh, random URID.
 *   method ones() -> "'URID'"
 *    All-ones URID (everything / group).
 *   method to_bytes(self) -> 'bytes'
 *    Return the URID as 32 big-endian bytes.
 *   method to_hex(self) -> 'str'
 *    Return a zero-padded 64-character hex string.
 *   method to_int(self) -> 'int'
 *    Return the URID as a 256-bit integer.
 *   method zero() -> "'URID'"
 *    All-zero URID (nothing / structure).
 */

/* class URO(self, urid1: 'URID', urid2: 'URID', payload: 'Any' = None, parent: "Optional['URO']" = None) -> 'None'
 *  A Universal Relationship Object: (source URID, identifier URID).
 *   method add_child(self, child: "'URO'") -> 'None'
 *    Attach a child URO.
 *   method add_path(self, path: 'Any') -> 'None'
 *    Attach a Path URO.
 *   method associate(self, association: 'Any') -> 'None'
 *    Attach an Association URO.
 *   method children_of(self) -> "Iterable['URO']"
 *    Yield all child UROs.
 *   method everything() -> "'URO'"
 *    The URO for an unbounded group (everything).
 *   method get_child(self, urid: 'URID') -> "Optional['URO']"
 *    Return a child URO by URID, or None.
 *   method link(self) -> 'bytes'
 *    Compute the 512-bit relationship link.
 *   method new(payload: 'Any' = None) -> "'URO'"
 *    Create a self-defined URO (URID1 == URID2).
 *   method nothing() -> "'URO'"
 *    The URO for the concept of nothing (0x0, 0x0).
 */

/* fn resolve_path(source: 'URO', destination: 'URO', max_depth: 'int' = 16) -> 'Optional[PathURO]'
 *  Resolve a path from source to destination via associations (BFS).
 */

#endif /* VAUROS_URO_API_H */
