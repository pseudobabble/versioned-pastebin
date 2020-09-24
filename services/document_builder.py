#!/usr/bin/env python

from infrastructure.repository.base_adaptor import BaseAdaptor
from services.document_repository import DocumentRepository
from services.exception.invalid_data import InvalidDataException

from models.document import Document
from models.revision import Revision


class DocumentBuilder:
    """
    DocumentBuilder builds Documents from data carrying dictionaries
    """
    def __init__(self, document_repository: BaseAdaptor = DocumentRepository):
        """
        Initialise the DocumentBuilder with a persistence adaptor.

        :param document_repository: BaseAdaptor
        """
        self.document_repository = document_repository()

    def build_document(self, data_dict: dict) -> None:
        """
        Build a Document from the data passed in.

        :param data_dict: dict
        """
        self._validate_data(data_dict)

        document = self.document_repository.get_by_title(data_dict['title'])

        if document:
            new_revision = Revision(content=data_dict['content'])
            document.revisions.append(new_revision)
            self.document_repository.save(document)
        else:
            revision = Revision(content=data_dict['content'])
            document = Document(title=data_dict['title'], revisions=[revision])
            self.document_repository.save(document)

    def _validate_data(self, data_dict: dict) -> None:
        """
        Validate data passed in to the DocumentBuilder

        :param data_dict:dict
        """
        if 'content' not in data_dict:
            raise InvalidDataException(
                "'content' key missing from request body"
            )
