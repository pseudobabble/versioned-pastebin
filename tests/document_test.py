#!/usr/bin/env python

from datetime import datetime

import pytest

from models.document import Document
from models.revision import Revision


def test__assertTrue():
    assert True


class TestDocument:

    def test__get_id(self):
        document = Document(id=5, title='blah')

        assert document.get_id() == 5

    def test__get_title(self):
        document = Document(id=5, title='blah')

        assert document.get_title() == 'blah'

    def test__get_revision_by_timestamp(self):
        timestamp = datetime(2020, 1, 1, 1, 1, 1)

        revision = Revision(
            id=1,
            content='hello',
            timestamp=timestamp,
            document_id=5
        )

        document = Document(
            id=5,
            title='blah',
            revisions=[revision]
        )

        assert document.get_revision_by_timestamp(timestamp) == revision

    def test__get_revision_by_timestamp_expect_most_recent(self):
        timestamp = datetime(2020, 1, 1, 1, 1, 1)
        timestamp_latest = datetime(2020, 2, 1, 1, 1, 1)
        timestamp_in_between = datetime(2020, 1, 29, 1, 1, 1)

        revision = Revision(
            id=1,
            content='hello',
            timestamp=timestamp,
            document_id=5
        )

        revision_latest = Revision(
            id=2,
            content='hello again',
            timestamp=timestamp_latest,
            document_id=5
        )

        document = Document(
            id=5,
            title='blah',
            revisions=[revision, revision_latest]
        )

        assert document.get_revision_by_timestamp(timestamp_in_between) == revision

    def test__get_latest_revision(self):
        timestamp = datetime(2020, 1, 1, 1, 1, 1)
        timestamp_latest = datetime(2020, 2, 1, 1, 1, 1)

        revision = Revision(
            id=1,
            content='hello',
            timestamp=timestamp,
            document_id=5
        )

        revision_latest = Revision(
            id=2,
            content='hello again',
            timestamp=timestamp_latest,
            document_id=5
        )

        document = Document(
            id=5,
            title='blah',
            revisions=[revision, revision_latest]
        )

        assert document.get_latest_revision() == revision_latest

