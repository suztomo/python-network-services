# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.network_services_v1.services.network_services import (
    NetworkServicesAsyncClient,
    NetworkServicesClient,
    pagers,
    transports,
)
from google.cloud.network_services_v1.types import (
    endpoint_policy as gcn_endpoint_policy,
)
from google.cloud.network_services_v1.types import (
    service_binding as gcn_service_binding,
)
from google.cloud.network_services_v1.types import common
from google.cloud.network_services_v1.types import endpoint_policy
from google.cloud.network_services_v1.types import gateway
from google.cloud.network_services_v1.types import gateway as gcn_gateway
from google.cloud.network_services_v1.types import grpc_route
from google.cloud.network_services_v1.types import grpc_route as gcn_grpc_route
from google.cloud.network_services_v1.types import http_route
from google.cloud.network_services_v1.types import http_route as gcn_http_route
from google.cloud.network_services_v1.types import mesh
from google.cloud.network_services_v1.types import mesh as gcn_mesh
from google.cloud.network_services_v1.types import service_binding
from google.cloud.network_services_v1.types import tcp_route
from google.cloud.network_services_v1.types import tcp_route as gcn_tcp_route
from google.cloud.network_services_v1.types import tls_route
from google.cloud.network_services_v1.types import tls_route as gcn_tls_route


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert NetworkServicesClient._get_default_mtls_endpoint(None) is None
    assert (
        NetworkServicesClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        NetworkServicesClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        NetworkServicesClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        NetworkServicesClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        NetworkServicesClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (NetworkServicesClient, "grpc"),
        (NetworkServicesAsyncClient, "grpc_asyncio"),
        (NetworkServicesClient, "rest"),
    ],
)
def test_network_services_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "networkservices.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://networkservices.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.NetworkServicesGrpcTransport, "grpc"),
        (transports.NetworkServicesGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.NetworkServicesRestTransport, "rest"),
    ],
)
def test_network_services_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (NetworkServicesClient, "grpc"),
        (NetworkServicesAsyncClient, "grpc_asyncio"),
        (NetworkServicesClient, "rest"),
    ],
)
def test_network_services_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "networkservices.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://networkservices.googleapis.com"
        )


def test_network_services_client_get_transport_class():
    transport = NetworkServicesClient.get_transport_class()
    available_transports = [
        transports.NetworkServicesGrpcTransport,
        transports.NetworkServicesRestTransport,
    ]
    assert transport in available_transports

    transport = NetworkServicesClient.get_transport_class("grpc")
    assert transport == transports.NetworkServicesGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (NetworkServicesClient, transports.NetworkServicesGrpcTransport, "grpc"),
        (
            NetworkServicesAsyncClient,
            transports.NetworkServicesGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (NetworkServicesClient, transports.NetworkServicesRestTransport, "rest"),
    ],
)
@mock.patch.object(
    NetworkServicesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NetworkServicesClient),
)
@mock.patch.object(
    NetworkServicesAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NetworkServicesAsyncClient),
)
def test_network_services_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(NetworkServicesClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(NetworkServicesClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            NetworkServicesClient,
            transports.NetworkServicesGrpcTransport,
            "grpc",
            "true",
        ),
        (
            NetworkServicesAsyncClient,
            transports.NetworkServicesGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            NetworkServicesClient,
            transports.NetworkServicesGrpcTransport,
            "grpc",
            "false",
        ),
        (
            NetworkServicesAsyncClient,
            transports.NetworkServicesGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            NetworkServicesClient,
            transports.NetworkServicesRestTransport,
            "rest",
            "true",
        ),
        (
            NetworkServicesClient,
            transports.NetworkServicesRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    NetworkServicesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NetworkServicesClient),
)
@mock.patch.object(
    NetworkServicesAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NetworkServicesAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_network_services_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [NetworkServicesClient, NetworkServicesAsyncClient]
)
@mock.patch.object(
    NetworkServicesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NetworkServicesClient),
)
@mock.patch.object(
    NetworkServicesAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NetworkServicesAsyncClient),
)
def test_network_services_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (NetworkServicesClient, transports.NetworkServicesGrpcTransport, "grpc"),
        (
            NetworkServicesAsyncClient,
            transports.NetworkServicesGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (NetworkServicesClient, transports.NetworkServicesRestTransport, "rest"),
    ],
)
def test_network_services_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            NetworkServicesClient,
            transports.NetworkServicesGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            NetworkServicesAsyncClient,
            transports.NetworkServicesGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (NetworkServicesClient, transports.NetworkServicesRestTransport, "rest", None),
    ],
)
def test_network_services_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_network_services_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.network_services_v1.services.network_services.transports.NetworkServicesGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = NetworkServicesClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            NetworkServicesClient,
            transports.NetworkServicesGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            NetworkServicesAsyncClient,
            transports.NetworkServicesGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_network_services_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "networkservices.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="networkservices.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        endpoint_policy.ListEndpointPoliciesRequest,
        dict,
    ],
)
def test_list_endpoint_policies(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = endpoint_policy.ListEndpointPoliciesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_endpoint_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.ListEndpointPoliciesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEndpointPoliciesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_endpoint_policies_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        client.list_endpoint_policies()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.ListEndpointPoliciesRequest()


@pytest.mark.asyncio
async def test_list_endpoint_policies_async(
    transport: str = "grpc_asyncio",
    request_type=endpoint_policy.ListEndpointPoliciesRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            endpoint_policy.ListEndpointPoliciesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_endpoint_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.ListEndpointPoliciesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEndpointPoliciesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_endpoint_policies_async_from_dict():
    await test_list_endpoint_policies_async(request_type=dict)


def test_list_endpoint_policies_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = endpoint_policy.ListEndpointPoliciesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        call.return_value = endpoint_policy.ListEndpointPoliciesResponse()
        client.list_endpoint_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_endpoint_policies_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = endpoint_policy.ListEndpointPoliciesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            endpoint_policy.ListEndpointPoliciesResponse()
        )
        await client.list_endpoint_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_endpoint_policies_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = endpoint_policy.ListEndpointPoliciesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_endpoint_policies(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_endpoint_policies_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_endpoint_policies(
            endpoint_policy.ListEndpointPoliciesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_endpoint_policies_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = endpoint_policy.ListEndpointPoliciesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            endpoint_policy.ListEndpointPoliciesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_endpoint_policies(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_endpoint_policies_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_endpoint_policies(
            endpoint_policy.ListEndpointPoliciesRequest(),
            parent="parent_value",
        )


def test_list_endpoint_policies_pager(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="abc",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[],
                next_page_token="def",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="ghi",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_endpoint_policies(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, endpoint_policy.EndpointPolicy) for i in results)


def test_list_endpoint_policies_pages(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="abc",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[],
                next_page_token="def",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="ghi",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_endpoint_policies(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_endpoint_policies_async_pager():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="abc",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[],
                next_page_token="def",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="ghi",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_endpoint_policies(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, endpoint_policy.EndpointPolicy) for i in responses)


@pytest.mark.asyncio
async def test_list_endpoint_policies_async_pages():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_endpoint_policies),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="abc",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[],
                next_page_token="def",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="ghi",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_endpoint_policies(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        endpoint_policy.GetEndpointPolicyRequest,
        dict,
    ],
)
def test_get_endpoint_policy(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = endpoint_policy.EndpointPolicy(
            name="name_value",
            type_=endpoint_policy.EndpointPolicy.EndpointPolicyType.SIDECAR_PROXY,
            authorization_policy="authorization_policy_value",
            description="description_value",
            server_tls_policy="server_tls_policy_value",
            client_tls_policy="client_tls_policy_value",
        )
        response = client.get_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.GetEndpointPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, endpoint_policy.EndpointPolicy)
    assert response.name == "name_value"
    assert (
        response.type_
        == endpoint_policy.EndpointPolicy.EndpointPolicyType.SIDECAR_PROXY
    )
    assert response.authorization_policy == "authorization_policy_value"
    assert response.description == "description_value"
    assert response.server_tls_policy == "server_tls_policy_value"
    assert response.client_tls_policy == "client_tls_policy_value"


def test_get_endpoint_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_endpoint_policy), "__call__"
    ) as call:
        client.get_endpoint_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.GetEndpointPolicyRequest()


@pytest.mark.asyncio
async def test_get_endpoint_policy_async(
    transport: str = "grpc_asyncio",
    request_type=endpoint_policy.GetEndpointPolicyRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            endpoint_policy.EndpointPolicy(
                name="name_value",
                type_=endpoint_policy.EndpointPolicy.EndpointPolicyType.SIDECAR_PROXY,
                authorization_policy="authorization_policy_value",
                description="description_value",
                server_tls_policy="server_tls_policy_value",
                client_tls_policy="client_tls_policy_value",
            )
        )
        response = await client.get_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.GetEndpointPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, endpoint_policy.EndpointPolicy)
    assert response.name == "name_value"
    assert (
        response.type_
        == endpoint_policy.EndpointPolicy.EndpointPolicyType.SIDECAR_PROXY
    )
    assert response.authorization_policy == "authorization_policy_value"
    assert response.description == "description_value"
    assert response.server_tls_policy == "server_tls_policy_value"
    assert response.client_tls_policy == "client_tls_policy_value"


@pytest.mark.asyncio
async def test_get_endpoint_policy_async_from_dict():
    await test_get_endpoint_policy_async(request_type=dict)


def test_get_endpoint_policy_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = endpoint_policy.GetEndpointPolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_endpoint_policy), "__call__"
    ) as call:
        call.return_value = endpoint_policy.EndpointPolicy()
        client.get_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_endpoint_policy_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = endpoint_policy.GetEndpointPolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_endpoint_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            endpoint_policy.EndpointPolicy()
        )
        await client.get_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_endpoint_policy_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = endpoint_policy.EndpointPolicy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_endpoint_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_endpoint_policy_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_endpoint_policy(
            endpoint_policy.GetEndpointPolicyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_endpoint_policy_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = endpoint_policy.EndpointPolicy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            endpoint_policy.EndpointPolicy()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_endpoint_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_endpoint_policy_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_endpoint_policy(
            endpoint_policy.GetEndpointPolicyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_endpoint_policy.CreateEndpointPolicyRequest,
        dict,
    ],
)
def test_create_endpoint_policy(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_endpoint_policy.CreateEndpointPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_endpoint_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_endpoint_policy), "__call__"
    ) as call:
        client.create_endpoint_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_endpoint_policy.CreateEndpointPolicyRequest()


@pytest.mark.asyncio
async def test_create_endpoint_policy_async(
    transport: str = "grpc_asyncio",
    request_type=gcn_endpoint_policy.CreateEndpointPolicyRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_endpoint_policy.CreateEndpointPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_endpoint_policy_async_from_dict():
    await test_create_endpoint_policy_async(request_type=dict)


def test_create_endpoint_policy_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_endpoint_policy.CreateEndpointPolicyRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_endpoint_policy), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_endpoint_policy_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_endpoint_policy.CreateEndpointPolicyRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_endpoint_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_endpoint_policy_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_endpoint_policy(
            parent="parent_value",
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            endpoint_policy_id="endpoint_policy_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].endpoint_policy
        mock_val = gcn_endpoint_policy.EndpointPolicy(name="name_value")
        assert arg == mock_val
        arg = args[0].endpoint_policy_id
        mock_val = "endpoint_policy_id_value"
        assert arg == mock_val


def test_create_endpoint_policy_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_endpoint_policy(
            gcn_endpoint_policy.CreateEndpointPolicyRequest(),
            parent="parent_value",
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            endpoint_policy_id="endpoint_policy_id_value",
        )


@pytest.mark.asyncio
async def test_create_endpoint_policy_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_endpoint_policy(
            parent="parent_value",
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            endpoint_policy_id="endpoint_policy_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].endpoint_policy
        mock_val = gcn_endpoint_policy.EndpointPolicy(name="name_value")
        assert arg == mock_val
        arg = args[0].endpoint_policy_id
        mock_val = "endpoint_policy_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_endpoint_policy_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_endpoint_policy(
            gcn_endpoint_policy.CreateEndpointPolicyRequest(),
            parent="parent_value",
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            endpoint_policy_id="endpoint_policy_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_endpoint_policy.UpdateEndpointPolicyRequest,
        dict,
    ],
)
def test_update_endpoint_policy(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_endpoint_policy.UpdateEndpointPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_endpoint_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_endpoint_policy), "__call__"
    ) as call:
        client.update_endpoint_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_endpoint_policy.UpdateEndpointPolicyRequest()


@pytest.mark.asyncio
async def test_update_endpoint_policy_async(
    transport: str = "grpc_asyncio",
    request_type=gcn_endpoint_policy.UpdateEndpointPolicyRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_endpoint_policy.UpdateEndpointPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_endpoint_policy_async_from_dict():
    await test_update_endpoint_policy_async(request_type=dict)


def test_update_endpoint_policy_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_endpoint_policy.UpdateEndpointPolicyRequest()

    request.endpoint_policy.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_endpoint_policy), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "endpoint_policy.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_endpoint_policy_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_endpoint_policy.UpdateEndpointPolicyRequest()

    request.endpoint_policy.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_endpoint_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "endpoint_policy.name=name_value",
    ) in kw["metadata"]


def test_update_endpoint_policy_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_endpoint_policy(
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].endpoint_policy
        mock_val = gcn_endpoint_policy.EndpointPolicy(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_endpoint_policy_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_endpoint_policy(
            gcn_endpoint_policy.UpdateEndpointPolicyRequest(),
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_endpoint_policy_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_endpoint_policy(
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].endpoint_policy
        mock_val = gcn_endpoint_policy.EndpointPolicy(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_endpoint_policy_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_endpoint_policy(
            gcn_endpoint_policy.UpdateEndpointPolicyRequest(),
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        endpoint_policy.DeleteEndpointPolicyRequest,
        dict,
    ],
)
def test_delete_endpoint_policy(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.DeleteEndpointPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_endpoint_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_endpoint_policy), "__call__"
    ) as call:
        client.delete_endpoint_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.DeleteEndpointPolicyRequest()


@pytest.mark.asyncio
async def test_delete_endpoint_policy_async(
    transport: str = "grpc_asyncio",
    request_type=endpoint_policy.DeleteEndpointPolicyRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == endpoint_policy.DeleteEndpointPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_endpoint_policy_async_from_dict():
    await test_delete_endpoint_policy_async(request_type=dict)


def test_delete_endpoint_policy_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = endpoint_policy.DeleteEndpointPolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_endpoint_policy), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_endpoint_policy_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = endpoint_policy.DeleteEndpointPolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_endpoint_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_endpoint_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_endpoint_policy_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_endpoint_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_endpoint_policy_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_endpoint_policy(
            endpoint_policy.DeleteEndpointPolicyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_endpoint_policy_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_endpoint_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_endpoint_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_endpoint_policy_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_endpoint_policy(
            endpoint_policy.DeleteEndpointPolicyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gateway.ListGatewaysRequest,
        dict,
    ],
)
def test_list_gateways(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gateway.ListGatewaysResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_gateways(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.ListGatewaysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGatewaysPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_gateways_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        client.list_gateways()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.ListGatewaysRequest()


@pytest.mark.asyncio
async def test_list_gateways_async(
    transport: str = "grpc_asyncio", request_type=gateway.ListGatewaysRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gateway.ListGatewaysResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_gateways(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.ListGatewaysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGatewaysAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_gateways_async_from_dict():
    await test_list_gateways_async(request_type=dict)


def test_list_gateways_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gateway.ListGatewaysRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        call.return_value = gateway.ListGatewaysResponse()
        client.list_gateways(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_gateways_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gateway.ListGatewaysRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gateway.ListGatewaysResponse()
        )
        await client.list_gateways(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_gateways_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gateway.ListGatewaysResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_gateways(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_gateways_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_gateways(
            gateway.ListGatewaysRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_gateways_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gateway.ListGatewaysResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gateway.ListGatewaysResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_gateways(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_gateways_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_gateways(
            gateway.ListGatewaysRequest(),
            parent="parent_value",
        )


def test_list_gateways_pager(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
                next_page_token="abc",
            ),
            gateway.ListGatewaysResponse(
                gateways=[],
                next_page_token="def",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                ],
                next_page_token="ghi",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_gateways(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, gateway.Gateway) for i in results)


def test_list_gateways_pages(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gateways), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
                next_page_token="abc",
            ),
            gateway.ListGatewaysResponse(
                gateways=[],
                next_page_token="def",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                ],
                next_page_token="ghi",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_gateways(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_gateways_async_pager():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_gateways), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
                next_page_token="abc",
            ),
            gateway.ListGatewaysResponse(
                gateways=[],
                next_page_token="def",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                ],
                next_page_token="ghi",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_gateways(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, gateway.Gateway) for i in responses)


@pytest.mark.asyncio
async def test_list_gateways_async_pages():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_gateways), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
                next_page_token="abc",
            ),
            gateway.ListGatewaysResponse(
                gateways=[],
                next_page_token="def",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                ],
                next_page_token="ghi",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_gateways(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gateway.GetGatewayRequest,
        dict,
    ],
)
def test_get_gateway(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gateway.Gateway(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            type_=gateway.Gateway.Type.OPEN_MESH,
            ports=[568],
            scope="scope_value",
            server_tls_policy="server_tls_policy_value",
        )
        response = client.get_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.GetGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gateway.Gateway)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.type_ == gateway.Gateway.Type.OPEN_MESH
    assert response.ports == [568]
    assert response.scope == "scope_value"
    assert response.server_tls_policy == "server_tls_policy_value"


def test_get_gateway_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_gateway), "__call__") as call:
        client.get_gateway()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.GetGatewayRequest()


@pytest.mark.asyncio
async def test_get_gateway_async(
    transport: str = "grpc_asyncio", request_type=gateway.GetGatewayRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gateway.Gateway(
                name="name_value",
                self_link="self_link_value",
                description="description_value",
                type_=gateway.Gateway.Type.OPEN_MESH,
                ports=[568],
                scope="scope_value",
                server_tls_policy="server_tls_policy_value",
            )
        )
        response = await client.get_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.GetGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gateway.Gateway)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.type_ == gateway.Gateway.Type.OPEN_MESH
    assert response.ports == [568]
    assert response.scope == "scope_value"
    assert response.server_tls_policy == "server_tls_policy_value"


@pytest.mark.asyncio
async def test_get_gateway_async_from_dict():
    await test_get_gateway_async(request_type=dict)


def test_get_gateway_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gateway.GetGatewayRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_gateway), "__call__") as call:
        call.return_value = gateway.Gateway()
        client.get_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_gateway_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gateway.GetGatewayRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_gateway), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gateway.Gateway())
        await client.get_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_gateway_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gateway.Gateway()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_gateway(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_gateway_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_gateway(
            gateway.GetGatewayRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_gateway_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gateway.Gateway()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gateway.Gateway())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_gateway(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_gateway_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_gateway(
            gateway.GetGatewayRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_gateway.CreateGatewayRequest,
        dict,
    ],
)
def test_create_gateway(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_gateway.CreateGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_gateway_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_gateway), "__call__") as call:
        client.create_gateway()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_gateway.CreateGatewayRequest()


