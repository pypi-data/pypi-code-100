# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ServiceArgs', 'Service']

@pulumi.input_type
class ServiceArgs:
    def __init__(__self__, *,
                 protocol: pulumi.Input[str],
                 ca_certificate_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 connect_timeout: Optional[pulumi.Input[int]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 read_timeout: Optional[pulumi.Input[int]] = None,
                 retries: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tls_verify: Optional[pulumi.Input[bool]] = None,
                 tls_verify_depth: Optional[pulumi.Input[int]] = None,
                 write_timeout: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Service resource.
        """
        pulumi.set(__self__, "protocol", protocol)
        if ca_certificate_ids is not None:
            pulumi.set(__self__, "ca_certificate_ids", ca_certificate_ids)
        if client_certificate_id is not None:
            pulumi.set(__self__, "client_certificate_id", client_certificate_id)
        if connect_timeout is not None:
            pulumi.set(__self__, "connect_timeout", connect_timeout)
        if host is not None:
            pulumi.set(__self__, "host", host)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if read_timeout is not None:
            pulumi.set(__self__, "read_timeout", read_timeout)
        if retries is not None:
            pulumi.set(__self__, "retries", retries)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tls_verify is not None:
            pulumi.set(__self__, "tls_verify", tls_verify)
        if tls_verify_depth is not None:
            pulumi.set(__self__, "tls_verify_depth", tls_verify_depth)
        if write_timeout is not None:
            pulumi.set(__self__, "write_timeout", write_timeout)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input[str]:
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="caCertificateIds")
    def ca_certificate_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "ca_certificate_ids")

    @ca_certificate_ids.setter
    def ca_certificate_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ca_certificate_ids", value)

    @property
    @pulumi.getter(name="clientCertificateId")
    def client_certificate_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "client_certificate_id")

    @client_certificate_id.setter
    def client_certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_certificate_id", value)

    @property
    @pulumi.getter(name="connectTimeout")
    def connect_timeout(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "connect_timeout")

    @connect_timeout.setter
    def connect_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "connect_timeout", value)

    @property
    @pulumi.getter
    def host(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "host")

    @host.setter
    def host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="readTimeout")
    def read_timeout(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "read_timeout")

    @read_timeout.setter
    def read_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "read_timeout", value)

    @property
    @pulumi.getter
    def retries(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "retries")

    @retries.setter
    def retries(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retries", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tlsVerify")
    def tls_verify(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "tls_verify")

    @tls_verify.setter
    def tls_verify(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "tls_verify", value)

    @property
    @pulumi.getter(name="tlsVerifyDepth")
    def tls_verify_depth(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "tls_verify_depth")

    @tls_verify_depth.setter
    def tls_verify_depth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "tls_verify_depth", value)

    @property
    @pulumi.getter(name="writeTimeout")
    def write_timeout(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "write_timeout")

    @write_timeout.setter
    def write_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "write_timeout", value)


@pulumi.input_type
class _ServiceState:
    def __init__(__self__, *,
                 ca_certificate_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 connect_timeout: Optional[pulumi.Input[int]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 read_timeout: Optional[pulumi.Input[int]] = None,
                 retries: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tls_verify: Optional[pulumi.Input[bool]] = None,
                 tls_verify_depth: Optional[pulumi.Input[int]] = None,
                 write_timeout: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Service resources.
        """
        if ca_certificate_ids is not None:
            pulumi.set(__self__, "ca_certificate_ids", ca_certificate_ids)
        if client_certificate_id is not None:
            pulumi.set(__self__, "client_certificate_id", client_certificate_id)
        if connect_timeout is not None:
            pulumi.set(__self__, "connect_timeout", connect_timeout)
        if host is not None:
            pulumi.set(__self__, "host", host)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if read_timeout is not None:
            pulumi.set(__self__, "read_timeout", read_timeout)
        if retries is not None:
            pulumi.set(__self__, "retries", retries)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tls_verify is not None:
            pulumi.set(__self__, "tls_verify", tls_verify)
        if tls_verify_depth is not None:
            pulumi.set(__self__, "tls_verify_depth", tls_verify_depth)
        if write_timeout is not None:
            pulumi.set(__self__, "write_timeout", write_timeout)

    @property
    @pulumi.getter(name="caCertificateIds")
    def ca_certificate_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "ca_certificate_ids")

    @ca_certificate_ids.setter
    def ca_certificate_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ca_certificate_ids", value)

    @property
    @pulumi.getter(name="clientCertificateId")
    def client_certificate_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "client_certificate_id")

    @client_certificate_id.setter
    def client_certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_certificate_id", value)

    @property
    @pulumi.getter(name="connectTimeout")
    def connect_timeout(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "connect_timeout")

    @connect_timeout.setter
    def connect_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "connect_timeout", value)

    @property
    @pulumi.getter
    def host(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "host")

    @host.setter
    def host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="readTimeout")
    def read_timeout(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "read_timeout")

    @read_timeout.setter
    def read_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "read_timeout", value)

    @property
    @pulumi.getter
    def retries(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "retries")

    @retries.setter
    def retries(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retries", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tlsVerify")
    def tls_verify(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "tls_verify")

    @tls_verify.setter
    def tls_verify(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "tls_verify", value)

    @property
    @pulumi.getter(name="tlsVerifyDepth")
    def tls_verify_depth(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "tls_verify_depth")

    @tls_verify_depth.setter
    def tls_verify_depth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "tls_verify_depth", value)

    @property
    @pulumi.getter(name="writeTimeout")
    def write_timeout(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "write_timeout")

    @write_timeout.setter
    def write_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "write_timeout", value)


