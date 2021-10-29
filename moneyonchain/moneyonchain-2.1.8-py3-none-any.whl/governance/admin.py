"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os
import logging
from web3.types import BlockIdentifier
from web3 import Web3

from moneyonchain.contract import ContractBase
from moneyonchain.events import BaseEvent
from .governor import OwnableInterface
from .governed import GovernedInterface


class ProxyAdmin(OwnableInterface):

    contract_name = 'ProxyAdmin'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/ProxyAdmin.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/ProxyAdmin.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['admin']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def implementation(self,
                       contract_address,
                       block_identifier: BlockIdentifier = 'latest'):
        """Get proxy implementation"""

        result = self.sc.getProxyImplementation(contract_address, block_identifier=block_identifier)

        return result


def admin_implementation(network_manager, contract_address, block_identifier: BlockIdentifier = 'latest'):
    """Implementation of contract"""

    contract_admin = ProxyAdmin(network_manager).from_abi()
    contract_address = Web3.toChecksumAddress(contract_address)

    return contract_admin.implementation(contract_address, block_identifier=block_identifier)


class ProxyAdminInterface(ContractBase):
    def implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Implementation of contract"""

        return admin_implementation(self.network_manager,
                                    self.contract_address,
                                    block_identifier=block_identifier)


class UpgradeDelegator(GovernedInterface):

    contract_name = 'UpgradeDelegator'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/UpgradeDelegator.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/UpgradeDelegator.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['upgradeDelegator']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def proxy_admin(self, block_identifier: BlockIdentifier = 'latest'):
        """Return Proxy admin address"""

        result = self.sc.proxyAdmin(block_identifier=block_identifier)

        return result

    def get_proxy_admin(self,
                        contract_address,
                        block_identifier: BlockIdentifier = 'latest'):
        """Returns the admin of a proxy. Only the admin can query it."""

        result = self.sc.getProxyAdmin(contract_address, block_identifier=block_identifier)

        return result

    def get_proxy_implementation(
            self,
            contract_address,
            block_identifier: BlockIdentifier = 'latest'):
        """Returns the current implementation of a proxy."""

        result = self.sc.getProxyImplementation(contract_address, block_identifier=block_identifier)

        return result


class AdminUpgradeabilityProxy(ContractBase):

    contract_name = 'AdminUpgradeabilityProxy'
    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/AdminUpgradeabilityProxy.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/AdminUpgradeabilityProxy.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            raise Exception("No contract address!")

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)


class UpgradeabilityProxyInterface(ContractBase):
    pass


class EventUpgradeabilityProxyUpgraded(BaseEvent):
    name = "Upgraded"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'Implementation']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['implementation'] = self.event['implementation']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['implementation']
                ]