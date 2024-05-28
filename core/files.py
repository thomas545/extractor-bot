import os
import requests
import tempfile
import mimetypes
from urllib import parse
from urllib.parse import quote
from typing import Tuple, Any
from requests.exceptions import HTTPError
from core.environment import get_environ
from core.logger import logger


def get_file_content_type(file_name):
    content_type, _ = mimetypes.guess_type(file_name)
    return content_type


def get_url_extension(url: str) -> Tuple[Any, Any]:
    file_type, encoding = mimetypes.guess_type(url, strict=True)
    extension = mimetypes.guess_extension(file_type, strict=False)
    return file_type, extension


def delete_files(file_paths: list) -> bool:
    for file_path in file_paths:
        if not file_path:
            continue

        try:
            os.remove(file_path)
        except Exception as e:
            pass
            # TODO add logger

    return True


def save_url_to_local_file(url: str) -> Tuple[str, str]:
    response = requests.get(
        url, headers={"User-Agent": "Mozilla/5.0"}, stream=True, timeout=300
    )

    file_type, extension = get_url_extension(url)
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tf:
        local_path = tf.name
        for chunk in response.iter_content(chunk_size=512 * 1024):
            if chunk:
                tf.write(chunk)

    return file_type, local_path


class Storage:

    def __init__(self, storage_zone_region=""):
        """
        Creates an object for using BunnyCDN Storage API
        Parameters
        ----------
        storage_zone_region(optional parameter) : String
                                                  The storage zone region code
                                                  as per BunnyCDN
        """
        self.headers = {
            # headers to be passed in HTTP requests
            "AccessKey": get_environ("BUNNY_API_KEY"),
            "Content-Type": "application/json",
            "Accept": "applcation/json",
        }

        # applying constraint that storage_zone must be specified
        self.storage_zone = get_environ("BUNNY_STORAGE_ZONE")

        # For generating base_url for sending requests
        if not storage_zone_region:
            self.base_url = "https://storage.bunnycdn.com/" + self.storage_zone + "/"
        else:
            self.base_url = (
                "https://"
                + storage_zone_region
                + ".storage.bunnycdn.com/"
                + self.storage_zone
                + "/"
            )

    def upload_file(self, file_name, storage_path=None, file_data=None):
        """
        This function uploads files to your BunnyCDN storage zone
        Parameters
        ----------
        storage_path                : String
                                      The path of directory in storage zone
                                      (including the name of file as desired and excluding storage zone name)
                                      to which file is to be uploaded
        file_name                   : String
                                      The name of the file as stored in local server
        file_data                   : Bytes
                                      The file bytes
        Examples
        --------
        file_name                   : 'ABC.txt'
        file_data                   : 'bytes'
        storage_path                : '<Directory name in storage zone>/<file name as to be uploaded on storage zone>.txt'
                                        #Here .txt because the file being uploaded in example is txt
        """

        # to build correct url
        if storage_path is not None and storage_path != "":
            if storage_path[0] == "/":
                storage_path = storage_path[1:]
            if storage_path[-1] == "/":
                storage_path = storage_path[:-1]
            url = self.base_url + parse.quote(storage_path)
        else:
            url = self.base_url + parse.quote(file_name)

        path = storage_path if storage_path else file_name

        response = requests.put(url, data=file_data, headers=self.headers)
        try:
            response.raise_for_status()
        except HTTPError as http:
            return {
                "status": "error",
                "HTTP": response.status_code,
                "msg": f"Upload Failed HTTP Error Occured: {http}",
            }
        else:
            return {
                "status": "success",
                "url": f"https://testingzone021.b-cdn.net/{path}",
                "HTTP": response.status_code,
                "msg": "The File Upload was Successful",
            }
