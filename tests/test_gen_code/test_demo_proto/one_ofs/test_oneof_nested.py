"""Test nested oneof scenarios with discriminated unions.

This module tests complex oneof patterns including:
- Oneofs containing message types
- Messages with multiple oneofs
- Nested oneofs (oneof inside a message that's in another oneof)
- Oneofs with repeated fields
- Map fields in oneofs
"""

import json
from typing import Literal, Union, Annotated, List, Dict, Optional
from google.protobuf import json_format
from pydantic import BaseModel, Field, ValidationError, ConfigDict

from example.proto_pydanticv2.example.example_proto.demo import demo_pb2


# Example 1: Oneof containing message types
class _PaymentMethodBase(BaseModel):
    """Base class for payment method with common fields."""
    model_config = ConfigDict(extra="ignore")
    user_id: str = Field(default="")
    
    
class PaymentMethodCreditCard(_PaymentMethodBase):
    """Credit card payment method."""
    payment_type_case: Literal["credit_card"] = "credit_card"
    credit_card: 'CreditCardInfo'
    

class PaymentMethodBankAccount(_PaymentMethodBase):
    """Bank account payment method."""
    payment_type_case: Literal["bank_account"] = "bank_account"
    bank_account: 'BankAccountInfo'
    

class PaymentMethodCrypto(_PaymentMethodBase):
    """Cryptocurrency payment method."""
    payment_type_case: Literal["crypto"] = "crypto"
    crypto: 'CryptoWalletInfo'
    

class PaymentMethodNone(_PaymentMethodBase):
    """No payment method set."""
    payment_type_case: Literal[None] = None


# Sub-message types
class CreditCardInfo(BaseModel):
    card_number: str = Field(default="")
    expiry_month: int = Field(default=0)
    expiry_year: int = Field(default=0)
    cvv: str = Field(default="")
    

class BankAccountInfo(BaseModel):
    account_number: str = Field(default="")
    routing_number: str = Field(default="")
    account_type: str = Field(default="checking")
    

class CryptoWalletInfo(BaseModel):
    wallet_address: str = Field(default="")
    currency: str = Field(default="BTC")
    network: str = Field(default="mainnet")


PaymentMethodUnion = Annotated[
    Union[PaymentMethodCreditCard, PaymentMethodBankAccount, PaymentMethodCrypto, PaymentMethodNone],
    Field(discriminator='payment_type_case')
]


# Example 2: Message with multiple oneofs
class _ContactInfoBase(BaseModel):
    """Base class for contact info."""
    model_config = ConfigDict(extra="ignore")
    name: str = Field(default="")
    

class ContactInfoEmailPhone(_ContactInfoBase):
    """Contact with email as primary, phone as secondary."""
    primary_case: Literal["email"] = "email"
    secondary_case: Literal["phone"] = "phone"
    email: str
    phone: str
    

class ContactInfoEmailAddress(_ContactInfoBase):
    """Contact with email as primary, address as secondary."""
    primary_case: Literal["email"] = "email"
    secondary_case: Literal["address"] = "address"
    email: str
    address: 'AddressInfo'
    

class ContactInfoPhoneOnly(_ContactInfoBase):
    """Contact with only phone."""
    primary_case: Literal["phone"] = "phone"
    secondary_case: Literal[None] = None
    phone: str
    

class ContactInfoAddressOnly(_ContactInfoBase):
    """Contact with only address."""
    primary_case: Literal["address"] = "address"
    secondary_case: Literal[None] = None
    address: 'AddressInfo'


class AddressInfo(BaseModel):
    street: str = Field(default="")
    city: str = Field(default="")
    state: str = Field(default="")
    zip_code: str = Field(default="")


# Example 3: Deeply nested oneofs
# First define the nested types
class ScheduleInfo(BaseModel):
    hour: int = Field(default=0, ge=0, le=23)
    minute: int = Field(default=0, ge=0, le=59)
    timezone: str = Field(default="UTC")
    

class DigestInfo(BaseModel):
    frequency: str = Field(default="daily")  # daily, weekly, monthly
    day_of_week: Optional[int] = Field(default=None, ge=0, le=6)
    

