import pytest
from unittest.mock import AsyncMock
from services.restaurant_service import RestaurantService
from models.restaurant import Restaurant

@pytest.mark.asyncio
async def test_search_returns_from_cache():
    # Arrange
    mock_cached_data = [
        {
            "id": "123",
            "name": "Cached Restaurant",
            "address": "123 Main St",
            "city": "Cache City",
            "rating": 4.5,
            "phone": "123-456-7890",
            "url": "http://example.com",
            "categories": ["Italian"],
            "distance_meters": 100
        }
    ]

    mock_redis = AsyncMock()
    mock_redis.get.return_value = mock_cached_data
    mock_yelp = AsyncMock()  # Yelp shouldn't be called in this test

    service = RestaurantService(redis_service=mock_redis, yelp=mock_yelp)

    # Act
    results = await service.search(term="pizza", limit=1)

    # Assert
    assert len(results) == 1
    assert isinstance(results[0], Restaurant)
    assert results[0].name == "Cached Restaurant"
    mock_redis.get.assert_awaited_once()
    mock_yelp.search.assert_not_awaited()


@pytest.mark.asyncio
async def test_search_calls_yelp_when_cache_empty():
    # Arrange
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None
    mock_redis.set = AsyncMock()

    mock_yelp = AsyncMock()
    mock_yelp.search.return_value = [
        {
            "id": "456",
            "name": "Yelp Restaurant",
            "location": {"display_address": ["456 Elm St"], "city": "Yelp City"},
            "rating": 4.0,
            "display_phone": "987-654-3210",
            "url": "http://yelp.com",
            "categories": [{"title": "Sushi"}],
            "distance": 200
        }
    ]

    service = RestaurantService(redis_service=mock_redis, yelp=mock_yelp)

    # Act
    results = await service.search(term="sushi", limit=1)

    # Assert
    assert len(results) == 1
    assert results[0].name == "Yelp Restaurant"
    mock_redis.get.assert_awaited_once()
    mock_yelp.search.assert_awaited_once()
    mock_redis.set.assert_awaited_once()


@pytest.mark.asyncio
async def test_search_returns_empty_on_yelp_exception():
    # Arrange
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None

    mock_yelp = AsyncMock()
    mock_yelp.search.side_effect = Exception("Yelp API error")

    service = RestaurantService(redis_service=mock_redis, yelp=mock_yelp)

    # Act
    results = await service.search(term="error_test", limit=1)

    # Assert
    assert results == []
    mock_redis.get.assert_awaited_once()
    mock_yelp.search.assert_awaited_once()


@pytest.mark.asyncio
async def test_business_to_restaurant_mapping():
    # Arrange
    biz = {
        "id": "789",
        "name": "Mapped Restaurant",
        "location": {"display_address": ["789 Pine St"], "city": "Map City"},
        "rating": 4.8,
        "display_phone": "555-1234",
        "url": "http://mapped.com",
        "categories": [{"title": "Mexican"}, {"title": "Bar"}],
        "distance": 500
    }

    # Act
    restaurant = RestaurantService._business_to_restaurant(biz)

    # Assert
    assert restaurant.id == "789"
    assert restaurant.name == "Mapped Restaurant"
    assert restaurant.address == "789 Pine St"
    assert restaurant.city == "Map City"
    assert restaurant.rating == 4.8
    assert restaurant.phone == "555-1234"
    assert restaurant.url == "http://mapped.com"
    assert restaurant.categories == ["Mexican", "Bar"]
    assert restaurant.distance_meters == 500
