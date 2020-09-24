#!/usr/bin/env python

def error_document(message):
    """
    Create a dictionary suitable to be passed to the API to represent
    error states

    :param message: str
    :return: dict
    """
    return {'error': str(message)}
