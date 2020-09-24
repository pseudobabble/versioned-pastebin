#!/usr/bin/env python

from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from infrastructure import repository
from models.revision import Revision


class Document(repository.Base):
    """
    A Document represents a versioned text document.

    Document is the Aggregate Root of the model. Revisions must be retrieved
    via a Document. Neither a Revision without a Document, nor a Document
    without at least one Revision, make sense in this domain.
    """
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=50), unique=True)
    revisions = relationship('Revision', back_populates='document')

    def get_id(self) -> int:
        """
        Get the id of the current Document.

        :return: int
        """
        return self.id

    def get_title(self) -> str:
        """
        Get the title of the current Document.

        :return: str
        """
        return self.title

    def get_revision_by_timestamp(self, timestamp: datetime) -> Revision:
        """
        Get the Revision belonging to the current Document, whose timestamp
        is most recent with regard to the passed datetime.

        :param timestamp: datetime
        :return: Revision
        """
        return self._get_closest_revision(self.revisions, timestamp)

    def get_latest_revision(self) -> Revision:
        """
        Get the latest Revision belonging to the current Document.

        :return: Revision
        """
        return max(self.revisions)

    def _get_closest_revision(
            self,
            revisions: list,
            target: datetime
    ) -> Revision:
        """
        Return that Revision whose timestamp is closest to the passed in
        datetime.

        :param revisions: List[Revision]
        :param target: datetime
        :return: Revision
        """
        revisions = [
            revision for revision in revisions if revision.timestamp <= target
        ]

        return max(revisions)

