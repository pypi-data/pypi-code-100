import abc
import enum
from DodayUtils._exceptions import *
from DodayUtils._dwrappers import *

class DodayPaymentType(enum.IntEnum):
	cash = 0
	easycard = 1
	creditcard = 2
	linepay = 3
	icash = 4
	jkopay = 5 #街口
	onecardpass = 6 #一卡通 

class DodayPayment(metaclass=abc.ABCMeta):
	"""
	This is the class for every 
	Doday payment. 
	"""
	def __init__(self, price, payment_method, plib=None, gui_response_page=None):
		"""
		Input:
			* price: the total price that should be paid
			* payment_method: the payment method that this
				payment is going to register. (int) that is 
				in the DodayPaymentType
		"""
		self.price = price
		self.payment_method = payment_method
		self.plib = plib

		# This allows for dynamic response on the gui page. 
		# Currently, only cash page requires this. In the future, 
		# EPay page also need to provide a response. 
		self.gui_response_page = gui_response_page
		self._check_rep()

	def _check_rep(self):
		# Need to supply plib for all the following
		if not self.plib:
			assert self.payment_method != DodayPaymentType.cash
			assert self.payment_method != DodayPaymentType.easycard
			assert self.payment_method != DodayPaymentType.creditcard
			assert self.payment_method != DodayPaymentType.icash
			assert self.payment_method != DodayPaymentType.jkopay
			assert self.payment_method != DodayPaymentType.onecardpass

		# Need to supply gui_response_page for all the following
		if not self.gui_response_page:
			assert self.payment_method != DodayPaymentType.cash

	@abc.abstractmethod
	def execute(self):
		return NotImplemented

	@abc.abstractmethod
	def terminate(self):
		"""
		Each Payment should be responsible 
		of holding its own termination function
		in the case of premature termination. 
		"""
		return NotImplemented


		

