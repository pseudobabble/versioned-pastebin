#!/usr/bin/env python

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure import repository


class Revision(repository.Base):
    """
    A Revision represents the content of a Document at a particular time and
    date
    """
    __tablename__ = 'revisions'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    document_id = Column(Integer, ForeignKey('documents.id'))
    document = relationship('Document', back_populates='revisions')

    def get_id(self) -> int:
        """
        Get the id of the current Revision.

        :return: int
        """
        return self.id

    def get_content(self) -> str:
        """
        Get the text content of the current Revision.

        :return: str
        """
        return self.content

    def get_timestamp(self) -> datetime:
        """
        Get the datetime at which the current Revision was added.

        :return: datetime
        """
        return self.timestamp

    def get_document_id(self) -> int:
        """
        Get the id of the Document the current Revision belongs to

        :return: int
        """
        return self.document_id

    def __ge__(self, other: 'Revision') -> bool:
        """
        Determine which Revision has a greater or equal timestamp

        :param other: Revision
        :return: bool
        """
        return self.timestamp >= other.timestamp

    def __le__(self, other: 'Revision') -> bool:
        """
        Determine which Revision has a less than or equal timestamp

        :param other: Revision
        :return: bool
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other: 'Revision') -> bool:
        """
        Determine which Revision has a greater timestamp

        :param other: Revision
        :return: bool
        """
        return self.timestamp > other.timestamp

    def __lt__(self, other: 'Revision') -> bool:
        """
        Determine which Revision has a lesser timestamp

        :param other: Revision
        :return: bool
        """
        return self.timestamp < other.timestamp

