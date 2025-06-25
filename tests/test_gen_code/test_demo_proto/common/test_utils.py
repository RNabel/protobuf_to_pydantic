"""
Utility functions for protobuf to pydantic testing.

Provides standalone utility functions for test support.
"""

import json
from typing import Any, Dict, Set, List, Optional
from google.protobuf.message import Message
from pydantic import BaseModel


def compare_json_dicts(
    dict1: dict,
    dict2: dict,
    ignore_keys: Optional[Set[str]] = None,
    ignore_empty_collections: bool = False,
) -> bool:
    """
    Compare two JSON dictionaries with flexible comparison options.

    Args:
        dict1: First dictionary to compare
        dict2: Second dictionary to compare
        ignore_keys: Set of keys to ignore in comparison
        ignore_empty_collections: Whether to treat empty lists/dicts as equivalent to missing

    Returns:
        True if dictionaries are equivalent according to comparison rules
    """
    if ignore_keys is None:
        ignore_keys = set()

    # Deep copy to avoid modifying originals
    d1 = json.loads(json.dumps(dict1))
    d2 = json.loads(json.dumps(dict2))

    # Remove ignored keys
    for key in ignore_keys:
        d1.pop(key, None)
        d2.pop(key, None)

    # Optionally normalize empty collections
    if ignore_empty_collections:
        _normalize_empty_collections(d1)
        _normalize_empty_collections(d2)

    return d1 == d2


def _normalize_empty_collections(d: dict) -> None:
    """Remove empty lists and dicts recursively."""
    keys_to_remove = []

    for key, value in d.items():
        if isinstance(value, (list, dict)) and len(value) == 0:
            keys_to_remove.append(key)
        elif isinstance(value, dict):
            _normalize_empty_collections(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _normalize_empty_collections(item)

    for key in keys_to_remove:
        del d[key]


def get_field_differences(msg1: Message, msg2: Message) -> List[str]:
    """
    Get list of fields that differ between two protobuf messages.

    Args:
        msg1: First protobuf message
        msg2: Second protobuf message

    Returns:
        List of field names that have different values
    """
    if type(msg1) != type(msg2):
        return ["_message_type"]

    differences = []

    for field in msg1.DESCRIPTOR.fields:
        value1 = getattr(msg1, field.name)
        value2 = getattr(msg2, field.name)

        if value1 != value2:
            differences.append(field.name)

    return differences


def create_nested_dict(path: str, value: Any, separator: str = ".") -> dict:
    """
    Create a nested dictionary from a dot-separated path.

    Args:
        path: Dot-separated path (e.g., "user.address.city")
        value: Value to set at the path
        separator: Path separator (default: ".")

    Returns:
        Nested dictionary with value at specified path
    """
    keys = path.split(separator)
    result = {}
    current = result

    for key in keys[:-1]:
        current[key] = {}
        current = current[key]

    current[keys[-1]] = value
    return result


def flatten_dict(d: dict, parent_key: str = "", separator: str = ".") -> dict:
    """
    Flatten a nested dictionary.

    Args:
        d: Dictionary to flatten
        parent_key: Key prefix for nested values
        separator: Separator for nested keys

    Returns:
        Flattened dictionary
    """
    items = []

    for k, v in d.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k

        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, separator).items())
        else:
            items.append((new_key, v))

    return dict(items)


def get_all_field_paths(msg_class: type[Message]) -> List[str]:
    """
    Get all possible field paths for a protobuf message class.

    Args:
        msg_class: Protobuf message class

    Returns:
        List of all field paths including nested fields
    """
    paths = []

    def _get_paths(descriptor, prefix=""):
        for field in descriptor.fields:
            field_path = f"{prefix}.{field.name}" if prefix else field.name
            paths.append(field_path)

            # Recurse into message fields
            if field.message_type and field.message_type.name != descriptor.name:
                _get_paths(field.message_type, field_path)

    _get_paths(msg_class.DESCRIPTOR)
    return paths


def assert_models_equivalent(
    model1: BaseModel, model2: BaseModel, ignore_fields: Optional[Set[str]] = None
) -> None:
    """
    Assert that two Pydantic models are equivalent.

    Args:
        model1: First Pydantic model
        model2: Second Pydantic model
        ignore_fields: Set of field names to ignore in comparison
    """
    if ignore_fields is None:
        ignore_fields = set()

    dict1 = model1.model_dump(by_alias=False)
    dict2 = model2.model_dump(by_alias=False)

    # Remove ignored fields
    for field in ignore_fields:
        dict1.pop(field, None)
        dict2.pop(field, None)

    assert dict1 == dict2, f"Models not equivalent:\\nModel1: {dict1}\\nModel2: {dict2}"


def create_test_data_matrix(
    base_values: Dict[str, List[Any]], combinations: Optional[List[List[str]]] = None
) -> List[Dict[str, Any]]:
    """
    Create a matrix of test data combinations.

    Args:
        base_values: Dictionary of field names to lists of test values
        combinations: Optional list of field combinations to test

    Returns:
        List of test data dictionaries
    """
    if combinations is None:
        # Test all fields individually
        combinations = [[field] for field in base_values.keys()]

    test_data = []

    for combo in combinations:
        # Generate test cases for this combination
        values_to_combine = [base_values[field] for field in combo]

        # Create cartesian product
        import itertools

        for values in itertools.product(*values_to_combine):
            test_case = {}
            for field, value in zip(combo, values):
                test_case[field] = value
            test_data.append(test_case)

    return test_data
