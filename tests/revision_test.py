#!/usr/bin/env python

from datetime import datetime

import pytest

from models.revision import Revision


def test__assertTrue():
    assert True


class TestRevision:

    def test__get_id(self):
        revision = Revision(
            id=1,
            content='hello',
            timestamp=datetime(2020, 1, 1, 1, 1, 1),
            document_id=5
        )

        assert revision.get_id() == 1

    def test__get_content(self):
        revision = Revision(
            id=1,
            content='hello',
            timestamp=datetime(2020, 1, 1, 1, 1, 1),
            document_id=5
        )

        assert revision.get_content() == 'hello'

    def test__get_timestamp(self):
        timestamp = datetime(2020, 1, 1, 1, 1, 1)

        revision = Revision(
            id=1,
            content='hello',
            timestamp=timestamp,
            document_id=5
        )

        assert revision.get_timestamp() == timestamp

    def test__get_document_id(self):
        revision = Revision(
            id=1,
            content='hello',
            timestamp=datetime(2020, 1, 1, 1, 1, 1),
            document_id=5
        )

        assert revision.get_document_id() == 5

    def test__gt_lt(self):
        timestamp_lesser = datetime(2020, 1, 1, 1, 1, 1)
        timestamp_greater = datetime(2020, 1, 1, 1, 1, 2)

        revision_lesser = Revision(
            id=1,
            content='hello',
            timestamp=timestamp_lesser,
            document_id=5
        )

        revision_greater = Revision(
            id=2,
            content='hello',
            timestamp=timestamp_greater,
            document_id=5
        )

        assert revision_greater > revision_lesser
        assert revision_lesser < revision_greater

    def test__ge_le(self):
        timestamp = datetime(2020, 1, 1, 1, 1, 1)
        timestamp_equal = datetime(2020, 1, 1, 1, 1, 1)

        revision = Revision(
            id=1,
            content='hello',
            timestamp=timestamp,
            document_id=5
        )

        revision_equal = Revision(
            id=2,
            content='hello',
            timestamp=timestamp_equal,
            document_id=5
        )

        assert revision >= revision_equal
        assert revision_equal >= revision

        assert revision <= revision_equal
        assert revision_equal <= revision