class Service(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ca_certificate_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 connect_timeout: Optional[pulumi.Input[int]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 read_timeout: Optional[pulumi.Input[int]] = None,
                 retries: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tls_verify: Optional[pulumi.Input[bool]] = None,
                 tls_verify_depth: Optional[pulumi.Input[int]] = None,
                 write_timeout: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        ## # Service

        The service resource maps directly onto the json for the service endpoint in Kong.  For more information on the parameters [see the Kong Service create documentation](https://docs.konghq.com/gateway-oss/2.5.x/admin-api/#service-object).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_kong as kong

        service = kong.Service("service",
            connect_timeout=1000,
            host="test.org",
            path="/mypath",
            port=8080,
            protocol="http",
            read_timeout=3000,
            retries=5,
            write_timeout=2000)
        ```

        To use a client certificate and ca certificates combine with certificate resource (note protocol must be `https`):

        ```python
        import pulumi
        import pulumi_kong as kong

        certificate = kong.Certificate("certificate",
            certificate=\"\"\"    -----BEGIN CERTIFICATE-----
            ......
            -----END CERTIFICATE-----
        \"\"\",
            private_key=\"\"\"    -----BEGIN PRIVATE KEY-----
            .....
            -----END PRIVATE KEY-----
        \"\"\",
            snis=["foo.com"])
        ca = kong.Certificate("ca",
            certificate=\"\"\"    -----BEGIN CERTIFICATE-----
            ......
            -----END CERTIFICATE-----
        \"\"\",
            private_key=\"\"\"    -----BEGIN PRIVATE KEY-----
            .....
            -----END PRIVATE KEY-----
        \"\"\",
            snis=["ca.com"])
        service = kong.Service("service",
            protocol="https",
            host="test.org",
            tls_verify=True,
            tls_verify_depth=2,
            client_certificate_id=certificate.id,
            ca_certificate_ids=[ca.id])
        ```
        ## Argument reference

        * `name` - (Required) Service name
        * `protocol` - (Required) Protocol to use
        * `host` - (Optional) Host to map to
        * `port` - (Optional, int) Port to map to. Default: 80
        * `path` - (Optional) Path to map to
        * `retries` - (Optional, int) Number of retries. Default: 5
        * `connect_timeout` - (Optional, int) Connection timeout. Default(ms): 60000
        * `write_timeout` - (Optional, int) Write timout. Default(ms): 60000
        * `read_timeout` - (Optional, int) Read timeout. Default(ms): 60000
        * `tags` - (Optional) A list of strings associated with the Service for grouping and filtering.
        * `client_certificate_id` - (Optional) ID of Certificate to be used as client certificate while TLS handshaking to the upstream server. Use ID from `Certificate` resource
        * `tls_verify` - (Optional) Whether to enable verification of upstream server TLS certificate. If not set then the nginx default is respected.
        * `tls_verify_depth` - (Optional) Maximum depth of chain while verifying Upstream server’s TLS certificate.
        * `ca_certificate_ids` - (Optional) A of CA Certificate IDs (created from the certificate resource). that are used to build the trust store while verifying upstream server’s TLS certificate.

        ## Import

        To import a service

        ```sh
         $ pulumi import kong:index/service:Service <service_identifier> <service_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## # Service

        The service resource maps directly onto the json for the service endpoint in Kong.  For more information on the parameters [see the Kong Service create documentation](https://docs.konghq.com/gateway-oss/2.5.x/admin-api/#service-object).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_kong as kong

        service = kong.Service("service",
            connect_timeout=1000,
            host="test.org",
            path="/mypath",
            port=8080,
            protocol="http",
            read_timeout=3000,
            retries=5,
            write_timeout=2000)
        ```

        To use a client certificate and ca certificates combine with certificate resource (note protocol must be `https`):

        ```python
        import pulumi
        import pulumi_kong as kong

        certificate = kong.Certificate("certificate",
            certificate=\"\"\"    -----BEGIN CERTIFICATE-----
            ......
            -----END CERTIFICATE-----
        \"\"\",
            private_key=\"\"\"    -----BEGIN PRIVATE KEY-----
            .....
            -----END PRIVATE KEY-----
        \"\"\",
            snis=["foo.com"])
        ca = kong.Certificate("ca",
            certificate=\"\"\"    -----BEGIN CERTIFICATE-----
            ......
            -----END CERTIFICATE-----
        \"\"\",
            private_key=\"\"\"    -----BEGIN PRIVATE KEY-----
            .....
            -----END PRIVATE KEY-----
        \"\"\",
            snis=["ca.com"])
        service = kong.Service("service",
            protocol="https",
            host="test.org",
            tls_verify=True,
            tls_verify_depth=2,
            client_certificate_id=certificate.id,
            ca_certificate_ids=[ca.id])
        ```
        ## Argument reference

        * `name` - (Required) Service name
        * `protocol` - (Required) Protocol to use
        * `host` - (Optional) Host to map to
        * `port` - (Optional, int) Port to map to. Default: 80
        * `path` - (Optional) Path to map to
        * `retries` - (Optional, int) Number of retries. Default: 5
        * `connect_timeout` - (Optional, int) Connection timeout. Default(ms): 60000
        * `write_timeout` - (Optional, int) Write timout. Default(ms): 60000
        * `read_timeout` - (Optional, int) Read timeout. Default(ms): 60000
        * `tags` - (Optional) A list of strings associated with the Service for grouping and filtering.
        * `client_certificate_id` - (Optional) ID of Certificate to be used as client certificate while TLS handshaking to the upstream server. Use ID from `Certificate` resource
        * `tls_verify` - (Optional) Whether to enable verification of upstream server TLS certificate. If not set then the nginx default is respected.
        * `tls_verify_depth` - (Optional) Maximum depth of chain while verifying Upstream server’s TLS certificate.
        * `ca_certificate_ids` - (Optional) A of CA Certificate IDs (created from the certificate resource). that are used to build the trust store while verifying upstream server’s TLS certificate.

        ## Import

        To import a service

        ```sh
         $ pulumi import kong:index/service:Service <service_identifier> <service_id>
        ```

        :param str resource_name: The name of the resource.
        :param ServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ca_certificate_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 connect_timeout: Optional[pulumi.Input[int]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 read_timeout: Optional[pulumi.Input[int]] = None,
                 retries: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tls_verify: Optional[pulumi.Input[bool]] = None,
                 tls_verify_depth: Optional[pulumi.Input[int]] = None,
                 write_timeout: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceArgs.__new__(ServiceArgs)

            __props__.__dict__["ca_certificate_ids"] = ca_certificate_ids
            __props__.__dict__["client_certificate_id"] = client_certificate_id
            __props__.__dict__["connect_timeout"] = connect_timeout
            __props__.__dict__["host"] = host
            __props__.__dict__["name"] = name
            __props__.__dict__["path"] = path
            __props__.__dict__["port"] = port
            if protocol is None and not opts.urn:
                raise TypeError("Missing required property 'protocol'")
            __props__.__dict__["protocol"] = protocol
            __props__.__dict__["read_timeout"] = read_timeout
            __props__.__dict__["retries"] = retries
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tls_verify"] = tls_verify
            __props__.__dict__["tls_verify_depth"] = tls_verify_depth
            __props__.__dict__["write_timeout"] = write_timeout
        super(Service, __self__).__init__(
            'kong:index/service:Service',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            ca_certificate_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            client_certificate_id: Optional[pulumi.Input[str]] = None,
            connect_timeout: Optional[pulumi.Input[int]] = None,
            host: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            path: Optional[pulumi.Input[str]] = None,
            port: Optional[pulumi.Input[int]] = None,
            protocol: Optional[pulumi.Input[str]] = None,
            read_timeout: Optional[pulumi.Input[int]] = None,
            retries: Optional[pulumi.Input[int]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            tls_verify: Optional[pulumi.Input[bool]] = None,
            tls_verify_depth: Optional[pulumi.Input[int]] = None,
            write_timeout: Optional[pulumi.Input[int]] = None) -> 'Service':
        """
        Get an existing Service resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceState.__new__(_ServiceState)

        __props__.__dict__["ca_certificate_ids"] = ca_certificate_ids
        __props__.__dict__["client_certificate_id"] = client_certificate_id
        __props__.__dict__["connect_timeout"] = connect_timeout
        __props__.__dict__["host"] = host
        __props__.__dict__["name"] = name
        __props__.__dict__["path"] = path
        __props__.__dict__["port"] = port
        __props__.__dict__["protocol"] = protocol
        __props__.__dict__["read_timeout"] = read_timeout
        __props__.__dict__["retries"] = retries
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tls_verify"] = tls_verify
        __props__.__dict__["tls_verify_depth"] = tls_verify_depth
        __props__.__dict__["write_timeout"] = write_timeout
        return Service(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="caCertificateIds")
    def ca_certificate_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "ca_certificate_ids")

    @property
    @pulumi.getter(name="clientCertificateId")
    def client_certificate_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "client_certificate_id")

    @property
    @pulumi.getter(name="connectTimeout")
    def connect_timeout(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "connect_timeout")

    @property
    @pulumi.getter
    def host(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "host")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="readTimeout")
    def read_timeout(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "read_timeout")

    @property
    @pulumi.getter
    def retries(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "retries")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tlsVerify")
    def tls_verify(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "tls_verify")

    @property
    @pulumi.getter(name="tlsVerifyDepth")
    def tls_verify_depth(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "tls_verify_depth")

    @property
    @pulumi.getter(name="writeTimeout")
    def write_timeout(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "write_timeout")

