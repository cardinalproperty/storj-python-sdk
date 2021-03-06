# -*- coding: utf-8 -*-
"""Storj package."""

import io


from abc import ABCMeta
from hashlib import sha256

from .api import ecdsa_to_hex
from .configuration import read_config
from .http import Client
from .metadata import __version__
from .model import Bucket, File, Token


def get_client():
    """Returns a pre-configured Storj HTTP client.

    Returns:
        (:py:class:`storj.http.Client`): Storj HTTP client.
    """
    return Client(*read_config())


class BucketManager(ABCMeta):
    """Class to manage buckets."""

    @staticmethod
    def all():
        buckets_json = get_client().bucket_list()
        return [Bucket(payload) for payload in buckets_json]

    @staticmethod
    def get(bucket_id):
        bucket_json = get_client().bucket_get(bucket_id=bucket_id)
        return Bucket(bucket_json)

    @staticmethod
    def create(name, storage_limit=None, transfer_limit=None):
        """Create bucket.

        Args:
            name (str):.
            storage_limit ():.
            transfer_limit ():.
        """
        bucket_json = get_client().bucket_create(
            name=name,
            storage=storage_limit,
            transfer=transfer_limit,
        )
        return Bucket(bucket_json)

    @staticmethod
    def delete(bucket_id):
        """Remove bucket.

        Args:
            bucket_id (int): bucket unique identifier.
        """
        get_client().bucket_delete(bucket_id=bucket_id)


class BucketKeyManager:
    """

    Attributes:
        bucket ():
    """

    def __init__(self, bucket, authorized_public_keys):
        self.bucket = bucket
        self._authorized_public_keys = authorized_public_keys

    def all(self):
        """"""
        return self._authorized_public_keys

    def add(self, key):
        """"""
        if not isinstance(key, str):
            key = ecdsa_to_hex(key)

        self._authorized_public_keys.append(key)
        get_client().bucket_set_keys(
            bucket_id=self.bucket.id,
            keys=self._authorized_public_keys)

    def clear(self):
        """"""
        self._authorized_public_keys = []
        get_client().bucket_set_keys(bucket_id=self.bucket.id, keys=[])

    def remove(self, key):
        """"""
        if not isinstance(key, str):
            key = ecdsa_to_hex(key)

        self._authorized_public_keys.remove(key)
        get_client().bucket_set_keys(
            bucket_id=self.bucket.id,
            keys=self._authorized_public_keys)


class FileManager:
    """"""

    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    def _upload(self, file, frame):
        """"""
        get_client().file_upload(
            bucket_id=self.bucket_id, file=file, frame=frame)

    def all(self):
        """"""
        files_json = get_client().file_list(bucket_id=self.bucket_id)
        return [File(payload) for payload in files_json]

    def delete(self, bucket_id, file_id):
        """"""
        get_client().file_remove(self, bucket_id, file_id)

    def download(self, file_id):
        """"""
        get_client().file_download(self, bucket_id, file_hash)

    def upload(self, file, frame):
        """"""
        # Support path strings as well as file-like objects
        if isinstance(file, str):
            with io.open(file, mode='rb') as file:
                self._upload(file, frame)
        else:
            self._upload(file, frame)


class TokenManager:
    """Bucket token manager.

    Attributes:
        bucket_id (int): bucket unique identifier.
    """

    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    def create(self, operation):
        """Creates a token.

        Args:
            operation (str): operation (PUSH or PULL).
        """
        operation = operation.upper()
        assert(operation in ['PUSH', 'PULL'])
        token_json = get_client().token_create(
            bucket_id=self.bucket_id, operation=operation)
        return Token(token_json)


class UserKeyManager(ABCMeta):
    """"""

    @staticmethod
    def all():
        """"""
        keys_json = get_client().key_get()
        return [payload['key'] for payload in keys_json]

    @staticmethod
    def add(key):
        """"""
        if not isinstance(key, str):
            key = ecdsa_to_hex(key)

            get_client().key_register(key)

    @staticmethod
    def clear():
        """"""
        for key in UserKeyManager.all():
            UserKeyManager.remove(key)

    @staticmethod
    def remove(key):
        """"""
        if not isinstance(key, str):
            key = ecdsa_to_hex(key)

        get_client().key_delete(key)
