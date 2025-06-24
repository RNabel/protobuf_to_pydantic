"""
Shared pytest fixtures for test_demo_proto tests.

Provides common test fixtures and configuration for all tests in this directory.
"""

import pytest
from typing import Type, Any
from google.protobuf.message import Message
from pydantic import BaseModel

# Import common protobuf modules used across tests
from example.proto_pydanticv2.example.example_proto.demo import (
    demo_pb2,
    demo_p2p,
)


@pytest.fixture
def proto_json_options():
    """Common JSON format options for protobuf serialization."""
    return {
        "always_print_fields_with_no_presence": True,
        "use_integers_for_enums": True,
        "including_default_value_fields": True,
        "preserving_proto_field_name": False,
    }


@pytest.fixture
def proto_json_options_string_enums():
    """JSON format options with string enum serialization."""
    return {
        "always_print_fields_with_no_presence": True,
        "use_integers_for_enums": False,
        "including_default_value_fields": True,
        "preserving_proto_field_name": False,
    }


@pytest.fixture
def sample_user_message():
    """Sample UserMessage protobuf instance for testing."""
    msg = demo_pb2.UserMessage()
    msg.uid = "12345"
    msg.age = 25
    msg.height = 1.75
    msg.sex = demo_pb2.SexType.man
    msg.is_adult = True
    msg.user_name = "test_user"
    return msg


@pytest.fixture
def sample_user_message_dict():
    """Sample UserMessage data as dictionary."""
    return {
        "uid": "12345",
        "age": 25,
        "height": 1.75,
        "sex": 0,  # man
        "isAdult": True,
        "userName": "test_user",
        "demo": 0,
        "demoMessage": {
            "earth": "",
            "mercury": "",
            "mars": ""
        }
    }


@pytest.fixture
def empty_message_instances():
    """Collection of empty message instances for testing defaults."""
    return {
        "EmptyMessage": demo_pb2.EmptyMessage(),
        "UserMessage": demo_pb2.UserMessage(),
        "MapMessage": demo_pb2.MapMessage(),
        "RepeatedMessage": demo_pb2.RepeatedMessage(),
        "NestedMessage": demo_pb2.NestedMessage(),
    }


@pytest.fixture
def pydantic_model_classes():
    """Collection of Pydantic model classes."""
    return {
        "EmptyMessage": demo_p2p.EmptyMessage,
        "UserMessage": demo_p2p.UserMessage,
        "MapMessage": demo_p2p.MapMessage,
        "RepeatedMessage": demo_p2p.RepeatedMessage,
        "NestedMessage": demo_p2p.NestedMessage,
    }


@pytest.fixture(autouse=True)
def clear_model_cache():
    """Clear any model generation caches before each test."""
    # Import here to avoid circular dependencies
    from protobuf_to_pydantic.gen_model import clear_create_model_cache
    clear_create_model_cache()
    yield
    clear_create_model_cache()


@pytest.fixture
def assert_json_equal():
    """Helper to assert JSON equality with better error messages."""
    def _assert_json_equal(actual: dict, expected: dict, ignore_keys: set = None):
        if ignore_keys:
            actual = {k: v for k, v in actual.items() if k not in ignore_keys}
            expected = {k: v for k, v in expected.items() if k not in ignore_keys}
        
        assert actual == expected, (
            f"JSON mismatch:\nActual: {actual}\nExpected: {expected}"
        )
    
    return _assert_json_equal