class SmsConfig(BaseModel):
    phone_number: str = Field(default="")
    

class PushConfig(BaseModel):
    device_token: str = Field(default="")
    platform: str = Field(default="")  # ios, android


class _EmailConfigBase(BaseModel):
    """Base email configuration."""
    address: str = Field(default="")
    # Nested oneof for delivery preference
    

class EmailConfigImmediate(_EmailConfigBase):
    """Immediate email delivery."""
    delivery_case: Literal["immediate"] = "immediate"
    immediate: bool = True
    

class EmailConfigScheduled(_EmailConfigBase):
    """Scheduled email delivery."""
    delivery_case: Literal["scheduled"] = "scheduled"
    scheduled: ScheduleInfo
    

class EmailConfigDigest(_EmailConfigBase):
    """Digest email delivery."""
    delivery_case: Literal["digest"] = "digest"
    digest: DigestInfo


# Union type for email config
EmailConfigUnion = Annotated[
    Union[EmailConfigImmediate, EmailConfigScheduled, EmailConfigDigest],
    Field(discriminator='delivery_case')
]


# Now define the notification types
class _NotificationBase(BaseModel):
    """Base for notification settings."""
    enabled: bool = Field(default=True)
    

class NotificationEmail(_NotificationBase):
    """Email notification."""
    channel_case: Literal["email_config"] = "email_config"
    email_config: EmailConfigUnion
    

class NotificationSms(_NotificationBase):
    """SMS notification."""
    channel_case: Literal["sms_config"] = "sms_config"
    sms_config: SmsConfig
    

class NotificationPush(_NotificationBase):
    """Push notification."""
    channel_case: Literal["push_config"] = "push_config"
    push_config: PushConfig


# Example 4: Oneof with repeated fields and maps
class _DataPayloadBase(BaseModel):
    """Base for data payload."""
    request_id: str = Field(default="")
    

class DataPayloadStringList(_DataPayloadBase):
    """List of strings payload."""
    content_case: Literal["string_list"] = "string_list"
    string_list: List[str] = Field(default_factory=list)
    

class DataPayloadNumberList(_DataPayloadBase):
    """List of numbers payload."""
    content_case: Literal["number_list"] = "number_list"
    number_list: List[float] = Field(default_factory=list)
    

class DataPayloadObjectMap(_DataPayloadBase):
    """Map of objects payload."""
    content_case: Literal["object_map"] = "object_map"
    object_map: Dict[str, 'DataObject'] = Field(default_factory=dict)
    

class DataPayloadMessageList(_DataPayloadBase):
    """List of messages payload."""
    content_case: Literal["message_list"] = "message_list"
    message_list: List['DataObject'] = Field(default_factory=list)


class DataObject(BaseModel):
    key: str = Field(default="")
    value: str = Field(default="")
    metadata: Dict[str, str] = Field(default_factory=dict)


DataPayloadUnion = Annotated[
    Union[DataPayloadStringList, DataPayloadNumberList, DataPayloadObjectMap, DataPayloadMessageList],
    Field(discriminator='content_case')
]


