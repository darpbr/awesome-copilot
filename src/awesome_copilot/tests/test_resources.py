from awesome_copilot.resources import get_resources




def test_store_set_get():
    res = get_resources()
    store = res["store"]
    store.set("x", 10)
    assert store.get("x") == 10