# -*- coding: utf-8 -*-
# Copyright 2014-2021 CERN
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# - Thomas Beermann <thomas.beermann@cern.ch>, 2014-2017
# - Vincent Garonne <vincent.garonne@cern.ch>, 2014
# - Mario Lassnig <mario.lassnig@cern.ch>, 2014-2018
# - Martin Barisits <martin.barisits@cern.ch>, 2014-2015
# - Ralph Vigne <ralph.vigne@cern.ch>, 2015
# - Cedric Serfon <cedric.serfon@cern.ch>, 2015-2019
# - Stefan Prenner <stefan.prenner@cern.ch>, 2018
# - Hannes Hansen <hannes.jakob.hansen@cern.ch>, 2018-2019
# - Ruturaj Gujar <ruturaj.gujar23@gmail.com>, 2019
# - Jaroslav Guenther <jaroslav.guenther@cern.ch>, 2020
# - Patrick Austin <patrick.austin@stfc.ac.uk>, 2020
# - Benedikt Ziemons <benedikt.ziemons@cern.ch>, 2020-2021
# - Radu Carpa <radu.carpa@cern.ch>, 2021

from rucio.web.ui.flask.main import application

if __name__ == '__main__':
    application.run()
