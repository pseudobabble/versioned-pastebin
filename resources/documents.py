#!/usr/bin/env python

from datetime import datetime

from flask import request
from flask_restful import Resource
from marshmallow import Schema

from infrastructure.repository.base_adaptor import BaseAdaptor
from infrastructure.repository.exception.entity_not_found import \
    EntityNotFoundException
from resources.exception.error_document import error_document
from services.document_builder import DocumentBuilder
from services.document_repository import DocumentRepository

from resources.schemata.document import DocumentSchema
from services.exception.invalid_data import InvalidDataException


class Documents(Resource):
    '''
    The Documents resource represents the ways that Document objects can be
    retrieved from the api
    '''

    def __init__(
            self,
            document_builder: DocumentBuilder = DocumentBuilder,
            document_repository: BaseAdaptor = DocumentRepository,
            document_schema: Schema = DocumentSchema
    ):
        """
        This method initialises the Documents resource with it's dependencies

        :param document_builder: DocumentBuilder
        :param document_repository: BaseAdaptor
        :param document_schema: Schema
        """
        self.document_builder = document_builder()
        self.document_repository = document_repository()
        self.document_schema = document_schema()

    def get(
            self,
            title: str = None,
            timestamp: str = None,
            latest: str = None
    ) -> dict:
        """
        Retrieve Documents from the Documents resource by various parameters

        :param title: str
        :param timestamp: datetime
        :param latest: str
        :return: dict
        """
        if timestamp and latest:
            raise ValueError(
                'Cannot request by latest timestamp and specific timestamp.'
            )

        documents = self.document_repository.get_all()
        document = {'documents': [document.title for document in documents]}

        if title:
            try:
                document = self.document_repository.get_by_title(title)
                document = self.document_schema.dump(document)
            except EntityNotFoundException:
                document = error_document(
                    'Document with title {} not found'.format(title)
                )

        if timestamp:
            try:
                document = self._get_for_timestamp(timestamp, title)
            except ValueError:
                document = error_document(
                    'Bad timestamp format. ' +
                    'Correct format is YYYY-MM-DD-HH:MM:SS'
                )
            except EntityNotFoundException:
                document = error_document(
                    'Document with title {} was not found.'.format(title)
                )

        if latest:
            try:
                document = self._get_latest(title)
            except EntityNotFoundException:
                document = error_document(
                    'Document with title {} was not found.'.format(title)
                )

        return document

    def post(self, title: str) -> None:
        """
        Create Documents by receiving POST requests with data specified as JSON
        in the request body

        :param title: str
        :return: dict
        """
        data_dict = request.get_json()
        data_dict['title'] = title

        response = {'success': 200}
        try:
            self.document_builder.build_document(data_dict)
        except InvalidDataException:
            response = error_document(
                "Bad request format, missing 'content' key"
            )

        return response

    def _get_for_timestamp(self, timestamp, title):
        """
        Retrieve a Document and the associated Revision whose timestamp is the
        most recent relative to the passed timestamp

        :param timestamp: datetime
        :param title: str
        :return: Document
        """
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d-%H:%M:%S')
        document = self.document_repository.get_by_title(title)
        try:
            revision = document.get_revision_by_timestamp(timestamp)
            document.revisions = [revision]
        except ValueError:
            document.revisions = []
        document = self.document_schema.dump(document)
        return document

    def _get_latest(self, title):
        """
        Get the latest Revision for the requested Document

        :param title: str
        :return: Document
        """
        document = self.document_repository.get_by_title(title)
        try:
            revision = document.get_latest_revision()
            document.revisions = [revision]
        except ValueError:
            document.revisions = []
        document = self.document_schema.dump(document)
        return document


