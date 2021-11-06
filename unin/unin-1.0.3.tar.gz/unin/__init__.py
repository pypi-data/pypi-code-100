'''

This is a connection to the main folder of the duality package.

AVAILABLE MODULES IN THE PACKAGE:
	HUB
	---
	duality.hub is a hub of data manipulation tools.
		print(help(duality.hub)) in order to see available features.
	MONTECARLO
	---
	duality.MonteCarlo is a module for performing the Monte Carlo simulation over the defined data with a lot of useful features.
		print(help(duality.MonteCarlo)) in order to see available features.
	EOQ
	---
	duality.EOQ is a module for finding an Economic order quantity over the defined data with a lot of useful features.
		print(help(duality.EOQ)) in order to see available features.

'''

#imports essential functions from the duality package.
from duality import EOQ
from duality.hub import hub
from duality.hub.hub import *
from duality import MonteCarlo
from unin.misc._meta import (
	__author__,
	__copyright__,
	__credits__,
	__license__,
	__version__,
	__documentation__,
	__contact__,
	__donate__
)