@pytest.mark.asyncio
async def test_create_gateway_async(
    transport: str = "grpc_asyncio", request_type=gcn_gateway.CreateGatewayRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_gateway.CreateGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_gateway_async_from_dict():
    await test_create_gateway_async(request_type=dict)


def test_create_gateway_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_gateway.CreateGatewayRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_gateway), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_gateway_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_gateway.CreateGatewayRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_gateway), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_gateway_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_gateway(
            parent="parent_value",
            gateway=gcn_gateway.Gateway(name="name_value"),
            gateway_id="gateway_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].gateway
        mock_val = gcn_gateway.Gateway(name="name_value")
        assert arg == mock_val
        arg = args[0].gateway_id
        mock_val = "gateway_id_value"
        assert arg == mock_val


def test_create_gateway_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_gateway(
            gcn_gateway.CreateGatewayRequest(),
            parent="parent_value",
            gateway=gcn_gateway.Gateway(name="name_value"),
            gateway_id="gateway_id_value",
        )


@pytest.mark.asyncio
async def test_create_gateway_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_gateway(
            parent="parent_value",
            gateway=gcn_gateway.Gateway(name="name_value"),
            gateway_id="gateway_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].gateway
        mock_val = gcn_gateway.Gateway(name="name_value")
        assert arg == mock_val
        arg = args[0].gateway_id
        mock_val = "gateway_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_gateway_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_gateway(
            gcn_gateway.CreateGatewayRequest(),
            parent="parent_value",
            gateway=gcn_gateway.Gateway(name="name_value"),
            gateway_id="gateway_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_gateway.UpdateGatewayRequest,
        dict,
    ],
)
def test_update_gateway(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_gateway.UpdateGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_gateway_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_gateway), "__call__") as call:
        client.update_gateway()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_gateway.UpdateGatewayRequest()


@pytest.mark.asyncio
async def test_update_gateway_async(
    transport: str = "grpc_asyncio", request_type=gcn_gateway.UpdateGatewayRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_gateway.UpdateGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_gateway_async_from_dict():
    await test_update_gateway_async(request_type=dict)


def test_update_gateway_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_gateway.UpdateGatewayRequest()

    request.gateway.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_gateway), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "gateway.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_gateway_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_gateway.UpdateGatewayRequest()

    request.gateway.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_gateway), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "gateway.name=name_value",
    ) in kw["metadata"]


def test_update_gateway_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_gateway(
            gateway=gcn_gateway.Gateway(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].gateway
        mock_val = gcn_gateway.Gateway(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_gateway_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_gateway(
            gcn_gateway.UpdateGatewayRequest(),
            gateway=gcn_gateway.Gateway(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_gateway_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_gateway(
            gateway=gcn_gateway.Gateway(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].gateway
        mock_val = gcn_gateway.Gateway(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_gateway_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_gateway(
            gcn_gateway.UpdateGatewayRequest(),
            gateway=gcn_gateway.Gateway(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gateway.DeleteGatewayRequest,
        dict,
    ],
)
def test_delete_gateway(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.DeleteGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_gateway_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_gateway), "__call__") as call:
        client.delete_gateway()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.DeleteGatewayRequest()


@pytest.mark.asyncio
async def test_delete_gateway_async(
    transport: str = "grpc_asyncio", request_type=gateway.DeleteGatewayRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gateway.DeleteGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_gateway_async_from_dict():
    await test_delete_gateway_async(request_type=dict)


def test_delete_gateway_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gateway.DeleteGatewayRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_gateway), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_gateway_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gateway.DeleteGatewayRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_gateway), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_gateway_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_gateway(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_gateway_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_gateway(
            gateway.DeleteGatewayRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_gateway_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_gateway), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_gateway(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_gateway_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_gateway(
            gateway.DeleteGatewayRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        grpc_route.ListGrpcRoutesRequest,
        dict,
    ],
)
def test_list_grpc_routes(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_route.ListGrpcRoutesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_grpc_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.ListGrpcRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGrpcRoutesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_grpc_routes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        client.list_grpc_routes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.ListGrpcRoutesRequest()


@pytest.mark.asyncio
async def test_list_grpc_routes_async(
    transport: str = "grpc_asyncio", request_type=grpc_route.ListGrpcRoutesRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grpc_route.ListGrpcRoutesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_grpc_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.ListGrpcRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGrpcRoutesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_grpc_routes_async_from_dict():
    await test_list_grpc_routes_async(request_type=dict)


def test_list_grpc_routes_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grpc_route.ListGrpcRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        call.return_value = grpc_route.ListGrpcRoutesResponse()
        client.list_grpc_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_grpc_routes_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grpc_route.ListGrpcRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grpc_route.ListGrpcRoutesResponse()
        )
        await client.list_grpc_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_grpc_routes_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_route.ListGrpcRoutesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_grpc_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_grpc_routes_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_grpc_routes(
            grpc_route.ListGrpcRoutesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_grpc_routes_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_route.ListGrpcRoutesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grpc_route.ListGrpcRoutesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_grpc_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_grpc_routes_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_grpc_routes(
            grpc_route.ListGrpcRoutesRequest(),
            parent="parent_value",
        )


def test_list_grpc_routes_pager(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="abc",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[],
                next_page_token="def",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="ghi",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_grpc_routes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, grpc_route.GrpcRoute) for i in results)


def test_list_grpc_routes_pages(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_grpc_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="abc",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[],
                next_page_token="def",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="ghi",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_grpc_routes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_grpc_routes_async_pager():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_grpc_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="abc",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[],
                next_page_token="def",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="ghi",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_grpc_routes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, grpc_route.GrpcRoute) for i in responses)


@pytest.mark.asyncio
async def test_list_grpc_routes_async_pages():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_grpc_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="abc",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[],
                next_page_token="def",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="ghi",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_grpc_routes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        grpc_route.GetGrpcRouteRequest,
        dict,
    ],
)
def test_get_grpc_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_grpc_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_route.GrpcRoute(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            hostnames=["hostnames_value"],
            meshes=["meshes_value"],
            gateways=["gateways_value"],
        )
        response = client.get_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.GetGrpcRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grpc_route.GrpcRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.hostnames == ["hostnames_value"]
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


def test_get_grpc_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_grpc_route), "__call__") as call:
        client.get_grpc_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.GetGrpcRouteRequest()


@pytest.mark.asyncio
async def test_get_grpc_route_async(
    transport: str = "grpc_asyncio", request_type=grpc_route.GetGrpcRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_grpc_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grpc_route.GrpcRoute(
                name="name_value",
                self_link="self_link_value",
                description="description_value",
                hostnames=["hostnames_value"],
                meshes=["meshes_value"],
                gateways=["gateways_value"],
            )
        )
        response = await client.get_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.GetGrpcRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grpc_route.GrpcRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.hostnames == ["hostnames_value"]
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


@pytest.mark.asyncio
async def test_get_grpc_route_async_from_dict():
    await test_get_grpc_route_async(request_type=dict)


def test_get_grpc_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grpc_route.GetGrpcRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_grpc_route), "__call__") as call:
        call.return_value = grpc_route.GrpcRoute()
        client.get_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_grpc_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grpc_route.GetGrpcRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_grpc_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grpc_route.GrpcRoute()
        )
        await client.get_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_grpc_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_grpc_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_route.GrpcRoute()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_grpc_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_grpc_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_grpc_route(
            grpc_route.GetGrpcRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_grpc_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_grpc_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_route.GrpcRoute()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grpc_route.GrpcRoute()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_grpc_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_grpc_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_grpc_route(
            grpc_route.GetGrpcRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_grpc_route.CreateGrpcRouteRequest,
        dict,
    ],
)
def test_create_grpc_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_grpc_route.CreateGrpcRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_grpc_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_grpc_route), "__call__"
    ) as call:
        client.create_grpc_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_grpc_route.CreateGrpcRouteRequest()


@pytest.mark.asyncio
async def test_create_grpc_route_async(
    transport: str = "grpc_asyncio", request_type=gcn_grpc_route.CreateGrpcRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_grpc_route.CreateGrpcRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_grpc_route_async_from_dict():
    await test_create_grpc_route_async(request_type=dict)


def test_create_grpc_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_grpc_route.CreateGrpcRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_grpc_route), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_grpc_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_grpc_route.CreateGrpcRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_grpc_route), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_grpc_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_grpc_route(
            parent="parent_value",
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            grpc_route_id="grpc_route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].grpc_route
        mock_val = gcn_grpc_route.GrpcRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].grpc_route_id
        mock_val = "grpc_route_id_value"
        assert arg == mock_val


def test_create_grpc_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_grpc_route(
            gcn_grpc_route.CreateGrpcRouteRequest(),
            parent="parent_value",
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            grpc_route_id="grpc_route_id_value",
        )


@pytest.mark.asyncio
async def test_create_grpc_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_grpc_route(
            parent="parent_value",
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            grpc_route_id="grpc_route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].grpc_route
        mock_val = gcn_grpc_route.GrpcRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].grpc_route_id
        mock_val = "grpc_route_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_grpc_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_grpc_route(
            gcn_grpc_route.CreateGrpcRouteRequest(),
            parent="parent_value",
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            grpc_route_id="grpc_route_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_grpc_route.UpdateGrpcRouteRequest,
        dict,
    ],
)
def test_update_grpc_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_grpc_route.UpdateGrpcRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_grpc_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_grpc_route), "__call__"
    ) as call:
        client.update_grpc_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_grpc_route.UpdateGrpcRouteRequest()


@pytest.mark.asyncio
async def test_update_grpc_route_async(
    transport: str = "grpc_asyncio", request_type=gcn_grpc_route.UpdateGrpcRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_grpc_route.UpdateGrpcRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_grpc_route_async_from_dict():
    await test_update_grpc_route_async(request_type=dict)


def test_update_grpc_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_grpc_route.UpdateGrpcRouteRequest()

    request.grpc_route.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_grpc_route), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "grpc_route.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_grpc_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_grpc_route.UpdateGrpcRouteRequest()

    request.grpc_route.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_grpc_route), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "grpc_route.name=name_value",
    ) in kw["metadata"]


def test_update_grpc_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_grpc_route(
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].grpc_route
        mock_val = gcn_grpc_route.GrpcRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_grpc_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_grpc_route(
            gcn_grpc_route.UpdateGrpcRouteRequest(),
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_grpc_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_grpc_route(
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].grpc_route
        mock_val = gcn_grpc_route.GrpcRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_grpc_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_grpc_route(
            gcn_grpc_route.UpdateGrpcRouteRequest(),
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        grpc_route.DeleteGrpcRouteRequest,
        dict,
    ],
)
def test_delete_grpc_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.DeleteGrpcRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_grpc_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_grpc_route), "__call__"
    ) as call:
        client.delete_grpc_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.DeleteGrpcRouteRequest()


@pytest.mark.asyncio
async def test_delete_grpc_route_async(
    transport: str = "grpc_asyncio", request_type=grpc_route.DeleteGrpcRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grpc_route.DeleteGrpcRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_grpc_route_async_from_dict():
    await test_delete_grpc_route_async(request_type=dict)


def test_delete_grpc_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grpc_route.DeleteGrpcRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_grpc_route), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_grpc_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grpc_route.DeleteGrpcRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_grpc_route), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_grpc_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_grpc_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_grpc_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_grpc_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_grpc_route(
            grpc_route.DeleteGrpcRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_grpc_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_grpc_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_grpc_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_grpc_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_grpc_route(
            grpc_route.DeleteGrpcRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        http_route.ListHttpRoutesRequest,
        dict,
    ],
)
def test_list_http_routes(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = http_route.ListHttpRoutesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_http_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.ListHttpRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListHttpRoutesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_http_routes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        client.list_http_routes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.ListHttpRoutesRequest()


@pytest.mark.asyncio
async def test_list_http_routes_async(
    transport: str = "grpc_asyncio", request_type=http_route.ListHttpRoutesRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            http_route.ListHttpRoutesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_http_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.ListHttpRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListHttpRoutesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_http_routes_async_from_dict():
    await test_list_http_routes_async(request_type=dict)


def test_list_http_routes_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = http_route.ListHttpRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        call.return_value = http_route.ListHttpRoutesResponse()
        client.list_http_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_http_routes_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = http_route.ListHttpRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            http_route.ListHttpRoutesResponse()
        )
        await client.list_http_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_http_routes_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = http_route.ListHttpRoutesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_http_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_http_routes_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_http_routes(
            http_route.ListHttpRoutesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_http_routes_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = http_route.ListHttpRoutesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            http_route.ListHttpRoutesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_http_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_http_routes_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_http_routes(
            http_route.ListHttpRoutesRequest(),
            parent="parent_value",
        )


def test_list_http_routes_pager(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
                next_page_token="abc",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[],
                next_page_token="def",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                ],
                next_page_token="ghi",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_http_routes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, http_route.HttpRoute) for i in results)


def test_list_http_routes_pages(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_http_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
                next_page_token="abc",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[],
                next_page_token="def",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                ],
                next_page_token="ghi",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_http_routes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_http_routes_async_pager():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_http_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
                next_page_token="abc",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[],
                next_page_token="def",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                ],
                next_page_token="ghi",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_http_routes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, http_route.HttpRoute) for i in responses)


@pytest.mark.asyncio
async def test_list_http_routes_async_pages():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_http_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
                next_page_token="abc",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[],
                next_page_token="def",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                ],
                next_page_token="ghi",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_http_routes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        http_route.GetHttpRouteRequest,
        dict,
    ],
)
def test_get_http_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_http_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = http_route.HttpRoute(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            hostnames=["hostnames_value"],
            meshes=["meshes_value"],
            gateways=["gateways_value"],
        )
        response = client.get_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.GetHttpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, http_route.HttpRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.hostnames == ["hostnames_value"]
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


def test_get_http_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_http_route), "__call__") as call:
        client.get_http_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.GetHttpRouteRequest()


@pytest.mark.asyncio
async def test_get_http_route_async(
    transport: str = "grpc_asyncio", request_type=http_route.GetHttpRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_http_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            http_route.HttpRoute(
                name="name_value",
                self_link="self_link_value",
                description="description_value",
                hostnames=["hostnames_value"],
                meshes=["meshes_value"],
                gateways=["gateways_value"],
            )
        )
        response = await client.get_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.GetHttpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, http_route.HttpRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.hostnames == ["hostnames_value"]
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


@pytest.mark.asyncio
async def test_get_http_route_async_from_dict():
    await test_get_http_route_async(request_type=dict)


def test_get_http_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = http_route.GetHttpRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_http_route), "__call__") as call:
        call.return_value = http_route.HttpRoute()
        client.get_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_http_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = http_route.GetHttpRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_http_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            http_route.HttpRoute()
        )
        await client.get_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_http_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_http_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = http_route.HttpRoute()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_http_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_http_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_http_route(
            http_route.GetHttpRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_http_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_http_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = http_route.HttpRoute()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            http_route.HttpRoute()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_http_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_http_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_http_route(
            http_route.GetHttpRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_http_route.CreateHttpRouteRequest,
        dict,
    ],
)
def test_create_http_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_http_route.CreateHttpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_http_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_http_route), "__call__"
    ) as call:
        client.create_http_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_http_route.CreateHttpRouteRequest()


@pytest.mark.asyncio
async def test_create_http_route_async(
    transport: str = "grpc_asyncio", request_type=gcn_http_route.CreateHttpRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_http_route.CreateHttpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_http_route_async_from_dict():
    await test_create_http_route_async(request_type=dict)


def test_create_http_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_http_route.CreateHttpRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_http_route), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_http_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_http_route.CreateHttpRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_http_route), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_http_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_http_route(
            parent="parent_value",
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            http_route_id="http_route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].http_route
        mock_val = gcn_http_route.HttpRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].http_route_id
        mock_val = "http_route_id_value"
        assert arg == mock_val


def test_create_http_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_http_route(
            gcn_http_route.CreateHttpRouteRequest(),
            parent="parent_value",
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            http_route_id="http_route_id_value",
        )


@pytest.mark.asyncio
async def test_create_http_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_http_route(
            parent="parent_value",
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            http_route_id="http_route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].http_route
        mock_val = gcn_http_route.HttpRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].http_route_id
        mock_val = "http_route_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_http_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_http_route(
            gcn_http_route.CreateHttpRouteRequest(),
            parent="parent_value",
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            http_route_id="http_route_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_http_route.UpdateHttpRouteRequest,
        dict,
    ],
)
def test_update_http_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_http_route.UpdateHttpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_http_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_http_route), "__call__"
    ) as call:
        client.update_http_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_http_route.UpdateHttpRouteRequest()


@pytest.mark.asyncio
async def test_update_http_route_async(
    transport: str = "grpc_asyncio", request_type=gcn_http_route.UpdateHttpRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_http_route.UpdateHttpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_http_route_async_from_dict():
    await test_update_http_route_async(request_type=dict)


def test_update_http_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_http_route.UpdateHttpRouteRequest()

    request.http_route.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_http_route), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "http_route.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_http_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_http_route.UpdateHttpRouteRequest()

    request.http_route.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_http_route), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "http_route.name=name_value",
    ) in kw["metadata"]


def test_update_http_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_http_route(
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].http_route
        mock_val = gcn_http_route.HttpRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_http_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_http_route(
            gcn_http_route.UpdateHttpRouteRequest(),
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_http_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_http_route(
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].http_route
        mock_val = gcn_http_route.HttpRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_http_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_http_route(
            gcn_http_route.UpdateHttpRouteRequest(),
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        http_route.DeleteHttpRouteRequest,
        dict,
    ],
)
def test_delete_http_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.DeleteHttpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_http_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_http_route), "__call__"
    ) as call:
        client.delete_http_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.DeleteHttpRouteRequest()


@pytest.mark.asyncio
async def test_delete_http_route_async(
    transport: str = "grpc_asyncio", request_type=http_route.DeleteHttpRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == http_route.DeleteHttpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_http_route_async_from_dict():
    await test_delete_http_route_async(request_type=dict)


def test_delete_http_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = http_route.DeleteHttpRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_http_route), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_http_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = http_route.DeleteHttpRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_http_route), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_http_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_http_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_http_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_http_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_http_route(
            http_route.DeleteHttpRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_http_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_http_route), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_http_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_http_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_http_route(
            http_route.DeleteHttpRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tcp_route.ListTcpRoutesRequest,
        dict,
    ],
)
def test_list_tcp_routes(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tcp_route.ListTcpRoutesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tcp_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.ListTcpRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTcpRoutesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tcp_routes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        client.list_tcp_routes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.ListTcpRoutesRequest()


@pytest.mark.asyncio
async def test_list_tcp_routes_async(
    transport: str = "grpc_asyncio", request_type=tcp_route.ListTcpRoutesRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tcp_route.ListTcpRoutesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tcp_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.ListTcpRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTcpRoutesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tcp_routes_async_from_dict():
    await test_list_tcp_routes_async(request_type=dict)


def test_list_tcp_routes_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tcp_route.ListTcpRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        call.return_value = tcp_route.ListTcpRoutesResponse()
        client.list_tcp_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tcp_routes_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tcp_route.ListTcpRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tcp_route.ListTcpRoutesResponse()
        )
        await client.list_tcp_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_tcp_routes_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tcp_route.ListTcpRoutesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tcp_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tcp_routes_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tcp_routes(
            tcp_route.ListTcpRoutesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tcp_routes_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tcp_route.ListTcpRoutesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tcp_route.ListTcpRoutesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tcp_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_tcp_routes_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tcp_routes(
            tcp_route.ListTcpRoutesRequest(),
            parent="parent_value",
        )


def test_list_tcp_routes_pager(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
                next_page_token="abc",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[],
                next_page_token="def",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                ],
                next_page_token="ghi",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tcp_routes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tcp_route.TcpRoute) for i in results)


def test_list_tcp_routes_pages(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tcp_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
                next_page_token="abc",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[],
                next_page_token="def",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                ],
                next_page_token="ghi",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tcp_routes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tcp_routes_async_pager():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tcp_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
                next_page_token="abc",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[],
                next_page_token="def",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                ],
                next_page_token="ghi",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tcp_routes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tcp_route.TcpRoute) for i in responses)


