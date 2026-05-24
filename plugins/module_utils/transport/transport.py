from __future__ import annotations

from abc import ABC, abstractmethod

import requests

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.transport.models import (
    TransportRequest,
    TransportResponse,
)


class TransportError(Exception):
    """
    Internal transport exception used to trigger retries.
    """


class Transport(ABC):
    """
    Base transport abstraction.
    """

    @abstractmethod
    def send(
        self,
        request: TransportRequest,
    ) -> TransportResponse:
        pass


class RequestsHttpTransport(Transport):
    """
    HTTP transport implementation using requests.
    """

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(
            multiplier=1,
            min=1,
            max=10,
        ),
        retry=retry_if_exception_type(
            (
                requests.RequestException,
                TransportError,
            ),
        ),
    )
    def _do_send(
        self,
        request: TransportRequest,
    ) -> requests.Response:
        response = requests.request(
            method=request.method,
            url=request.target,
            headers=request.headers,
            params=request.params,
            json=request.json,
            data=request.data,
            timeout=request.timeout,
            verify=request.ssl_verify,
        )

        #
        # Retry transient server-side failures.
        #
        if response.status_code >= 500:
            raise TransportError(f"Server error: {response.status_code}")

        return response

    def send(
        self,
        request: TransportRequest,
    ) -> TransportResponse:
        try:
            response = self._do_send(request)

            return TransportResponse(
                ok=response.ok,
                status_code=response.status_code,
                body=response.text,
                headers=dict(response.headers),
                error=None,
            )

        except Exception as exc:
            return TransportResponse(
                ok=False,
                status_code=None,
                body="",
                headers={},
                error=str(exc),
            )
