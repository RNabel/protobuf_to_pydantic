"""
Comprehensive roundtrip tests for well-known protobuf types.
Tests both directions:
1. Protobuf -> Pydantic -> Protobuf
2. Pydantic -> Protobuf -> Pydantic
"""

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from google.protobuf import json_format, struct_pb2
from google.protobuf.message import Message

from example.proto_pydanticv2.example.example_proto.demo import (
    well_known_types_roundtrip_pb2,
    well_known_types_roundtrip_p2p,
    value_demo_pb2,
    value_demo_p2p,
)

class TestComprehensiveRoundtrip:
    """Test comprehensive roundtrip conversions for all well-known types."""

    def test_protobuf_to_pydantic_roundtrip_value(self):
        """Test Protobuf -> Pydantic -> Protobuf for Value fields."""
        # Create protobuf message
        proto_msg = value_demo_pb2.ValueTestMessage()
        proto_msg.id = "proto_first"
        
        # Set various value types
        # Use the utility function to properly set Value fields
        from protobuf_to_pydantic.util import python_value_to_protobuf_value
        python_value_to_protobuf_value({
            "name": "Alice",
            "age": 25,
            "active": True
        }, proto_msg.dynamic_value)
        
        # Add to value list
        proto_msg.value_list.add().number_value = 42
        proto_msg.value_list.add().string_value = "hello"
        proto_msg.value_list.add().bool_value = False
        proto_msg.value_list.add().null_value = struct_pb2.NULL_VALUE
        
        # Add to value map
        proto_msg.value_map["num"].number_value = 123
        proto_msg.value_map["str"].string_value = "test"
        proto_msg.value_map["null"].null_value = struct_pb2.NULL_VALUE
        
        # Convert to JSON
        json_str = json_format.MessageToJson(proto_msg)
        
        # Parse to Pydantic
        pydantic_model = value_demo_p2p.ValueTestMessage.model_validate_json(json_str)
        
        # Convert back to protobuf via JSON
        pydantic_json = pydantic_model.model_dump_json(by_alias=True)
        proto_msg_2 = json_format.Parse(pydantic_json, value_demo_pb2.ValueTestMessage())
        
        # Compare JSONs
        json_str_2 = json_format.MessageToJson(proto_msg_2)
        assert json.loads(json_str) == json.loads(json_str_2)
        
        # Verify specific values
        assert pydantic_model.id == "proto_first"
        assert pydantic_model.dynamic_value["name"] == "Alice"
        assert pydantic_model.dynamic_value["age"] == 25
        assert pydantic_model.dynamic_value["active"] is True
        assert pydantic_model.value_list == [42, "hello", False, None]
        assert pydantic_model.value_map["null"] is None

    def test_pydantic_to_protobuf_roundtrip_value(self):
        """Test Pydantic -> Protobuf -> Pydantic for Value fields."""
        # Create Pydantic model
        model = value_demo_p2p.ValueTestMessage(
            id="pydantic_first",
            dynamic_value={
                "nested": {
                    "array": [1, 2, 3],
                    "mixed": ["a", 1, True, None]
                },
                "simple": "value"
            },
            value_list=[
                {"object": "in_list"},
                [1, 2, 3],
                "string",
                42.5,
                True,
                None
            ],
            value_map={
                "complex": {"a": 1, "b": [2, 3]},
                "simple": "text",
                "number": 99,
                "null": None
            }
        )
        
        # Convert to protobuf via JSON
        json_str = model.model_dump_json(by_alias=True)
        proto_msg = json_format.Parse(json_str, value_demo_pb2.ValueTestMessage())
        
        # Convert to JSON
        json_str = json_format.MessageToJson(proto_msg)
        
        # Parse back to Pydantic
        model_2 = value_demo_p2p.ValueTestMessage.model_validate_json(json_str)
        
        # Compare models
        assert model.id == model_2.id
        assert model.dynamic_value == model_2.dynamic_value
        assert model.value_list == model_2.value_list
        assert model.value_map == model_2.value_map

    def test_protobuf_to_pydantic_roundtrip_timestamp(self):
        """Test Protobuf -> Pydantic -> Protobuf for Timestamp fields."""
        # Create protobuf message
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        # Set timestamps
        now = datetime.now(timezone.utc)
        proto_msg.created_at.FromDatetime(datetime(2023, 1, 1, tzinfo=timezone.utc))
        proto_msg.updated_at.FromDatetime(now)
        
        # Optional timestamp
        proto_msg.optional_timestamp.FromDatetime(datetime(2023, 6, 15, 10, 30, tzinfo=timezone.utc))
        
        # Repeated timestamps
        ts1 = proto_msg.event_timestamps.add()
        ts1.FromDatetime(datetime(2023, 1, 1, tzinfo=timezone.utc))
        ts2 = proto_msg.event_timestamps.add()
        ts2.FromDatetime(datetime(2023, 12, 31, tzinfo=timezone.utc))
        
        # Convert to JSON
        json_str = json_format.MessageToJson(proto_msg)
        
        # Parse to Pydantic
        pydantic_model = well_known_types_roundtrip_p2p.WellKnownTypesMessage.model_validate_json(json_str)
        
        # Convert back to protobuf via JSON
        pydantic_json = pydantic_model.model_dump_json(by_alias=True)
        proto_msg_2 = json_format.Parse(pydantic_json, well_known_types_roundtrip_pb2.WellKnownTypesMessage())
        
        # Compare timestamps
        assert proto_msg.created_at.ToDatetime() == proto_msg_2.created_at.ToDatetime()
        assert len(proto_msg.event_timestamps) == len(proto_msg_2.event_timestamps)
        
        # Verify Pydantic values
        assert pydantic_model.created_at.year == 2023
        assert pydantic_model.created_at.month == 1
        assert pydantic_model.created_at.day == 1
        assert len(pydantic_model.event_timestamps) == 2

    def test_pydantic_to_protobuf_roundtrip_timestamp(self):
        """Test Pydantic -> Protobuf -> Pydantic for Timestamp fields."""
        # Create Pydantic model
        now = datetime.now(timezone.utc)
        model = well_known_types_roundtrip_p2p.WellKnownTypesMessage(
            created_at=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            updated_at=now,
            expires_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            optional_timestamp=datetime(2023, 6, 15, tzinfo=timezone.utc),
            event_timestamps=[
                datetime(2023, 3, 1, tzinfo=timezone.utc),
                datetime(2023, 6, 1, tzinfo=timezone.utc),
                datetime(2023, 9, 1, tzinfo=timezone.utc)
            ]
        )
        
        # Convert to protobuf via JSON
        json_str = model.model_dump_json(by_alias=True)
        proto_msg = json_format.Parse(json_str, well_known_types_roundtrip_pb2.WellKnownTypesMessage())
        
        # Convert to JSON
        json_str = json_format.MessageToJson(proto_msg)
        
        # Parse back to Pydantic
        model_2 = well_known_types_roundtrip_p2p.WellKnownTypesMessage.model_validate_json(json_str)
        
        # Compare models
        assert model.created_at == model_2.created_at
        assert model.updated_at.replace(microsecond=0) == model_2.updated_at.replace(microsecond=0)
        assert len(model.event_timestamps) == len(model_2.event_timestamps)
        assert all(a == b for a, b in zip(model.event_timestamps, model_2.event_timestamps))

    def test_protobuf_to_pydantic_roundtrip_duration(self):
        """Test Protobuf -> Pydantic -> Protobuf for Duration fields."""
        # Create protobuf message
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        # Set durations
        proto_msg.timeout.FromTimedelta(timedelta(minutes=30))
        proto_msg.processing_time.FromTimedelta(timedelta(seconds=2, microseconds=500000))
        proto_msg.ttl.FromTimedelta(timedelta(hours=24))
        
        # Optional duration
        proto_msg.optional_duration.FromTimedelta(timedelta(minutes=15))
        
        # Repeated durations
        dur1 = proto_msg.intervals.add()
        dur1.FromTimedelta(timedelta(minutes=5))
        dur2 = proto_msg.intervals.add()
        dur2.FromTimedelta(timedelta(hours=1))
        
        # Convert to JSON
        json_str = json_format.MessageToJson(proto_msg)
        
        # Parse to Pydantic
        pydantic_model = well_known_types_roundtrip_p2p.WellKnownTypesMessage.model_validate_json(json_str)
        
        # Convert back to protobuf via JSON
        pydantic_json = pydantic_model.model_dump_json(by_alias=True)
        proto_msg_2 = json_format.Parse(pydantic_json, well_known_types_roundtrip_pb2.WellKnownTypesMessage())
        
        # Compare durations
        assert proto_msg.timeout.ToTimedelta() == proto_msg_2.timeout.ToTimedelta()
        assert proto_msg.processing_time.ToTimedelta() == proto_msg_2.processing_time.ToTimedelta()
        assert len(proto_msg.intervals) == len(proto_msg_2.intervals)
        
        # Verify Pydantic values
        assert pydantic_model.timeout == timedelta(minutes=30)
        assert pydantic_model.processing_time == timedelta(seconds=2.5)
        assert pydantic_model.ttl == timedelta(hours=24)

    def test_pydantic_to_protobuf_roundtrip_duration(self):
        """Test Pydantic -> Protobuf -> Pydantic for Duration fields."""
        # Create Pydantic model
        model = well_known_types_roundtrip_p2p.WellKnownTypesMessage(
            timeout=timedelta(seconds=60),
            processing_time=timedelta(milliseconds=123),
            ttl=timedelta(days=7),
            optional_duration=timedelta(hours=2, minutes=30),
            intervals=[
                timedelta(minutes=10),
                timedelta(minutes=20),
                timedelta(minutes=30),
                timedelta(hours=1)
            ]
        )
        
        # Convert to protobuf via JSON
        json_str = model.model_dump_json(by_alias=True)
        proto_msg = json_format.Parse(json_str, well_known_types_roundtrip_pb2.WellKnownTypesMessage())
        
        # Convert to JSON
        json_str = json_format.MessageToJson(proto_msg)
        
        # Parse back to Pydantic
        model_2 = well_known_types_roundtrip_p2p.WellKnownTypesMessage.model_validate_json(json_str)
        
        # Compare models
        assert model.timeout == model_2.timeout
        assert model.processing_time == model_2.processing_time
        assert model.ttl == model_2.ttl
        assert model.optional_duration == model_2.optional_duration
        assert len(model.intervals) == len(model_2.intervals)
        assert all(a == b for a, b in zip(model.intervals, model_2.intervals))

    def test_mixed_well_known_types_both_directions(self):
        """Test all well-known types together in both directions."""
        # Test data
        test_data = {
            "created_at": datetime(2023, 1, 1, tzinfo=timezone.utc),
            "timeout": timedelta(minutes=30),
            "event_timestamps": [
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 6, 15, tzinfo=timezone.utc)
            ],
            "intervals": [timedelta(hours=1), timedelta(minutes=30)]
        }
        
        # Direction 1: Pydantic -> Protobuf -> Pydantic
        model_1 = well_known_types_roundtrip_p2p.WellKnownTypesMessage(**test_data)
        json_1 = model_1.model_dump_json(by_alias=True)
        proto_1 = json_format.Parse(json_1, well_known_types_roundtrip_pb2.WellKnownTypesMessage())
        json_1_from_proto = json_format.MessageToJson(proto_1)
        model_1_back = well_known_types_roundtrip_p2p.WellKnownTypesMessage.model_validate_json(json_1_from_proto)
        
        # Direction 2: Protobuf -> Pydantic -> Protobuf
        proto_2 = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        proto_2.created_at.FromDatetime(test_data["created_at"])
        proto_2.timeout.FromTimedelta(test_data["timeout"])
        for ts in test_data["event_timestamps"]:
            proto_2.event_timestamps.add().FromDatetime(ts)
        for interval in test_data["intervals"]:
            proto_2.intervals.add().FromTimedelta(interval)
        
        json_2 = json_format.MessageToJson(proto_2)
        model_2 = well_known_types_roundtrip_p2p.WellKnownTypesMessage.model_validate_json(json_2)
        json_2_back = model_2.model_dump_json(by_alias=True)
        proto_2_back = json_format.Parse(json_2_back, well_known_types_roundtrip_pb2.WellKnownTypesMessage())
        
        # Verify both directions produce the same result
        # We need to compare only the fields that were originally set, since
        # Pydantic models add default values for unset fields
        json_1_dict = json.loads(json_1_from_proto)
        json_2_dict = json.loads(json_2)
        
        # Compare only the fields that exist in json_2 (the original protobuf)
        for key in json_2_dict:
            assert key in json_1_dict
            assert json_1_dict[key] == json_2_dict[key]
        assert model_1_back.created_at == model_2.created_at
        assert model_1_back.timeout == model_2.timeout

    def test_edge_cases_value_types(self):
        """Test edge cases for Value field types."""
        edge_cases = [
            # Empty collections
            {"id": "empty", "dynamic_value": {}, "value_list": [], "value_map": {}},
            # Deeply nested
            {
                "id": "nested",
                "dynamic_value": {
                    "level1": {
                        "level2": {
                            "level3": {
                                "data": [1, 2, {"level4": "deep"}]
                            }
                        }
                    }
                },
                "value_list": [],
                "value_map": {}
            },
            # Large numbers
            {
                "id": "numbers",
                "dynamic_value": {
                    "int": 9007199254740991,  # Max safe integer
                    "float": 3.141592653589793,
                    "negative": -1000000
                },
                "value_list": [0, -0, 1e10, -1e10],
                "value_map": {"inf": float('inf'), "neg_inf": float('-inf')}
            },
            # Unicode strings
            {
                "id": "unicode",
                "dynamic_value": {
                    "emoji": "🐍🔥",
                    "chinese": "你好世界",
                    "arabic": "مرحبا بالعالم"
                },
                "value_list": ["café", "naïve", "résumé"],
                "value_map": {"special": "line\nbreak\ttab"}
            }
        ]
        
        for test_case in edge_cases:
            # Pydantic -> Protobuf -> Pydantic
            model = value_demo_p2p.ValueTestMessage(**test_case)
            json_str = model.model_dump_json(by_alias=True)
            proto = json_format.Parse(json_str, value_demo_pb2.ValueTestMessage())
            json_str = json_format.MessageToJson(proto)
            model_back = value_demo_p2p.ValueTestMessage.model_validate_json(json_str)
            
            # Verify
            assert model.id == model_back.id
            if model.dynamic_value:
                assert model.dynamic_value == model_back.dynamic_value
            
            # Handle special float values
            if "inf" in test_case.get("value_map", {}):
                # JSON represents inf as string "Infinity" and it stays as string
                # through the protobuf Value field (since Value can hold strings)
                assert model_back.value_map["inf"] == "Infinity"
                assert model_back.value_map["neg_inf"] == "-Infinity"

    def test_null_and_none_handling(self):
        """Test proper handling of null/None values in all field types."""
        # Test with Value fields containing None
        model = value_demo_p2p.ValueTestMessage(
            id="null_test",
            dynamic_value=None,
            value_list=[None, "not_null", None],
            value_map={"key1": None, "key2": "value", "key3": None}
        )
        
        # Convert to protobuf and back via JSON
        json_str = model.model_dump_json(by_alias=True)
        proto = json_format.Parse(json_str, value_demo_pb2.ValueTestMessage())
        json_str = json_format.MessageToJson(proto)
        model_back = value_demo_p2p.ValueTestMessage.model_validate_json(json_str)
        
        # Verify None values are preserved
        assert model_back.dynamic_value is None
        assert model_back.value_list[0] is None
        assert model_back.value_list[2] is None
        assert model_back.value_map["key1"] is None
        assert model_back.value_map["key3"] is None

    def test_precision_preservation(self):
        """Test that timestamp and duration precision is preserved."""
        # Test microsecond precision for timestamps
        precise_time = datetime(2023, 1, 1, 12, 30, 45, 123456, tzinfo=timezone.utc)
        model = well_known_types_roundtrip_p2p.WellKnownTypesMessage(
            created_at=precise_time,
            timeout=timedelta(seconds=1, microseconds=123456)
        )
        
        # Roundtrip via JSON
        json_str = model.model_dump_json(by_alias=True)
        proto = json_format.Parse(json_str, well_known_types_roundtrip_pb2.WellKnownTypesMessage())
        json_str = json_format.MessageToJson(proto)
        model_back = well_known_types_roundtrip_p2p.WellKnownTypesMessage.model_validate_json(json_str)
        
        # Check precision (protobuf supports nanoseconds, but Python datetime only microseconds)
        assert model_back.created_at.microsecond == 123456
        assert model_back.timeout.total_seconds() == 1.123456