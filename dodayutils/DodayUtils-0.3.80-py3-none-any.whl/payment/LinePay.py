import json
import random
from DodayUtils.payment.DodayPayment import *
from gadgethiServerUtils.time_basics import *
from gadgethiServerUtils.GadgethiClient import *

class LinePay(DodayPayment):
	"""
	This is the LinePay for doday
	ordering machine. 
	"""
	def __init__(self, price, qr_data, server_url):
		super(LinePay, self).__init__(price, DodayPaymentType.linepay)
		self.linepay_terminate_flag = False
		self.qr_data = qr_data
		self.server_url = server_url

	def execute(self):
		"""
		This is the main execution function
		for linepay payment. 
		"""
		self.linepay_terminate_flag = False
		logging.info("[Inside linepay Payment] start linepay helper, " + serverTime(TimeMode.STRING) + ", $" + str(self.price))
		
		if not self.qr_data:
			return {"indicator":False, "message":"qr data failed", "payment_method":self.payment_method}
		
		client = GadgetHiClient(line_server_http_url=self.server_url)
		line_pay_dict = {
		    "service": "order",
		    "operation": "line_offline_payment",
		    "charge_amount": self.price,
		    "payment_id": serverTime(TimeMode.STRING) + "-" +str(random.randint(0, 100)),
		    "qr_code": self.qr_data
		}
		response = client.client_post("line_server_http_url", line_pay_dict)
		return json.loads(response)

	def terminate(self):
		"""
		Terminates linepay sequence.
		"""
		self.linepay_terminate_flag = True
		# TODO: Add linepay termination api here!