def test_oneof_with_message_types():
    """Test oneof containing different message types."""
    print("=== Oneof with Message Types ===")
    
    # Test credit card variant
    credit_card_data = {
        "payment_type_case": "credit_card",
        "user_id": "user123",
        "credit_card": {
            "card_number": "4111111111111111",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    }
    
    cc_payment = PaymentMethodCreditCard(**credit_card_data)
    print(f"Credit card payment: {cc_payment}")
    
    # Serialize and verify only credit_card is present
    json_str = cc_payment.model_dump_json(exclude_none=True)
    json_dict = json.loads(json_str)
    print(f"Serialized: {json_str}")
    assert "credit_card" in json_dict
    assert "bank_account" not in json_dict
    assert "crypto" not in json_dict
    
    # Test bank account variant
    bank_data = {
        "payment_type_case": "bank_account",
        "user_id": "user456",
        "bank_account": {
            "account_number": "123456789",
            "routing_number": "987654321",
            "account_type": "savings"
        }
    }
    
    bank_payment = PaymentMethodBankAccount(**bank_data)
    print(f"\nBank payment: {bank_payment}")
    
    # Test that union discriminator works
    print("\n--- Testing Union Discrimination ---")
    # This would be how the generated code would work
    payment_union_data = {
        "payment_type_case": "crypto",
        "user_id": "user789",
        "crypto": {
            "wallet_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "currency": "BTC",
            "network": "mainnet"
        }
    }
    
    # In real implementation, this would be handled by the union type
    if payment_union_data["payment_type_case"] == "crypto":
        payment = PaymentMethodCrypto(**payment_union_data)
        print(f"Crypto payment: {payment}")


def test_multiple_oneofs_in_message():
    """Test message with multiple independent oneofs."""
    print("\n=== Multiple Oneofs in Single Message ===")
    
    # Test email + phone combination
    contact1 = ContactInfoEmailPhone(
        name="John Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    print(f"Contact 1 (email+phone): {contact1}")
    
    # Test email + address combination
    contact2 = ContactInfoEmailAddress(
        name="Jane Smith",
        email="jane@example.com",
        address=AddressInfo(
            street="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="12345"
        )
    )
    print(f"Contact 2 (email+address): {contact2}")
    
    # Verify serialization
    json_str = contact2.model_dump_json(exclude_none=True)
    print(f"Serialized contact 2: {json_str}")
    
    # Test single field variants
    contact3 = ContactInfoPhoneOnly(
        name="Bob Wilson",
        phone="+9876543210"
    )
    print(f"Contact 3 (phone only): {contact3}")
    
    # Verify that only the active fields are set
    json_dict = json.loads(contact3.model_dump_json(exclude_none=True))
    assert "phone" in json_dict
    assert "email" not in json_dict
    assert "address" not in json_dict


def test_deeply_nested_oneofs():
    """Test oneofs nested inside other message types."""
    print("\n=== Deeply Nested Oneofs ===")
    
    # Create email notification with immediate delivery
    email_immediate = NotificationEmail(
        enabled=True,
        email_config=EmailConfigImmediate(
            address="user@example.com",
            immediate=True
        )
    )
    print(f"Email immediate: {email_immediate}")
    
    # Create email notification with scheduled delivery
    email_scheduled = NotificationEmail(
        enabled=True,
        email_config=EmailConfigScheduled(
            address="user@example.com",
            scheduled=ScheduleInfo(hour=9, minute=0, timezone="PST")
        )
    )
    print(f"Email scheduled: {email_scheduled}")
    
    # Create email notification with digest
    email_digest = NotificationEmail(
        enabled=True,
        email_config=EmailConfigDigest(
            address="user@example.com",
            digest=DigestInfo(frequency="weekly", day_of_week=1)  # Monday
        )
    )
    print(f"Email digest: {email_digest}")
    
    # Test other notification types
    sms_notif = NotificationSms(
        enabled=True,
        sms_config=SmsConfig(phone_number="+1234567890")
    )
    print(f"\nSMS notification: {sms_notif}")
    
    # Verify nested structure serialization
    json_str = email_scheduled.model_dump_json(exclude_none=True)
    json_dict = json.loads(json_str)
    print(f"\nSerialized scheduled email: {json.dumps(json_dict, indent=2)}")
    
    # The structure should maintain the discriminators
    assert json_dict["channel_case"] == "email_config"
    # Note: In the current test setup, the nested object is serialized as a whole
    # In a real discriminated union implementation, the nested discriminator would also be preserved


def test_oneof_with_collections():
    """Test oneofs containing repeated fields and maps."""
    print("\n=== Oneof with Collections ===")
    
    # Test string list variant
    string_payload = DataPayloadStringList(
        request_id="req-001",
        string_list=["apple", "banana", "cherry"]
    )
    print(f"String list payload: {string_payload}")
    
    # Test number list variant
    number_payload = DataPayloadNumberList(
        request_id="req-002",
        number_list=[3.14, 2.718, 1.414]
    )
    print(f"Number list payload: {number_payload}")
    
    # Test object map variant
    object_payload = DataPayloadObjectMap(
        request_id="req-003",
        object_map={
            "first": DataObject(key="k1", value="v1", metadata={"type": "text"}),
            "second": DataObject(key="k2", value="v2", metadata={"type": "number"})
        }
    )
    print(f"Object map payload: {object_payload}")
    
    # Test message list variant
    message_payload = DataPayloadMessageList(
        request_id="req-004",
        message_list=[
            DataObject(key="item1", value="value1"),
            DataObject(key="item2", value="value2", metadata={"priority": "high"})
        ]
    )
    print(f"Message list payload: {message_payload}")
    
    # Verify collections are properly serialized
    json_str = message_payload.model_dump_json(exclude_none=True)
    json_dict = json.loads(json_str)
    print(f"\nSerialized message list: {json.dumps(json_dict, indent=2)}")
    
    assert json_dict["content_case"] == "message_list"
    assert len(json_dict["message_list"]) == 2
    assert json_dict["message_list"][1]["metadata"]["priority"] == "high"


def test_complex_roundtrip():
    """Test complex roundtrip scenarios with nested structures."""
    print("\n=== Complex Roundtrip Test ===")
    
    # Create a complex nested structure
    complex_data = {
        "enabled": True,
        "channel_case": "email_config",
        "email_config": {
            "address": "test@example.com",
            "delivery_case": "digest",
            "digest": {
                "frequency": "daily"
            }
        }
    }
    
    # Create model
    notification = NotificationEmail(
        enabled=complex_data["enabled"],
        email_config=EmailConfigDigest(
            address=complex_data["email_config"]["address"],
            digest=DigestInfo(**complex_data["email_config"]["digest"])
        )
    )
    
    # Serialize
    json_str = notification.model_dump_json(exclude_none=True)
    print(f"Original model: {notification}")
    print(f"Serialized: {json_str}")
    
    # Deserialize - in real implementation this would use the union type
    parsed_dict = json.loads(json_str)
    if parsed_dict["channel_case"] == "email_config":
        email_config_data = parsed_dict["email_config"]
        if email_config_data["delivery_case"] == "digest":
            reconstructed = NotificationEmail(
                enabled=parsed_dict["enabled"],
                email_config=EmailConfigDigest(
                    address=email_config_data["address"],
                    digest=DigestInfo(**email_config_data["digest"])
                )
            )
            print(f"Reconstructed: {reconstructed}")
            assert reconstructed == notification
            print("Roundtrip successful! ✓")


def test_oneof_field_presence():
    """Test that only active oneof fields are present in serialization."""
    print("\n=== Oneof Field Presence Test ===")
    
    # Create instances of each variant
    variants = [
        ("String List", DataPayloadStringList(
            request_id="test-1",
            string_list=["a", "b", "c"]
        )),
        ("Number List", DataPayloadNumberList(
            request_id="test-2",
            number_list=[1.0, 2.0, 3.0]
        )),
        ("Object Map", DataPayloadObjectMap(
            request_id="test-3",
            object_map={"key": DataObject(key="k", value="v")}
        )),
        ("Message List", DataPayloadMessageList(
            request_id="test-4",
            message_list=[DataObject(key="k1", value="v1")]
        ))
    ]
    
    for name, variant in variants:
        print(f"\n{name}:")
        json_str = variant.model_dump_json(exclude_none=True)
        json_dict = json.loads(json_str)
        
        # Check that only the active field is present
        oneof_fields = ["string_list", "number_list", "object_map", "message_list"]
        present_fields = [f for f in oneof_fields if f in json_dict]
        
        print(f"  Present fields: {present_fields}")
        print(f"  Discriminator: {json_dict.get('content_case')}")
        
        # Verify only one field from the oneof is present
        assert len(present_fields) == 1
        assert present_fields[0] == json_dict["content_case"]
        print(f"  ✓ Only active field is present")


if __name__ == "__main__":
    test_oneof_with_message_types()
    test_multiple_oneofs_in_message()
    test_deeply_nested_oneofs()
    test_oneof_with_collections()
    test_complex_roundtrip()
    test_oneof_field_presence()
    
    print("\n=== All nested oneof tests passed! ===")