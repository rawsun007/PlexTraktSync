from __future__ import annotations

from plextraktsync.trakt.TraktUserList import TraktUserList


class FakePersonalList:
    """
    Stands in for trakt.users.UserList, which has no __len__ and loads its
    items lazily: _items stays None until the items property is read.
    """

    name = "My List"
    description = "a description"

    def __init__(self, items):
        self._loaded = items
        self._items = None

    @property
    def items(self):
        if self._items is None:
            self._items = self._loaded
        return self._items


class FakeTraktApi:
    def __init__(self, user_list):
        self.user_list = user_list

    @property
    def me(self):
        class Me:
            username = "someone"

        return Me()

    def get_personal_list(self, username, listname):
        return self.user_list


def test_personal_list_is_downloaded(monkeypatch):
    user_list = FakePersonalList([])
    monkeypatch.setattr(
        "plextraktsync.factory.factory.trakt_api",
        FakeTraktApi(user_list),
        raising=False,
    )

    tl = TraktUserList(
        trakt_id=1,
        name="My List",
        username="someone",
        list_type="personal",
    )
    description, items = tl.load_items()

    assert description == "a description"
    assert items == {}


def test_personal_list_reads_items_through_the_property(monkeypatch):
    """The lazy property is what populates _items, so reading it is required."""
    user_list = FakePersonalList([])
    monkeypatch.setattr(
        "plextraktsync.factory.factory.trakt_api",
        FakeTraktApi(user_list),
        raising=False,
    )

    tl = TraktUserList(
        trakt_id=1,
        name="My List",
        username="someone",
        list_type="personal",
    )
    tl.load_items()

    assert user_list._items is not None
