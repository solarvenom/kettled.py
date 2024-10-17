from nuthatch.types import StorageEvent

def test_storage_event():
    test_name = "test_name"
    test_date = "2024-10-17 09:57:28"
    test_timestamp = 1729151848
    test_phrase = "Sitta europaea"

    def test_callback():
        return test_phrase

    test_event = StorageEvent(
        name=test_name,
        date_time=test_date,
        callback=lambda: test_callback()
    )

    assert test_event.name == test_name
    assert test_event.expires_at == test_timestamp
    assert test_event.callback() == test_phrase