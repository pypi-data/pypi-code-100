'''
# AWS::HealthLake Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_healthlake as healthlake
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnFHIRDatastore(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-healthlake.CfnFHIRDatastore",
):
    '''A CloudFormation ``AWS::HealthLake::FHIRDatastore``.

    :cloudformationResource: AWS::HealthLake::FHIRDatastore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        datastore_type_version: builtins.str,
        datastore_name: typing.Optional[builtins.str] = None,
        preload_data_config: typing.Optional[typing.Union["CfnFHIRDatastore.PreloadDataConfigProperty", aws_cdk.core.IResolvable]] = None,
        sse_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFHIRDatastore.SseConfigurationProperty"]] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::HealthLake::FHIRDatastore``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param datastore_type_version: ``AWS::HealthLake::FHIRDatastore.DatastoreTypeVersion``.
        :param datastore_name: ``AWS::HealthLake::FHIRDatastore.DatastoreName``.
        :param preload_data_config: ``AWS::HealthLake::FHIRDatastore.PreloadDataConfig``.
        :param sse_configuration: ``AWS::HealthLake::FHIRDatastore.SseConfiguration``.
        :param tags: ``AWS::HealthLake::FHIRDatastore.Tags``.
        '''
        props = CfnFHIRDatastoreProps(
            datastore_type_version=datastore_type_version,
            datastore_name=datastore_name,
            preload_data_config=preload_data_config,
            sse_configuration=sse_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDatastoreArn")
    def attr_datastore_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: DatastoreArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDatastoreArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDatastoreEndpoint")
    def attr_datastore_endpoint(self) -> builtins.str:
        '''
        :cloudformationAttribute: DatastoreEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDatastoreEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDatastoreId")
    def attr_datastore_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: DatastoreId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDatastoreId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDatastoreStatus")
    def attr_datastore_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: DatastoreStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDatastoreStatus"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::HealthLake::FHIRDatastore.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="datastoreTypeVersion")
    def datastore_type_version(self) -> builtins.str:
        '''``AWS::HealthLake::FHIRDatastore.DatastoreTypeVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-datastoretypeversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "datastoreTypeVersion"))

    @datastore_type_version.setter
    def datastore_type_version(self, value: builtins.str) -> None:
        jsii.set(self, "datastoreTypeVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="datastoreName")
    def datastore_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::HealthLake::FHIRDatastore.DatastoreName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-datastorename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datastoreName"))

    @datastore_name.setter
    def datastore_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "datastoreName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="preloadDataConfig")
    def preload_data_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFHIRDatastore.PreloadDataConfigProperty", aws_cdk.core.IResolvable]]:
        '''``AWS::HealthLake::FHIRDatastore.PreloadDataConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-preloaddataconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFHIRDatastore.PreloadDataConfigProperty", aws_cdk.core.IResolvable]], jsii.get(self, "preloadDataConfig"))

    @preload_data_config.setter
    def preload_data_config(
        self,
        value: typing.Optional[typing.Union["CfnFHIRDatastore.PreloadDataConfigProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "preloadDataConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sseConfiguration")
    def sse_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFHIRDatastore.SseConfigurationProperty"]]:
        '''``AWS::HealthLake::FHIRDatastore.SseConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-sseconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFHIRDatastore.SseConfigurationProperty"]], jsii.get(self, "sseConfiguration"))

    @sse_configuration.setter
    def sse_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFHIRDatastore.SseConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "sseConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-healthlake.CfnFHIRDatastore.KmsEncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"cmk_type": "cmkType", "kms_key_id": "kmsKeyId"},
    )
    class KmsEncryptionConfigProperty:
        def __init__(
            self,
            *,
            cmk_type: builtins.str,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param cmk_type: ``CfnFHIRDatastore.KmsEncryptionConfigProperty.CmkType``.
            :param kms_key_id: ``CfnFHIRDatastore.KmsEncryptionConfigProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-kmsencryptionconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "cmk_type": cmk_type,
            }
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def cmk_type(self) -> builtins.str:
            '''``CfnFHIRDatastore.KmsEncryptionConfigProperty.CmkType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-kmsencryptionconfig.html#cfn-healthlake-fhirdatastore-kmsencryptionconfig-cmktype
            '''
            result = self._values.get("cmk_type")
            assert result is not None, "Required property 'cmk_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''``CfnFHIRDatastore.KmsEncryptionConfigProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-kmsencryptionconfig.html#cfn-healthlake-fhirdatastore-kmsencryptionconfig-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KmsEncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-healthlake.CfnFHIRDatastore.PreloadDataConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"preload_data_type": "preloadDataType"},
    )
    class PreloadDataConfigProperty:
        def __init__(self, *, preload_data_type: builtins.str) -> None:
            '''
            :param preload_data_type: ``CfnFHIRDatastore.PreloadDataConfigProperty.PreloadDataType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-preloaddataconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "preload_data_type": preload_data_type,
            }

        @builtins.property
        def preload_data_type(self) -> builtins.str:
            '''``CfnFHIRDatastore.PreloadDataConfigProperty.PreloadDataType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-preloaddataconfig.html#cfn-healthlake-fhirdatastore-preloaddataconfig-preloaddatatype
            '''
            result = self._values.get("preload_data_type")
            assert result is not None, "Required property 'preload_data_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PreloadDataConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-healthlake.CfnFHIRDatastore.SseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_encryption_config": "kmsEncryptionConfig"},
    )
    class SseConfigurationProperty:
        def __init__(
            self,
            *,
            kms_encryption_config: typing.Union[aws_cdk.core.IResolvable, "CfnFHIRDatastore.KmsEncryptionConfigProperty"],
        ) -> None:
            '''
            :param kms_encryption_config: ``CfnFHIRDatastore.SseConfigurationProperty.KmsEncryptionConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-sseconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "kms_encryption_config": kms_encryption_config,
            }

        @builtins.property
        def kms_encryption_config(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnFHIRDatastore.KmsEncryptionConfigProperty"]:
            '''``CfnFHIRDatastore.SseConfigurationProperty.KmsEncryptionConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-sseconfiguration.html#cfn-healthlake-fhirdatastore-sseconfiguration-kmsencryptionconfig
            '''
            result = self._values.get("kms_encryption_config")
            assert result is not None, "Required property 'kms_encryption_config' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnFHIRDatastore.KmsEncryptionConfigProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-healthlake.CfnFHIRDatastoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "datastore_type_version": "datastoreTypeVersion",
        "datastore_name": "datastoreName",
        "preload_data_config": "preloadDataConfig",
        "sse_configuration": "sseConfiguration",
        "tags": "tags",
    },
)
class CfnFHIRDatastoreProps:
    def __init__(
        self,
        *,
        datastore_type_version: builtins.str,
        datastore_name: typing.Optional[builtins.str] = None,
        preload_data_config: typing.Optional[typing.Union[CfnFHIRDatastore.PreloadDataConfigProperty, aws_cdk.core.IResolvable]] = None,
        sse_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFHIRDatastore.SseConfigurationProperty]] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::HealthLake::FHIRDatastore``.

        :param datastore_type_version: ``AWS::HealthLake::FHIRDatastore.DatastoreTypeVersion``.
        :param datastore_name: ``AWS::HealthLake::FHIRDatastore.DatastoreName``.
        :param preload_data_config: ``AWS::HealthLake::FHIRDatastore.PreloadDataConfig``.
        :param sse_configuration: ``AWS::HealthLake::FHIRDatastore.SseConfiguration``.
        :param tags: ``AWS::HealthLake::FHIRDatastore.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "datastore_type_version": datastore_type_version,
        }
        if datastore_name is not None:
            self._values["datastore_name"] = datastore_name
        if preload_data_config is not None:
            self._values["preload_data_config"] = preload_data_config
        if sse_configuration is not None:
            self._values["sse_configuration"] = sse_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def datastore_type_version(self) -> builtins.str:
        '''``AWS::HealthLake::FHIRDatastore.DatastoreTypeVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-datastoretypeversion
        '''
        result = self._values.get("datastore_type_version")
        assert result is not None, "Required property 'datastore_type_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datastore_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::HealthLake::FHIRDatastore.DatastoreName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-datastorename
        '''
        result = self._values.get("datastore_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preload_data_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFHIRDatastore.PreloadDataConfigProperty, aws_cdk.core.IResolvable]]:
        '''``AWS::HealthLake::FHIRDatastore.PreloadDataConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-preloaddataconfig
        '''
        result = self._values.get("preload_data_config")
        return typing.cast(typing.Optional[typing.Union[CfnFHIRDatastore.PreloadDataConfigProperty, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def sse_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFHIRDatastore.SseConfigurationProperty]]:
        '''``AWS::HealthLake::FHIRDatastore.SseConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-sseconfiguration
        '''
        result = self._values.get("sse_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFHIRDatastore.SseConfigurationProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::HealthLake::FHIRDatastore.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFHIRDatastoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnFHIRDatastore",
    "CfnFHIRDatastoreProps",
]

publication.publish()