@pytest.mark.asyncio
async def test_list_tcp_routes_async_pages():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tcp_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
                next_page_token="abc",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[],
                next_page_token="def",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                ],
                next_page_token="ghi",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tcp_routes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tcp_route.GetTcpRouteRequest,
        dict,
    ],
)
def test_get_tcp_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tcp_route.TcpRoute(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            meshes=["meshes_value"],
            gateways=["gateways_value"],
        )
        response = client.get_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.GetTcpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tcp_route.TcpRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


def test_get_tcp_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tcp_route), "__call__") as call:
        client.get_tcp_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.GetTcpRouteRequest()


@pytest.mark.asyncio
async def test_get_tcp_route_async(
    transport: str = "grpc_asyncio", request_type=tcp_route.GetTcpRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tcp_route.TcpRoute(
                name="name_value",
                self_link="self_link_value",
                description="description_value",
                meshes=["meshes_value"],
                gateways=["gateways_value"],
            )
        )
        response = await client.get_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.GetTcpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tcp_route.TcpRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


@pytest.mark.asyncio
async def test_get_tcp_route_async_from_dict():
    await test_get_tcp_route_async(request_type=dict)


def test_get_tcp_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tcp_route.GetTcpRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tcp_route), "__call__") as call:
        call.return_value = tcp_route.TcpRoute()
        client.get_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tcp_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tcp_route.GetTcpRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tcp_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tcp_route.TcpRoute())
        await client.get_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_tcp_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tcp_route.TcpRoute()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tcp_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tcp_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tcp_route(
            tcp_route.GetTcpRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tcp_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tcp_route.TcpRoute()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tcp_route.TcpRoute())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tcp_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_tcp_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tcp_route(
            tcp_route.GetTcpRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_tcp_route.CreateTcpRouteRequest,
        dict,
    ],
)
def test_create_tcp_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tcp_route.CreateTcpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_tcp_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tcp_route), "__call__") as call:
        client.create_tcp_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tcp_route.CreateTcpRouteRequest()


@pytest.mark.asyncio
async def test_create_tcp_route_async(
    transport: str = "grpc_asyncio", request_type=gcn_tcp_route.CreateTcpRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tcp_route.CreateTcpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_tcp_route_async_from_dict():
    await test_create_tcp_route_async(request_type=dict)


def test_create_tcp_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_tcp_route.CreateTcpRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tcp_route), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tcp_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_tcp_route.CreateTcpRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tcp_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_tcp_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tcp_route(
            parent="parent_value",
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            tcp_route_id="tcp_route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tcp_route
        mock_val = gcn_tcp_route.TcpRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].tcp_route_id
        mock_val = "tcp_route_id_value"
        assert arg == mock_val


def test_create_tcp_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tcp_route(
            gcn_tcp_route.CreateTcpRouteRequest(),
            parent="parent_value",
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            tcp_route_id="tcp_route_id_value",
        )


@pytest.mark.asyncio
async def test_create_tcp_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tcp_route(
            parent="parent_value",
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            tcp_route_id="tcp_route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tcp_route
        mock_val = gcn_tcp_route.TcpRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].tcp_route_id
        mock_val = "tcp_route_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tcp_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tcp_route(
            gcn_tcp_route.CreateTcpRouteRequest(),
            parent="parent_value",
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            tcp_route_id="tcp_route_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_tcp_route.UpdateTcpRouteRequest,
        dict,
    ],
)
def test_update_tcp_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tcp_route.UpdateTcpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_tcp_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tcp_route), "__call__") as call:
        client.update_tcp_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tcp_route.UpdateTcpRouteRequest()


@pytest.mark.asyncio
async def test_update_tcp_route_async(
    transport: str = "grpc_asyncio", request_type=gcn_tcp_route.UpdateTcpRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tcp_route.UpdateTcpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_tcp_route_async_from_dict():
    await test_update_tcp_route_async(request_type=dict)


def test_update_tcp_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_tcp_route.UpdateTcpRouteRequest()

    request.tcp_route.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tcp_route), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tcp_route.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tcp_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_tcp_route.UpdateTcpRouteRequest()

    request.tcp_route.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tcp_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tcp_route.name=name_value",
    ) in kw["metadata"]


def test_update_tcp_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tcp_route(
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tcp_route
        mock_val = gcn_tcp_route.TcpRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tcp_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tcp_route(
            gcn_tcp_route.UpdateTcpRouteRequest(),
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tcp_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tcp_route(
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tcp_route
        mock_val = gcn_tcp_route.TcpRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tcp_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tcp_route(
            gcn_tcp_route.UpdateTcpRouteRequest(),
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tcp_route.DeleteTcpRouteRequest,
        dict,
    ],
)
def test_delete_tcp_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.DeleteTcpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_tcp_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tcp_route), "__call__") as call:
        client.delete_tcp_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.DeleteTcpRouteRequest()


@pytest.mark.asyncio
async def test_delete_tcp_route_async(
    transport: str = "grpc_asyncio", request_type=tcp_route.DeleteTcpRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tcp_route.DeleteTcpRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_tcp_route_async_from_dict():
    await test_delete_tcp_route_async(request_type=dict)


def test_delete_tcp_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tcp_route.DeleteTcpRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tcp_route), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tcp_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tcp_route.DeleteTcpRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tcp_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_tcp_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_tcp_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tcp_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_tcp_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tcp_route(
            tcp_route.DeleteTcpRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tcp_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tcp_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tcp_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_tcp_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tcp_route(
            tcp_route.DeleteTcpRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tls_route.ListTlsRoutesRequest,
        dict,
    ],
)
def test_list_tls_routes(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tls_route.ListTlsRoutesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tls_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.ListTlsRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTlsRoutesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tls_routes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        client.list_tls_routes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.ListTlsRoutesRequest()


@pytest.mark.asyncio
async def test_list_tls_routes_async(
    transport: str = "grpc_asyncio", request_type=tls_route.ListTlsRoutesRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tls_route.ListTlsRoutesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tls_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.ListTlsRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTlsRoutesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tls_routes_async_from_dict():
    await test_list_tls_routes_async(request_type=dict)


def test_list_tls_routes_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tls_route.ListTlsRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        call.return_value = tls_route.ListTlsRoutesResponse()
        client.list_tls_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tls_routes_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tls_route.ListTlsRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tls_route.ListTlsRoutesResponse()
        )
        await client.list_tls_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_tls_routes_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tls_route.ListTlsRoutesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tls_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tls_routes_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tls_routes(
            tls_route.ListTlsRoutesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tls_routes_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tls_route.ListTlsRoutesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tls_route.ListTlsRoutesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tls_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_tls_routes_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tls_routes(
            tls_route.ListTlsRoutesRequest(),
            parent="parent_value",
        )


def test_list_tls_routes_pager(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
                next_page_token="abc",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[],
                next_page_token="def",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                ],
                next_page_token="ghi",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tls_routes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tls_route.TlsRoute) for i in results)


def test_list_tls_routes_pages(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tls_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
                next_page_token="abc",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[],
                next_page_token="def",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                ],
                next_page_token="ghi",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tls_routes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tls_routes_async_pager():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tls_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
                next_page_token="abc",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[],
                next_page_token="def",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                ],
                next_page_token="ghi",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tls_routes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tls_route.TlsRoute) for i in responses)


@pytest.mark.asyncio
async def test_list_tls_routes_async_pages():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tls_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
                next_page_token="abc",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[],
                next_page_token="def",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                ],
                next_page_token="ghi",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tls_routes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tls_route.GetTlsRouteRequest,
        dict,
    ],
)
def test_get_tls_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tls_route.TlsRoute(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            meshes=["meshes_value"],
            gateways=["gateways_value"],
        )
        response = client.get_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.GetTlsRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tls_route.TlsRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


def test_get_tls_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tls_route), "__call__") as call:
        client.get_tls_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.GetTlsRouteRequest()


@pytest.mark.asyncio
async def test_get_tls_route_async(
    transport: str = "grpc_asyncio", request_type=tls_route.GetTlsRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tls_route.TlsRoute(
                name="name_value",
                self_link="self_link_value",
                description="description_value",
                meshes=["meshes_value"],
                gateways=["gateways_value"],
            )
        )
        response = await client.get_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.GetTlsRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tls_route.TlsRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


@pytest.mark.asyncio
async def test_get_tls_route_async_from_dict():
    await test_get_tls_route_async(request_type=dict)


def test_get_tls_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tls_route.GetTlsRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tls_route), "__call__") as call:
        call.return_value = tls_route.TlsRoute()
        client.get_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tls_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tls_route.GetTlsRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tls_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tls_route.TlsRoute())
        await client.get_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_tls_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tls_route.TlsRoute()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tls_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tls_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tls_route(
            tls_route.GetTlsRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tls_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tls_route.TlsRoute()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tls_route.TlsRoute())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tls_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_tls_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tls_route(
            tls_route.GetTlsRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_tls_route.CreateTlsRouteRequest,
        dict,
    ],
)
def test_create_tls_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tls_route.CreateTlsRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_tls_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tls_route), "__call__") as call:
        client.create_tls_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tls_route.CreateTlsRouteRequest()


@pytest.mark.asyncio
async def test_create_tls_route_async(
    transport: str = "grpc_asyncio", request_type=gcn_tls_route.CreateTlsRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tls_route.CreateTlsRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_tls_route_async_from_dict():
    await test_create_tls_route_async(request_type=dict)


def test_create_tls_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_tls_route.CreateTlsRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tls_route), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tls_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_tls_route.CreateTlsRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tls_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_tls_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tls_route(
            parent="parent_value",
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            tls_route_id="tls_route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tls_route
        mock_val = gcn_tls_route.TlsRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].tls_route_id
        mock_val = "tls_route_id_value"
        assert arg == mock_val


def test_create_tls_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tls_route(
            gcn_tls_route.CreateTlsRouteRequest(),
            parent="parent_value",
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            tls_route_id="tls_route_id_value",
        )


@pytest.mark.asyncio
async def test_create_tls_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tls_route(
            parent="parent_value",
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            tls_route_id="tls_route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tls_route
        mock_val = gcn_tls_route.TlsRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].tls_route_id
        mock_val = "tls_route_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tls_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tls_route(
            gcn_tls_route.CreateTlsRouteRequest(),
            parent="parent_value",
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            tls_route_id="tls_route_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_tls_route.UpdateTlsRouteRequest,
        dict,
    ],
)
def test_update_tls_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tls_route.UpdateTlsRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_tls_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tls_route), "__call__") as call:
        client.update_tls_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tls_route.UpdateTlsRouteRequest()


@pytest.mark.asyncio
async def test_update_tls_route_async(
    transport: str = "grpc_asyncio", request_type=gcn_tls_route.UpdateTlsRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_tls_route.UpdateTlsRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_tls_route_async_from_dict():
    await test_update_tls_route_async(request_type=dict)


def test_update_tls_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_tls_route.UpdateTlsRouteRequest()

    request.tls_route.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tls_route), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tls_route.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tls_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_tls_route.UpdateTlsRouteRequest()

    request.tls_route.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tls_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tls_route.name=name_value",
    ) in kw["metadata"]


def test_update_tls_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tls_route(
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tls_route
        mock_val = gcn_tls_route.TlsRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tls_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tls_route(
            gcn_tls_route.UpdateTlsRouteRequest(),
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tls_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tls_route(
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tls_route
        mock_val = gcn_tls_route.TlsRoute(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tls_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tls_route(
            gcn_tls_route.UpdateTlsRouteRequest(),
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tls_route.DeleteTlsRouteRequest,
        dict,
    ],
)
def test_delete_tls_route(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.DeleteTlsRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_tls_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tls_route), "__call__") as call:
        client.delete_tls_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.DeleteTlsRouteRequest()


@pytest.mark.asyncio
async def test_delete_tls_route_async(
    transport: str = "grpc_asyncio", request_type=tls_route.DeleteTlsRouteRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tls_route.DeleteTlsRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_tls_route_async_from_dict():
    await test_delete_tls_route_async(request_type=dict)


def test_delete_tls_route_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tls_route.DeleteTlsRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tls_route), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tls_route_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tls_route.DeleteTlsRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tls_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_tls_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_tls_route_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tls_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_tls_route_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tls_route(
            tls_route.DeleteTlsRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tls_route_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tls_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tls_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_tls_route_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tls_route(
            tls_route.DeleteTlsRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service_binding.ListServiceBindingsRequest,
        dict,
    ],
)
def test_list_service_bindings(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_binding.ListServiceBindingsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_service_bindings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.ListServiceBindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceBindingsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_service_bindings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        client.list_service_bindings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.ListServiceBindingsRequest()


@pytest.mark.asyncio
async def test_list_service_bindings_async(
    transport: str = "grpc_asyncio",
    request_type=service_binding.ListServiceBindingsRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_binding.ListServiceBindingsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_service_bindings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.ListServiceBindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceBindingsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_service_bindings_async_from_dict():
    await test_list_service_bindings_async(request_type=dict)


def test_list_service_bindings_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_binding.ListServiceBindingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        call.return_value = service_binding.ListServiceBindingsResponse()
        client.list_service_bindings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_service_bindings_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_binding.ListServiceBindingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_binding.ListServiceBindingsResponse()
        )
        await client.list_service_bindings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_service_bindings_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_binding.ListServiceBindingsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_service_bindings(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_service_bindings_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_service_bindings(
            service_binding.ListServiceBindingsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_service_bindings_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_binding.ListServiceBindingsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_binding.ListServiceBindingsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_service_bindings(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_service_bindings_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_service_bindings(
            service_binding.ListServiceBindingsRequest(),
            parent="parent_value",
        )


def test_list_service_bindings_pager(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
                next_page_token="abc",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[],
                next_page_token="def",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                ],
                next_page_token="ghi",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_service_bindings(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, service_binding.ServiceBinding) for i in results)


def test_list_service_bindings_pages(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
                next_page_token="abc",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[],
                next_page_token="def",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                ],
                next_page_token="ghi",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_service_bindings(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_service_bindings_async_pager():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
                next_page_token="abc",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[],
                next_page_token="def",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                ],
                next_page_token="ghi",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_service_bindings(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, service_binding.ServiceBinding) for i in responses)


@pytest.mark.asyncio
async def test_list_service_bindings_async_pages():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_bindings),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
                next_page_token="abc",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[],
                next_page_token="def",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                ],
                next_page_token="ghi",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_service_bindings(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service_binding.GetServiceBindingRequest,
        dict,
    ],
)
def test_get_service_binding(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_binding.ServiceBinding(
            name="name_value",
            description="description_value",
            service="service_value",
        )
        response = client.get_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.GetServiceBindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service_binding.ServiceBinding)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.service == "service_value"


def test_get_service_binding_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_binding), "__call__"
    ) as call:
        client.get_service_binding()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.GetServiceBindingRequest()


@pytest.mark.asyncio
async def test_get_service_binding_async(
    transport: str = "grpc_asyncio",
    request_type=service_binding.GetServiceBindingRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_binding.ServiceBinding(
                name="name_value",
                description="description_value",
                service="service_value",
            )
        )
        response = await client.get_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.GetServiceBindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service_binding.ServiceBinding)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.service == "service_value"


@pytest.mark.asyncio
async def test_get_service_binding_async_from_dict():
    await test_get_service_binding_async(request_type=dict)


def test_get_service_binding_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_binding.GetServiceBindingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_binding), "__call__"
    ) as call:
        call.return_value = service_binding.ServiceBinding()
        client.get_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_service_binding_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_binding.GetServiceBindingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_binding), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_binding.ServiceBinding()
        )
        await client.get_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_service_binding_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_binding.ServiceBinding()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service_binding(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_service_binding_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service_binding(
            service_binding.GetServiceBindingRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_service_binding_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_binding.ServiceBinding()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_binding.ServiceBinding()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_service_binding(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_service_binding_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service_binding(
            service_binding.GetServiceBindingRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_service_binding.CreateServiceBindingRequest,
        dict,
    ],
)
def test_create_service_binding(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_service_binding.CreateServiceBindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_service_binding_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_binding), "__call__"
    ) as call:
        client.create_service_binding()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_service_binding.CreateServiceBindingRequest()


@pytest.mark.asyncio
async def test_create_service_binding_async(
    transport: str = "grpc_asyncio",
    request_type=gcn_service_binding.CreateServiceBindingRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_service_binding.CreateServiceBindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_service_binding_async_from_dict():
    await test_create_service_binding_async(request_type=dict)


def test_create_service_binding_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_service_binding.CreateServiceBindingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_binding), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_service_binding_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_service_binding.CreateServiceBindingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_binding), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_service_binding_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service_binding(
            parent="parent_value",
            service_binding=gcn_service_binding.ServiceBinding(name="name_value"),
            service_binding_id="service_binding_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].service_binding
        mock_val = gcn_service_binding.ServiceBinding(name="name_value")
        assert arg == mock_val
        arg = args[0].service_binding_id
        mock_val = "service_binding_id_value"
        assert arg == mock_val


def test_create_service_binding_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service_binding(
            gcn_service_binding.CreateServiceBindingRequest(),
            parent="parent_value",
            service_binding=gcn_service_binding.ServiceBinding(name="name_value"),
            service_binding_id="service_binding_id_value",
        )


@pytest.mark.asyncio
async def test_create_service_binding_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_service_binding(
            parent="parent_value",
            service_binding=gcn_service_binding.ServiceBinding(name="name_value"),
            service_binding_id="service_binding_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].service_binding
        mock_val = gcn_service_binding.ServiceBinding(name="name_value")
        assert arg == mock_val
        arg = args[0].service_binding_id
        mock_val = "service_binding_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_service_binding_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_service_binding(
            gcn_service_binding.CreateServiceBindingRequest(),
            parent="parent_value",
            service_binding=gcn_service_binding.ServiceBinding(name="name_value"),
            service_binding_id="service_binding_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service_binding.DeleteServiceBindingRequest,
        dict,
    ],
)
def test_delete_service_binding(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.DeleteServiceBindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_service_binding_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_service_binding), "__call__"
    ) as call:
        client.delete_service_binding()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.DeleteServiceBindingRequest()


@pytest.mark.asyncio
async def test_delete_service_binding_async(
    transport: str = "grpc_asyncio",
    request_type=service_binding.DeleteServiceBindingRequest,
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service_binding.DeleteServiceBindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_service_binding_async_from_dict():
    await test_delete_service_binding_async(request_type=dict)


def test_delete_service_binding_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_binding.DeleteServiceBindingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_service_binding), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_service_binding_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_binding.DeleteServiceBindingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_service_binding), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_service_binding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_service_binding_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_service_binding(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_service_binding_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service_binding(
            service_binding.DeleteServiceBindingRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_service_binding_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_service_binding), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_service_binding(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_service_binding_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_service_binding(
            service_binding.DeleteServiceBindingRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        mesh.ListMeshesRequest,
        dict,
    ],
)
def test_list_meshes(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mesh.ListMeshesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_meshes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.ListMeshesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMeshesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_meshes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        client.list_meshes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.ListMeshesRequest()


@pytest.mark.asyncio
async def test_list_meshes_async(
    transport: str = "grpc_asyncio", request_type=mesh.ListMeshesRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            mesh.ListMeshesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_meshes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.ListMeshesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMeshesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_meshes_async_from_dict():
    await test_list_meshes_async(request_type=dict)


def test_list_meshes_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = mesh.ListMeshesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        call.return_value = mesh.ListMeshesResponse()
        client.list_meshes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_meshes_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = mesh.ListMeshesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            mesh.ListMeshesResponse()
        )
        await client.list_meshes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_meshes_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mesh.ListMeshesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_meshes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_meshes_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_meshes(
            mesh.ListMeshesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_meshes_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mesh.ListMeshesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            mesh.ListMeshesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_meshes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_meshes_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_meshes(
            mesh.ListMeshesRequest(),
            parent="parent_value",
        )


def test_list_meshes_pager(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
                next_page_token="abc",
            ),
            mesh.ListMeshesResponse(
                meshes=[],
                next_page_token="def",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                ],
                next_page_token="ghi",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_meshes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, mesh.Mesh) for i in results)


def test_list_meshes_pages(transport_name: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_meshes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
                next_page_token="abc",
            ),
            mesh.ListMeshesResponse(
                meshes=[],
                next_page_token="def",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                ],
                next_page_token="ghi",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_meshes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_meshes_async_pager():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_meshes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
                next_page_token="abc",
            ),
            mesh.ListMeshesResponse(
                meshes=[],
                next_page_token="def",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                ],
                next_page_token="ghi",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_meshes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, mesh.Mesh) for i in responses)


