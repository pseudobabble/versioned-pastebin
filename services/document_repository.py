#!/usr/bin/env python

from datetime import datetime
from typing import List

from infrastructure.repository.sqlalchemy_adaptor import SqlAlchemyAdaptor
from models.document import Document

DocumentList = List[Document]


class DocumentRepository(SqlAlchemyAdaptor):
    """
    The DocumentRepository represents a collection of Documents.

    It is the means by which Documents and their associated Revisions are
    retrieved from and posted to persistent storage.
    """

    entity = Document

    def get_all(self) -> DocumentList:
        """
        Get all Documents in storage

        :return: DocumentList
        """
        return self.session.query(self.entity).all()

    def get_by_title(self, title: str) -> Document:
        """
        Get a Document and associated Revisions by Document title

        :param title: str
        :return: Document
        """
        return self.session.query(self.entity).filter_by(title=title).first()

    def get_revisions(self, title: str) -> Document:
        """
        Get the Revisions associated with a Document, by Document title.

        Document is the Aggregate Root - Revisions are always associated with a
        Document, and a Revision without a Document does not make sense in the
        domain. Getting a Document and it's associated Revisions, and getting
        the Revisions associated with a Document, are the same operation, from
        the domain perspective. However, from the perspective of the client
        code, the Document itself may be irrelevant to the task at hand, other
        than as the key by which Revisions are retrieved, meaning that although
        this method has the same implementation as get_by_title(), the two
        should be distinguished on the interface.


        :param title: str
        :return: Document
        """
        return self.get_by_title(title)

    def get_revision(self, title: str, timestamp: datetime) -> Document:
        """
        Get a Document with a single Revision whose timestamp is closest to
        the provided timestamp.

        :param title: str
        :param timestamp: datetime
        :return: Document
        """
        document = self.get_by_title(title)
        revision = document.get_revision_by_timestamp(timestamp)
        document.revisions = [revision]

        return document

    def get_latest(self, title: str) -> Document:
        """
        Get a Document with a singe Revision whose timestamp is the latest of
        those Revisions belonging to the Document.

        :param title: str
        :return: Document
        """
        document = self.get_by_title(title)
        revision = document.get_latest_revision()
        document.revisions = [revision]

        return document



