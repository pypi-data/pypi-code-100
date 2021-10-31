import time
import enum
from ctypes import *
from DodayUtils.payment.DodayPayment import *
from gadgethiServerUtils.time_basics import *

class CashErrorCode(enum.Enum):
	timeout = "Payment Timeout"
	manual_terminate = "Manual Termination"
	hopper_not_enough_coins = "Not Enough Coins"

class Cash(DodayPayment):
	"""
	This is the cash payment for doday
	ordering machine. 
	"""
	def __init__(self, price, plib, gui_response_page):
		super(Cash, self).__init__(price, DodayPaymentType.cash, plib, gui_response_page)
		self.cash_terminate_flag = False
		self.cash_timeout_second = 240

		# bill, coin info
		self.bill_dict = {
			"100":0,
			"200":0,
			"500":0
		}
		self.coin_input_dict = {
			"1":0,
			"5":0,
			"10":0,
			"50":0
		}

	def execute(self):
		"""
		This is the main execution function
		for cash payment. 
		"""
		self.cash_terminate_flag = False
		logging.info("[Inside Cash Payment] start cash helper, " + serverTime(TimeMode.STRING) + ", $" + str(self.price))

		# Enable cash payment, initialization
		self.plib.minc_enable_payment()
		total_num = 0
		tout_start_time = time.time()

		while total_num < self.price:
			# This polls the current paid dollar from the api
			dol = self.plib.minc_paid_dollar()
			total_num += dol

			# Update the real time bill and coin add and minus
			if str(dol) in self.bill_dict.keys():
				self.bill_dict[str(dol)] += 1

			if str(dol) in self.coin_input_dict.keys():
				self.coin_input_dict[str(dol)] += 1

			# If this dol not equal 0, then update the gui response page, and reset timeout flag
			if dol != 0:
				self.gui_response_page.add_money_signal.emit(int(self.price), int(min(total_num, self.price)), int(max(0, total_num-self.price)))
				tout_start_time = time.time()

			# payment timeout -> set to three minutes
			if time.time() - tout_start_time >= self.cash_timeout_second:
				break

			# If manual termination is pressed, perform the following clause
			if self.cash_terminate_flag:
				# Reset cash termination flag
				self.cash_terminate_flag = False
				logging.warning("[Cash Terminated] " + serverTime(TimeMode.STRING))
				self.plib.minc_disable_payment()
				payment_feedback = self.gbridge_return_changes(total_num)
				
				# Prepare return change and remaining change info and return
				ret_cash_info = self.prepare_return_change_info(payment_feedback)
				return {"indicator":False, "message": CashErrorCode.manual_terminate.value, "remaining_changes":str(payment_feedback[-1]), 
					"return_changes": ret_cash_info}
			
			# loop sleep
			time.sleep(0.1)

		else:
			# This is the case when no premature termination has occurred. 
			self.plib.minc_disable_payment()

			logging.info("[Cash Finished] " + serverTime(TimeMode.STRING) + ", Total Payment: " + str(total_num))

			# Case For Return Change
			logging.info("[Cash Returning Changes] return change amount: "+ str(total_num-self.price))
			payment_feedback = self.gbridge_return_changes(total_num-self.price)
			ret_cash_info = self.prepare_return_change_info(payment_feedback)

			if payment_feedback[-1] > 0:
				# The case when there isn't enough money to return
				logging.error("[Hopper not enough coins] Remaining: "+str(payment_feedback[-1]))
				return {"indicator":False, "message": CashErrorCode.hopper_not_enough_coins.value, "remaining_changes":str(payment_feedback[-1]), 
				"return_changes": ret_cash_info}

			logging.info("[Cash Payment Succeed] Return Change Succeed: "+str(ret_cash_info))
			# remaining_changes implies the number that the customers paid and should be returned to them but haven't
			return {"indicator":True, "message":"payment succeed", "remaining_changes":str(payment_feedback[-1]), 
			"return_changes": ret_cash_info}
		
		# Timeout Case
		# ----------------------
		logging.error("[Cash Timeout] " + serverTime(TimeMode.STRING) + ", Total Payment: " + str(total_num))

		self.plib.minc_disable_payment()
		payment_feedback = self.gbridge_return_changes(total_num)
		ret_cash_info = self.prepare_return_change_info(payment_feedback)
		logging.error("[Timeout] Returning: "+str(total_num))
		# timeout failure
		return {"indicator":False, "message": CashErrorCode.timeout.value, "remaining_changes":str(payment_feedback[-1]), 
					"return_changes": ret_cash_info}

	def terminate(self):
		"""
		This is the main termination function
		for cash payment. 
		"""
		self.cash_terminate_flag = True


	# HELPER FUNCTIONS
	# --------------------
	def gbridge_return_changes(self, changes):
		"""
		This is the bridge to return the changes
		from the coin dispenser machine. 
		- Input:
			* changes (number): the change you want
			to return
		- Return:
			* (number of 50's, number of 10's, 5's, 1's), This
			is the number of coins returned for each types
		"""
		p_int_50 = pointer(c_int(0))
		p_int_10 = pointer(c_int(0))
		p_int_5 = pointer(c_int(0))
		p_int_1 = pointer(c_int(0))
		remaining_changes = pointer(c_int(0))

		self.plib.minc_return_change(c_int(changes), p_int_50, p_int_10, p_int_5, p_int_1, remaining_changes)

		return (p_int_50[0], p_int_10[0], p_int_5[0], p_int_1[0], remaining_changes[0])

	def subtract_coin_input(self, current_info, input_dict):
		"""
		This is the helper function to 
		subtract coin input amount
		"""
		for key in input_dict.keys():
			current_info[key] -= input_dict[key]

	def prepare_return_change_info(self, payment_feedback):
		"""
		This is the helper function to prepare the return 
		change info from the payment feedback. 
		"""
		return_change_fn = lambda r: {"50":r[0], "10":r[1], "5":r[2], "1":r[3]}
		ret_cash_info = return_change_fn(payment_feedback)
		ret_cash_info.update(self.bill_dict)
		self.subtract_coin_input(ret_cash_info, self.coin_input_dict)
		return ret_cash_info