@pytest.mark.asyncio
async def test_list_meshes_async_pages():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_meshes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
                next_page_token="abc",
            ),
            mesh.ListMeshesResponse(
                meshes=[],
                next_page_token="def",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                ],
                next_page_token="ghi",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_meshes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        mesh.GetMeshRequest,
        dict,
    ],
)
def test_get_mesh(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mesh.Mesh(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            interception_port=1848,
        )
        response = client.get_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.GetMeshRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, mesh.Mesh)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.interception_port == 1848


def test_get_mesh_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mesh), "__call__") as call:
        client.get_mesh()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.GetMeshRequest()


@pytest.mark.asyncio
async def test_get_mesh_async(
    transport: str = "grpc_asyncio", request_type=mesh.GetMeshRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            mesh.Mesh(
                name="name_value",
                self_link="self_link_value",
                description="description_value",
                interception_port=1848,
            )
        )
        response = await client.get_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.GetMeshRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, mesh.Mesh)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.interception_port == 1848


@pytest.mark.asyncio
async def test_get_mesh_async_from_dict():
    await test_get_mesh_async(request_type=dict)


def test_get_mesh_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = mesh.GetMeshRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mesh), "__call__") as call:
        call.return_value = mesh.Mesh()
        client.get_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_mesh_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = mesh.GetMeshRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mesh), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(mesh.Mesh())
        await client.get_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_mesh_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mesh.Mesh()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_mesh(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_mesh_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_mesh(
            mesh.GetMeshRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_mesh_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mesh.Mesh()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(mesh.Mesh())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_mesh(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_mesh_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_mesh(
            mesh.GetMeshRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_mesh.CreateMeshRequest,
        dict,
    ],
)
def test_create_mesh(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_mesh.CreateMeshRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_mesh_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_mesh), "__call__") as call:
        client.create_mesh()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_mesh.CreateMeshRequest()


@pytest.mark.asyncio
async def test_create_mesh_async(
    transport: str = "grpc_asyncio", request_type=gcn_mesh.CreateMeshRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_mesh.CreateMeshRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_mesh_async_from_dict():
    await test_create_mesh_async(request_type=dict)


def test_create_mesh_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_mesh.CreateMeshRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_mesh), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_mesh_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_mesh.CreateMeshRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_mesh), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_mesh_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_mesh(
            parent="parent_value",
            mesh=gcn_mesh.Mesh(name="name_value"),
            mesh_id="mesh_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].mesh
        mock_val = gcn_mesh.Mesh(name="name_value")
        assert arg == mock_val
        arg = args[0].mesh_id
        mock_val = "mesh_id_value"
        assert arg == mock_val


def test_create_mesh_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_mesh(
            gcn_mesh.CreateMeshRequest(),
            parent="parent_value",
            mesh=gcn_mesh.Mesh(name="name_value"),
            mesh_id="mesh_id_value",
        )


@pytest.mark.asyncio
async def test_create_mesh_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_mesh(
            parent="parent_value",
            mesh=gcn_mesh.Mesh(name="name_value"),
            mesh_id="mesh_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].mesh
        mock_val = gcn_mesh.Mesh(name="name_value")
        assert arg == mock_val
        arg = args[0].mesh_id
        mock_val = "mesh_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_mesh_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_mesh(
            gcn_mesh.CreateMeshRequest(),
            parent="parent_value",
            mesh=gcn_mesh.Mesh(name="name_value"),
            mesh_id="mesh_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_mesh.UpdateMeshRequest,
        dict,
    ],
)
def test_update_mesh(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_mesh.UpdateMeshRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_mesh_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_mesh), "__call__") as call:
        client.update_mesh()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_mesh.UpdateMeshRequest()


@pytest.mark.asyncio
async def test_update_mesh_async(
    transport: str = "grpc_asyncio", request_type=gcn_mesh.UpdateMeshRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcn_mesh.UpdateMeshRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_mesh_async_from_dict():
    await test_update_mesh_async(request_type=dict)


def test_update_mesh_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_mesh.UpdateMeshRequest()

    request.mesh.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_mesh), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "mesh.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_mesh_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcn_mesh.UpdateMeshRequest()

    request.mesh.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_mesh), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "mesh.name=name_value",
    ) in kw["metadata"]


