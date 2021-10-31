import enum
from ctypes import *
from DodayUtils.payment.DodayPayment import *
from gadgethiServerUtils.time_basics import *

class EpayErrorCode(enum.Enum):
	epay_failed = "EPay Reading Failed"

class IntegratedEPay(DodayPayment):
	"""
	This is the EPayment for doday
	ordering machine. 
	"""
	def __init__(self, price, payment_method, plib):
		super(IntegratedEPay, self).__init__(price, payment_method, plib)
		self.epay_terminate_flag = False

		self.payment_method_to_code_map = {
			DodayPaymentType.easycard: 31,
			DodayPaymentType.jkopay: 22,
			DodayPaymentType.creditcard: 1,
			DodayPaymentType.icash: 51,
			DodayPaymentType.onecardpass: 41
		}

		# Assert Payment Method is within the allowed ones
		assert self.payment_method in self.payment_method_to_code_map.keys()

	def execute(self):
		"""
		This is the main execution function
		for epay payment. 
		"""
		self.epay_terminate_flag = False
		logging.info("[Inside EPay Payment] start epay helper, " + serverTime(TimeMode.STRING) + ", $" + str(self.price))
		# Main Epay function
		status = self.plib.minc_paid_epay(c_int(self.payment_method_to_code_map[self.payment_method]), c_int(self.price), c_char_p(serverTime(TimeMode.STRING).encode('utf-8')))

		if status == 0:
			logging.info("[EPay Success]: Payment Succeed: "+str(self.payment_method))
			return {"indicator":True, "message":"EPay Success", "payment_method":self.payment_method}
		
		logging.error("[EPay Failed]: Payment Failed: "+str(self.payment_method))
		return {"indicator":False, "message":EpayErrorCode.epay_failed.value, "payment_method":self.payment_method}

	def terminate(self):
		"""
		Terminates epayment sequence.
		"""
		self.epay_terminate_flag = True
		# TODO: Add Epay termination api here!

