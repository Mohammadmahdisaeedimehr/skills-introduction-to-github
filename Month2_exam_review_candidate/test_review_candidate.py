from review_candidate import find_user


def test_find_user():
    assert find_user("ali_data") is not None