def test_update_mesh_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_mesh(
            mesh=gcn_mesh.Mesh(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].mesh
        mock_val = gcn_mesh.Mesh(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_mesh_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_mesh(
            gcn_mesh.UpdateMeshRequest(),
            mesh=gcn_mesh.Mesh(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_mesh_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_mesh(
            mesh=gcn_mesh.Mesh(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].mesh
        mock_val = gcn_mesh.Mesh(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_mesh_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_mesh(
            gcn_mesh.UpdateMeshRequest(),
            mesh=gcn_mesh.Mesh(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        mesh.DeleteMeshRequest,
        dict,
    ],
)
def test_delete_mesh(request_type, transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.DeleteMeshRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_mesh_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_mesh), "__call__") as call:
        client.delete_mesh()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.DeleteMeshRequest()


@pytest.mark.asyncio
async def test_delete_mesh_async(
    transport: str = "grpc_asyncio", request_type=mesh.DeleteMeshRequest
):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == mesh.DeleteMeshRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_mesh_async_from_dict():
    await test_delete_mesh_async(request_type=dict)


def test_delete_mesh_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = mesh.DeleteMeshRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_mesh), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_mesh_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = mesh.DeleteMeshRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_mesh), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_mesh(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_mesh_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_mesh(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_mesh_flattened_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_mesh(
            mesh.DeleteMeshRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_mesh_flattened_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_mesh), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_mesh(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_mesh_flattened_error_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_mesh(
            mesh.DeleteMeshRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        endpoint_policy.ListEndpointPoliciesRequest,
        dict,
    ],
)
def test_list_endpoint_policies_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = endpoint_policy.ListEndpointPoliciesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = endpoint_policy.ListEndpointPoliciesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_endpoint_policies(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEndpointPoliciesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_endpoint_policies_rest_required_fields(
    request_type=endpoint_policy.ListEndpointPoliciesRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_endpoint_policies._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_endpoint_policies._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = endpoint_policy.ListEndpointPoliciesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = endpoint_policy.ListEndpointPoliciesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_endpoint_policies(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_endpoint_policies_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_endpoint_policies._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_endpoint_policies_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_list_endpoint_policies"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_list_endpoint_policies"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = endpoint_policy.ListEndpointPoliciesRequest.pb(
            endpoint_policy.ListEndpointPoliciesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            endpoint_policy.ListEndpointPoliciesResponse.to_json(
                endpoint_policy.ListEndpointPoliciesResponse()
            )
        )

        request = endpoint_policy.ListEndpointPoliciesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = endpoint_policy.ListEndpointPoliciesResponse()

        client.list_endpoint_policies(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_endpoint_policies_rest_bad_request(
    transport: str = "rest", request_type=endpoint_policy.ListEndpointPoliciesRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_endpoint_policies(request)


def test_list_endpoint_policies_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = endpoint_policy.ListEndpointPoliciesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = endpoint_policy.ListEndpointPoliciesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_endpoint_policies(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/endpointPolicies"
            % client.transport._host,
            args[1],
        )


def test_list_endpoint_policies_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_endpoint_policies(
            endpoint_policy.ListEndpointPoliciesRequest(),
            parent="parent_value",
        )


def test_list_endpoint_policies_rest_pager(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="abc",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[],
                next_page_token="def",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                ],
                next_page_token="ghi",
            ),
            endpoint_policy.ListEndpointPoliciesResponse(
                endpoint_policies=[
                    endpoint_policy.EndpointPolicy(),
                    endpoint_policy.EndpointPolicy(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            endpoint_policy.ListEndpointPoliciesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_endpoint_policies(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, endpoint_policy.EndpointPolicy) for i in results)

        pages = list(client.list_endpoint_policies(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        endpoint_policy.GetEndpointPolicyRequest,
        dict,
    ],
)
def test_get_endpoint_policy_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = endpoint_policy.EndpointPolicy(
            name="name_value",
            type_=endpoint_policy.EndpointPolicy.EndpointPolicyType.SIDECAR_PROXY,
            authorization_policy="authorization_policy_value",
            description="description_value",
            server_tls_policy="server_tls_policy_value",
            client_tls_policy="client_tls_policy_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = endpoint_policy.EndpointPolicy.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_endpoint_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, endpoint_policy.EndpointPolicy)
    assert response.name == "name_value"
    assert (
        response.type_
        == endpoint_policy.EndpointPolicy.EndpointPolicyType.SIDECAR_PROXY
    )
    assert response.authorization_policy == "authorization_policy_value"
    assert response.description == "description_value"
    assert response.server_tls_policy == "server_tls_policy_value"
    assert response.client_tls_policy == "client_tls_policy_value"


def test_get_endpoint_policy_rest_required_fields(
    request_type=endpoint_policy.GetEndpointPolicyRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_endpoint_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_endpoint_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = endpoint_policy.EndpointPolicy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = endpoint_policy.EndpointPolicy.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_endpoint_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_endpoint_policy_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_endpoint_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_endpoint_policy_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_get_endpoint_policy"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_get_endpoint_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = endpoint_policy.GetEndpointPolicyRequest.pb(
            endpoint_policy.GetEndpointPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = endpoint_policy.EndpointPolicy.to_json(
            endpoint_policy.EndpointPolicy()
        )

        request = endpoint_policy.GetEndpointPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = endpoint_policy.EndpointPolicy()

        client.get_endpoint_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_endpoint_policy_rest_bad_request(
    transport: str = "rest", request_type=endpoint_policy.GetEndpointPolicyRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_endpoint_policy(request)


def test_get_endpoint_policy_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = endpoint_policy.EndpointPolicy()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = endpoint_policy.EndpointPolicy.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_endpoint_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/endpointPolicies/*}"
            % client.transport._host,
            args[1],
        )


def test_get_endpoint_policy_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_endpoint_policy(
            endpoint_policy.GetEndpointPolicyRequest(),
            name="name_value",
        )


def test_get_endpoint_policy_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_endpoint_policy.CreateEndpointPolicyRequest,
        dict,
    ],
)
def test_create_endpoint_policy_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["endpoint_policy"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "type_": 1,
        "authorization_policy": "authorization_policy_value",
        "endpoint_matcher": {
            "metadata_label_matcher": {
                "metadata_label_match_criteria": 1,
                "metadata_labels": [
                    {
                        "label_name": "label_name_value",
                        "label_value": "label_value_value",
                    }
                ],
            }
        },
        "traffic_port_selector": {"ports": ["ports_value1", "ports_value2"]},
        "description": "description_value",
        "server_tls_policy": "server_tls_policy_value",
        "client_tls_policy": "client_tls_policy_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_endpoint_policy(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_endpoint_policy_rest_required_fields(
    request_type=gcn_endpoint_policy.CreateEndpointPolicyRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["endpoint_policy_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "endpointPolicyId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_endpoint_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "endpointPolicyId" in jsonified_request
    assert jsonified_request["endpointPolicyId"] == request_init["endpoint_policy_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["endpointPolicyId"] = "endpoint_policy_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_endpoint_policy._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("endpoint_policy_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "endpointPolicyId" in jsonified_request
    assert jsonified_request["endpointPolicyId"] == "endpoint_policy_id_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_endpoint_policy(request)

            expected_params = [
                (
                    "endpointPolicyId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_endpoint_policy_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_endpoint_policy._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("endpointPolicyId",))
        & set(
            (
                "parent",
                "endpointPolicyId",
                "endpointPolicy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_endpoint_policy_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_create_endpoint_policy"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_create_endpoint_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_endpoint_policy.CreateEndpointPolicyRequest.pb(
            gcn_endpoint_policy.CreateEndpointPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_endpoint_policy.CreateEndpointPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_endpoint_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_endpoint_policy_rest_bad_request(
    transport: str = "rest",
    request_type=gcn_endpoint_policy.CreateEndpointPolicyRequest,
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["endpoint_policy"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "type_": 1,
        "authorization_policy": "authorization_policy_value",
        "endpoint_matcher": {
            "metadata_label_matcher": {
                "metadata_label_match_criteria": 1,
                "metadata_labels": [
                    {
                        "label_name": "label_name_value",
                        "label_value": "label_value_value",
                    }
                ],
            }
        },
        "traffic_port_selector": {"ports": ["ports_value1", "ports_value2"]},
        "description": "description_value",
        "server_tls_policy": "server_tls_policy_value",
        "client_tls_policy": "client_tls_policy_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_endpoint_policy(request)


def test_create_endpoint_policy_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            endpoint_policy_id="endpoint_policy_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_endpoint_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/endpointPolicies"
            % client.transport._host,
            args[1],
        )


def test_create_endpoint_policy_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_endpoint_policy(
            gcn_endpoint_policy.CreateEndpointPolicyRequest(),
            parent="parent_value",
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            endpoint_policy_id="endpoint_policy_id_value",
        )


def test_create_endpoint_policy_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_endpoint_policy.UpdateEndpointPolicyRequest,
        dict,
    ],
)
def test_update_endpoint_policy_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "endpoint_policy": {
            "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
        }
    }
    request_init["endpoint_policy"] = {
        "name": "projects/sample1/locations/sample2/endpointPolicies/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "type_": 1,
        "authorization_policy": "authorization_policy_value",
        "endpoint_matcher": {
            "metadata_label_matcher": {
                "metadata_label_match_criteria": 1,
                "metadata_labels": [
                    {
                        "label_name": "label_name_value",
                        "label_value": "label_value_value",
                    }
                ],
            }
        },
        "traffic_port_selector": {"ports": ["ports_value1", "ports_value2"]},
        "description": "description_value",
        "server_tls_policy": "server_tls_policy_value",
        "client_tls_policy": "client_tls_policy_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_endpoint_policy(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_endpoint_policy_rest_required_fields(
    request_type=gcn_endpoint_policy.UpdateEndpointPolicyRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_endpoint_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_endpoint_policy._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_endpoint_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_endpoint_policy_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_endpoint_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("endpointPolicy",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_endpoint_policy_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_update_endpoint_policy"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_update_endpoint_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_endpoint_policy.UpdateEndpointPolicyRequest.pb(
            gcn_endpoint_policy.UpdateEndpointPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_endpoint_policy.UpdateEndpointPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_endpoint_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_endpoint_policy_rest_bad_request(
    transport: str = "rest",
    request_type=gcn_endpoint_policy.UpdateEndpointPolicyRequest,
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "endpoint_policy": {
            "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
        }
    }
    request_init["endpoint_policy"] = {
        "name": "projects/sample1/locations/sample2/endpointPolicies/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "type_": 1,
        "authorization_policy": "authorization_policy_value",
        "endpoint_matcher": {
            "metadata_label_matcher": {
                "metadata_label_match_criteria": 1,
                "metadata_labels": [
                    {
                        "label_name": "label_name_value",
                        "label_value": "label_value_value",
                    }
                ],
            }
        },
        "traffic_port_selector": {"ports": ["ports_value1", "ports_value2"]},
        "description": "description_value",
        "server_tls_policy": "server_tls_policy_value",
        "client_tls_policy": "client_tls_policy_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_endpoint_policy(request)


def test_update_endpoint_policy_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "endpoint_policy": {
                "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_endpoint_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{endpoint_policy.name=projects/*/locations/*/endpointPolicies/*}"
            % client.transport._host,
            args[1],
        )


def test_update_endpoint_policy_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_endpoint_policy(
            gcn_endpoint_policy.UpdateEndpointPolicyRequest(),
            endpoint_policy=gcn_endpoint_policy.EndpointPolicy(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_endpoint_policy_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        endpoint_policy.DeleteEndpointPolicyRequest,
        dict,
    ],
)
def test_delete_endpoint_policy_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_endpoint_policy(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_endpoint_policy_rest_required_fields(
    request_type=endpoint_policy.DeleteEndpointPolicyRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_endpoint_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_endpoint_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_endpoint_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_endpoint_policy_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_endpoint_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_endpoint_policy_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_delete_endpoint_policy"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_delete_endpoint_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = endpoint_policy.DeleteEndpointPolicyRequest.pb(
            endpoint_policy.DeleteEndpointPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = endpoint_policy.DeleteEndpointPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_endpoint_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_endpoint_policy_rest_bad_request(
    transport: str = "rest", request_type=endpoint_policy.DeleteEndpointPolicyRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_endpoint_policy(request)


def test_delete_endpoint_policy_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/endpointPolicies/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_endpoint_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/endpointPolicies/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_endpoint_policy_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_endpoint_policy(
            endpoint_policy.DeleteEndpointPolicyRequest(),
            name="name_value",
        )


def test_delete_endpoint_policy_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gateway.ListGatewaysRequest,
        dict,
    ],
)
def test_list_gateways_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gateway.ListGatewaysResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gateway.ListGatewaysResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_gateways(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGatewaysPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_gateways_rest_required_fields(request_type=gateway.ListGatewaysRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_gateways._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_gateways._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gateway.ListGatewaysResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gateway.ListGatewaysResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_gateways(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_gateways_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_gateways._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_gateways_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_list_gateways"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_list_gateways"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gateway.ListGatewaysRequest.pb(gateway.ListGatewaysRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gateway.ListGatewaysResponse.to_json(
            gateway.ListGatewaysResponse()
        )

        request = gateway.ListGatewaysRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gateway.ListGatewaysResponse()

        client.list_gateways(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_gateways_rest_bad_request(
    transport: str = "rest", request_type=gateway.ListGatewaysRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_gateways(request)


def test_list_gateways_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gateway.ListGatewaysResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gateway.ListGatewaysResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_gateways(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/gateways" % client.transport._host,
            args[1],
        )


def test_list_gateways_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_gateways(
            gateway.ListGatewaysRequest(),
            parent="parent_value",
        )


def test_list_gateways_rest_pager(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
                next_page_token="abc",
            ),
            gateway.ListGatewaysResponse(
                gateways=[],
                next_page_token="def",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                ],
                next_page_token="ghi",
            ),
            gateway.ListGatewaysResponse(
                gateways=[
                    gateway.Gateway(),
                    gateway.Gateway(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(gateway.ListGatewaysResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_gateways(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, gateway.Gateway) for i in results)

        pages = list(client.list_gateways(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gateway.GetGatewayRequest,
        dict,
    ],
)
def test_get_gateway_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/gateways/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gateway.Gateway(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            type_=gateway.Gateway.Type.OPEN_MESH,
            ports=[568],
            scope="scope_value",
            server_tls_policy="server_tls_policy_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gateway.Gateway.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_gateway(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gateway.Gateway)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.type_ == gateway.Gateway.Type.OPEN_MESH
    assert response.ports == [568]
    assert response.scope == "scope_value"
    assert response.server_tls_policy == "server_tls_policy_value"


def test_get_gateway_rest_required_fields(request_type=gateway.GetGatewayRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gateway.Gateway()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gateway.Gateway.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_gateway(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_gateway_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_gateway._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_gateway_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_get_gateway"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_get_gateway"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gateway.GetGatewayRequest.pb(gateway.GetGatewayRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gateway.Gateway.to_json(gateway.Gateway())

        request = gateway.GetGatewayRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gateway.Gateway()

        client.get_gateway(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_gateway_rest_bad_request(
    transport: str = "rest", request_type=gateway.GetGatewayRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/gateways/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_gateway(request)


def test_get_gateway_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gateway.Gateway()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/gateways/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gateway.Gateway.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_gateway(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/gateways/*}" % client.transport._host,
            args[1],
        )


def test_get_gateway_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_gateway(
            gateway.GetGatewayRequest(),
            name="name_value",
        )


def test_get_gateway_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_gateway.CreateGatewayRequest,
        dict,
    ],
)
def test_create_gateway_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["gateway"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "type_": 1,
        "ports": [569, 570],
        "scope": "scope_value",
        "server_tls_policy": "server_tls_policy_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_gateway(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_gateway_rest_required_fields(
    request_type=gcn_gateway.CreateGatewayRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["gateway_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "gatewayId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "gatewayId" in jsonified_request
    assert jsonified_request["gatewayId"] == request_init["gateway_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["gatewayId"] = "gateway_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_gateway._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("gateway_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "gatewayId" in jsonified_request
    assert jsonified_request["gatewayId"] == "gateway_id_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_gateway(request)

            expected_params = [
                (
                    "gatewayId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_gateway_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_gateway._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("gatewayId",))
        & set(
            (
                "parent",
                "gatewayId",
                "gateway",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_gateway_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_create_gateway"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_create_gateway"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_gateway.CreateGatewayRequest.pb(
            gcn_gateway.CreateGatewayRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_gateway.CreateGatewayRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_gateway(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_gateway_rest_bad_request(
    transport: str = "rest", request_type=gcn_gateway.CreateGatewayRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["gateway"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "type_": 1,
        "ports": [569, 570],
        "scope": "scope_value",
        "server_tls_policy": "server_tls_policy_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_gateway(request)


def test_create_gateway_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            gateway=gcn_gateway.Gateway(name="name_value"),
            gateway_id="gateway_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_gateway(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/gateways" % client.transport._host,
            args[1],
        )


def test_create_gateway_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_gateway(
            gcn_gateway.CreateGatewayRequest(),
            parent="parent_value",
            gateway=gcn_gateway.Gateway(name="name_value"),
            gateway_id="gateway_id_value",
        )


def test_create_gateway_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_gateway.UpdateGatewayRequest,
        dict,
    ],
)
def test_update_gateway_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "gateway": {"name": "projects/sample1/locations/sample2/gateways/sample3"}
    }
    request_init["gateway"] = {
        "name": "projects/sample1/locations/sample2/gateways/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "type_": 1,
        "ports": [569, 570],
        "scope": "scope_value",
        "server_tls_policy": "server_tls_policy_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_gateway(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_gateway_rest_required_fields(
    request_type=gcn_gateway.UpdateGatewayRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_gateway._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_gateway(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_gateway_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_gateway._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("gateway",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_gateway_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_update_gateway"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_update_gateway"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_gateway.UpdateGatewayRequest.pb(
            gcn_gateway.UpdateGatewayRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_gateway.UpdateGatewayRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_gateway(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_gateway_rest_bad_request(
    transport: str = "rest", request_type=gcn_gateway.UpdateGatewayRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "gateway": {"name": "projects/sample1/locations/sample2/gateways/sample3"}
    }
    request_init["gateway"] = {
        "name": "projects/sample1/locations/sample2/gateways/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "type_": 1,
        "ports": [569, 570],
        "scope": "scope_value",
        "server_tls_policy": "server_tls_policy_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_gateway(request)


def test_update_gateway_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "gateway": {"name": "projects/sample1/locations/sample2/gateways/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            gateway=gcn_gateway.Gateway(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_gateway(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{gateway.name=projects/*/locations/*/gateways/*}"
            % client.transport._host,
            args[1],
        )


def test_update_gateway_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_gateway(
            gcn_gateway.UpdateGatewayRequest(),
            gateway=gcn_gateway.Gateway(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_gateway_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gateway.DeleteGatewayRequest,
        dict,
    ],
)
def test_delete_gateway_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/gateways/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_gateway(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_gateway_rest_required_fields(request_type=gateway.DeleteGatewayRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_gateway(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_gateway_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_gateway._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_gateway_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_delete_gateway"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_delete_gateway"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gateway.DeleteGatewayRequest.pb(gateway.DeleteGatewayRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gateway.DeleteGatewayRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_gateway(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_gateway_rest_bad_request(
    transport: str = "rest", request_type=gateway.DeleteGatewayRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/gateways/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_gateway(request)


def test_delete_gateway_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/gateways/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_gateway(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/gateways/*}" % client.transport._host,
            args[1],
        )


def test_delete_gateway_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_gateway(
            gateway.DeleteGatewayRequest(),
            name="name_value",
        )


def test_delete_gateway_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        grpc_route.ListGrpcRoutesRequest,
        dict,
    ],
)
def test_list_grpc_routes_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = grpc_route.ListGrpcRoutesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grpc_route.ListGrpcRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_grpc_routes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGrpcRoutesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_grpc_routes_rest_required_fields(
    request_type=grpc_route.ListGrpcRoutesRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_grpc_routes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_grpc_routes._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grpc_route.ListGrpcRoutesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grpc_route.ListGrpcRoutesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_grpc_routes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_grpc_routes_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_grpc_routes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_grpc_routes_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_list_grpc_routes"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_list_grpc_routes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grpc_route.ListGrpcRoutesRequest.pb(
            grpc_route.ListGrpcRoutesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grpc_route.ListGrpcRoutesResponse.to_json(
            grpc_route.ListGrpcRoutesResponse()
        )

        request = grpc_route.ListGrpcRoutesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grpc_route.ListGrpcRoutesResponse()

        client.list_grpc_routes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_grpc_routes_rest_bad_request(
    transport: str = "rest", request_type=grpc_route.ListGrpcRoutesRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_grpc_routes(request)


def test_list_grpc_routes_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = grpc_route.ListGrpcRoutesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grpc_route.ListGrpcRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_grpc_routes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/grpcRoutes" % client.transport._host,
            args[1],
        )


def test_list_grpc_routes_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_grpc_routes(
            grpc_route.ListGrpcRoutesRequest(),
            parent="parent_value",
        )


def test_list_grpc_routes_rest_pager(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="abc",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[],
                next_page_token="def",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                ],
                next_page_token="ghi",
            ),
            grpc_route.ListGrpcRoutesResponse(
                grpc_routes=[
                    grpc_route.GrpcRoute(),
                    grpc_route.GrpcRoute(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(grpc_route.ListGrpcRoutesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_grpc_routes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, grpc_route.GrpcRoute) for i in results)

        pages = list(client.list_grpc_routes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        grpc_route.GetGrpcRouteRequest,
        dict,
    ],
)
def test_get_grpc_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/grpcRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = grpc_route.GrpcRoute(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            hostnames=["hostnames_value"],
            meshes=["meshes_value"],
            gateways=["gateways_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grpc_route.GrpcRoute.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_grpc_route(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grpc_route.GrpcRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.hostnames == ["hostnames_value"]
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


def test_get_grpc_route_rest_required_fields(
    request_type=grpc_route.GetGrpcRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_grpc_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_grpc_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grpc_route.GrpcRoute()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grpc_route.GrpcRoute.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_grpc_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_grpc_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_grpc_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_grpc_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_get_grpc_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_get_grpc_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grpc_route.GetGrpcRouteRequest.pb(grpc_route.GetGrpcRouteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grpc_route.GrpcRoute.to_json(grpc_route.GrpcRoute())

        request = grpc_route.GetGrpcRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grpc_route.GrpcRoute()

        client.get_grpc_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_grpc_route_rest_bad_request(
    transport: str = "rest", request_type=grpc_route.GetGrpcRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/grpcRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_grpc_route(request)


def test_get_grpc_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = grpc_route.GrpcRoute()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/grpcRoutes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grpc_route.GrpcRoute.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_grpc_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/grpcRoutes/*}" % client.transport._host,
            args[1],
        )


def test_get_grpc_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_grpc_route(
            grpc_route.GetGrpcRouteRequest(),
            name="name_value",
        )


def test_get_grpc_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_grpc_route.CreateGrpcRouteRequest,
        dict,
    ],
)
def test_create_grpc_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["grpc_route"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "hostnames": ["hostnames_value1", "hostnames_value2"],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "rules": [
            {
                "matches": [
                    {
                        "method": {
                            "type_": 1,
                            "grpc_service": "grpc_service_value",
                            "grpc_method": "grpc_method_value",
                            "case_sensitive": True,
                        },
                        "headers": [
                            {"type_": 1, "key": "key_value", "value": "value_value"}
                        ],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "fault_injection_policy": {
                        "delay": {
                            "fixed_delay": {"seconds": 751, "nanos": 543},
                            "percentage": 1054,
                        },
                        "abort": {"http_status": 1219, "percentage": 1054},
                    },
                    "timeout": {},
                    "retry_policy": {
                        "retry_conditions": [
                            "retry_conditions_value1",
                            "retry_conditions_value2",
                        ],
                        "num_retries": 1197,
                    },
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_grpc_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_grpc_route_rest_required_fields(
    request_type=gcn_grpc_route.CreateGrpcRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["grpc_route_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "grpcRouteId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_grpc_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "grpcRouteId" in jsonified_request
    assert jsonified_request["grpcRouteId"] == request_init["grpc_route_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["grpcRouteId"] = "grpc_route_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_grpc_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("grpc_route_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "grpcRouteId" in jsonified_request
    assert jsonified_request["grpcRouteId"] == "grpc_route_id_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_grpc_route(request)

            expected_params = [
                (
                    "grpcRouteId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_grpc_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_grpc_route._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("grpcRouteId",))
        & set(
            (
                "parent",
                "grpcRouteId",
                "grpcRoute",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_grpc_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_create_grpc_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_create_grpc_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_grpc_route.CreateGrpcRouteRequest.pb(
            gcn_grpc_route.CreateGrpcRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_grpc_route.CreateGrpcRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_grpc_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_grpc_route_rest_bad_request(
    transport: str = "rest", request_type=gcn_grpc_route.CreateGrpcRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["grpc_route"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "hostnames": ["hostnames_value1", "hostnames_value2"],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "rules": [
            {
                "matches": [
                    {
                        "method": {
                            "type_": 1,
                            "grpc_service": "grpc_service_value",
                            "grpc_method": "grpc_method_value",
                            "case_sensitive": True,
                        },
                        "headers": [
                            {"type_": 1, "key": "key_value", "value": "value_value"}
                        ],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "fault_injection_policy": {
                        "delay": {
                            "fixed_delay": {"seconds": 751, "nanos": 543},
                            "percentage": 1054,
                        },
                        "abort": {"http_status": 1219, "percentage": 1054},
                    },
                    "timeout": {},
                    "retry_policy": {
                        "retry_conditions": [
                            "retry_conditions_value1",
                            "retry_conditions_value2",
                        ],
                        "num_retries": 1197,
                    },
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_grpc_route(request)


def test_create_grpc_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            grpc_route_id="grpc_route_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_grpc_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/grpcRoutes" % client.transport._host,
            args[1],
        )


def test_create_grpc_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_grpc_route(
            gcn_grpc_route.CreateGrpcRouteRequest(),
            parent="parent_value",
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            grpc_route_id="grpc_route_id_value",
        )


def test_create_grpc_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_grpc_route.UpdateGrpcRouteRequest,
        dict,
    ],
)
def test_update_grpc_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "grpc_route": {"name": "projects/sample1/locations/sample2/grpcRoutes/sample3"}
    }
    request_init["grpc_route"] = {
        "name": "projects/sample1/locations/sample2/grpcRoutes/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "hostnames": ["hostnames_value1", "hostnames_value2"],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "rules": [
            {
                "matches": [
                    {
                        "method": {
                            "type_": 1,
                            "grpc_service": "grpc_service_value",
                            "grpc_method": "grpc_method_value",
                            "case_sensitive": True,
                        },
                        "headers": [
                            {"type_": 1, "key": "key_value", "value": "value_value"}
                        ],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "fault_injection_policy": {
                        "delay": {
                            "fixed_delay": {"seconds": 751, "nanos": 543},
                            "percentage": 1054,
                        },
                        "abort": {"http_status": 1219, "percentage": 1054},
                    },
                    "timeout": {},
                    "retry_policy": {
                        "retry_conditions": [
                            "retry_conditions_value1",
                            "retry_conditions_value2",
                        ],
                        "num_retries": 1197,
                    },
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_grpc_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_grpc_route_rest_required_fields(
    request_type=gcn_grpc_route.UpdateGrpcRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_grpc_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_grpc_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_grpc_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_grpc_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_grpc_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("grpcRoute",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_grpc_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_update_grpc_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_update_grpc_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_grpc_route.UpdateGrpcRouteRequest.pb(
            gcn_grpc_route.UpdateGrpcRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_grpc_route.UpdateGrpcRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_grpc_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_grpc_route_rest_bad_request(
    transport: str = "rest", request_type=gcn_grpc_route.UpdateGrpcRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "grpc_route": {"name": "projects/sample1/locations/sample2/grpcRoutes/sample3"}
    }
    request_init["grpc_route"] = {
        "name": "projects/sample1/locations/sample2/grpcRoutes/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "hostnames": ["hostnames_value1", "hostnames_value2"],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "rules": [
            {
                "matches": [
                    {
                        "method": {
                            "type_": 1,
                            "grpc_service": "grpc_service_value",
                            "grpc_method": "grpc_method_value",
                            "case_sensitive": True,
                        },
                        "headers": [
                            {"type_": 1, "key": "key_value", "value": "value_value"}
                        ],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "fault_injection_policy": {
                        "delay": {
                            "fixed_delay": {"seconds": 751, "nanos": 543},
                            "percentage": 1054,
                        },
                        "abort": {"http_status": 1219, "percentage": 1054},
                    },
                    "timeout": {},
                    "retry_policy": {
                        "retry_conditions": [
                            "retry_conditions_value1",
                            "retry_conditions_value2",
                        ],
                        "num_retries": 1197,
                    },
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_grpc_route(request)


def test_update_grpc_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "grpc_route": {
                "name": "projects/sample1/locations/sample2/grpcRoutes/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_grpc_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{grpc_route.name=projects/*/locations/*/grpcRoutes/*}"
            % client.transport._host,
            args[1],
        )


def test_update_grpc_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_grpc_route(
            gcn_grpc_route.UpdateGrpcRouteRequest(),
            grpc_route=gcn_grpc_route.GrpcRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_grpc_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        grpc_route.DeleteGrpcRouteRequest,
        dict,
    ],
)
def test_delete_grpc_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/grpcRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_grpc_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_grpc_route_rest_required_fields(
    request_type=grpc_route.DeleteGrpcRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_grpc_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_grpc_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_grpc_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_grpc_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_grpc_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_grpc_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_delete_grpc_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_delete_grpc_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grpc_route.DeleteGrpcRouteRequest.pb(
            grpc_route.DeleteGrpcRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = grpc_route.DeleteGrpcRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_grpc_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_grpc_route_rest_bad_request(
    transport: str = "rest", request_type=grpc_route.DeleteGrpcRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/grpcRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_grpc_route(request)


def test_delete_grpc_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/grpcRoutes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_grpc_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/grpcRoutes/*}" % client.transport._host,
            args[1],
        )


def test_delete_grpc_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_grpc_route(
            grpc_route.DeleteGrpcRouteRequest(),
            name="name_value",
        )


def test_delete_grpc_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        http_route.ListHttpRoutesRequest,
        dict,
    ],
)
def test_list_http_routes_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = http_route.ListHttpRoutesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = http_route.ListHttpRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_http_routes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListHttpRoutesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_http_routes_rest_required_fields(
    request_type=http_route.ListHttpRoutesRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_http_routes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_http_routes._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = http_route.ListHttpRoutesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = http_route.ListHttpRoutesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_http_routes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_http_routes_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_http_routes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_http_routes_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_list_http_routes"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_list_http_routes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = http_route.ListHttpRoutesRequest.pb(
            http_route.ListHttpRoutesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = http_route.ListHttpRoutesResponse.to_json(
            http_route.ListHttpRoutesResponse()
        )

        request = http_route.ListHttpRoutesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = http_route.ListHttpRoutesResponse()

        client.list_http_routes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_http_routes_rest_bad_request(
    transport: str = "rest", request_type=http_route.ListHttpRoutesRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_http_routes(request)


def test_list_http_routes_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = http_route.ListHttpRoutesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = http_route.ListHttpRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_http_routes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/httpRoutes" % client.transport._host,
            args[1],
        )


def test_list_http_routes_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_http_routes(
            http_route.ListHttpRoutesRequest(),
            parent="parent_value",
        )


def test_list_http_routes_rest_pager(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
                next_page_token="abc",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[],
                next_page_token="def",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                ],
                next_page_token="ghi",
            ),
            http_route.ListHttpRoutesResponse(
                http_routes=[
                    http_route.HttpRoute(),
                    http_route.HttpRoute(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(http_route.ListHttpRoutesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_http_routes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, http_route.HttpRoute) for i in results)

        pages = list(client.list_http_routes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        http_route.GetHttpRouteRequest,
        dict,
    ],
)
def test_get_http_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/httpRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = http_route.HttpRoute(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            hostnames=["hostnames_value"],
            meshes=["meshes_value"],
            gateways=["gateways_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = http_route.HttpRoute.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_http_route(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, http_route.HttpRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.hostnames == ["hostnames_value"]
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


def test_get_http_route_rest_required_fields(
    request_type=http_route.GetHttpRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_http_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_http_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = http_route.HttpRoute()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = http_route.HttpRoute.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_http_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_http_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_http_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_http_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_get_http_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_get_http_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = http_route.GetHttpRouteRequest.pb(http_route.GetHttpRouteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = http_route.HttpRoute.to_json(http_route.HttpRoute())

        request = http_route.GetHttpRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = http_route.HttpRoute()

        client.get_http_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_http_route_rest_bad_request(
    transport: str = "rest", request_type=http_route.GetHttpRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/httpRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_http_route(request)


def test_get_http_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = http_route.HttpRoute()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/httpRoutes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = http_route.HttpRoute.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_http_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/httpRoutes/*}" % client.transport._host,
            args[1],
        )


def test_get_http_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_http_route(
            http_route.GetHttpRouteRequest(),
            name="name_value",
        )


def test_get_http_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_http_route.CreateHttpRouteRequest,
        dict,
    ],
)
def test_create_http_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["http_route"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "hostnames": ["hostnames_value1", "hostnames_value2"],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "labels": {},
        "rules": [
            {
                "matches": [
                    {
                        "full_path_match": "full_path_match_value",
                        "prefix_match": "prefix_match_value",
                        "regex_match": "regex_match_value",
                        "ignore_case": True,
                        "headers": [
                            {
                                "exact_match": "exact_match_value",
                                "regex_match": "regex_match_value",
                                "prefix_match": "prefix_match_value",
                                "present_match": True,
                                "suffix_match": "suffix_match_value",
                                "range_match": {"start": 558, "end": 311},
                                "header": "header_value",
                                "invert_match": True,
                            }
                        ],
                        "query_parameters": [
                            {
                                "exact_match": "exact_match_value",
                                "regex_match": "regex_match_value",
                                "present_match": True,
                                "query_parameter": "query_parameter_value",
                            }
                        ],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "redirect": {
                        "host_redirect": "host_redirect_value",
                        "path_redirect": "path_redirect_value",
                        "prefix_rewrite": "prefix_rewrite_value",
                        "response_code": 1,
                        "https_redirect": True,
                        "strip_query": True,
                        "port_redirect": 1398,
                    },
                    "fault_injection_policy": {
                        "delay": {
                            "fixed_delay": {"seconds": 751, "nanos": 543},
                            "percentage": 1054,
                        },
                        "abort": {"http_status": 1219, "percentage": 1054},
                    },
                    "request_header_modifier": {
                        "set": {},
                        "add": {},
                        "remove": ["remove_value1", "remove_value2"],
                    },
                    "response_header_modifier": {},
                    "url_rewrite": {
                        "path_prefix_rewrite": "path_prefix_rewrite_value",
                        "host_rewrite": "host_rewrite_value",
                    },
                    "timeout": {},
                    "retry_policy": {
                        "retry_conditions": [
                            "retry_conditions_value1",
                            "retry_conditions_value2",
                        ],
                        "num_retries": 1197,
                        "per_try_timeout": {},
                    },
                    "request_mirror_policy": {"destination": {}},
                    "cors_policy": {
                        "allow_origins": [
                            "allow_origins_value1",
                            "allow_origins_value2",
                        ],
                        "allow_origin_regexes": [
                            "allow_origin_regexes_value1",
                            "allow_origin_regexes_value2",
                        ],
                        "allow_methods": [
                            "allow_methods_value1",
                            "allow_methods_value2",
                        ],
                        "allow_headers": [
                            "allow_headers_value1",
                            "allow_headers_value2",
                        ],
                        "expose_headers": [
                            "expose_headers_value1",
                            "expose_headers_value2",
                        ],
                        "max_age": "max_age_value",
                        "allow_credentials": True,
                        "disabled": True,
                    },
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_http_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_http_route_rest_required_fields(
    request_type=gcn_http_route.CreateHttpRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["http_route_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "httpRouteId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_http_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "httpRouteId" in jsonified_request
    assert jsonified_request["httpRouteId"] == request_init["http_route_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["httpRouteId"] = "http_route_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_http_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("http_route_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "httpRouteId" in jsonified_request
    assert jsonified_request["httpRouteId"] == "http_route_id_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_http_route(request)

            expected_params = [
                (
                    "httpRouteId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_http_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_http_route._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("httpRouteId",))
        & set(
            (
                "parent",
                "httpRouteId",
                "httpRoute",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_http_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_create_http_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_create_http_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_http_route.CreateHttpRouteRequest.pb(
            gcn_http_route.CreateHttpRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_http_route.CreateHttpRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_http_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_http_route_rest_bad_request(
    transport: str = "rest", request_type=gcn_http_route.CreateHttpRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["http_route"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "hostnames": ["hostnames_value1", "hostnames_value2"],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "labels": {},
        "rules": [
            {
                "matches": [
                    {
                        "full_path_match": "full_path_match_value",
                        "prefix_match": "prefix_match_value",
                        "regex_match": "regex_match_value",
                        "ignore_case": True,
                        "headers": [
                            {
                                "exact_match": "exact_match_value",
                                "regex_match": "regex_match_value",
                                "prefix_match": "prefix_match_value",
                                "present_match": True,
                                "suffix_match": "suffix_match_value",
                                "range_match": {"start": 558, "end": 311},
                                "header": "header_value",
                                "invert_match": True,
                            }
                        ],
                        "query_parameters": [
                            {
                                "exact_match": "exact_match_value",
                                "regex_match": "regex_match_value",
                                "present_match": True,
                                "query_parameter": "query_parameter_value",
                            }
                        ],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "redirect": {
                        "host_redirect": "host_redirect_value",
                        "path_redirect": "path_redirect_value",
                        "prefix_rewrite": "prefix_rewrite_value",
                        "response_code": 1,
                        "https_redirect": True,
                        "strip_query": True,
                        "port_redirect": 1398,
                    },
                    "fault_injection_policy": {
                        "delay": {
                            "fixed_delay": {"seconds": 751, "nanos": 543},
                            "percentage": 1054,
                        },
                        "abort": {"http_status": 1219, "percentage": 1054},
                    },
                    "request_header_modifier": {
                        "set": {},
                        "add": {},
                        "remove": ["remove_value1", "remove_value2"],
                    },
                    "response_header_modifier": {},
                    "url_rewrite": {
                        "path_prefix_rewrite": "path_prefix_rewrite_value",
                        "host_rewrite": "host_rewrite_value",
                    },
                    "timeout": {},
                    "retry_policy": {
                        "retry_conditions": [
                            "retry_conditions_value1",
                            "retry_conditions_value2",
                        ],
                        "num_retries": 1197,
                        "per_try_timeout": {},
                    },
                    "request_mirror_policy": {"destination": {}},
                    "cors_policy": {
                        "allow_origins": [
                            "allow_origins_value1",
                            "allow_origins_value2",
                        ],
                        "allow_origin_regexes": [
                            "allow_origin_regexes_value1",
                            "allow_origin_regexes_value2",
                        ],
                        "allow_methods": [
                            "allow_methods_value1",
                            "allow_methods_value2",
                        ],
                        "allow_headers": [
                            "allow_headers_value1",
                            "allow_headers_value2",
                        ],
                        "expose_headers": [
                            "expose_headers_value1",
                            "expose_headers_value2",
                        ],
                        "max_age": "max_age_value",
                        "allow_credentials": True,
                        "disabled": True,
                    },
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_http_route(request)


def test_create_http_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            http_route_id="http_route_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_http_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/httpRoutes" % client.transport._host,
            args[1],
        )


def test_create_http_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_http_route(
            gcn_http_route.CreateHttpRouteRequest(),
            parent="parent_value",
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            http_route_id="http_route_id_value",
        )


def test_create_http_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_http_route.UpdateHttpRouteRequest,
        dict,
    ],
)
def test_update_http_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "http_route": {"name": "projects/sample1/locations/sample2/httpRoutes/sample3"}
    }
    request_init["http_route"] = {
        "name": "projects/sample1/locations/sample2/httpRoutes/sample3",
        "self_link": "self_link_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "hostnames": ["hostnames_value1", "hostnames_value2"],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "labels": {},
        "rules": [
            {
                "matches": [
                    {
                        "full_path_match": "full_path_match_value",
                        "prefix_match": "prefix_match_value",
                        "regex_match": "regex_match_value",
                        "ignore_case": True,
                        "headers": [
                            {
                                "exact_match": "exact_match_value",
                                "regex_match": "regex_match_value",
                                "prefix_match": "prefix_match_value",
                                "present_match": True,
                                "suffix_match": "suffix_match_value",
                                "range_match": {"start": 558, "end": 311},
                                "header": "header_value",
                                "invert_match": True,
                            }
                        ],
                        "query_parameters": [
                            {
                                "exact_match": "exact_match_value",
                                "regex_match": "regex_match_value",
                                "present_match": True,
                                "query_parameter": "query_parameter_value",
                            }
                        ],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "redirect": {
                        "host_redirect": "host_redirect_value",
                        "path_redirect": "path_redirect_value",
                        "prefix_rewrite": "prefix_rewrite_value",
                        "response_code": 1,
                        "https_redirect": True,
                        "strip_query": True,
                        "port_redirect": 1398,
                    },
                    "fault_injection_policy": {
                        "delay": {
                            "fixed_delay": {"seconds": 751, "nanos": 543},
                            "percentage": 1054,
                        },
                        "abort": {"http_status": 1219, "percentage": 1054},
                    },
                    "request_header_modifier": {
                        "set": {},
                        "add": {},
                        "remove": ["remove_value1", "remove_value2"],
                    },
                    "response_header_modifier": {},
                    "url_rewrite": {
                        "path_prefix_rewrite": "path_prefix_rewrite_value",
                        "host_rewrite": "host_rewrite_value",
                    },
                    "timeout": {},
                    "retry_policy": {
                        "retry_conditions": [
                            "retry_conditions_value1",
                            "retry_conditions_value2",
                        ],
                        "num_retries": 1197,
                        "per_try_timeout": {},
                    },
                    "request_mirror_policy": {"destination": {}},
                    "cors_policy": {
                        "allow_origins": [
                            "allow_origins_value1",
                            "allow_origins_value2",
                        ],
                        "allow_origin_regexes": [
                            "allow_origin_regexes_value1",
                            "allow_origin_regexes_value2",
                        ],
                        "allow_methods": [
                            "allow_methods_value1",
                            "allow_methods_value2",
                        ],
                        "allow_headers": [
                            "allow_headers_value1",
                            "allow_headers_value2",
                        ],
                        "expose_headers": [
                            "expose_headers_value1",
                            "expose_headers_value2",
                        ],
                        "max_age": "max_age_value",
                        "allow_credentials": True,
                        "disabled": True,
                    },
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_http_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_http_route_rest_required_fields(
    request_type=gcn_http_route.UpdateHttpRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_http_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_http_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_http_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_http_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_http_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("httpRoute",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_http_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_update_http_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_update_http_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_http_route.UpdateHttpRouteRequest.pb(
            gcn_http_route.UpdateHttpRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_http_route.UpdateHttpRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_http_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_http_route_rest_bad_request(
    transport: str = "rest", request_type=gcn_http_route.UpdateHttpRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "http_route": {"name": "projects/sample1/locations/sample2/httpRoutes/sample3"}
    }
    request_init["http_route"] = {
        "name": "projects/sample1/locations/sample2/httpRoutes/sample3",
        "self_link": "self_link_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "hostnames": ["hostnames_value1", "hostnames_value2"],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "labels": {},
        "rules": [
            {
                "matches": [
                    {
                        "full_path_match": "full_path_match_value",
                        "prefix_match": "prefix_match_value",
                        "regex_match": "regex_match_value",
                        "ignore_case": True,
                        "headers": [
                            {
                                "exact_match": "exact_match_value",
                                "regex_match": "regex_match_value",
                                "prefix_match": "prefix_match_value",
                                "present_match": True,
                                "suffix_match": "suffix_match_value",
                                "range_match": {"start": 558, "end": 311},
                                "header": "header_value",
                                "invert_match": True,
                            }
                        ],
                        "query_parameters": [
                            {
                                "exact_match": "exact_match_value",
                                "regex_match": "regex_match_value",
                                "present_match": True,
                                "query_parameter": "query_parameter_value",
                            }
                        ],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "redirect": {
                        "host_redirect": "host_redirect_value",
                        "path_redirect": "path_redirect_value",
                        "prefix_rewrite": "prefix_rewrite_value",
                        "response_code": 1,
                        "https_redirect": True,
                        "strip_query": True,
                        "port_redirect": 1398,
                    },
                    "fault_injection_policy": {
                        "delay": {
                            "fixed_delay": {"seconds": 751, "nanos": 543},
                            "percentage": 1054,
                        },
                        "abort": {"http_status": 1219, "percentage": 1054},
                    },
                    "request_header_modifier": {
                        "set": {},
                        "add": {},
                        "remove": ["remove_value1", "remove_value2"],
                    },
                    "response_header_modifier": {},
                    "url_rewrite": {
                        "path_prefix_rewrite": "path_prefix_rewrite_value",
                        "host_rewrite": "host_rewrite_value",
                    },
                    "timeout": {},
                    "retry_policy": {
                        "retry_conditions": [
                            "retry_conditions_value1",
                            "retry_conditions_value2",
                        ],
                        "num_retries": 1197,
                        "per_try_timeout": {},
                    },
                    "request_mirror_policy": {"destination": {}},
                    "cors_policy": {
                        "allow_origins": [
                            "allow_origins_value1",
                            "allow_origins_value2",
                        ],
                        "allow_origin_regexes": [
                            "allow_origin_regexes_value1",
                            "allow_origin_regexes_value2",
                        ],
                        "allow_methods": [
                            "allow_methods_value1",
                            "allow_methods_value2",
                        ],
                        "allow_headers": [
                            "allow_headers_value1",
                            "allow_headers_value2",
                        ],
                        "expose_headers": [
                            "expose_headers_value1",
                            "expose_headers_value2",
                        ],
                        "max_age": "max_age_value",
                        "allow_credentials": True,
                        "disabled": True,
                    },
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_http_route(request)


def test_update_http_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "http_route": {
                "name": "projects/sample1/locations/sample2/httpRoutes/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_http_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{http_route.name=projects/*/locations/*/httpRoutes/*}"
            % client.transport._host,
            args[1],
        )


def test_update_http_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_http_route(
            gcn_http_route.UpdateHttpRouteRequest(),
            http_route=gcn_http_route.HttpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_http_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        http_route.DeleteHttpRouteRequest,
        dict,
    ],
)
def test_delete_http_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/httpRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_http_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_http_route_rest_required_fields(
    request_type=http_route.DeleteHttpRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_http_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_http_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_http_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_http_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_http_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_http_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_delete_http_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_delete_http_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = http_route.DeleteHttpRouteRequest.pb(
            http_route.DeleteHttpRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = http_route.DeleteHttpRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_http_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_http_route_rest_bad_request(
    transport: str = "rest", request_type=http_route.DeleteHttpRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/httpRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_http_route(request)


def test_delete_http_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/httpRoutes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_http_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/httpRoutes/*}" % client.transport._host,
            args[1],
        )


def test_delete_http_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_http_route(
            http_route.DeleteHttpRouteRequest(),
            name="name_value",
        )


def test_delete_http_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tcp_route.ListTcpRoutesRequest,
        dict,
    ],
)
def test_list_tcp_routes_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tcp_route.ListTcpRoutesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tcp_route.ListTcpRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tcp_routes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTcpRoutesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tcp_routes_rest_required_fields(
    request_type=tcp_route.ListTcpRoutesRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tcp_routes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tcp_routes._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tcp_route.ListTcpRoutesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = tcp_route.ListTcpRoutesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_tcp_routes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_tcp_routes_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_tcp_routes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tcp_routes_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_list_tcp_routes"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_list_tcp_routes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tcp_route.ListTcpRoutesRequest.pb(tcp_route.ListTcpRoutesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = tcp_route.ListTcpRoutesResponse.to_json(
            tcp_route.ListTcpRoutesResponse()
        )

        request = tcp_route.ListTcpRoutesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tcp_route.ListTcpRoutesResponse()

        client.list_tcp_routes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tcp_routes_rest_bad_request(
    transport: str = "rest", request_type=tcp_route.ListTcpRoutesRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_tcp_routes(request)


def test_list_tcp_routes_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tcp_route.ListTcpRoutesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tcp_route.ListTcpRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tcp_routes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/tcpRoutes" % client.transport._host,
            args[1],
        )


def test_list_tcp_routes_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tcp_routes(
            tcp_route.ListTcpRoutesRequest(),
            parent="parent_value",
        )


def test_list_tcp_routes_rest_pager(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
                next_page_token="abc",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[],
                next_page_token="def",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                ],
                next_page_token="ghi",
            ),
            tcp_route.ListTcpRoutesResponse(
                tcp_routes=[
                    tcp_route.TcpRoute(),
                    tcp_route.TcpRoute(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(tcp_route.ListTcpRoutesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_tcp_routes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tcp_route.TcpRoute) for i in results)

        pages = list(client.list_tcp_routes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tcp_route.GetTcpRouteRequest,
        dict,
    ],
)
def test_get_tcp_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tcpRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tcp_route.TcpRoute(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            meshes=["meshes_value"],
            gateways=["gateways_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tcp_route.TcpRoute.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_tcp_route(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tcp_route.TcpRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


def test_get_tcp_route_rest_required_fields(request_type=tcp_route.GetTcpRouteRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tcp_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tcp_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tcp_route.TcpRoute()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = tcp_route.TcpRoute.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_tcp_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_tcp_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_tcp_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_tcp_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_get_tcp_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_get_tcp_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tcp_route.GetTcpRouteRequest.pb(tcp_route.GetTcpRouteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = tcp_route.TcpRoute.to_json(tcp_route.TcpRoute())

        request = tcp_route.GetTcpRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tcp_route.TcpRoute()

        client.get_tcp_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_tcp_route_rest_bad_request(
    transport: str = "rest", request_type=tcp_route.GetTcpRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tcpRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_tcp_route(request)


def test_get_tcp_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tcp_route.TcpRoute()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tcpRoutes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tcp_route.TcpRoute.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_tcp_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tcpRoutes/*}" % client.transport._host,
            args[1],
        )


def test_get_tcp_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tcp_route(
            tcp_route.GetTcpRouteRequest(),
            name="name_value",
        )


def test_get_tcp_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_tcp_route.CreateTcpRouteRequest,
        dict,
    ],
)
def test_create_tcp_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["tcp_route"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "description": "description_value",
        "rules": [
            {
                "matches": [{"address": "address_value", "port": "port_value"}],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "original_destination": True,
                },
            }
        ],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "labels": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_tcp_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_tcp_route_rest_required_fields(
    request_type=gcn_tcp_route.CreateTcpRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["tcp_route_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "tcpRouteId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tcp_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "tcpRouteId" in jsonified_request
    assert jsonified_request["tcpRouteId"] == request_init["tcp_route_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["tcpRouteId"] = "tcp_route_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tcp_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("tcp_route_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "tcpRouteId" in jsonified_request
    assert jsonified_request["tcpRouteId"] == "tcp_route_id_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_tcp_route(request)

            expected_params = [
                (
                    "tcpRouteId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_tcp_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_tcp_route._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("tcpRouteId",))
        & set(
            (
                "parent",
                "tcpRouteId",
                "tcpRoute",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_tcp_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_create_tcp_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_create_tcp_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_tcp_route.CreateTcpRouteRequest.pb(
            gcn_tcp_route.CreateTcpRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_tcp_route.CreateTcpRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_tcp_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_tcp_route_rest_bad_request(
    transport: str = "rest", request_type=gcn_tcp_route.CreateTcpRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["tcp_route"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "description": "description_value",
        "rules": [
            {
                "matches": [{"address": "address_value", "port": "port_value"}],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "original_destination": True,
                },
            }
        ],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "labels": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_tcp_route(request)


def test_create_tcp_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            tcp_route_id="tcp_route_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_tcp_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/tcpRoutes" % client.transport._host,
            args[1],
        )


def test_create_tcp_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tcp_route(
            gcn_tcp_route.CreateTcpRouteRequest(),
            parent="parent_value",
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            tcp_route_id="tcp_route_id_value",
        )


def test_create_tcp_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_tcp_route.UpdateTcpRouteRequest,
        dict,
    ],
)
def test_update_tcp_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tcp_route": {"name": "projects/sample1/locations/sample2/tcpRoutes/sample3"}
    }
    request_init["tcp_route"] = {
        "name": "projects/sample1/locations/sample2/tcpRoutes/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "description": "description_value",
        "rules": [
            {
                "matches": [{"address": "address_value", "port": "port_value"}],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "original_destination": True,
                },
            }
        ],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "labels": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_tcp_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_tcp_route_rest_required_fields(
    request_type=gcn_tcp_route.UpdateTcpRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tcp_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tcp_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_tcp_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_tcp_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_tcp_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("tcpRoute",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_tcp_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_update_tcp_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_update_tcp_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_tcp_route.UpdateTcpRouteRequest.pb(
            gcn_tcp_route.UpdateTcpRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_tcp_route.UpdateTcpRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_tcp_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_tcp_route_rest_bad_request(
    transport: str = "rest", request_type=gcn_tcp_route.UpdateTcpRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tcp_route": {"name": "projects/sample1/locations/sample2/tcpRoutes/sample3"}
    }
    request_init["tcp_route"] = {
        "name": "projects/sample1/locations/sample2/tcpRoutes/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "description": "description_value",
        "rules": [
            {
                "matches": [{"address": "address_value", "port": "port_value"}],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ],
                    "original_destination": True,
                },
            }
        ],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
        "labels": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_tcp_route(request)


def test_update_tcp_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tcp_route": {
                "name": "projects/sample1/locations/sample2/tcpRoutes/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_tcp_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tcp_route.name=projects/*/locations/*/tcpRoutes/*}"
            % client.transport._host,
            args[1],
        )


def test_update_tcp_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tcp_route(
            gcn_tcp_route.UpdateTcpRouteRequest(),
            tcp_route=gcn_tcp_route.TcpRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_tcp_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tcp_route.DeleteTcpRouteRequest,
        dict,
    ],
)
def test_delete_tcp_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tcpRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_tcp_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_tcp_route_rest_required_fields(
    request_type=tcp_route.DeleteTcpRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tcp_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tcp_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_tcp_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_tcp_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_tcp_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_tcp_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_delete_tcp_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_delete_tcp_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tcp_route.DeleteTcpRouteRequest.pb(
            tcp_route.DeleteTcpRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = tcp_route.DeleteTcpRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_tcp_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_tcp_route_rest_bad_request(
    transport: str = "rest", request_type=tcp_route.DeleteTcpRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tcpRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_tcp_route(request)


def test_delete_tcp_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tcpRoutes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_tcp_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tcpRoutes/*}" % client.transport._host,
            args[1],
        )


def test_delete_tcp_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tcp_route(
            tcp_route.DeleteTcpRouteRequest(),
            name="name_value",
        )


def test_delete_tcp_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tls_route.ListTlsRoutesRequest,
        dict,
    ],
)
def test_list_tls_routes_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tls_route.ListTlsRoutesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tls_route.ListTlsRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tls_routes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTlsRoutesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tls_routes_rest_required_fields(
    request_type=tls_route.ListTlsRoutesRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tls_routes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tls_routes._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tls_route.ListTlsRoutesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = tls_route.ListTlsRoutesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_tls_routes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_tls_routes_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_tls_routes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tls_routes_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_list_tls_routes"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_list_tls_routes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tls_route.ListTlsRoutesRequest.pb(tls_route.ListTlsRoutesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = tls_route.ListTlsRoutesResponse.to_json(
            tls_route.ListTlsRoutesResponse()
        )

        request = tls_route.ListTlsRoutesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tls_route.ListTlsRoutesResponse()

        client.list_tls_routes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tls_routes_rest_bad_request(
    transport: str = "rest", request_type=tls_route.ListTlsRoutesRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_tls_routes(request)


def test_list_tls_routes_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tls_route.ListTlsRoutesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tls_route.ListTlsRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tls_routes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/tlsRoutes" % client.transport._host,
            args[1],
        )


def test_list_tls_routes_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tls_routes(
            tls_route.ListTlsRoutesRequest(),
            parent="parent_value",
        )


def test_list_tls_routes_rest_pager(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
                next_page_token="abc",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[],
                next_page_token="def",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                ],
                next_page_token="ghi",
            ),
            tls_route.ListTlsRoutesResponse(
                tls_routes=[
                    tls_route.TlsRoute(),
                    tls_route.TlsRoute(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(tls_route.ListTlsRoutesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_tls_routes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tls_route.TlsRoute) for i in results)

        pages = list(client.list_tls_routes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tls_route.GetTlsRouteRequest,
        dict,
    ],
)
def test_get_tls_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tlsRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tls_route.TlsRoute(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            meshes=["meshes_value"],
            gateways=["gateways_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tls_route.TlsRoute.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_tls_route(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tls_route.TlsRoute)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.meshes == ["meshes_value"]
    assert response.gateways == ["gateways_value"]


def test_get_tls_route_rest_required_fields(request_type=tls_route.GetTlsRouteRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tls_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tls_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tls_route.TlsRoute()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = tls_route.TlsRoute.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_tls_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_tls_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_tls_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_tls_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_get_tls_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_get_tls_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tls_route.GetTlsRouteRequest.pb(tls_route.GetTlsRouteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = tls_route.TlsRoute.to_json(tls_route.TlsRoute())

        request = tls_route.GetTlsRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tls_route.TlsRoute()

        client.get_tls_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_tls_route_rest_bad_request(
    transport: str = "rest", request_type=tls_route.GetTlsRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tlsRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_tls_route(request)


def test_get_tls_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tls_route.TlsRoute()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tlsRoutes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tls_route.TlsRoute.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_tls_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tlsRoutes/*}" % client.transport._host,
            args[1],
        )


def test_get_tls_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tls_route(
            tls_route.GetTlsRouteRequest(),
            name="name_value",
        )


def test_get_tls_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_tls_route.CreateTlsRouteRequest,
        dict,
    ],
)
def test_create_tls_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["tls_route"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "description": "description_value",
        "rules": [
            {
                "matches": [
                    {
                        "sni_host": ["sni_host_value1", "sni_host_value2"],
                        "alpn": ["alpn_value1", "alpn_value2"],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ]
                },
            }
        ],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_tls_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_tls_route_rest_required_fields(
    request_type=gcn_tls_route.CreateTlsRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["tls_route_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "tlsRouteId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tls_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "tlsRouteId" in jsonified_request
    assert jsonified_request["tlsRouteId"] == request_init["tls_route_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["tlsRouteId"] = "tls_route_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tls_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("tls_route_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "tlsRouteId" in jsonified_request
    assert jsonified_request["tlsRouteId"] == "tls_route_id_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_tls_route(request)

            expected_params = [
                (
                    "tlsRouteId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_tls_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_tls_route._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("tlsRouteId",))
        & set(
            (
                "parent",
                "tlsRouteId",
                "tlsRoute",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_tls_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_create_tls_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_create_tls_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_tls_route.CreateTlsRouteRequest.pb(
            gcn_tls_route.CreateTlsRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_tls_route.CreateTlsRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_tls_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_tls_route_rest_bad_request(
    transport: str = "rest", request_type=gcn_tls_route.CreateTlsRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["tls_route"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "description": "description_value",
        "rules": [
            {
                "matches": [
                    {
                        "sni_host": ["sni_host_value1", "sni_host_value2"],
                        "alpn": ["alpn_value1", "alpn_value2"],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ]
                },
            }
        ],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_tls_route(request)


def test_create_tls_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            tls_route_id="tls_route_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_tls_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/tlsRoutes" % client.transport._host,
            args[1],
        )


def test_create_tls_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tls_route(
            gcn_tls_route.CreateTlsRouteRequest(),
            parent="parent_value",
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            tls_route_id="tls_route_id_value",
        )


def test_create_tls_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_tls_route.UpdateTlsRouteRequest,
        dict,
    ],
)
def test_update_tls_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tls_route": {"name": "projects/sample1/locations/sample2/tlsRoutes/sample3"}
    }
    request_init["tls_route"] = {
        "name": "projects/sample1/locations/sample2/tlsRoutes/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "description": "description_value",
        "rules": [
            {
                "matches": [
                    {
                        "sni_host": ["sni_host_value1", "sni_host_value2"],
                        "alpn": ["alpn_value1", "alpn_value2"],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ]
                },
            }
        ],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_tls_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_tls_route_rest_required_fields(
    request_type=gcn_tls_route.UpdateTlsRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tls_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tls_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_tls_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_tls_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_tls_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("tlsRoute",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_tls_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_update_tls_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_update_tls_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_tls_route.UpdateTlsRouteRequest.pb(
            gcn_tls_route.UpdateTlsRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_tls_route.UpdateTlsRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_tls_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_tls_route_rest_bad_request(
    transport: str = "rest", request_type=gcn_tls_route.UpdateTlsRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tls_route": {"name": "projects/sample1/locations/sample2/tlsRoutes/sample3"}
    }
    request_init["tls_route"] = {
        "name": "projects/sample1/locations/sample2/tlsRoutes/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "description": "description_value",
        "rules": [
            {
                "matches": [
                    {
                        "sni_host": ["sni_host_value1", "sni_host_value2"],
                        "alpn": ["alpn_value1", "alpn_value2"],
                    }
                ],
                "action": {
                    "destinations": [
                        {"service_name": "service_name_value", "weight": 648}
                    ]
                },
            }
        ],
        "meshes": ["meshes_value1", "meshes_value2"],
        "gateways": ["gateways_value1", "gateways_value2"],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_tls_route(request)


def test_update_tls_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tls_route": {
                "name": "projects/sample1/locations/sample2/tlsRoutes/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_tls_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tls_route.name=projects/*/locations/*/tlsRoutes/*}"
            % client.transport._host,
            args[1],
        )


def test_update_tls_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tls_route(
            gcn_tls_route.UpdateTlsRouteRequest(),
            tls_route=gcn_tls_route.TlsRoute(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_tls_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tls_route.DeleteTlsRouteRequest,
        dict,
    ],
)
def test_delete_tls_route_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tlsRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_tls_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_tls_route_rest_required_fields(
    request_type=tls_route.DeleteTlsRouteRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tls_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tls_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_tls_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_tls_route_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_tls_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_tls_route_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_delete_tls_route"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_delete_tls_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tls_route.DeleteTlsRouteRequest.pb(
            tls_route.DeleteTlsRouteRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = tls_route.DeleteTlsRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_tls_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_tls_route_rest_bad_request(
    transport: str = "rest", request_type=tls_route.DeleteTlsRouteRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tlsRoutes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_tls_route(request)


def test_delete_tls_route_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tlsRoutes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_tls_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tlsRoutes/*}" % client.transport._host,
            args[1],
        )


def test_delete_tls_route_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tls_route(
            tls_route.DeleteTlsRouteRequest(),
            name="name_value",
        )


def test_delete_tls_route_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service_binding.ListServiceBindingsRequest,
        dict,
    ],
)
def test_list_service_bindings_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service_binding.ListServiceBindingsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = service_binding.ListServiceBindingsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_service_bindings(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceBindingsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_service_bindings_rest_required_fields(
    request_type=service_binding.ListServiceBindingsRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_service_bindings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_service_bindings._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service_binding.ListServiceBindingsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = service_binding.ListServiceBindingsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_service_bindings(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_service_bindings_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_service_bindings._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_service_bindings_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_list_service_bindings"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_list_service_bindings"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service_binding.ListServiceBindingsRequest.pb(
            service_binding.ListServiceBindingsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = service_binding.ListServiceBindingsResponse.to_json(
            service_binding.ListServiceBindingsResponse()
        )

        request = service_binding.ListServiceBindingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service_binding.ListServiceBindingsResponse()

        client.list_service_bindings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_service_bindings_rest_bad_request(
    transport: str = "rest", request_type=service_binding.ListServiceBindingsRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_service_bindings(request)


def test_list_service_bindings_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service_binding.ListServiceBindingsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = service_binding.ListServiceBindingsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_service_bindings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/serviceBindings"
            % client.transport._host,
            args[1],
        )


def test_list_service_bindings_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_service_bindings(
            service_binding.ListServiceBindingsRequest(),
            parent="parent_value",
        )


def test_list_service_bindings_rest_pager(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
                next_page_token="abc",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[],
                next_page_token="def",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                ],
                next_page_token="ghi",
            ),
            service_binding.ListServiceBindingsResponse(
                service_bindings=[
                    service_binding.ServiceBinding(),
                    service_binding.ServiceBinding(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            service_binding.ListServiceBindingsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_service_bindings(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, service_binding.ServiceBinding) for i in results)

        pages = list(client.list_service_bindings(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service_binding.GetServiceBindingRequest,
        dict,
    ],
)
def test_get_service_binding_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/serviceBindings/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service_binding.ServiceBinding(
            name="name_value",
            description="description_value",
            service="service_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = service_binding.ServiceBinding.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_service_binding(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service_binding.ServiceBinding)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.service == "service_value"


def test_get_service_binding_rest_required_fields(
    request_type=service_binding.GetServiceBindingRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_service_binding._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_service_binding._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service_binding.ServiceBinding()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = service_binding.ServiceBinding.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_service_binding(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_service_binding_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_service_binding._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_service_binding_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_get_service_binding"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_get_service_binding"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service_binding.GetServiceBindingRequest.pb(
            service_binding.GetServiceBindingRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = service_binding.ServiceBinding.to_json(
            service_binding.ServiceBinding()
        )

        request = service_binding.GetServiceBindingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service_binding.ServiceBinding()

        client.get_service_binding(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_service_binding_rest_bad_request(
    transport: str = "rest", request_type=service_binding.GetServiceBindingRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/serviceBindings/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_service_binding(request)


def test_get_service_binding_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service_binding.ServiceBinding()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/serviceBindings/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = service_binding.ServiceBinding.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_service_binding(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/serviceBindings/*}"
            % client.transport._host,
            args[1],
        )


def test_get_service_binding_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service_binding(
            service_binding.GetServiceBindingRequest(),
            name="name_value",
        )


def test_get_service_binding_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_service_binding.CreateServiceBindingRequest,
        dict,
    ],
)
def test_create_service_binding_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["service_binding"] = {
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "service": "service_value",
        "labels": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_service_binding(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_service_binding_rest_required_fields(
    request_type=gcn_service_binding.CreateServiceBindingRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["service_binding_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "serviceBindingId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_service_binding._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "serviceBindingId" in jsonified_request
    assert jsonified_request["serviceBindingId"] == request_init["service_binding_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["serviceBindingId"] = "service_binding_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_service_binding._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("service_binding_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "serviceBindingId" in jsonified_request
    assert jsonified_request["serviceBindingId"] == "service_binding_id_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_service_binding(request)

            expected_params = [
                (
                    "serviceBindingId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_service_binding_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_service_binding._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("serviceBindingId",))
        & set(
            (
                "parent",
                "serviceBindingId",
                "serviceBinding",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_service_binding_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_create_service_binding"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_create_service_binding"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_service_binding.CreateServiceBindingRequest.pb(
            gcn_service_binding.CreateServiceBindingRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_service_binding.CreateServiceBindingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_service_binding(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_service_binding_rest_bad_request(
    transport: str = "rest",
    request_type=gcn_service_binding.CreateServiceBindingRequest,
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["service_binding"] = {
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "service": "service_value",
        "labels": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_service_binding(request)


def test_create_service_binding_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            service_binding=gcn_service_binding.ServiceBinding(name="name_value"),
            service_binding_id="service_binding_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_service_binding(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/serviceBindings"
            % client.transport._host,
            args[1],
        )


def test_create_service_binding_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service_binding(
            gcn_service_binding.CreateServiceBindingRequest(),
            parent="parent_value",
            service_binding=gcn_service_binding.ServiceBinding(name="name_value"),
            service_binding_id="service_binding_id_value",
        )


def test_create_service_binding_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service_binding.DeleteServiceBindingRequest,
        dict,
    ],
)
def test_delete_service_binding_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/serviceBindings/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_service_binding(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_service_binding_rest_required_fields(
    request_type=service_binding.DeleteServiceBindingRequest,
):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_service_binding._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_service_binding._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_service_binding(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_service_binding_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_service_binding._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_service_binding_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_delete_service_binding"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_delete_service_binding"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service_binding.DeleteServiceBindingRequest.pb(
            service_binding.DeleteServiceBindingRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service_binding.DeleteServiceBindingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_service_binding(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_service_binding_rest_bad_request(
    transport: str = "rest", request_type=service_binding.DeleteServiceBindingRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/serviceBindings/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_service_binding(request)


def test_delete_service_binding_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/serviceBindings/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_service_binding(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/serviceBindings/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_service_binding_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service_binding(
            service_binding.DeleteServiceBindingRequest(),
            name="name_value",
        )


def test_delete_service_binding_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        mesh.ListMeshesRequest,
        dict,
    ],
)
def test_list_meshes_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = mesh.ListMeshesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = mesh.ListMeshesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_meshes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMeshesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_meshes_rest_required_fields(request_type=mesh.ListMeshesRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_meshes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_meshes._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = mesh.ListMeshesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = mesh.ListMeshesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_meshes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_meshes_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_meshes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_meshes_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_list_meshes"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_list_meshes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = mesh.ListMeshesRequest.pb(mesh.ListMeshesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = mesh.ListMeshesResponse.to_json(
            mesh.ListMeshesResponse()
        )

        request = mesh.ListMeshesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = mesh.ListMeshesResponse()

        client.list_meshes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_meshes_rest_bad_request(
    transport: str = "rest", request_type=mesh.ListMeshesRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_meshes(request)


def test_list_meshes_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = mesh.ListMeshesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = mesh.ListMeshesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_meshes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/meshes" % client.transport._host,
            args[1],
        )


def test_list_meshes_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_meshes(
            mesh.ListMeshesRequest(),
            parent="parent_value",
        )


def test_list_meshes_rest_pager(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
                next_page_token="abc",
            ),
            mesh.ListMeshesResponse(
                meshes=[],
                next_page_token="def",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                ],
                next_page_token="ghi",
            ),
            mesh.ListMeshesResponse(
                meshes=[
                    mesh.Mesh(),
                    mesh.Mesh(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(mesh.ListMeshesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_meshes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, mesh.Mesh) for i in results)

        pages = list(client.list_meshes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        mesh.GetMeshRequest,
        dict,
    ],
)
def test_get_mesh_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/meshes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = mesh.Mesh(
            name="name_value",
            self_link="self_link_value",
            description="description_value",
            interception_port=1848,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = mesh.Mesh.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_mesh(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, mesh.Mesh)
    assert response.name == "name_value"
    assert response.self_link == "self_link_value"
    assert response.description == "description_value"
    assert response.interception_port == 1848


def test_get_mesh_rest_required_fields(request_type=mesh.GetMeshRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_mesh._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_mesh._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = mesh.Mesh()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = mesh.Mesh.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_mesh(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_mesh_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_mesh._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_mesh_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_get_mesh"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_get_mesh"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = mesh.GetMeshRequest.pb(mesh.GetMeshRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = mesh.Mesh.to_json(mesh.Mesh())

        request = mesh.GetMeshRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = mesh.Mesh()

        client.get_mesh(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_mesh_rest_bad_request(
    transport: str = "rest", request_type=mesh.GetMeshRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/meshes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_mesh(request)


def test_get_mesh_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = mesh.Mesh()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/meshes/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = mesh.Mesh.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_mesh(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/meshes/*}" % client.transport._host,
            args[1],
        )


def test_get_mesh_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_mesh(
            mesh.GetMeshRequest(),
            name="name_value",
        )


def test_get_mesh_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_mesh.CreateMeshRequest,
        dict,
    ],
)
def test_create_mesh_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["mesh"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "interception_port": 1848,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_mesh(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_mesh_rest_required_fields(request_type=gcn_mesh.CreateMeshRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["mesh_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "meshId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_mesh._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "meshId" in jsonified_request
    assert jsonified_request["meshId"] == request_init["mesh_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["meshId"] = "mesh_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_mesh._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("mesh_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "meshId" in jsonified_request
    assert jsonified_request["meshId"] == "mesh_id_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_mesh(request)

            expected_params = [
                (
                    "meshId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_mesh_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_mesh._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("meshId",))
        & set(
            (
                "parent",
                "meshId",
                "mesh",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_mesh_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_create_mesh"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_create_mesh"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_mesh.CreateMeshRequest.pb(gcn_mesh.CreateMeshRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_mesh.CreateMeshRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_mesh(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_mesh_rest_bad_request(
    transport: str = "rest", request_type=gcn_mesh.CreateMeshRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["mesh"] = {
        "name": "name_value",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "interception_port": 1848,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_mesh(request)


def test_create_mesh_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            mesh=gcn_mesh.Mesh(name="name_value"),
            mesh_id="mesh_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_mesh(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/meshes" % client.transport._host,
            args[1],
        )


def test_create_mesh_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_mesh(
            gcn_mesh.CreateMeshRequest(),
            parent="parent_value",
            mesh=gcn_mesh.Mesh(name="name_value"),
            mesh_id="mesh_id_value",
        )


def test_create_mesh_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcn_mesh.UpdateMeshRequest,
        dict,
    ],
)
def test_update_mesh_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "mesh": {"name": "projects/sample1/locations/sample2/meshes/sample3"}
    }
    request_init["mesh"] = {
        "name": "projects/sample1/locations/sample2/meshes/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "interception_port": 1848,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_mesh(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_mesh_rest_required_fields(request_type=gcn_mesh.UpdateMeshRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_mesh._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_mesh._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_mesh(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_mesh_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_mesh._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("mesh",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_mesh_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_update_mesh"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_update_mesh"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcn_mesh.UpdateMeshRequest.pb(gcn_mesh.UpdateMeshRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = gcn_mesh.UpdateMeshRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_mesh(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_mesh_rest_bad_request(
    transport: str = "rest", request_type=gcn_mesh.UpdateMeshRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "mesh": {"name": "projects/sample1/locations/sample2/meshes/sample3"}
    }
    request_init["mesh"] = {
        "name": "projects/sample1/locations/sample2/meshes/sample3",
        "self_link": "self_link_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "interception_port": 1848,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_mesh(request)


def test_update_mesh_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "mesh": {"name": "projects/sample1/locations/sample2/meshes/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            mesh=gcn_mesh.Mesh(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_mesh(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{mesh.name=projects/*/locations/*/meshes/*}"
            % client.transport._host,
            args[1],
        )


def test_update_mesh_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_mesh(
            gcn_mesh.UpdateMeshRequest(),
            mesh=gcn_mesh.Mesh(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_mesh_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        mesh.DeleteMeshRequest,
        dict,
    ],
)
def test_delete_mesh_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/meshes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_mesh(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_mesh_rest_required_fields(request_type=mesh.DeleteMeshRequest):
    transport_class = transports.NetworkServicesRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_mesh._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_mesh._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_mesh(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_mesh_rest_unset_required_fields():
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_mesh._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_mesh_rest_interceptors(null_interceptor):
    transport = transports.NetworkServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.NetworkServicesRestInterceptor(),
    )
    client = NetworkServicesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.NetworkServicesRestInterceptor, "post_delete_mesh"
    ) as post, mock.patch.object(
        transports.NetworkServicesRestInterceptor, "pre_delete_mesh"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = mesh.DeleteMeshRequest.pb(mesh.DeleteMeshRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = mesh.DeleteMeshRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_mesh(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_mesh_rest_bad_request(
    transport: str = "rest", request_type=mesh.DeleteMeshRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/meshes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_mesh(request)


def test_delete_mesh_rest_flattened():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/meshes/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_mesh(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/meshes/*}" % client.transport._host,
            args[1],
        )


def test_delete_mesh_rest_flattened_error(transport: str = "rest"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_mesh(
            mesh.DeleteMeshRequest(),
            name="name_value",
        )


def test_delete_mesh_rest_error():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.NetworkServicesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = NetworkServicesClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.NetworkServicesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = NetworkServicesClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.NetworkServicesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = NetworkServicesClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = NetworkServicesClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.NetworkServicesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = NetworkServicesClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.NetworkServicesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = NetworkServicesClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.NetworkServicesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.NetworkServicesGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NetworkServicesGrpcTransport,
        transports.NetworkServicesGrpcAsyncIOTransport,
        transports.NetworkServicesRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = NetworkServicesClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.NetworkServicesGrpcTransport,
    )


def test_network_services_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.NetworkServicesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_network_services_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.network_services_v1.services.network_services.transports.NetworkServicesTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.NetworkServicesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_endpoint_policies",
        "get_endpoint_policy",
        "create_endpoint_policy",
        "update_endpoint_policy",
        "delete_endpoint_policy",
        "list_gateways",
        "get_gateway",
        "create_gateway",
        "update_gateway",
        "delete_gateway",
        "list_grpc_routes",
        "get_grpc_route",
        "create_grpc_route",
        "update_grpc_route",
        "delete_grpc_route",
        "list_http_routes",
        "get_http_route",
        "create_http_route",
        "update_http_route",
        "delete_http_route",
        "list_tcp_routes",
        "get_tcp_route",
        "create_tcp_route",
        "update_tcp_route",
        "delete_tcp_route",
        "list_tls_routes",
        "get_tls_route",
        "create_tls_route",
        "update_tls_route",
        "delete_tls_route",
        "list_service_bindings",
        "get_service_binding",
        "create_service_binding",
        "delete_service_binding",
        "list_meshes",
        "get_mesh",
        "create_mesh",
        "update_mesh",
        "delete_mesh",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
        "delete_operation",
        "list_operations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_network_services_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.network_services_v1.services.network_services.transports.NetworkServicesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.NetworkServicesTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_network_services_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.network_services_v1.services.network_services.transports.NetworkServicesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.NetworkServicesTransport()
        adc.assert_called_once()


def test_network_services_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        NetworkServicesClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NetworkServicesGrpcTransport,
        transports.NetworkServicesGrpcAsyncIOTransport,
    ],
)
def test_network_services_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NetworkServicesGrpcTransport,
        transports.NetworkServicesGrpcAsyncIOTransport,
        transports.NetworkServicesRestTransport,
    ],
)
def test_network_services_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.NetworkServicesGrpcTransport, grpc_helpers),
        (transports.NetworkServicesGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_network_services_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "networkservices.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="networkservices.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NetworkServicesGrpcTransport,
        transports.NetworkServicesGrpcAsyncIOTransport,
    ],
)
def test_network_services_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_network_services_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.NetworkServicesRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_network_services_rest_lro_client():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_network_services_host_no_port(transport_name):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="networkservices.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "networkservices.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://networkservices.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_network_services_host_with_port(transport_name):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="networkservices.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "networkservices.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://networkservices.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_network_services_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = NetworkServicesClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = NetworkServicesClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_endpoint_policies._session
    session2 = client2.transport.list_endpoint_policies._session
    assert session1 != session2
    session1 = client1.transport.get_endpoint_policy._session
    session2 = client2.transport.get_endpoint_policy._session
    assert session1 != session2
    session1 = client1.transport.create_endpoint_policy._session
    session2 = client2.transport.create_endpoint_policy._session
    assert session1 != session2
    session1 = client1.transport.update_endpoint_policy._session
    session2 = client2.transport.update_endpoint_policy._session
    assert session1 != session2
    session1 = client1.transport.delete_endpoint_policy._session
    session2 = client2.transport.delete_endpoint_policy._session
    assert session1 != session2
    session1 = client1.transport.list_gateways._session
    session2 = client2.transport.list_gateways._session
    assert session1 != session2
    session1 = client1.transport.get_gateway._session
    session2 = client2.transport.get_gateway._session
    assert session1 != session2
    session1 = client1.transport.create_gateway._session
    session2 = client2.transport.create_gateway._session
    assert session1 != session2
    session1 = client1.transport.update_gateway._session
    session2 = client2.transport.update_gateway._session
    assert session1 != session2
    session1 = client1.transport.delete_gateway._session
    session2 = client2.transport.delete_gateway._session
    assert session1 != session2
    session1 = client1.transport.list_grpc_routes._session
    session2 = client2.transport.list_grpc_routes._session
    assert session1 != session2
    session1 = client1.transport.get_grpc_route._session
    session2 = client2.transport.get_grpc_route._session
    assert session1 != session2
    session1 = client1.transport.create_grpc_route._session
    session2 = client2.transport.create_grpc_route._session
    assert session1 != session2
    session1 = client1.transport.update_grpc_route._session
    session2 = client2.transport.update_grpc_route._session
    assert session1 != session2
    session1 = client1.transport.delete_grpc_route._session
    session2 = client2.transport.delete_grpc_route._session
    assert session1 != session2
    session1 = client1.transport.list_http_routes._session
    session2 = client2.transport.list_http_routes._session
    assert session1 != session2
    session1 = client1.transport.get_http_route._session
    session2 = client2.transport.get_http_route._session
    assert session1 != session2
    session1 = client1.transport.create_http_route._session
    session2 = client2.transport.create_http_route._session
    assert session1 != session2
    session1 = client1.transport.update_http_route._session
    session2 = client2.transport.update_http_route._session
    assert session1 != session2
    session1 = client1.transport.delete_http_route._session
    session2 = client2.transport.delete_http_route._session
    assert session1 != session2
    session1 = client1.transport.list_tcp_routes._session
    session2 = client2.transport.list_tcp_routes._session
    assert session1 != session2
    session1 = client1.transport.get_tcp_route._session
    session2 = client2.transport.get_tcp_route._session
    assert session1 != session2
    session1 = client1.transport.create_tcp_route._session
    session2 = client2.transport.create_tcp_route._session
    assert session1 != session2
    session1 = client1.transport.update_tcp_route._session
    session2 = client2.transport.update_tcp_route._session
    assert session1 != session2
    session1 = client1.transport.delete_tcp_route._session
    session2 = client2.transport.delete_tcp_route._session
    assert session1 != session2
    session1 = client1.transport.list_tls_routes._session
    session2 = client2.transport.list_tls_routes._session
    assert session1 != session2
    session1 = client1.transport.get_tls_route._session
    session2 = client2.transport.get_tls_route._session
    assert session1 != session2
    session1 = client1.transport.create_tls_route._session
    session2 = client2.transport.create_tls_route._session
    assert session1 != session2
    session1 = client1.transport.update_tls_route._session
    session2 = client2.transport.update_tls_route._session
    assert session1 != session2
    session1 = client1.transport.delete_tls_route._session
    session2 = client2.transport.delete_tls_route._session
    assert session1 != session2
    session1 = client1.transport.list_service_bindings._session
    session2 = client2.transport.list_service_bindings._session
    assert session1 != session2
    session1 = client1.transport.get_service_binding._session
    session2 = client2.transport.get_service_binding._session
    assert session1 != session2
    session1 = client1.transport.create_service_binding._session
    session2 = client2.transport.create_service_binding._session
    assert session1 != session2
    session1 = client1.transport.delete_service_binding._session
    session2 = client2.transport.delete_service_binding._session
    assert session1 != session2
    session1 = client1.transport.list_meshes._session
    session2 = client2.transport.list_meshes._session
    assert session1 != session2
    session1 = client1.transport.get_mesh._session
    session2 = client2.transport.get_mesh._session
    assert session1 != session2
    session1 = client1.transport.create_mesh._session
    session2 = client2.transport.create_mesh._session
    assert session1 != session2
    session1 = client1.transport.update_mesh._session
    session2 = client2.transport.update_mesh._session
    assert session1 != session2
    session1 = client1.transport.delete_mesh._session
    session2 = client2.transport.delete_mesh._session
    assert session1 != session2


def test_network_services_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.NetworkServicesGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_network_services_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.NetworkServicesGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NetworkServicesGrpcTransport,
        transports.NetworkServicesGrpcAsyncIOTransport,
    ],
)
def test_network_services_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NetworkServicesGrpcTransport,
        transports.NetworkServicesGrpcAsyncIOTransport,
    ],
)
def test_network_services_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_network_services_grpc_lro_client():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_network_services_grpc_lro_async_client():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_authorization_policy_path():
    project = "squid"
    location = "clam"
    authorization_policy = "whelk"
    expected = "projects/{project}/locations/{location}/authorizationPolicies/{authorization_policy}".format(
        project=project,
        location=location,
        authorization_policy=authorization_policy,
    )
    actual = NetworkServicesClient.authorization_policy_path(
        project, location, authorization_policy
    )
    assert expected == actual


def test_parse_authorization_policy_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "authorization_policy": "nudibranch",
    }
    path = NetworkServicesClient.authorization_policy_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_authorization_policy_path(path)
    assert expected == actual


def test_backend_service_path():
    project = "cuttlefish"
    location = "mussel"
    backend_service = "winkle"
    expected = "projects/{project}/locations/{location}/backendServices/{backend_service}".format(
        project=project,
        location=location,
        backend_service=backend_service,
    )
    actual = NetworkServicesClient.backend_service_path(
        project, location, backend_service
    )
    assert expected == actual


def test_parse_backend_service_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "backend_service": "abalone",
    }
    path = NetworkServicesClient.backend_service_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_backend_service_path(path)
    assert expected == actual


def test_client_tls_policy_path():
    project = "squid"
    location = "clam"
    client_tls_policy = "whelk"
    expected = "projects/{project}/locations/{location}/clientTlsPolicies/{client_tls_policy}".format(
        project=project,
        location=location,
        client_tls_policy=client_tls_policy,
    )
    actual = NetworkServicesClient.client_tls_policy_path(
        project, location, client_tls_policy
    )
    assert expected == actual


def test_parse_client_tls_policy_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "client_tls_policy": "nudibranch",
    }
    path = NetworkServicesClient.client_tls_policy_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_client_tls_policy_path(path)
    assert expected == actual


def test_endpoint_policy_path():
    project = "cuttlefish"
    location = "mussel"
    endpoint_policy = "winkle"
    expected = "projects/{project}/locations/{location}/endpointPolicies/{endpoint_policy}".format(
        project=project,
        location=location,
        endpoint_policy=endpoint_policy,
    )
    actual = NetworkServicesClient.endpoint_policy_path(
        project, location, endpoint_policy
    )
    assert expected == actual


def test_parse_endpoint_policy_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "endpoint_policy": "abalone",
    }
    path = NetworkServicesClient.endpoint_policy_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_endpoint_policy_path(path)
    assert expected == actual


def test_gateway_path():
    project = "squid"
    location = "clam"
    gateway = "whelk"
    expected = "projects/{project}/locations/{location}/gateways/{gateway}".format(
        project=project,
        location=location,
        gateway=gateway,
    )
    actual = NetworkServicesClient.gateway_path(project, location, gateway)
    assert expected == actual


def test_parse_gateway_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "gateway": "nudibranch",
    }
    path = NetworkServicesClient.gateway_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_gateway_path(path)
    assert expected == actual


def test_grpc_route_path():
    project = "cuttlefish"
    location = "mussel"
    grpc_route = "winkle"
    expected = "projects/{project}/locations/{location}/grpcRoutes/{grpc_route}".format(
        project=project,
        location=location,
        grpc_route=grpc_route,
    )
    actual = NetworkServicesClient.grpc_route_path(project, location, grpc_route)
    assert expected == actual


def test_parse_grpc_route_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "grpc_route": "abalone",
    }
    path = NetworkServicesClient.grpc_route_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_grpc_route_path(path)
    assert expected == actual


def test_http_route_path():
    project = "squid"
    location = "clam"
    http_route = "whelk"
    expected = "projects/{project}/locations/{location}/httpRoutes/{http_route}".format(
        project=project,
        location=location,
        http_route=http_route,
    )
    actual = NetworkServicesClient.http_route_path(project, location, http_route)
    assert expected == actual


def test_parse_http_route_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "http_route": "nudibranch",
    }
    path = NetworkServicesClient.http_route_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_http_route_path(path)
    assert expected == actual


def test_mesh_path():
    project = "cuttlefish"
    location = "mussel"
    mesh = "winkle"
    expected = "projects/{project}/locations/{location}/meshes/{mesh}".format(
        project=project,
        location=location,
        mesh=mesh,
    )
    actual = NetworkServicesClient.mesh_path(project, location, mesh)
    assert expected == actual


def test_parse_mesh_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "mesh": "abalone",
    }
    path = NetworkServicesClient.mesh_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_mesh_path(path)
    assert expected == actual


def test_server_tls_policy_path():
    project = "squid"
    location = "clam"
    server_tls_policy = "whelk"
    expected = "projects/{project}/locations/{location}/serverTlsPolicies/{server_tls_policy}".format(
        project=project,
        location=location,
        server_tls_policy=server_tls_policy,
    )
    actual = NetworkServicesClient.server_tls_policy_path(
        project, location, server_tls_policy
    )
    assert expected == actual


def test_parse_server_tls_policy_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "server_tls_policy": "nudibranch",
    }
    path = NetworkServicesClient.server_tls_policy_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_server_tls_policy_path(path)
    assert expected == actual


def test_service_binding_path():
    project = "cuttlefish"
    location = "mussel"
    service_binding = "winkle"
    expected = "projects/{project}/locations/{location}/serviceBindings/{service_binding}".format(
        project=project,
        location=location,
        service_binding=service_binding,
    )
    actual = NetworkServicesClient.service_binding_path(
        project, location, service_binding
    )
    assert expected == actual


def test_parse_service_binding_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "service_binding": "abalone",
    }
    path = NetworkServicesClient.service_binding_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_service_binding_path(path)
    assert expected == actual


def test_tcp_route_path():
    project = "squid"
    location = "clam"
    tcp_route = "whelk"
    expected = "projects/{project}/locations/{location}/tcpRoutes/{tcp_route}".format(
        project=project,
        location=location,
        tcp_route=tcp_route,
    )
    actual = NetworkServicesClient.tcp_route_path(project, location, tcp_route)
    assert expected == actual


def test_parse_tcp_route_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "tcp_route": "nudibranch",
    }
    path = NetworkServicesClient.tcp_route_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_tcp_route_path(path)
    assert expected == actual


def test_tls_route_path():
    project = "cuttlefish"
    location = "mussel"
    tls_route = "winkle"
    expected = "projects/{project}/locations/{location}/tlsRoutes/{tls_route}".format(
        project=project,
        location=location,
        tls_route=tls_route,
    )
    actual = NetworkServicesClient.tls_route_path(project, location, tls_route)
    assert expected == actual


def test_parse_tls_route_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "tls_route": "abalone",
    }
    path = NetworkServicesClient.tls_route_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_tls_route_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = NetworkServicesClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = NetworkServicesClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = NetworkServicesClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = NetworkServicesClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = NetworkServicesClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = NetworkServicesClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = NetworkServicesClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = NetworkServicesClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = NetworkServicesClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = NetworkServicesClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = NetworkServicesClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.NetworkServicesTransport, "_prep_wrapped_messages"
    ) as prep:
        client = NetworkServicesClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.NetworkServicesTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = NetworkServicesClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_location_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.GetLocationRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.ListLocationsRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/edgeCacheKeysets/sample3"},
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {
        "resource": "projects/sample1/locations/sample2/edgeCacheKeysets/sample3"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/edgeCacheKeysets/sample3"},
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {
        "resource": "projects/sample1/locations/sample2/edgeCacheKeysets/sample3"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.TestIamPermissionsRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/edgeCacheKeysets/sample3"},
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.test_iam_permissions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {
        "resource": "projects/sample1/locations/sample2/edgeCacheKeysets/sample3"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_delete_operation_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = NetworkServicesClient(credentials=ga_credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_set_iam_policy(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_set_iam_policy_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


def test_get_iam_policy(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_iam_policy_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = NetworkServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_test_iam_permissions_from_dict_async():
    client = NetworkServicesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        response = await client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = NetworkServicesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = NetworkServicesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (NetworkServicesClient, transports.NetworkServicesGrpcTransport),
        (NetworkServicesAsyncClient, transports.NetworkServicesGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
