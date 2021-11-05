# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Rattail-COREPOS Config Extension
"""

from rattail.config import ConfigExtension
from rattail.db.config import get_engines


class RattailCOREPOSExtension(ConfigExtension):
    """
    Config extension for Rattail-COREPOS
    """
    key = 'rattail-corepos'

    def configure(self, config):

        # office_op
        from corepos.db.office_op import Session
        engines = get_engines(config, section='corepos.db.office_op')
        config.core_office_op_engines = engines
        config.core_office_op_engine = engines.get('default')
        Session.configure(bind=config.core_office_op_engine)
        # TODO: deprecate / remove these next 2 lines
        config.corepos_engines = engines
        config.corepos_engine = engines.get('default')

        # office_trans
        from corepos.db.office_trans import Session
        engines = get_engines(config, section='corepos.db.office_trans')
        config.core_office_trans_engines = engines
        config.core_office_trans_engine = engines.get('default')
        Session.configure(bind=config.core_office_trans_engine)
        # TODO: deprecate / remove these next 2 lines
        config.coretrans_engines = engines
        config.coretrans_engine = engines.get('default')

        # lane_op
        from corepos.db.lane_op import Session
        engines = get_engines(config, section='corepos.db.lane_op')
        config.core_lane_op_engines = engines
        config.core_lane_op_engine = engines.get('default')
        Session.configure(bind=config.core_lane_op_engine)


def core_office_url(config, require=False, **kwargs):
    """
    Returns the base URL for the CORE Office web app.  Note that this URL will
    *not* have a trailing slash.
    """
    args = ['corepos', 'office.url']
    if require:
        url = config.require(*args, **kwargs)
        return url.rstrip('/')
    else:
        url = config.get(*args, **kwargs)
        if url:
            return url.rstrip('/')


def core_office_customer_account_url(config, card_number, office_url=None):
    """
    Returns the CORE Office URL for the customer account with the given card
    number.
    """
    if not office_url:
        office_url = core_office_url(config, require=True)
    return '{}/mem/MemberEditor.php?memNum={}'.format(
        office_url, card_number)
