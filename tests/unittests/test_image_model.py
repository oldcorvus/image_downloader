from datetime import datetime

import pytest
from pydantic import ValidationError

from src.domain.entities import Image


def test_image_immutable():
    data = {
        "query": "cute puppies",
        "image_url": "http://example.com/image2.jpg",
        "image_data": b"someotherbinarydata",
        "width": 1024,
        "height": 768,
    }

    image = Image(**data)

    with pytest.raises(ValidationError):
        image.width = 800


def test_image_missing_required_fields():
    data = {
        "image_url": "http://example.com/image.jpg",
        "image_data": b"somebinarydata",
        "width": 800,
        "height": 600,
    }

    with pytest.raises(ValidationError):
        Image(**data)


def test_image_creation_success():
    data = {
        "query": "cute kittens",
        "image_url": "http://example.com/image.jpg",
        "image_data": b"somebinarydata",
        "width": 800,
        "height": 600,
    }

    image = Image(**data)

    assert image.query == data["query"]
    assert image.image_url == data["image_url"]
    assert image.image_data == data["image_data"]
    assert image.width == data["width"]
    assert image.height == data["height"]
    assert image.downloaded_at is not None
    assert isinstance(image.downloaded_at, datetime)


def test_image_creation_negative_width():
    data = {
        "query": "cute kittens",
        "image_url": "http://example.com/image.jpg",
        "image_data": b"somebinarydata",
        "width": -800,
        "height": 600,
    }

    with pytest.raises(ValidationError) as exc_info:
        Image(**data)
    assert "Width and height must be positive integers." in str(exc_info.value)
