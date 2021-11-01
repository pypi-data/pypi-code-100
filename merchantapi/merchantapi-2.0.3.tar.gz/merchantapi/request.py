"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

$Id$
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from merchantapi.listquery import ListQueryRequest
from requests.models import Response as HttpResponse

"""
Handles API Request AvailabilityGroupBusinessAccount_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupbusinessaccount_update_assigned
"""


class AvailabilityGroupBusinessAccountUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupBusinessAccountUpdateAssigned Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.business_account_id = None
		self.business_account_title = None
		self.assigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())
			elif availability_group.get_name():
				self.set_edit_availability_group(availability_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupBusinessAccount_Update_Assigned'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_business_account_id(self, business_account_id: int) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.business_account_id = business_account_id
		return self

	def set_business_account_title(self, business_account_title: str) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.business_account_title = business_account_title
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request AvailabilityGroupCustomer_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupcustomer_update_assigned
"""


class AvailabilityGroupCustomerUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupCustomerUpdateAssigned Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.assigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())
			elif availability_group.get_name():
				self.set_edit_availability_group(availability_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupCustomer_Update_Assigned'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_customer_id(self, customer_id: int) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.customer_login = customer_login
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupCustomerUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupCustomerUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request AvailabilityGroupList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygrouplist_load_query
"""


class AvailabilityGroupListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'name'
	]

	available_sort_fields = [
		'id',
		'name'
	]

	def __init__(self, client: Client = None):
		"""
		AvailabilityGroupListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupListLoadQuery(self, http_response, data)


"""
Handles API Request AvailabilityGroupPaymentMethod_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygrouppaymentmethod_update_assigned
"""


class AvailabilityGroupPaymentMethodUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupPaymentMethodUpdateAssigned Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.module_code = None
		self.method_code = None
		self.payment_card_type_id = None
		self.assigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())
			elif availability_group.get_name():
				self.set_edit_availability_group(availability_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupPaymentMethod_Update_Assigned'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_module_code(self) -> str:
		"""
		Get Module_Code.

		:returns: str
		"""

		return self.module_code

	def get_method_code(self) -> str:
		"""
		Get Method_Code.

		:returns: str
		"""

		return self.method_code

	def get_payment_card_type_id(self) -> int:
		"""
		Get PaymentCardType_ID.

		:returns: int
		"""

		return self.payment_card_type_id

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupPaymentMethodUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupPaymentMethodUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupPaymentMethodUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupPaymentMethodUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupPaymentMethodUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupPaymentMethodUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_module_code(self, module_code: str) -> 'AvailabilityGroupPaymentMethodUpdateAssigned':
		"""
		Set Module_Code.

		:param module_code: str
		:returns: AvailabilityGroupPaymentMethodUpdateAssigned
		"""

		self.module_code = module_code
		return self

	def set_method_code(self, method_code: str) -> 'AvailabilityGroupPaymentMethodUpdateAssigned':
		"""
		Set Method_Code.

		:param method_code: str
		:returns: AvailabilityGroupPaymentMethodUpdateAssigned
		"""

		self.method_code = method_code
		return self

	def set_payment_card_type_id(self, payment_card_type_id: int) -> 'AvailabilityGroupPaymentMethodUpdateAssigned':
		"""
		Set PaymentCardType_ID.

		:param payment_card_type_id: int
		:returns: AvailabilityGroupPaymentMethodUpdateAssigned
		"""

		self.payment_card_type_id = payment_card_type_id
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupPaymentMethodUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupPaymentMethodUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupPaymentMethodUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupPaymentMethodUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupPaymentMethodUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		data['Module_Code'] = self.module_code
		data['Method_Code'] = self.method_code
		if self.payment_card_type_id is not None:
			data['PaymentCardType_ID'] = self.payment_card_type_id
		data['Assigned'] = self.assigned
		return data


"""
Handles API Request AvailabilityGroupProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupproduct_update_assigned
"""


class AvailabilityGroupProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupProductUpdateAssigned Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.product_id = None
		self.product_code = None
		self.product_sku = None
		self.edit_product = None
		self.assigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())
			elif availability_group.get_name():
				self.set_edit_availability_group(availability_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupProduct_Update_Assigned'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_product_id(self, product_id: int) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.product_sku = product_sku
		return self

	def set_edit_product(self, edit_product: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupProductUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		data['Assigned'] = self.assigned
		return data


"""
Handles API Request AvailabilityGroupShippingMethod_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupshippingmethod_update_assigned
"""


class AvailabilityGroupShippingMethodUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupShippingMethodUpdateAssigned Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.module_code = None
		self.method_code = None
		self.assigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())
			elif availability_group.get_name():
				self.set_edit_availability_group(availability_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupShippingMethod_Update_Assigned'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_module_code(self) -> str:
		"""
		Get Module_Code.

		:returns: str
		"""

		return self.module_code

	def get_method_code(self) -> str:
		"""
		Get Method_Code.

		:returns: str
		"""

		return self.method_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupShippingMethodUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupShippingMethodUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupShippingMethodUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupShippingMethodUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupShippingMethodUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupShippingMethodUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_module_code(self, module_code: str) -> 'AvailabilityGroupShippingMethodUpdateAssigned':
		"""
		Set Module_Code.

		:param module_code: str
		:returns: AvailabilityGroupShippingMethodUpdateAssigned
		"""

		self.module_code = module_code
		return self

	def set_method_code(self, method_code: str) -> 'AvailabilityGroupShippingMethodUpdateAssigned':
		"""
		Set Method_Code.

		:param method_code: str
		:returns: AvailabilityGroupShippingMethodUpdateAssigned
		"""

		self.method_code = method_code
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupShippingMethodUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupShippingMethodUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupShippingMethodUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		data['Module_Code'] = self.module_code
		data['Method_Code'] = self.method_code
		data['Assigned'] = self.assigned
		return data


"""
Handles API Request CategoryList_Load_Parent. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categorylist_load_parent
"""


class CategoryListLoadParent(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryListLoadParent Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.parent_id = None
		if isinstance(category, merchantapi.model.Category):
			self.set_parent_id(category.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryList_Load_Parent'

	def get_parent_id(self) -> int:
		"""
		Get Parent_ID.

		:returns: int
		"""

		return self.parent_id

	def set_parent_id(self, parent_id: int) -> 'CategoryListLoadParent':
		"""
		Set Parent_ID.

		:param parent_id: int
		:returns: CategoryListLoadParent
		"""

		self.parent_id = parent_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryListLoadParent':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryListLoadParent':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryListLoadParent(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Parent_ID'] = self.get_parent_id()

		return data


"""
Handles API Request CategoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categorylist_load_query
"""


class CategoryListLoadQuery(ListQueryRequest):
	# CATEGORY_SHOW constants.
	CATEGORY_SHOW_ALL = 'All'
	CATEGORY_SHOW_ACTIVE = 'Active'

	available_search_fields = [
		'id',
		'code',
		'name',
		'page_title',
		'parent_category',
		'page_code',
		'dt_created',
		'dt_updated',
		'depth'
	]

	available_sort_fields = [
		'id',
		'code',
		'name',
		'page_title',
		'active',
		'page_code',
		'parent_category',
		'disp_order',
		'dt_created',
		'dt_updated',
		'depth'
	]

	available_on_demand_columns = [
		'uris'
	]

	available_custom_filters = {
		'Category_Show': [
			CATEGORY_SHOW_ALL,
			CATEGORY_SHOW_ACTIVE
		]
	}

	def __init__(self, client: Client = None):
		"""
		CategoryListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryListLoadQuery(self, http_response, data)


"""
Handles API Request CategoryProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryproduct_update_assigned
"""


class CategoryProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryProductUpdateAssigned Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.product_sku = None
		self.assigned = False
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_category(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryProduct_Update_Assigned'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_category_id(self, category_id: int) -> 'CategoryProductUpdateAssigned':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryProductUpdateAssigned
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.category_code = category_code
		return self

	def set_product_id(self, product_id: int) -> 'CategoryProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: CategoryProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.product_sku = product_sku
		return self

	def set_assigned(self, assigned: bool) -> 'CategoryProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CategoryProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryProductUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		data['Assigned'] = self.assigned
		return data


"""
Handles API Request Category_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/category_insert
"""


class CategoryInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryInsert Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_code = None
		self.category_name = None
		self.category_active = False
		self.category_page_title = None
		self.category_parent_category = None
		self.category_alternate_display_page = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(category, merchantapi.model.Category):
			self.set_category_code(category.get_code())
			self.set_category_name(category.get_name())
			self.set_category_active(category.get_active())
			self.set_category_page_title(category.get_page_title())
			self.set_category_parent_category(category.get_parent_category())
			self.set_category_alternate_display_page(category.get_page_code())

			if category.get_custom_field_values():
				self.set_custom_field_values(category.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Category_Insert'

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_category_name(self) -> str:
		"""
		Get Category_Name.

		:returns: str
		"""

		return self.category_name

	def get_category_active(self) -> bool:
		"""
		Get Category_Active.

		:returns: bool
		"""

		return self.category_active

	def get_category_page_title(self) -> str:
		"""
		Get Category_Page_Title.

		:returns: str
		"""

		return self.category_page_title

	def get_category_parent_category(self) -> str:
		"""
		Get Category_Parent_Category.

		:returns: str
		"""

		return self.category_parent_category

	def get_category_alternate_display_page(self) -> str:
		"""
		Get Category_Alternate_Display_Page.

		:returns: str
		"""

		return self.category_alternate_display_page

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_category_code(self, category_code: str) -> 'CategoryInsert':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryInsert
		"""

		self.category_code = category_code
		return self

	def set_category_name(self, category_name: str) -> 'CategoryInsert':
		"""
		Set Category_Name.

		:param category_name: str
		:returns: CategoryInsert
		"""

		self.category_name = category_name
		return self

	def set_category_active(self, category_active: bool) -> 'CategoryInsert':
		"""
		Set Category_Active.

		:param category_active: bool
		:returns: CategoryInsert
		"""

		self.category_active = category_active
		return self

	def set_category_page_title(self, category_page_title: str) -> 'CategoryInsert':
		"""
		Set Category_Page_Title.

		:param category_page_title: str
		:returns: CategoryInsert
		"""

		self.category_page_title = category_page_title
		return self

	def set_category_parent_category(self, category_parent_category: str) -> 'CategoryInsert':
		"""
		Set Category_Parent_Category.

		:param category_parent_category: str
		:returns: CategoryInsert
		"""

		self.category_parent_category = category_parent_category
		return self

	def set_category_alternate_display_page(self, category_alternate_display_page: str) -> 'CategoryInsert':
		"""
		Set Category_Alternate_Display_Page.

		:param category_alternate_display_page: str
		:returns: CategoryInsert
		"""

		self.category_alternate_display_page = category_alternate_display_page
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'CategoryInsert':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: CategoryInsert
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Category_Code'] = self.category_code
		data['Category_Name'] = self.category_name
		if self.category_active is not None:
			data['Category_Active'] = self.category_active
		if self.category_page_title is not None:
			data['Category_Page_Title'] = self.category_page_title
		if self.category_parent_category is not None:
			data['Category_Parent_Category'] = self.category_parent_category
		if self.category_alternate_display_page is not None:
			data['Category_Alternate_Display_Page'] = self.category_alternate_display_page
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data


"""
Handles API Request Category_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/category_delete
"""


class CategoryDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryDelete Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_category(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Category_Delete'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def set_category_id(self, category_id: int) -> 'CategoryDelete':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryDelete
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryDelete':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryDelete
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'CategoryDelete':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryDelete
		"""

		self.category_code = category_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		return data


"""
Handles API Request Category_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/category_update
"""


class CategoryUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryUpdate Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.category_code = None
		self.edit_category = None
		self.category_name = None
		self.category_page_title = None
		self.category_active = False
		self.category_parent_category = None
		self.category_alternate_display_page = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_category(category.get_code())

			self.set_category_code(category.get_code())
			self.set_category_name(category.get_name())
			self.set_category_page_title(category.get_page_title())
			self.set_category_active(category.get_active())
			self.set_category_parent_category(category.get_parent_category())
			self.set_category_alternate_display_page(category.get_page_code())

			if category.get_custom_field_values():
				self.set_custom_field_values(category.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Category_Update'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_category_name(self) -> str:
		"""
		Get Category_Name.

		:returns: str
		"""

		return self.category_name

	def get_category_page_title(self) -> str:
		"""
		Get Category_Page_Title.

		:returns: str
		"""

		return self.category_page_title

	def get_category_active(self) -> bool:
		"""
		Get Category_Active.

		:returns: bool
		"""

		return self.category_active

	def get_category_parent_category(self) -> str:
		"""
		Get Category_Parent_Category.

		:returns: str
		"""

		return self.category_parent_category

	def get_category_alternate_display_page(self) -> str:
		"""
		Get Category_Alternate_Display_Page.

		:returns: str
		"""

		return self.category_alternate_display_page

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_category_id(self, category_id: int) -> 'CategoryUpdate':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryUpdate
		"""

		self.category_id = category_id
		return self

	def set_category_code(self, category_code: str) -> 'CategoryUpdate':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryUpdate
		"""

		self.category_code = category_code
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryUpdate':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryUpdate
		"""

		self.edit_category = edit_category
		return self

	def set_category_name(self, category_name: str) -> 'CategoryUpdate':
		"""
		Set Category_Name.

		:param category_name: str
		:returns: CategoryUpdate
		"""

		self.category_name = category_name
		return self

	def set_category_page_title(self, category_page_title: str) -> 'CategoryUpdate':
		"""
		Set Category_Page_Title.

		:param category_page_title: str
		:returns: CategoryUpdate
		"""

		self.category_page_title = category_page_title
		return self

	def set_category_active(self, category_active: bool) -> 'CategoryUpdate':
		"""
		Set Category_Active.

		:param category_active: bool
		:returns: CategoryUpdate
		"""

		self.category_active = category_active
		return self

	def set_category_parent_category(self, category_parent_category: str) -> 'CategoryUpdate':
		"""
		Set Category_Parent_Category.

		:param category_parent_category: str
		:returns: CategoryUpdate
		"""

		self.category_parent_category = category_parent_category
		return self

	def set_category_alternate_display_page(self, category_alternate_display_page: str) -> 'CategoryUpdate':
		"""
		Set Category_Alternate_Display_Page.

		:param category_alternate_display_page: str
		:returns: CategoryUpdate
		"""

		self.category_alternate_display_page = category_alternate_display_page
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'CategoryUpdate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: CategoryUpdate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category

		if self.category_code is not None:
			data['Category_Code'] = self.category_code
		if self.category_name is not None:
			data['Category_Name'] = self.category_name
		if self.category_page_title is not None:
			data['Category_Page_Title'] = self.category_page_title
		if self.category_active is not None:
			data['Category_Active'] = self.category_active
		if self.category_parent_category is not None:
			data['Category_Parent_Category'] = self.category_parent_category
		if self.category_alternate_display_page is not None:
			data['Category_Alternate_Display_Page'] = self.category_alternate_display_page
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data


"""
Handles API Request CouponList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponlist_delete
"""


class CouponListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		CouponListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.coupon_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponList_Delete'

	def get_coupon_ids(self):
		"""
		Get Coupon_IDs.

		:returns: list
		"""

		return self.coupon_ids
	
	def add_coupon_id(self, coupon_id) -> 'CouponListDelete':
		"""
		Add Coupon_IDs.

		:param coupon_id: int
		:returns: {CouponListDelete}
		"""

		self.coupon_ids.append(coupon_id)
		return self

	def add_coupon(self, coupon: merchantapi.model.Coupon) -> 'CouponListDelete':
		"""
		Add Coupon model.

		:param coupon: Coupon
		:raises Exception:
		:returns: CouponListDelete
		"""
		if not isinstance(coupon, merchantapi.model.Coupon):
			raise Exception('Expected an instance of Coupon')

		if coupon.get_id():
			self.coupon_ids.append(coupon.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Coupon_IDs'] = self.coupon_ids
		return data


"""
Handles API Request CouponList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponlist_load_query
"""


class CouponListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'code',
		'descrip',
		'custscope',
		'dt_start',
		'dt_end',
		'max_use',
		'max_per',
		'active',
		'use_count'
	]

	available_sort_fields = [
		'id',
		'code',
		'descrip',
		'custscope',
		'dt_start',
		'dt_end',
		'max_use',
		'max_per',
		'active',
		'use_count'
	]

	def __init__(self, client: Client = None):
		"""
		CouponListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponListLoadQuery(self, http_response, data)


"""
Handles API Request CouponPriceGroup_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponpricegroup_update_assigned
"""


class CouponPriceGroupUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponPriceGroupUpdateAssigned Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.price_group_id = None
		self.price_group_name = None
		self.assigned = False
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())
			elif coupon.get_code():
				self.set_edit_coupon(coupon.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponPriceGroup_Update_Assigned'

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_coupon_id(self, coupon_id: int) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.coupon_code = coupon_code
		return self

	def set_price_group_id(self, price_group_id: int) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponPriceGroupUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponPriceGroupUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon
		elif self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		data['Assigned'] = self.assigned
		return data


"""
Handles API Request Coupon_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/coupon_insert
"""


class CouponInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponInsert Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.code = None
		self.description = None
		self.customer_scope = None
		self.date_time_start = None
		self.date_time_end = None
		self.max_use = None
		self.max_per = None
		self.active = False
		self.price_group_id = None
		if isinstance(coupon, merchantapi.model.Coupon):
			self.set_code(coupon.get_code())
			self.set_description(coupon.get_description())
			self.set_customer_scope(coupon.get_customer_scope())
			self.set_date_time_start(coupon.get_date_time_start())
			self.set_date_time_end(coupon.get_date_time_end())
			self.set_max_use(coupon.get_max_use())
			self.set_max_per(coupon.get_max_per())
			self.set_active(coupon.get_active())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Coupon_Insert'

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_customer_scope(self) -> str:
		"""
		Get CustomerScope.

		:returns: str
		"""

		return self.customer_scope

	def get_date_time_start(self) -> int:
		"""
		Get DateTime_Start.

		:returns: int
		"""

		return self.date_time_start

	def get_date_time_end(self) -> int:
		"""
		Get DateTime_End.

		:returns: int
		"""

		return self.date_time_end

	def get_max_use(self) -> int:
		"""
		Get Max_Use.

		:returns: int
		"""

		return self.max_use

	def get_max_per(self) -> int:
		"""
		Get Max_Per.

		:returns: int
		"""

		return self.max_per

	def get_active(self) -> bool:
		"""
		Get Active.

		:returns: bool
		"""

		return self.active

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def set_code(self, code: str) -> 'CouponInsert':
		"""
		Set Code.

		:param code: str
		:returns: CouponInsert
		"""

		self.code = code
		return self

	def set_description(self, description: str) -> 'CouponInsert':
		"""
		Set Description.

		:param description: str
		:returns: CouponInsert
		"""

		self.description = description
		return self

	def set_customer_scope(self, customer_scope: str) -> 'CouponInsert':
		"""
		Set CustomerScope.

		:param customer_scope: str
		:returns: CouponInsert
		"""

		self.customer_scope = customer_scope
		return self

	def set_date_time_start(self, date_time_start: int) -> 'CouponInsert':
		"""
		Set DateTime_Start.

		:param date_time_start: int
		:returns: CouponInsert
		"""

		self.date_time_start = date_time_start
		return self

	def set_date_time_end(self, date_time_end: int) -> 'CouponInsert':
		"""
		Set DateTime_End.

		:param date_time_end: int
		:returns: CouponInsert
		"""

		self.date_time_end = date_time_end
		return self

	def set_max_use(self, max_use: int) -> 'CouponInsert':
		"""
		Set Max_Use.

		:param max_use: int
		:returns: CouponInsert
		"""

		self.max_use = max_use
		return self

	def set_max_per(self, max_per: int) -> 'CouponInsert':
		"""
		Set Max_Per.

		:param max_per: int
		:returns: CouponInsert
		"""

		self.max_per = max_per
		return self

	def set_active(self, active: bool) -> 'CouponInsert':
		"""
		Set Active.

		:param active: bool
		:returns: CouponInsert
		"""

		self.active = active
		return self

	def set_price_group_id(self, price_group_id: int) -> 'CouponInsert':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: CouponInsert
		"""

		self.price_group_id = price_group_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Code'] = self.code
		if self.description is not None:
			data['Description'] = self.description
		if self.customer_scope is not None:
			data['CustomerScope'] = self.customer_scope
		if self.date_time_start is not None:
			data['DateTime_Start'] = self.date_time_start
		if self.date_time_end is not None:
			data['DateTime_End'] = self.date_time_end
		if self.max_use is not None:
			data['Max_Use'] = self.max_use
		if self.max_per is not None:
			data['Max_Per'] = self.max_per
		if self.active is not None:
			data['Active'] = self.active
		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		return data


"""
Handles API Request Coupon_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/coupon_update
"""


class CouponUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponUpdate Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.coupon_id = None
		self.coupon_code = None
		self.edit_coupon = None
		self.code = None
		self.description = None
		self.customer_scope = None
		self.date_time_start = None
		self.date_time_end = None
		self.max_use = None
		self.max_per = None
		self.active = False
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())
			elif coupon.get_code():
				self.set_edit_coupon(coupon.get_code())

			self.set_coupon_code(coupon.get_code())
			self.set_code(coupon.get_code())
			self.set_description(coupon.get_description())
			self.set_customer_scope(coupon.get_customer_scope())
			self.set_date_time_start(coupon.get_date_time_start())
			self.set_date_time_end(coupon.get_date_time_end())
			self.set_max_use(coupon.get_max_use())
			self.set_max_per(coupon.get_max_per())
			self.set_active(coupon.get_active())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Coupon_Update'

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_customer_scope(self) -> str:
		"""
		Get CustomerScope.

		:returns: str
		"""

		return self.customer_scope

	def get_date_time_start(self) -> int:
		"""
		Get DateTime_Start.

		:returns: int
		"""

		return self.date_time_start

	def get_date_time_end(self) -> int:
		"""
		Get DateTime_End.

		:returns: int
		"""

		return self.date_time_end

	def get_max_use(self) -> int:
		"""
		Get Max_Use.

		:returns: int
		"""

		return self.max_use

	def get_max_per(self) -> int:
		"""
		Get Max_Per.

		:returns: int
		"""

		return self.max_per

	def get_active(self) -> bool:
		"""
		Get Active.

		:returns: bool
		"""

		return self.active

	def set_coupon_id(self, coupon_id: int) -> 'CouponUpdate':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponUpdate
		"""

		self.coupon_id = coupon_id
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponUpdate':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponUpdate
		"""

		self.coupon_code = coupon_code
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponUpdate':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponUpdate
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_code(self, code: str) -> 'CouponUpdate':
		"""
		Set Code.

		:param code: str
		:returns: CouponUpdate
		"""

		self.code = code
		return self

	def set_description(self, description: str) -> 'CouponUpdate':
		"""
		Set Description.

		:param description: str
		:returns: CouponUpdate
		"""

		self.description = description
		return self

	def set_customer_scope(self, customer_scope: str) -> 'CouponUpdate':
		"""
		Set CustomerScope.

		:param customer_scope: str
		:returns: CouponUpdate
		"""

		self.customer_scope = customer_scope
		return self

	def set_date_time_start(self, date_time_start: int) -> 'CouponUpdate':
		"""
		Set DateTime_Start.

		:param date_time_start: int
		:returns: CouponUpdate
		"""

		self.date_time_start = date_time_start
		return self

	def set_date_time_end(self, date_time_end: int) -> 'CouponUpdate':
		"""
		Set DateTime_End.

		:param date_time_end: int
		:returns: CouponUpdate
		"""

		self.date_time_end = date_time_end
		return self

	def set_max_use(self, max_use: int) -> 'CouponUpdate':
		"""
		Set Max_Use.

		:param max_use: int
		:returns: CouponUpdate
		"""

		self.max_use = max_use
		return self

	def set_max_per(self, max_per: int) -> 'CouponUpdate':
		"""
		Set Max_Per.

		:param max_per: int
		:returns: CouponUpdate
		"""

		self.max_per = max_per
		return self

	def set_active(self, active: bool) -> 'CouponUpdate':
		"""
		Set Active.

		:param active: bool
		:returns: CouponUpdate
		"""

		self.active = active
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon

		if self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code
		if self.code is not None:
			data['Code'] = self.code
		if self.description is not None:
			data['Description'] = self.description
		if self.customer_scope is not None:
			data['CustomerScope'] = self.customer_scope
		if self.date_time_start is not None:
			data['DateTime_Start'] = self.date_time_start
		if self.date_time_end is not None:
			data['DateTime_End'] = self.date_time_end
		if self.max_use is not None:
			data['Max_Use'] = self.max_use
		if self.max_per is not None:
			data['Max_Per'] = self.max_per
		if self.active is not None:
			data['Active'] = self.active
		return data


"""
Handles API Request CustomerList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customerlist_load_query
"""


class CustomerListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'login',
		'pw_email',
		'ship_fname',
		'ship_lname',
		'ship_email',
		'ship_comp',
		'ship_phone',
		'ship_fax',
		'ship_addr1',
		'ship_addr2',
		'ship_city',
		'ship_state',
		'ship_zip',
		'ship_cntry',
		'ship_res',
		'bill_fname',
		'bill_lname',
		'bill_email',
		'bill_comp',
		'bill_phone',
		'bill_fax',
		'bill_addr1',
		'bill_addr2',
		'bill_city',
		'bill_state',
		'bill_zip',
		'bill_cntry',
		'business_title',
		'note_count',
		'dt_created',
		'dt_login',
		'credit'
	]

	available_sort_fields = [
		'id',
		'login',
		'pw_email',
		'ship_fname',
		'ship_lname',
		'ship_email',
		'ship_comp',
		'ship_phone',
		'ship_fax',
		'ship_addr1',
		'ship_addr2',
		'ship_city',
		'ship_state',
		'ship_zip',
		'ship_cntry',
		'ship_res',
		'bill_fname',
		'bill_lname',
		'bill_email',
		'bill_comp',
		'bill_phone',
		'bill_fax',
		'bill_addr1',
		'bill_addr2',
		'bill_city',
		'bill_state',
		'bill_zip',
		'bill_cntry',
		'business_title',
		'note_count',
		'dt_created',
		'dt_login',
		'credit'
	]

	def __init__(self, client: Client = None):
		"""
		CustomerListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerListLoadQuery(self, http_response, data)


"""
Handles API Request Customer_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customer_delete
"""


class CustomerDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerDelete Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.customer_login = None
		self.edit_customer = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Customer_Delete'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def set_customer_id(self, customer_id: int) -> 'CustomerDelete':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerDelete
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerDelete':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerDelete
		"""

		self.customer_login = customer_login
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerDelete':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerDelete
		"""

		self.edit_customer = edit_customer
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer

		return data


"""
Handles API Request Customer_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customer_insert
"""


class CustomerInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerInsert Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_login = None
		self.customer_password_email = None
		self.customer_password = None
		self.customer_ship_residential = False
		self.customer_ship_first_name = None
		self.customer_ship_last_name = None
		self.customer_ship_email = None
		self.customer_ship_company = None
		self.customer_ship_phone = None
		self.customer_ship_fax = None
		self.customer_ship_address1 = None
		self.customer_ship_address2 = None
		self.customer_ship_city = None
		self.customer_ship_state = None
		self.customer_ship_zip = None
		self.customer_ship_country = None
		self.customer_bill_first_name = None
		self.customer_bill_last_name = None
		self.customer_bill_email = None
		self.customer_bill_company = None
		self.customer_bill_phone = None
		self.customer_bill_fax = None
		self.customer_bill_address1 = None
		self.customer_bill_address2 = None
		self.customer_bill_city = None
		self.customer_bill_state = None
		self.customer_bill_zip = None
		self.customer_bill_country = None
		self.customer_tax_exempt = False
		self.customer_business_account = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(customer, merchantapi.model.Customer):
			self.set_customer_login(customer.get_login())
			self.set_customer_password_email(customer.get_password_email())
			self.set_customer_ship_residential(customer.get_shipping_residential())
			self.set_customer_ship_first_name(customer.get_ship_first_name())
			self.set_customer_ship_last_name(customer.get_ship_last_name())
			self.set_customer_ship_email(customer.get_ship_email())
			self.set_customer_ship_company(customer.get_ship_company())
			self.set_customer_ship_phone(customer.get_ship_phone())
			self.set_customer_ship_fax(customer.get_ship_fax())
			self.set_customer_ship_address1(customer.get_ship_address1())
			self.set_customer_ship_address2(customer.get_ship_address2())
			self.set_customer_ship_city(customer.get_ship_city())
			self.set_customer_ship_state(customer.get_ship_state())
			self.set_customer_ship_zip(customer.get_ship_zip())
			self.set_customer_ship_country(customer.get_ship_country())
			self.set_customer_bill_first_name(customer.get_bill_first_name())
			self.set_customer_bill_last_name(customer.get_bill_last_name())
			self.set_customer_bill_email(customer.get_bill_email())
			self.set_customer_bill_company(customer.get_bill_company())
			self.set_customer_bill_phone(customer.get_bill_phone())
			self.set_customer_bill_fax(customer.get_bill_fax())
			self.set_customer_bill_address1(customer.get_bill_address1())
			self.set_customer_bill_address2(customer.get_bill_address2())
			self.set_customer_bill_city(customer.get_bill_city())
			self.set_customer_bill_state(customer.get_bill_state())
			self.set_customer_bill_zip(customer.get_bill_zip())
			self.set_customer_bill_country(customer.get_bill_country())
			self.set_customer_tax_exempt(customer.get_tax_exempt())
			self.set_customer_business_account(customer.get_business_title())

			if customer.get_custom_field_values():
				self.set_custom_field_values(customer.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Customer_Insert'

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_customer_password_email(self) -> str:
		"""
		Get Customer_PasswordEmail.

		:returns: str
		"""

		return self.customer_password_email

	def get_customer_password(self) -> str:
		"""
		Get Customer_Password.

		:returns: str
		"""

		return self.customer_password

	def get_customer_ship_residential(self) -> bool:
		"""
		Get Customer_ShipResidential.

		:returns: bool
		"""

		return self.customer_ship_residential

	def get_customer_ship_first_name(self) -> str:
		"""
		Get Customer_ShipFirstName.

		:returns: str
		"""

		return self.customer_ship_first_name

	def get_customer_ship_last_name(self) -> str:
		"""
		Get Customer_ShipLastName.

		:returns: str
		"""

		return self.customer_ship_last_name

	def get_customer_ship_email(self) -> str:
		"""
		Get Customer_ShipEmail.

		:returns: str
		"""

		return self.customer_ship_email

	def get_customer_ship_company(self) -> str:
		"""
		Get Customer_ShipCompany.

		:returns: str
		"""

		return self.customer_ship_company

	def get_customer_ship_phone(self) -> str:
		"""
		Get Customer_ShipPhone.

		:returns: str
		"""

		return self.customer_ship_phone

	def get_customer_ship_fax(self) -> str:
		"""
		Get Customer_ShipFax.

		:returns: str
		"""

		return self.customer_ship_fax

	def get_customer_ship_address1(self) -> str:
		"""
		Get Customer_ShipAddress1.

		:returns: str
		"""

		return self.customer_ship_address1

	def get_customer_ship_address2(self) -> str:
		"""
		Get Customer_ShipAddress2.

		:returns: str
		"""

		return self.customer_ship_address2

	def get_customer_ship_city(self) -> str:
		"""
		Get Customer_ShipCity.

		:returns: str
		"""

		return self.customer_ship_city

	def get_customer_ship_state(self) -> str:
		"""
		Get Customer_ShipState.

		:returns: str
		"""

		return self.customer_ship_state

	def get_customer_ship_zip(self) -> str:
		"""
		Get Customer_ShipZip.

		:returns: str
		"""

		return self.customer_ship_zip

	def get_customer_ship_country(self) -> str:
		"""
		Get Customer_ShipCountry.

		:returns: str
		"""

		return self.customer_ship_country

	def get_customer_bill_first_name(self) -> str:
		"""
		Get Customer_BillFirstName.

		:returns: str
		"""

		return self.customer_bill_first_name

	def get_customer_bill_last_name(self) -> str:
		"""
		Get Customer_BillLastName.

		:returns: str
		"""

		return self.customer_bill_last_name

	def get_customer_bill_email(self) -> str:
		"""
		Get Customer_BillEmail.

		:returns: str
		"""

		return self.customer_bill_email

	def get_customer_bill_company(self) -> str:
		"""
		Get Customer_BillCompany.

		:returns: str
		"""

		return self.customer_bill_company

	def get_customer_bill_phone(self) -> str:
		"""
		Get Customer_BillPhone.

		:returns: str
		"""

		return self.customer_bill_phone

	def get_customer_bill_fax(self) -> str:
		"""
		Get Customer_BillFax.

		:returns: str
		"""

		return self.customer_bill_fax

	def get_customer_bill_address1(self) -> str:
		"""
		Get Customer_BillAddress1.

		:returns: str
		"""

		return self.customer_bill_address1

	def get_customer_bill_address2(self) -> str:
		"""
		Get Customer_BillAddress2.

		:returns: str
		"""

		return self.customer_bill_address2

	def get_customer_bill_city(self) -> str:
		"""
		Get Customer_BillCity.

		:returns: str
		"""

		return self.customer_bill_city

	def get_customer_bill_state(self) -> str:
		"""
		Get Customer_BillState.

		:returns: str
		"""

		return self.customer_bill_state

	def get_customer_bill_zip(self) -> str:
		"""
		Get Customer_BillZip.

		:returns: str
		"""

		return self.customer_bill_zip

	def get_customer_bill_country(self) -> str:
		"""
		Get Customer_BillCountry.

		:returns: str
		"""

		return self.customer_bill_country

	def get_customer_tax_exempt(self) -> bool:
		"""
		Get Customer_Tax_Exempt.

		:returns: bool
		"""

		return self.customer_tax_exempt

	def get_customer_business_account(self) -> str:
		"""
		Get Customer_BusinessAccount.

		:returns: str
		"""

		return self.customer_business_account

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_customer_login(self, customer_login: str) -> 'CustomerInsert':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerInsert
		"""

		self.customer_login = customer_login
		return self

	def set_customer_password_email(self, customer_password_email: str) -> 'CustomerInsert':
		"""
		Set Customer_PasswordEmail.

		:param customer_password_email: str
		:returns: CustomerInsert
		"""

		self.customer_password_email = customer_password_email
		return self

	def set_customer_password(self, customer_password: str) -> 'CustomerInsert':
		"""
		Set Customer_Password.

		:param customer_password: str
		:returns: CustomerInsert
		"""

		self.customer_password = customer_password
		return self

	def set_customer_ship_residential(self, customer_ship_residential: bool) -> 'CustomerInsert':
		"""
		Set Customer_ShipResidential.

		:param customer_ship_residential: bool
		:returns: CustomerInsert
		"""

		self.customer_ship_residential = customer_ship_residential
		return self

	def set_customer_ship_first_name(self, customer_ship_first_name: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipFirstName.

		:param customer_ship_first_name: str
		:returns: CustomerInsert
		"""

		self.customer_ship_first_name = customer_ship_first_name
		return self

	def set_customer_ship_last_name(self, customer_ship_last_name: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipLastName.

		:param customer_ship_last_name: str
		:returns: CustomerInsert
		"""

		self.customer_ship_last_name = customer_ship_last_name
		return self

	def set_customer_ship_email(self, customer_ship_email: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipEmail.

		:param customer_ship_email: str
		:returns: CustomerInsert
		"""

		self.customer_ship_email = customer_ship_email
		return self

	def set_customer_ship_company(self, customer_ship_company: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipCompany.

		:param customer_ship_company: str
		:returns: CustomerInsert
		"""

		self.customer_ship_company = customer_ship_company
		return self

	def set_customer_ship_phone(self, customer_ship_phone: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipPhone.

		:param customer_ship_phone: str
		:returns: CustomerInsert
		"""

		self.customer_ship_phone = customer_ship_phone
		return self

	def set_customer_ship_fax(self, customer_ship_fax: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipFax.

		:param customer_ship_fax: str
		:returns: CustomerInsert
		"""

		self.customer_ship_fax = customer_ship_fax
		return self

	def set_customer_ship_address1(self, customer_ship_address1: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipAddress1.

		:param customer_ship_address1: str
		:returns: CustomerInsert
		"""

		self.customer_ship_address1 = customer_ship_address1
		return self

	def set_customer_ship_address2(self, customer_ship_address2: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipAddress2.

		:param customer_ship_address2: str
		:returns: CustomerInsert
		"""

		self.customer_ship_address2 = customer_ship_address2
		return self

	def set_customer_ship_city(self, customer_ship_city: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipCity.

		:param customer_ship_city: str
		:returns: CustomerInsert
		"""

		self.customer_ship_city = customer_ship_city
		return self

	def set_customer_ship_state(self, customer_ship_state: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipState.

		:param customer_ship_state: str
		:returns: CustomerInsert
		"""

		self.customer_ship_state = customer_ship_state
		return self

	def set_customer_ship_zip(self, customer_ship_zip: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipZip.

		:param customer_ship_zip: str
		:returns: CustomerInsert
		"""

		self.customer_ship_zip = customer_ship_zip
		return self

	def set_customer_ship_country(self, customer_ship_country: str) -> 'CustomerInsert':
		"""
		Set Customer_ShipCountry.

		:param customer_ship_country: str
		:returns: CustomerInsert
		"""

		self.customer_ship_country = customer_ship_country
		return self

	def set_customer_bill_first_name(self, customer_bill_first_name: str) -> 'CustomerInsert':
		"""
		Set Customer_BillFirstName.

		:param customer_bill_first_name: str
		:returns: CustomerInsert
		"""

		self.customer_bill_first_name = customer_bill_first_name
		return self

	def set_customer_bill_last_name(self, customer_bill_last_name: str) -> 'CustomerInsert':
		"""
		Set Customer_BillLastName.

		:param customer_bill_last_name: str
		:returns: CustomerInsert
		"""

		self.customer_bill_last_name = customer_bill_last_name
		return self

	def set_customer_bill_email(self, customer_bill_email: str) -> 'CustomerInsert':
		"""
		Set Customer_BillEmail.

		:param customer_bill_email: str
		:returns: CustomerInsert
		"""

		self.customer_bill_email = customer_bill_email
		return self

	def set_customer_bill_company(self, customer_bill_company: str) -> 'CustomerInsert':
		"""
		Set Customer_BillCompany.

		:param customer_bill_company: str
		:returns: CustomerInsert
		"""

		self.customer_bill_company = customer_bill_company
		return self

	def set_customer_bill_phone(self, customer_bill_phone: str) -> 'CustomerInsert':
		"""
		Set Customer_BillPhone.

		:param customer_bill_phone: str
		:returns: CustomerInsert
		"""

		self.customer_bill_phone = customer_bill_phone
		return self

	def set_customer_bill_fax(self, customer_bill_fax: str) -> 'CustomerInsert':
		"""
		Set Customer_BillFax.

		:param customer_bill_fax: str
		:returns: CustomerInsert
		"""

		self.customer_bill_fax = customer_bill_fax
		return self

	def set_customer_bill_address1(self, customer_bill_address1: str) -> 'CustomerInsert':
		"""
		Set Customer_BillAddress1.

		:param customer_bill_address1: str
		:returns: CustomerInsert
		"""

		self.customer_bill_address1 = customer_bill_address1
		return self

	def set_customer_bill_address2(self, customer_bill_address2: str) -> 'CustomerInsert':
		"""
		Set Customer_BillAddress2.

		:param customer_bill_address2: str
		:returns: CustomerInsert
		"""

		self.customer_bill_address2 = customer_bill_address2
		return self

	def set_customer_bill_city(self, customer_bill_city: str) -> 'CustomerInsert':
		"""
		Set Customer_BillCity.

		:param customer_bill_city: str
		:returns: CustomerInsert
		"""

		self.customer_bill_city = customer_bill_city
		return self

	def set_customer_bill_state(self, customer_bill_state: str) -> 'CustomerInsert':
		"""
		Set Customer_BillState.

		:param customer_bill_state: str
		:returns: CustomerInsert
		"""

		self.customer_bill_state = customer_bill_state
		return self

	def set_customer_bill_zip(self, customer_bill_zip: str) -> 'CustomerInsert':
		"""
		Set Customer_BillZip.

		:param customer_bill_zip: str
		:returns: CustomerInsert
		"""

		self.customer_bill_zip = customer_bill_zip
		return self

	def set_customer_bill_country(self, customer_bill_country: str) -> 'CustomerInsert':
		"""
		Set Customer_BillCountry.

		:param customer_bill_country: str
		:returns: CustomerInsert
		"""

		self.customer_bill_country = customer_bill_country
		return self

	def set_customer_tax_exempt(self, customer_tax_exempt: bool) -> 'CustomerInsert':
		"""
		Set Customer_Tax_Exempt.

		:param customer_tax_exempt: bool
		:returns: CustomerInsert
		"""

		self.customer_tax_exempt = customer_tax_exempt
		return self

	def set_customer_business_account(self, customer_business_account: str) -> 'CustomerInsert':
		"""
		Set Customer_BusinessAccount.

		:param customer_business_account: str
		:returns: CustomerInsert
		"""

		self.customer_business_account = customer_business_account
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'CustomerInsert':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: CustomerInsert
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Customer_Login'] = self.customer_login
		data['Customer_PasswordEmail'] = self.customer_password_email
		data['Customer_Password'] = self.customer_password
		if self.customer_ship_residential is not None:
			data['Customer_ShipResidential'] = self.customer_ship_residential
		if self.customer_ship_first_name is not None:
			data['Customer_ShipFirstName'] = self.customer_ship_first_name
		if self.customer_ship_last_name is not None:
			data['Customer_ShipLastName'] = self.customer_ship_last_name
		if self.customer_ship_email is not None:
			data['Customer_ShipEmail'] = self.customer_ship_email
		if self.customer_ship_company is not None:
			data['Customer_ShipCompany'] = self.customer_ship_company
		if self.customer_ship_phone is not None:
			data['Customer_ShipPhone'] = self.customer_ship_phone
		if self.customer_ship_fax is not None:
			data['Customer_ShipFax'] = self.customer_ship_fax
		if self.customer_ship_address1 is not None:
			data['Customer_ShipAddress1'] = self.customer_ship_address1
		if self.customer_ship_address2 is not None:
			data['Customer_ShipAddress2'] = self.customer_ship_address2
		if self.customer_ship_city is not None:
			data['Customer_ShipCity'] = self.customer_ship_city
		if self.customer_ship_state is not None:
			data['Customer_ShipState'] = self.customer_ship_state
		if self.customer_ship_zip is not None:
			data['Customer_ShipZip'] = self.customer_ship_zip
		if self.customer_ship_country is not None:
			data['Customer_ShipCountry'] = self.customer_ship_country
		if self.customer_bill_first_name is not None:
			data['Customer_BillFirstName'] = self.customer_bill_first_name
		if self.customer_bill_last_name is not None:
			data['Customer_BillLastName'] = self.customer_bill_last_name
		if self.customer_bill_email is not None:
			data['Customer_BillEmail'] = self.customer_bill_email
		if self.customer_bill_company is not None:
			data['Customer_BillCompany'] = self.customer_bill_company
		if self.customer_bill_phone is not None:
			data['Customer_BillPhone'] = self.customer_bill_phone
		if self.customer_bill_fax is not None:
			data['Customer_BillFax'] = self.customer_bill_fax
		if self.customer_bill_address1 is not None:
			data['Customer_BillAddress1'] = self.customer_bill_address1
		if self.customer_bill_address2 is not None:
			data['Customer_BillAddress2'] = self.customer_bill_address2
		if self.customer_bill_city is not None:
			data['Customer_BillCity'] = self.customer_bill_city
		if self.customer_bill_state is not None:
			data['Customer_BillState'] = self.customer_bill_state
		if self.customer_bill_zip is not None:
			data['Customer_BillZip'] = self.customer_bill_zip
		if self.customer_bill_country is not None:
			data['Customer_BillCountry'] = self.customer_bill_country
		if self.customer_tax_exempt is not None:
			data['Customer_Tax_Exempt'] = self.customer_tax_exempt
		if self.customer_business_account is not None:
			data['Customer_BusinessAccount'] = self.customer_business_account
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data


"""
Handles API Request Customer_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customer_update
"""


class CustomerUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerUpdate Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.customer_password_email = None
		self.customer_password = None
		self.customer_ship_residential = False
		self.customer_ship_first_name = None
		self.customer_ship_last_name = None
		self.customer_ship_email = None
		self.customer_ship_company = None
		self.customer_ship_phone = None
		self.customer_ship_fax = None
		self.customer_ship_address1 = None
		self.customer_ship_address2 = None
		self.customer_ship_city = None
		self.customer_ship_state = None
		self.customer_ship_zip = None
		self.customer_ship_country = None
		self.customer_bill_first_name = None
		self.customer_bill_last_name = None
		self.customer_bill_email = None
		self.customer_bill_company = None
		self.customer_bill_phone = None
		self.customer_bill_fax = None
		self.customer_bill_address1 = None
		self.customer_bill_address2 = None
		self.customer_bill_city = None
		self.customer_bill_state = None
		self.customer_bill_zip = None
		self.customer_bill_country = None
		self.customer_tax_exempt = False
		self.customer_business_account = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

			self.set_customer_login(customer.get_login())
			self.set_customer_password_email(customer.get_password_email())
			self.set_customer_ship_residential(customer.get_shipping_residential())
			self.set_customer_ship_first_name(customer.get_ship_first_name())
			self.set_customer_ship_last_name(customer.get_ship_last_name())
			self.set_customer_ship_email(customer.get_ship_email())
			self.set_customer_ship_company(customer.get_ship_company())
			self.set_customer_ship_phone(customer.get_ship_phone())
			self.set_customer_ship_fax(customer.get_ship_fax())
			self.set_customer_ship_address1(customer.get_ship_address1())
			self.set_customer_ship_address2(customer.get_ship_address2())
			self.set_customer_ship_city(customer.get_ship_city())
			self.set_customer_ship_state(customer.get_ship_state())
			self.set_customer_ship_zip(customer.get_ship_zip())
			self.set_customer_ship_country(customer.get_ship_country())
			self.set_customer_bill_first_name(customer.get_bill_first_name())
			self.set_customer_bill_last_name(customer.get_bill_last_name())
			self.set_customer_bill_email(customer.get_bill_email())
			self.set_customer_bill_company(customer.get_bill_company())
			self.set_customer_bill_phone(customer.get_bill_phone())
			self.set_customer_bill_fax(customer.get_bill_fax())
			self.set_customer_bill_address1(customer.get_bill_address1())
			self.set_customer_bill_address2(customer.get_bill_address2())
			self.set_customer_bill_city(customer.get_bill_city())
			self.set_customer_bill_state(customer.get_bill_state())
			self.set_customer_bill_zip(customer.get_bill_zip())
			self.set_customer_bill_country(customer.get_bill_country())
			self.set_customer_tax_exempt(customer.get_tax_exempt())
			self.set_customer_business_account(customer.get_business_title())

			if customer.get_custom_field_values():
				self.set_custom_field_values(customer.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Customer_Update'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_customer_password_email(self) -> str:
		"""
		Get Customer_PasswordEmail.

		:returns: str
		"""

		return self.customer_password_email

	def get_customer_password(self) -> str:
		"""
		Get Customer_Password.

		:returns: str
		"""

		return self.customer_password

	def get_customer_ship_residential(self) -> bool:
		"""
		Get Customer_ShipResidential.

		:returns: bool
		"""

		return self.customer_ship_residential

	def get_customer_ship_first_name(self) -> str:
		"""
		Get Customer_ShipFirstName.

		:returns: str
		"""

		return self.customer_ship_first_name

	def get_customer_ship_last_name(self) -> str:
		"""
		Get Customer_ShipLastName.

		:returns: str
		"""

		return self.customer_ship_last_name

	def get_customer_ship_email(self) -> str:
		"""
		Get Customer_ShipEmail.

		:returns: str
		"""

		return self.customer_ship_email

	def get_customer_ship_company(self) -> str:
		"""
		Get Customer_ShipCompany.

		:returns: str
		"""

		return self.customer_ship_company

	def get_customer_ship_phone(self) -> str:
		"""
		Get Customer_ShipPhone.

		:returns: str
		"""

		return self.customer_ship_phone

	def get_customer_ship_fax(self) -> str:
		"""
		Get Customer_ShipFax.

		:returns: str
		"""

		return self.customer_ship_fax

	def get_customer_ship_address1(self) -> str:
		"""
		Get Customer_ShipAddress1.

		:returns: str
		"""

		return self.customer_ship_address1

	def get_customer_ship_address2(self) -> str:
		"""
		Get Customer_ShipAddress2.

		:returns: str
		"""

		return self.customer_ship_address2

	def get_customer_ship_city(self) -> str:
		"""
		Get Customer_ShipCity.

		:returns: str
		"""

		return self.customer_ship_city

	def get_customer_ship_state(self) -> str:
		"""
		Get Customer_ShipState.

		:returns: str
		"""

		return self.customer_ship_state

	def get_customer_ship_zip(self) -> str:
		"""
		Get Customer_ShipZip.

		:returns: str
		"""

		return self.customer_ship_zip

	def get_customer_ship_country(self) -> str:
		"""
		Get Customer_ShipCountry.

		:returns: str
		"""

		return self.customer_ship_country

	def get_customer_bill_first_name(self) -> str:
		"""
		Get Customer_BillFirstName.

		:returns: str
		"""

		return self.customer_bill_first_name

	def get_customer_bill_last_name(self) -> str:
		"""
		Get Customer_BillLastName.

		:returns: str
		"""

		return self.customer_bill_last_name

	def get_customer_bill_email(self) -> str:
		"""
		Get Customer_BillEmail.

		:returns: str
		"""

		return self.customer_bill_email

	def get_customer_bill_company(self) -> str:
		"""
		Get Customer_BillCompany.

		:returns: str
		"""

		return self.customer_bill_company

	def get_customer_bill_phone(self) -> str:
		"""
		Get Customer_BillPhone.

		:returns: str
		"""

		return self.customer_bill_phone

	def get_customer_bill_fax(self) -> str:
		"""
		Get Customer_BillFax.

		:returns: str
		"""

		return self.customer_bill_fax

	def get_customer_bill_address1(self) -> str:
		"""
		Get Customer_BillAddress1.

		:returns: str
		"""

		return self.customer_bill_address1

	def get_customer_bill_address2(self) -> str:
		"""
		Get Customer_BillAddress2.

		:returns: str
		"""

		return self.customer_bill_address2

	def get_customer_bill_city(self) -> str:
		"""
		Get Customer_BillCity.

		:returns: str
		"""

		return self.customer_bill_city

	def get_customer_bill_state(self) -> str:
		"""
		Get Customer_BillState.

		:returns: str
		"""

		return self.customer_bill_state

	def get_customer_bill_zip(self) -> str:
		"""
		Get Customer_BillZip.

		:returns: str
		"""

		return self.customer_bill_zip

	def get_customer_bill_country(self) -> str:
		"""
		Get Customer_BillCountry.

		:returns: str
		"""

		return self.customer_bill_country

	def get_customer_tax_exempt(self) -> bool:
		"""
		Get Customer_Tax_Exempt.

		:returns: bool
		"""

		return self.customer_tax_exempt

	def get_customer_business_account(self) -> str:
		"""
		Get Customer_BusinessAccount.

		:returns: str
		"""

		return self.customer_business_account

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_customer_id(self, customer_id: int) -> 'CustomerUpdate':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerUpdate
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerUpdate':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerUpdate
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerUpdate':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerUpdate
		"""

		self.customer_login = customer_login
		return self

	def set_customer_password_email(self, customer_password_email: str) -> 'CustomerUpdate':
		"""
		Set Customer_PasswordEmail.

		:param customer_password_email: str
		:returns: CustomerUpdate
		"""

		self.customer_password_email = customer_password_email
		return self

	def set_customer_password(self, customer_password: str) -> 'CustomerUpdate':
		"""
		Set Customer_Password.

		:param customer_password: str
		:returns: CustomerUpdate
		"""

		self.customer_password = customer_password
		return self

	def set_customer_ship_residential(self, customer_ship_residential: bool) -> 'CustomerUpdate':
		"""
		Set Customer_ShipResidential.

		:param customer_ship_residential: bool
		:returns: CustomerUpdate
		"""

		self.customer_ship_residential = customer_ship_residential
		return self

	def set_customer_ship_first_name(self, customer_ship_first_name: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipFirstName.

		:param customer_ship_first_name: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_first_name = customer_ship_first_name
		return self

	def set_customer_ship_last_name(self, customer_ship_last_name: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipLastName.

		:param customer_ship_last_name: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_last_name = customer_ship_last_name
		return self

	def set_customer_ship_email(self, customer_ship_email: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipEmail.

		:param customer_ship_email: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_email = customer_ship_email
		return self

	def set_customer_ship_company(self, customer_ship_company: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipCompany.

		:param customer_ship_company: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_company = customer_ship_company
		return self

	def set_customer_ship_phone(self, customer_ship_phone: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipPhone.

		:param customer_ship_phone: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_phone = customer_ship_phone
		return self

	def set_customer_ship_fax(self, customer_ship_fax: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipFax.

		:param customer_ship_fax: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_fax = customer_ship_fax
		return self

	def set_customer_ship_address1(self, customer_ship_address1: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipAddress1.

		:param customer_ship_address1: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_address1 = customer_ship_address1
		return self

	def set_customer_ship_address2(self, customer_ship_address2: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipAddress2.

		:param customer_ship_address2: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_address2 = customer_ship_address2
		return self

	def set_customer_ship_city(self, customer_ship_city: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipCity.

		:param customer_ship_city: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_city = customer_ship_city
		return self

	def set_customer_ship_state(self, customer_ship_state: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipState.

		:param customer_ship_state: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_state = customer_ship_state
		return self

	def set_customer_ship_zip(self, customer_ship_zip: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipZip.

		:param customer_ship_zip: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_zip = customer_ship_zip
		return self

	def set_customer_ship_country(self, customer_ship_country: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipCountry.

		:param customer_ship_country: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_country = customer_ship_country
		return self

	def set_customer_bill_first_name(self, customer_bill_first_name: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillFirstName.

		:param customer_bill_first_name: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_first_name = customer_bill_first_name
		return self

	def set_customer_bill_last_name(self, customer_bill_last_name: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillLastName.

		:param customer_bill_last_name: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_last_name = customer_bill_last_name
		return self

	def set_customer_bill_email(self, customer_bill_email: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillEmail.

		:param customer_bill_email: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_email = customer_bill_email
		return self

	def set_customer_bill_company(self, customer_bill_company: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillCompany.

		:param customer_bill_company: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_company = customer_bill_company
		return self

	def set_customer_bill_phone(self, customer_bill_phone: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillPhone.

		:param customer_bill_phone: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_phone = customer_bill_phone
		return self

	def set_customer_bill_fax(self, customer_bill_fax: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillFax.

		:param customer_bill_fax: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_fax = customer_bill_fax
		return self

	def set_customer_bill_address1(self, customer_bill_address1: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillAddress1.

		:param customer_bill_address1: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_address1 = customer_bill_address1
		return self

	def set_customer_bill_address2(self, customer_bill_address2: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillAddress2.

		:param customer_bill_address2: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_address2 = customer_bill_address2
		return self

	def set_customer_bill_city(self, customer_bill_city: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillCity.

		:param customer_bill_city: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_city = customer_bill_city
		return self

	def set_customer_bill_state(self, customer_bill_state: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillState.

		:param customer_bill_state: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_state = customer_bill_state
		return self

	def set_customer_bill_zip(self, customer_bill_zip: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillZip.

		:param customer_bill_zip: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_zip = customer_bill_zip
		return self

	def set_customer_bill_country(self, customer_bill_country: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillCountry.

		:param customer_bill_country: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_country = customer_bill_country
		return self

	def set_customer_tax_exempt(self, customer_tax_exempt: bool) -> 'CustomerUpdate':
		"""
		Set Customer_Tax_Exempt.

		:param customer_tax_exempt: bool
		:returns: CustomerUpdate
		"""

		self.customer_tax_exempt = customer_tax_exempt
		return self

	def set_customer_business_account(self, customer_business_account: str) -> 'CustomerUpdate':
		"""
		Set Customer_BusinessAccount.

		:param customer_business_account: str
		:returns: CustomerUpdate
		"""

		self.customer_business_account = customer_business_account
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'CustomerUpdate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: CustomerUpdate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer

		if self.customer_login is not None:
			data['Customer_Login'] = self.customer_login
		if self.customer_password_email is not None:
			data['Customer_PasswordEmail'] = self.customer_password_email
		if self.customer_password is not None:
			data['Customer_Password'] = self.customer_password
		if self.customer_ship_residential is not None:
			data['Customer_ShipResidential'] = self.customer_ship_residential
		if self.customer_ship_first_name is not None:
			data['Customer_ShipFirstName'] = self.customer_ship_first_name
		if self.customer_ship_last_name is not None:
			data['Customer_ShipLastName'] = self.customer_ship_last_name
		if self.customer_ship_email is not None:
			data['Customer_ShipEmail'] = self.customer_ship_email
		if self.customer_ship_company is not None:
			data['Customer_ShipCompany'] = self.customer_ship_company
		if self.customer_ship_phone is not None:
			data['Customer_ShipPhone'] = self.customer_ship_phone
		if self.customer_ship_fax is not None:
			data['Customer_ShipFax'] = self.customer_ship_fax
		if self.customer_ship_address1 is not None:
			data['Customer_ShipAddress1'] = self.customer_ship_address1
		if self.customer_ship_address2 is not None:
			data['Customer_ShipAddress2'] = self.customer_ship_address2
		if self.customer_ship_city is not None:
			data['Customer_ShipCity'] = self.customer_ship_city
		if self.customer_ship_state is not None:
			data['Customer_ShipState'] = self.customer_ship_state
		if self.customer_ship_zip is not None:
			data['Customer_ShipZip'] = self.customer_ship_zip
		if self.customer_ship_country is not None:
			data['Customer_ShipCountry'] = self.customer_ship_country
		if self.customer_bill_first_name is not None:
			data['Customer_BillFirstName'] = self.customer_bill_first_name
		if self.customer_bill_last_name is not None:
			data['Customer_BillLastName'] = self.customer_bill_last_name
		if self.customer_bill_email is not None:
			data['Customer_BillEmail'] = self.customer_bill_email
		if self.customer_bill_company is not None:
			data['Customer_BillCompany'] = self.customer_bill_company
		if self.customer_bill_phone is not None:
			data['Customer_BillPhone'] = self.customer_bill_phone
		if self.customer_bill_fax is not None:
			data['Customer_BillFax'] = self.customer_bill_fax
		if self.customer_bill_address1 is not None:
			data['Customer_BillAddress1'] = self.customer_bill_address1
		if self.customer_bill_address2 is not None:
			data['Customer_BillAddress2'] = self.customer_bill_address2
		if self.customer_bill_city is not None:
			data['Customer_BillCity'] = self.customer_bill_city
		if self.customer_bill_state is not None:
			data['Customer_BillState'] = self.customer_bill_state
		if self.customer_bill_zip is not None:
			data['Customer_BillZip'] = self.customer_bill_zip
		if self.customer_bill_country is not None:
			data['Customer_BillCountry'] = self.customer_bill_country
		if self.customer_tax_exempt is not None:
			data['Customer_Tax_Exempt'] = self.customer_tax_exempt
		if self.customer_business_account is not None:
			data['Customer_BusinessAccount'] = self.customer_business_account
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data


"""
Handles API Request CustomerPaymentCard_Register. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customerpaymentcard_register
"""


class CustomerPaymentCardRegister(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerPaymentCardRegister Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.first_name = None
		self.last_name = None
		self.card_type = None
		self.card_number = None
		self.expiration_month = None
		self.expiration_year = None
		self.address1 = None
		self.address2 = None
		self.city = None
		self.state = None
		self.zip = None
		self.country = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerPaymentCard_Register'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_first_name(self) -> str:
		"""
		Get FirstName.

		:returns: str
		"""

		return self.first_name

	def get_last_name(self) -> str:
		"""
		Get LastName.

		:returns: str
		"""

		return self.last_name

	def get_card_type(self) -> str:
		"""
		Get CardType.

		:returns: str
		"""

		return self.card_type

	def get_card_number(self) -> str:
		"""
		Get CardNumber.

		:returns: str
		"""

		return self.card_number

	def get_expiration_month(self) -> int:
		"""
		Get ExpirationMonth.

		:returns: int
		"""

		return self.expiration_month

	def get_expiration_year(self) -> int:
		"""
		Get ExpirationYear.

		:returns: int
		"""

		return self.expiration_year

	def get_address1(self) -> str:
		"""
		Get Address1.

		:returns: str
		"""

		return self.address1

	def get_address2(self) -> str:
		"""
		Get Address2.

		:returns: str
		"""

		return self.address2

	def get_city(self) -> str:
		"""
		Get City.

		:returns: str
		"""

		return self.city

	def get_state(self) -> str:
		"""
		Get State.

		:returns: str
		"""

		return self.state

	def get_zip(self) -> str:
		"""
		Get Zip.

		:returns: str
		"""

		return self.zip

	def get_country(self) -> str:
		"""
		Get Country.

		:returns: str
		"""

		return self.country

	def set_customer_id(self, customer_id: int) -> 'CustomerPaymentCardRegister':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerPaymentCardRegister
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerPaymentCardRegister
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerPaymentCardRegister
		"""

		self.customer_login = customer_login
		return self

	def set_first_name(self, first_name: str) -> 'CustomerPaymentCardRegister':
		"""
		Set FirstName.

		:param first_name: str
		:returns: CustomerPaymentCardRegister
		"""

		self.first_name = first_name
		return self

	def set_last_name(self, last_name: str) -> 'CustomerPaymentCardRegister':
		"""
		Set LastName.

		:param last_name: str
		:returns: CustomerPaymentCardRegister
		"""

		self.last_name = last_name
		return self

	def set_card_type(self, card_type: str) -> 'CustomerPaymentCardRegister':
		"""
		Set CardType.

		:param card_type: str
		:returns: CustomerPaymentCardRegister
		"""

		self.card_type = card_type
		return self

	def set_card_number(self, card_number: str) -> 'CustomerPaymentCardRegister':
		"""
		Set CardNumber.

		:param card_number: str
		:returns: CustomerPaymentCardRegister
		"""

		self.card_number = card_number
		return self

	def set_expiration_month(self, expiration_month: int) -> 'CustomerPaymentCardRegister':
		"""
		Set ExpirationMonth.

		:param expiration_month: int
		:returns: CustomerPaymentCardRegister
		"""

		self.expiration_month = expiration_month
		return self

	def set_expiration_year(self, expiration_year: int) -> 'CustomerPaymentCardRegister':
		"""
		Set ExpirationYear.

		:param expiration_year: int
		:returns: CustomerPaymentCardRegister
		"""

		self.expiration_year = expiration_year
		return self

	def set_address1(self, address1: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Address1.

		:param address1: str
		:returns: CustomerPaymentCardRegister
		"""

		self.address1 = address1
		return self

	def set_address2(self, address2: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Address2.

		:param address2: str
		:returns: CustomerPaymentCardRegister
		"""

		self.address2 = address2
		return self

	def set_city(self, city: str) -> 'CustomerPaymentCardRegister':
		"""
		Set City.

		:param city: str
		:returns: CustomerPaymentCardRegister
		"""

		self.city = city
		return self

	def set_state(self, state: str) -> 'CustomerPaymentCardRegister':
		"""
		Set State.

		:param state: str
		:returns: CustomerPaymentCardRegister
		"""

		self.state = state
		return self

	def set_zip(self, zip: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Zip.

		:param zip: str
		:returns: CustomerPaymentCardRegister
		"""

		self.zip = zip
		return self

	def set_country(self, country: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Country.

		:param country: str
		:returns: CustomerPaymentCardRegister
		"""

		self.country = country
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerPaymentCardRegister':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerPaymentCardRegister':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerPaymentCardRegister(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.first_name is not None:
			data['FirstName'] = self.first_name
		if self.last_name is not None:
			data['LastName'] = self.last_name
		if self.card_type is not None:
			data['CardType'] = self.card_type
		if self.card_number is not None:
			data['CardNumber'] = self.card_number
		if self.expiration_month is not None:
			data['ExpirationMonth'] = self.expiration_month
		if self.expiration_year is not None:
			data['ExpirationYear'] = self.expiration_year
		if self.address1 is not None:
			data['Address1'] = self.address1
		if self.address2 is not None:
			data['Address2'] = self.address2
		if self.city is not None:
			data['City'] = self.city
		if self.state is not None:
			data['State'] = self.state
		if self.zip is not None:
			data['Zip'] = self.zip
		if self.country is not None:
			data['Country'] = self.country
		return data


"""
Handles API Request Module. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/module
"""


class Module(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		Module Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.module_code = None
		self.module_function = None
		self.module_fields = {}

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Module'

	def get_module_code(self) -> str:
		"""
		Get Module_Code.

		:returns: str
		"""

		return self.module_code

	def get_module_function(self) -> str:
		"""
		Get Module_Function.

		:returns: str
		"""

		return self.module_function

	def get_module_fields(self):
		"""
		Get Module_Fields.

		:returns: dict
		"""

		return self.module_fields

	def set_module_code(self, module_code: str) -> 'Module':
		"""
		Set Module_Code.

		:param module_code: str
		:returns: Module
		"""

		self.module_code = module_code
		return self

	def set_module_function(self, module_function: str) -> 'Module':
		"""
		Set Module_Function.

		:param module_function: str
		:returns: Module
		"""

		self.module_function = module_function
		return self

	def set_module_fields(self, module_fields) -> 'Module':
		"""
		Set Module_Fields.

		:param module_fields: dict
		:returns: Module
		"""

		self.module_fields = module_fields
		return self

	def set_module_field(self, field: str, value) -> 'Module':
		"""
		Add custom data to the request.

		:param field: str
		:param value: mixed
		:returns: {Module}
		"""

		self.module_fields[field] = value
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.Module':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'Module':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.Module(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()
		data.update(self.get_module_fields())

		data['Module_Code'] = self.module_code
		data['Module_Function'] = self.module_function
		return data


"""
Handles API Request NoteList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/notelist_load_query
"""


class NoteListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'notetext',
		'dtstamp',
		'cust_id',
		'account_id',
		'order_id',
		'admin_user',
		'cust_login',
		'business_title'
	]

	available_sort_fields = [
		'id',
		'notetext',
		'dtstamp',
		'cust_id',
		'account_id',
		'order_id',
		'admin_user',
		'cust_login',
		'business_title'
	]

	def __init__(self, client: Client = None):
		"""
		NoteListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'NoteList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.NoteListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'NoteListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.NoteListLoadQuery(self, http_response, data)


"""
Handles API Request Note_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/note_delete
"""


class NoteDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, note: merchantapi.model.Note = None):
		"""
		NoteDelete Constructor.

		:param client: Client
		:param note: Note
		"""

		super().__init__(client)
		self.note_id = None
		if isinstance(note, merchantapi.model.Note):
			self.set_note_id(note.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Note_Delete'

	def get_note_id(self) -> int:
		"""
		Get Note_ID.

		:returns: int
		"""

		return self.note_id

	def set_note_id(self, note_id: int) -> 'NoteDelete':
		"""
		Set Note_ID.

		:param note_id: int
		:returns: NoteDelete
		"""

		self.note_id = note_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.NoteDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'NoteDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.NoteDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Note_ID'] = self.note_id
		return data


"""
Handles API Request Note_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/note_insert
"""


class NoteInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		NoteInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.note_text = None
		self.customer_id = None
		self.account_id = None
		self.order_id = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Note_Insert'

	def get_note_text(self) -> str:
		"""
		Get NoteText.

		:returns: str
		"""

		return self.note_text

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_account_id(self) -> int:
		"""
		Get Account_ID.

		:returns: int
		"""

		return self.account_id

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def set_note_text(self, note_text: str) -> 'NoteInsert':
		"""
		Set NoteText.

		:param note_text: str
		:returns: NoteInsert
		"""

		self.note_text = note_text
		return self

	def set_customer_id(self, customer_id: int) -> 'NoteInsert':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: NoteInsert
		"""

		self.customer_id = customer_id
		return self

	def set_account_id(self, account_id: int) -> 'NoteInsert':
		"""
		Set Account_ID.

		:param account_id: int
		:returns: NoteInsert
		"""

		self.account_id = account_id
		return self

	def set_order_id(self, order_id: int) -> 'NoteInsert':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: NoteInsert
		"""

		self.order_id = order_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.NoteInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'NoteInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.NoteInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['NoteText'] = self.note_text
		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		if self.account_id is not None:
			data['Account_ID'] = self.account_id
		if self.order_id is not None:
			data['Order_ID'] = self.order_id
		return data


"""
Handles API Request Note_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/note_update
"""


class NoteUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, note: merchantapi.model.Note = None):
		"""
		NoteUpdate Constructor.

		:param client: Client
		:param note: Note
		"""

		super().__init__(client)
		self.note_id = None
		self.note_text = None
		if isinstance(note, merchantapi.model.Note):
			self.set_note_id(note.get_id())
			self.set_note_text(note.get_note_text())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Note_Update'

	def get_note_id(self) -> int:
		"""
		Get Note_ID.

		:returns: int
		"""

		return self.note_id

	def get_note_text(self) -> str:
		"""
		Get NoteText.

		:returns: str
		"""

		return self.note_text

	def set_note_id(self, note_id: int) -> 'NoteUpdate':
		"""
		Set Note_ID.

		:param note_id: int
		:returns: NoteUpdate
		"""

		self.note_id = note_id
		return self

	def set_note_text(self, note_text: str) -> 'NoteUpdate':
		"""
		Set NoteText.

		:param note_text: str
		:returns: NoteUpdate
		"""

		self.note_text = note_text
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.NoteUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'NoteUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.NoteUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Note_ID'] = self.get_note_id()

		data['NoteText'] = self.note_text
		return data


"""
Handles API Request OrderCustomFieldList_Load. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordercustomfieldlist_load
"""


class OrderCustomFieldListLoad(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		OrderCustomFieldListLoad Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderCustomFieldList_Load'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCustomFieldListLoad':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCustomFieldListLoad':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCustomFieldListLoad(self, http_response, data)


"""
Handles API Request OrderCustomFields_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordercustomfields_update
"""


class OrderCustomFieldsUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderCustomFieldsUpdate Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderCustomFields_Update'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_order_id(self, order_id: int) -> 'OrderCustomFieldsUpdate':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderCustomFieldsUpdate
		"""

		self.order_id = order_id
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'OrderCustomFieldsUpdate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: OrderCustomFieldsUpdate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCustomFieldsUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCustomFieldsUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCustomFieldsUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data


"""
Handles API Request OrderItemList_BackOrder. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitemlist_backorder
"""


class OrderItemListBackOrder(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemListBackOrder Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.line_ids = []
		self.date_in_stock = None
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItemList_BackOrder'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_ids(self):
		"""
		Get Line_IDs.

		:returns: list
		"""

		return self.line_ids

	def get_date_in_stock(self) -> int:
		"""
		Get Date_InStock.

		:returns: int
		"""

		return self.date_in_stock

	def set_order_id(self, order_id: int) -> 'OrderItemListBackOrder':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemListBackOrder
		"""

		self.order_id = order_id
		return self

	def set_date_in_stock(self, date_in_stock: int) -> 'OrderItemListBackOrder':
		"""
		Set Date_InStock.

		:param date_in_stock: int
		:returns: OrderItemListBackOrder
		"""

		self.date_in_stock = date_in_stock
		return self
	
	def add_line_id(self, line_id) -> 'OrderItemListBackOrder':
		"""
		Add Line_IDs.

		:param line_id: int
		:returns: {OrderItemListBackOrder}
		"""

		self.line_ids.append(line_id)
		return self

	def add_order_item(self, order_item: merchantapi.model.OrderItem) -> 'OrderItemListBackOrder':
		"""
		Add OrderItem model.

		:param order_item: OrderItem
		:raises Exception:
		:returns: OrderItemListBackOrder
		"""
		if not isinstance(order_item, merchantapi.model.OrderItem):
			raise Exception('Expected an instance of OrderItem')

		if order_item.get_line_id():
			self.line_ids.append(order_item.get_line_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemListBackOrder':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemListBackOrder':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemListBackOrder(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		data['Line_IDs'] = self.line_ids
		if self.date_in_stock is not None:
			data['Date_InStock'] = self.date_in_stock
		return data


"""
Handles API Request OrderItemList_Cancel. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitemlist_cancel
"""


class OrderItemListCancel(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemListCancel Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.line_ids = []
		self.reason = None
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItemList_Cancel'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_ids(self):
		"""
		Get Line_IDs.

		:returns: list
		"""

		return self.line_ids

	def get_reason(self) -> str:
		"""
		Get Reason.

		:returns: str
		"""

		return self.reason

	def set_order_id(self, order_id: int) -> 'OrderItemListCancel':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemListCancel
		"""

		self.order_id = order_id
		return self

	def set_reason(self, reason: str) -> 'OrderItemListCancel':
		"""
		Set Reason.

		:param reason: str
		:returns: OrderItemListCancel
		"""

		self.reason = reason
		return self
	
	def add_line_id(self, line_id) -> 'OrderItemListCancel':
		"""
		Add Line_IDs.

		:param line_id: int
		:returns: {OrderItemListCancel}
		"""

		self.line_ids.append(line_id)
		return self

	def add_order_item(self, order_item: merchantapi.model.OrderItem) -> 'OrderItemListCancel':
		"""
		Add OrderItem model.

		:param order_item: OrderItem
		:raises Exception:
		:returns: OrderItemListCancel
		"""
		if not isinstance(order_item, merchantapi.model.OrderItem):
			raise Exception('Expected an instance of OrderItem')

		if order_item.get_line_id():
			self.line_ids.append(order_item.get_line_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemListCancel':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemListCancel':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemListCancel(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.get_order_id()

		data['Line_IDs'] = self.line_ids
		if self.reason is not None:
			data['Reason'] = self.reason
		return data


"""
Handles API Request OrderItemList_CreateShipment. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitemlist_createshipment
"""


class OrderItemListCreateShipment(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemListCreateShipment Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.line_ids = []
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItemList_CreateShipment'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_ids(self):
		"""
		Get Line_IDs.

		:returns: list
		"""

		return self.line_ids

	def set_order_id(self, order_id: int) -> 'OrderItemListCreateShipment':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemListCreateShipment
		"""

		self.order_id = order_id
		return self
	
	def add_line_id(self, line_id) -> 'OrderItemListCreateShipment':
		"""
		Add Line_IDs.

		:param line_id: int
		:returns: {OrderItemListCreateShipment}
		"""

		self.line_ids.append(line_id)
		return self

	def add_order_item(self, order_item: merchantapi.model.OrderItem) -> 'OrderItemListCreateShipment':
		"""
		Add OrderItem model.

		:param order_item: OrderItem
		:raises Exception:
		:returns: OrderItemListCreateShipment
		"""
		if not isinstance(order_item, merchantapi.model.OrderItem):
			raise Exception('Expected an instance of OrderItem')

		if order_item.get_line_id():
			self.line_ids.append(order_item.get_line_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemListCreateShipment':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemListCreateShipment':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemListCreateShipment(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.get_order_id()

		data['Line_IDs'] = self.line_ids
		return data


"""
Handles API Request OrderItemList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitemlist_delete
"""


class OrderItemListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemListDelete Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.line_ids = []
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItemList_Delete'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_ids(self):
		"""
		Get Line_IDs.

		:returns: list
		"""

		return self.line_ids

	def set_order_id(self, order_id: int) -> 'OrderItemListDelete':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemListDelete
		"""

		self.order_id = order_id
		return self
	
	def add_line_id(self, line_id) -> 'OrderItemListDelete':
		"""
		Add Line_IDs.

		:param line_id: int
		:returns: {OrderItemListDelete}
		"""

		self.line_ids.append(line_id)
		return self

	def add_order_item(self, order_item: merchantapi.model.OrderItem) -> 'OrderItemListDelete':
		"""
		Add OrderItem model.

		:param order_item: OrderItem
		:raises Exception:
		:returns: OrderItemListDelete
		"""
		if not isinstance(order_item, merchantapi.model.OrderItem):
			raise Exception('Expected an instance of OrderItem')

		if order_item.get_line_id():
			self.line_ids.append(order_item.get_line_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.order_id
		data['Line_IDs'] = self.line_ids
		return data


"""
Handles API Request OrderItem_Add. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitem_add
"""


class OrderItemAdd(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemAdd Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.code = None
		self.name = None
		self.sku = None
		self.quantity = None
		self.price = None
		self.weight = None
		self.taxable = False
		self.options = []
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItem_Add'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_sku(self) -> str:
		"""
		Get Sku.

		:returns: str
		"""

		return self.sku

	def get_quantity(self) -> int:
		"""
		Get Quantity.

		:returns: int
		"""

		return self.quantity

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_taxable(self) -> bool:
		"""
		Get Taxable.

		:returns: bool
		"""

		return self.taxable

	def get_options(self) -> list:
		"""
		Get Options.

		:returns: List of OrderItemOption
		"""

		return self.options

	def set_order_id(self, order_id: int) -> 'OrderItemAdd':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemAdd
		"""

		self.order_id = order_id
		return self

	def set_code(self, code: str) -> 'OrderItemAdd':
		"""
		Set Code.

		:param code: str
		:returns: OrderItemAdd
		"""

		self.code = code
		return self

	def set_name(self, name: str) -> 'OrderItemAdd':
		"""
		Set Name.

		:param name: str
		:returns: OrderItemAdd
		"""

		self.name = name
		return self

	def set_sku(self, sku: str) -> 'OrderItemAdd':
		"""
		Set Sku.

		:param sku: str
		:returns: OrderItemAdd
		"""

		self.sku = sku
		return self

	def set_quantity(self, quantity: int) -> 'OrderItemAdd':
		"""
		Set Quantity.

		:param quantity: int
		:returns: OrderItemAdd
		"""

		self.quantity = quantity
		return self

	def set_price(self, price: float) -> 'OrderItemAdd':
		"""
		Set Price.

		:param price: float
		:returns: OrderItemAdd
		"""

		self.price = price
		return self

	def set_weight(self, weight: float) -> 'OrderItemAdd':
		"""
		Set Weight.

		:param weight: float
		:returns: OrderItemAdd
		"""

		self.weight = weight
		return self

	def set_taxable(self, taxable: bool) -> 'OrderItemAdd':
		"""
		Set Taxable.

		:param taxable: bool
		:returns: OrderItemAdd
		"""

		self.taxable = taxable
		return self

	def set_options(self, options: list) -> 'OrderItemAdd':
		"""
		Set Options.

		:param options: {OrderItemOption[]}
		:raises Exception:
		:returns: OrderItemAdd
		"""

		for e in options:
			if not isinstance(e, merchantapi.model.OrderItemOption):
				raise Exception("")
		self.options = options
		return self
	
	def add_option(self, option) -> 'OrderItemAdd':
		"""
		Add Options.

		:param option: OrderItemOption 
		:raises Exception:
		:returns: {OrderItemAdd}
		"""

		if isinstance(option, merchantapi.model.OrderItemOption):
			self.options.append(option)
		elif isinstance(option, dict):
			self.options.append(merchantapi.model.OrderItemOption(option))
		else:
			raise Exception('Expected instance of OrderItemOption or dict')
		return self

	def add_options(self, options: list) -> 'OrderItemAdd':
		"""
		Add many OrderItemOption.

		:param options: List of OrderItemOption
		:raises Exception:
		:returns: OrderItemAdd
		"""

		for e in options:
			if not isinstance(e, merchantapi.model.OrderItemOption):
				raise Exception('')
			self.options.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemAdd':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemAdd':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemAdd(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.get_order_id()

		data['Code'] = self.code
		data['Name'] = self.name
		if self.sku is not None:
			data['Sku'] = self.sku
		data['Quantity'] = self.quantity
		if self.price is not None:
			data['Price'] = self.price
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.taxable is not None:
			data['Taxable'] = self.taxable
		if len(self.options):
			data['Options'] = []

			for f in self.options:
				data['Options'].append(f.to_dict())
		return data


"""
Handles API Request OrderItem_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitem_update
"""


class OrderItemUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order_item: merchantapi.model.OrderItem = None):
		"""
		OrderItemUpdate Constructor.

		:param client: Client
		:param order_item: OrderItem
		"""

		super().__init__(client)
		self.order_id = None
		self.line_id = None
		self.code = None
		self.name = None
		self.sku = None
		self.quantity = None
		self.price = None
		self.weight = None
		self.taxable = False
		self.options = []
		if isinstance(order_item, merchantapi.model.OrderItem):
			self.set_order_id(order_item.get_order_id())
			self.set_line_id(order_item.get_line_id())
			self.set_code(order_item.get_code())
			self.set_name(order_item.get_name())
			self.set_sku(order_item.get_sku())
			self.set_quantity(order_item.get_quantity())
			self.set_price(order_item.get_price())
			self.set_weight(order_item.get_weight())
			self.set_taxable(order_item.get_taxable())

			if len(order_item.get_options()):
				self.options = order_item.get_options()

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItem_Update'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_id(self) -> int:
		"""
		Get Line_ID.

		:returns: int
		"""

		return self.line_id

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_sku(self) -> str:
		"""
		Get Sku.

		:returns: str
		"""

		return self.sku

	def get_quantity(self) -> int:
		"""
		Get Quantity.

		:returns: int
		"""

		return self.quantity

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_taxable(self) -> bool:
		"""
		Get Taxable.

		:returns: bool
		"""

		return self.taxable

	def get_options(self) -> list:
		"""
		Get Options.

		:returns: List of OrderItemOption
		"""

		return self.options

	def set_order_id(self, order_id: int) -> 'OrderItemUpdate':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemUpdate
		"""

		self.order_id = order_id
		return self

	def set_line_id(self, line_id: int) -> 'OrderItemUpdate':
		"""
		Set Line_ID.

		:param line_id: int
		:returns: OrderItemUpdate
		"""

		self.line_id = line_id
		return self

	def set_code(self, code: str) -> 'OrderItemUpdate':
		"""
		Set Code.

		:param code: str
		:returns: OrderItemUpdate
		"""

		self.code = code
		return self

	def set_name(self, name: str) -> 'OrderItemUpdate':
		"""
		Set Name.

		:param name: str
		:returns: OrderItemUpdate
		"""

		self.name = name
		return self

	def set_sku(self, sku: str) -> 'OrderItemUpdate':
		"""
		Set Sku.

		:param sku: str
		:returns: OrderItemUpdate
		"""

		self.sku = sku
		return self

	def set_quantity(self, quantity: int) -> 'OrderItemUpdate':
		"""
		Set Quantity.

		:param quantity: int
		:returns: OrderItemUpdate
		"""

		self.quantity = quantity
		return self

	def set_price(self, price: float) -> 'OrderItemUpdate':
		"""
		Set Price.

		:param price: float
		:returns: OrderItemUpdate
		"""

		self.price = price
		return self

	def set_weight(self, weight: float) -> 'OrderItemUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: OrderItemUpdate
		"""

		self.weight = weight
		return self

	def set_taxable(self, taxable: bool) -> 'OrderItemUpdate':
		"""
		Set Taxable.

		:param taxable: bool
		:returns: OrderItemUpdate
		"""

		self.taxable = taxable
		return self

	def set_options(self, options: list) -> 'OrderItemUpdate':
		"""
		Set Options.

		:param options: {OrderItemOption[]}
		:raises Exception:
		:returns: OrderItemUpdate
		"""

		for e in options:
			if not isinstance(e, merchantapi.model.OrderItemOption):
				raise Exception("")
		self.options = options
		return self
	
	def add_option(self, option) -> 'OrderItemUpdate':
		"""
		Add Options.

		:param option: OrderItemOption 
		:raises Exception:
		:returns: {OrderItemUpdate}
		"""

		if isinstance(option, merchantapi.model.OrderItemOption):
			self.options.append(option)
		elif isinstance(option, dict):
			self.options.append(merchantapi.model.OrderItemOption(option))
		else:
			raise Exception('Expected instance of OrderItemOption or dict')
		return self

	def add_options(self, options: list) -> 'OrderItemUpdate':
		"""
		Add many OrderItemOption.

		:param options: List of OrderItemOption
		:raises Exception:
		:returns: OrderItemUpdate
		"""

		for e in options:
			if not isinstance(e, merchantapi.model.OrderItemOption):
				raise Exception('')
			self.options.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.get_order_id()

		data['Line_ID'] = self.get_line_id()

		if self.code is not None:
			data['Code'] = self.code
		if self.name is not None:
			data['Name'] = self.name
		if self.sku is not None:
			data['Sku'] = self.sku
		if self.quantity is not None:
			data['Quantity'] = self.quantity
		if self.price is not None:
			data['Price'] = self.price
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.taxable is not None:
			data['Taxable'] = self.taxable
		if len(self.options):
			data['Options'] = []

			for f in self.options:
				data['Options'].append(f.to_dict())
		return data


"""
Handles API Request OrderList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderlist_load_query
"""


class OrderListLoadQuery(ListQueryRequest):
	# PAY_STATUS_FILTER constants.
	PAY_STATUS_FILTER_AUTH_ONLY = 'auth_0_capt'
	PAY_STATUS_FILTER_PARTIAL_CAPTURE = 'partial_capt'
	PAY_STATUS_FILTER_CAPTURED_NOT_SHIPPED = 'capt_not_ship'
	PAY_STATUS_FILTER_SHIPPED_NOT_CAPTURED = 'ship_not_capt'

	available_search_fields = [
		'id',
		'batch_id',
		'status',
		'pay_status',
		'orderdate',
		'dt_instock',
		'ship_res',
		'ship_fname',
		'ship_lname',
		'ship_email',
		'ship_comp',
		'ship_phone',
		'ship_fax',
		'ship_addr1',
		'ship_addr2',
		'ship_city',
		'ship_state',
		'ship_zip',
		'ship_cntry',
		'bill_fname',
		'bill_lname',
		'bill_email',
		'bill_comp',
		'bill_phone',
		'bill_fax',
		'bill_addr1',
		'bill_addr2',
		'bill_city',
		'bill_state',
		'bill_zip',
		'bill_cntry',
		'ship_id',
		'ship_data',
		'source',
		'source_id',
		'total',
		'total_ship',
		'total_tax',
		'total_auth',
		'total_capt',
		'total_rfnd',
		'net_capt',
		'pend_count',
		'bord_count',
		'cust_login',
		'cust_pw_email',
		'business_title',
		'note_count'
	]

	available_sort_fields = [
		'id',
		'batch_id',
		'status',
		'pay_status',
		'orderdate',
		'dt_instock',
		'ship_res',
		'ship_fname',
		'ship_lname',
		'ship_email',
		'ship_comp',
		'ship_phone',
		'ship_fax',
		'ship_addr1',
		'ship_addr2',
		'ship_city',
		'ship_state',
		'ship_zip',
		'ship_cntry',
		'bill_fname',
		'bill_lname',
		'bill_email',
		'bill_comp',
		'bill_phone',
		'bill_fax',
		'bill_addr1',
		'bill_addr2',
		'bill_city',
		'bill_state',
		'bill_zip',
		'bill_cntry',
		'ship_data',
		'source',
		'source_id',
		'total',
		'total_ship',
		'total_tax',
		'total_auth',
		'total_capt',
		'total_rfnd',
		'net_capt',
		'pend_count',
		'bord_count',
		'cust_login',
		'cust_pw_email',
		'business_title',
		'note_count',
		'payment_module'
	]

	available_on_demand_columns = [
		'ship_method',
		'cust_login',
		'cust_pw_email',
		'business_title',
		'payment_module',
		'customer',
		'items',
		'charges',
		'coupons',
		'discounts',
		'payments',
		'notes',
		'parts'
	]

	available_custom_filters = {
		'Customer_ID': 'int',
		'BusinessAccount_ID': 'int',
		'pay_id': 'int',
		'payment': [
			PAY_STATUS_FILTER_AUTH_ONLY,
			PAY_STATUS_FILTER_PARTIAL_CAPTURE,
			PAY_STATUS_FILTER_CAPTURED_NOT_SHIPPED,
			PAY_STATUS_FILTER_SHIPPED_NOT_CAPTURED
		],
		'product_code': 'string'
	}

	def __init__(self, client: Client = None):
		"""
		OrderListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.passphrase = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderList_Load_Query'

	def get_passphrase(self) -> str:
		"""
		Get Passphrase.

		:returns: str
		"""

		return self.passphrase

	def set_passphrase(self, passphrase: str) -> 'OrderListLoadQuery':
		"""
		Set Passphrase.

		:param passphrase: str
		:returns: OrderListLoadQuery
		"""

		self.passphrase = passphrase
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.passphrase is not None:
			data['Passphrase'] = self.passphrase
		return data


"""
Handles API Request OrderPayment_Capture. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderpayment_capture
"""


class OrderPaymentCapture(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order_payment: merchantapi.model.OrderPayment = None):
		"""
		OrderPaymentCapture Constructor.

		:param client: Client
		:param order_payment: OrderPayment
		"""

		super().__init__(client)
		self.order_payment_id = None
		self.amount = None
		if isinstance(order_payment, merchantapi.model.OrderPayment):
			self.set_order_payment_id(order_payment.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderPayment_Capture'

	def get_order_payment_id(self) -> int:
		"""
		Get OrderPayment_ID.

		:returns: int
		"""

		return self.order_payment_id

	def get_amount(self) -> float:
		"""
		Get Amount.

		:returns: float
		"""

		return self.amount

	def set_order_payment_id(self, order_payment_id: int) -> 'OrderPaymentCapture':
		"""
		Set OrderPayment_ID.

		:param order_payment_id: int
		:returns: OrderPaymentCapture
		"""

		self.order_payment_id = order_payment_id
		return self

	def set_amount(self, amount: float) -> 'OrderPaymentCapture':
		"""
		Set Amount.

		:param amount: float
		:returns: OrderPaymentCapture
		"""

		self.amount = amount
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderPaymentCapture':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderPaymentCapture':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderPaymentCapture(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['OrderPayment_ID'] = self.order_payment_id
		if self.amount is not None:
			data['Amount'] = self.amount
		return data


"""
Handles API Request OrderPayment_Refund. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderpayment_refund
"""


class OrderPaymentRefund(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order_payment: merchantapi.model.OrderPayment = None):
		"""
		OrderPaymentRefund Constructor.

		:param client: Client
		:param order_payment: OrderPayment
		"""

		super().__init__(client)
		self.order_payment_id = None
		self.amount = None
		if isinstance(order_payment, merchantapi.model.OrderPayment):
			self.set_order_payment_id(order_payment.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderPayment_Refund'

	def get_order_payment_id(self) -> int:
		"""
		Get OrderPayment_ID.

		:returns: int
		"""

		return self.order_payment_id

	def get_amount(self) -> float:
		"""
		Get Amount.

		:returns: float
		"""

		return self.amount

	def set_order_payment_id(self, order_payment_id: int) -> 'OrderPaymentRefund':
		"""
		Set OrderPayment_ID.

		:param order_payment_id: int
		:returns: OrderPaymentRefund
		"""

		self.order_payment_id = order_payment_id
		return self

	def set_amount(self, amount: float) -> 'OrderPaymentRefund':
		"""
		Set Amount.

		:param amount: float
		:returns: OrderPaymentRefund
		"""

		self.amount = amount
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderPaymentRefund':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderPaymentRefund':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderPaymentRefund(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['OrderPayment_ID'] = self.order_payment_id
		if self.amount is not None:
			data['Amount'] = self.amount
		return data


"""
Handles API Request OrderPayment_VOID. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderpayment_void
"""


class OrderPaymentVoid(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order_payment: merchantapi.model.OrderPayment = None):
		"""
		OrderPaymentVoid Constructor.

		:param client: Client
		:param order_payment: OrderPayment
		"""

		super().__init__(client)
		self.order_payment_id = None
		self.amount = None
		if isinstance(order_payment, merchantapi.model.OrderPayment):
			self.set_order_payment_id(order_payment.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderPayment_VOID'

	def get_order_payment_id(self) -> int:
		"""
		Get OrderPayment_ID.

		:returns: int
		"""

		return self.order_payment_id

	def get_amount(self) -> float:
		"""
		Get Amount.

		:returns: float
		"""

		return self.amount

	def set_order_payment_id(self, order_payment_id: int) -> 'OrderPaymentVoid':
		"""
		Set OrderPayment_ID.

		:param order_payment_id: int
		:returns: OrderPaymentVoid
		"""

		self.order_payment_id = order_payment_id
		return self

	def set_amount(self, amount: float) -> 'OrderPaymentVoid':
		"""
		Set Amount.

		:param amount: float
		:returns: OrderPaymentVoid
		"""

		self.amount = amount
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderPaymentVoid':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderPaymentVoid':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderPaymentVoid(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['OrderPayment_ID'] = self.order_payment_id
		if self.amount is not None:
			data['Amount'] = self.amount
		return data


"""
Handles API Request OrderShipmentList_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordershipmentlist_update
"""


class OrderShipmentListUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		OrderShipmentListUpdate Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.shipment_updates = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderShipmentList_Update'

	def get_shipment_updates(self) -> list:
		"""
		Get Shipment_Updates.

		:returns: List of OrderShipmentUpdate
		"""

		return self.shipment_updates

	def set_shipment_updates(self, shipment_updates: list) -> 'OrderShipmentListUpdate':
		"""
		Set Shipment_Updates.

		:param shipment_updates: {OrderShipmentUpdate[]}
		:raises Exception:
		:returns: OrderShipmentListUpdate
		"""

		for e in shipment_updates:
			if not isinstance(e, merchantapi.model.OrderShipmentUpdate):
				raise Exception("")
		self.shipment_updates = shipment_updates
		return self
	
	def add_shipment_update(self, shipment_update) -> 'OrderShipmentListUpdate':
		"""
		Add Shipment_Updates.

		:param shipment_update: OrderShipmentUpdate 
		:raises Exception:
		:returns: {OrderShipmentListUpdate}
		"""

		if isinstance(shipment_update, merchantapi.model.OrderShipmentUpdate):
			self.shipment_updates.append(shipment_update)
		elif isinstance(shipment_update, dict):
			self.shipment_updates.append(merchantapi.model.OrderShipmentUpdate(shipment_update))
		else:
			raise Exception('Expected instance of OrderShipmentUpdate or dict')
		return self

	def add_shipment_updates(self, shipment_updates: list) -> 'OrderShipmentListUpdate':
		"""
		Add many OrderShipmentUpdate.

		:param shipment_updates: List of OrderShipmentUpdate
		:raises Exception:
		:returns: OrderShipmentListUpdate
		"""

		for e in shipment_updates:
			if not isinstance(e, merchantapi.model.OrderShipmentUpdate):
				raise Exception('')
			self.shipment_updates.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderShipmentListUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderShipmentListUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderShipmentListUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if len(self.shipment_updates):
			data['Shipment_Updates'] = []

			for f in self.shipment_updates:
				data['Shipment_Updates'].append(f.to_dict())
		return data


"""
Handles API Request Order_Create. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_create
"""


class OrderCreate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		OrderCreate Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_login = None
		self.customer_id = None
		self.ship_first_name = None
		self.ship_last_name = None
		self.ship_email = None
		self.ship_phone = None
		self.ship_fax = None
		self.ship_company = None
		self.ship_address1 = None
		self.ship_address2 = None
		self.ship_city = None
		self.ship_state = None
		self.ship_zip = None
		self.ship_country = None
		self.ship_residential = False
		self.bill_first_name = None
		self.bill_last_name = None
		self.bill_email = None
		self.bill_phone = None
		self.bill_fax = None
		self.bill_company = None
		self.bill_address1 = None
		self.bill_address2 = None
		self.bill_city = None
		self.bill_state = None
		self.bill_zip = None
		self.bill_country = None
		self.items = []
		self.products = []
		self.charges = []
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		self.shipping_module_code = None
		self.shipping_module_data = None
		self.calculate_charges = False
		self.trigger_fulfillment_modules = False
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_customer_login(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Create'

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_ship_first_name(self) -> str:
		"""
		Get ShipFirstName.

		:returns: str
		"""

		return self.ship_first_name

	def get_ship_last_name(self) -> str:
		"""
		Get ShipLastName.

		:returns: str
		"""

		return self.ship_last_name

	def get_ship_email(self) -> str:
		"""
		Get ShipEmail.

		:returns: str
		"""

		return self.ship_email

	def get_ship_phone(self) -> str:
		"""
		Get ShipPhone.

		:returns: str
		"""

		return self.ship_phone

	def get_ship_fax(self) -> str:
		"""
		Get ShipFax.

		:returns: str
		"""

		return self.ship_fax

	def get_ship_company(self) -> str:
		"""
		Get ShipCompany.

		:returns: str
		"""

		return self.ship_company

	def get_ship_address1(self) -> str:
		"""
		Get ShipAddress1.

		:returns: str
		"""

		return self.ship_address1

	def get_ship_address2(self) -> str:
		"""
		Get ShipAddress2.

		:returns: str
		"""

		return self.ship_address2

	def get_ship_city(self) -> str:
		"""
		Get ShipCity.

		:returns: str
		"""

		return self.ship_city

	def get_ship_state(self) -> str:
		"""
		Get ShipState.

		:returns: str
		"""

		return self.ship_state

	def get_ship_zip(self) -> str:
		"""
		Get ShipZip.

		:returns: str
		"""

		return self.ship_zip

	def get_ship_country(self) -> str:
		"""
		Get ShipCountry.

		:returns: str
		"""

		return self.ship_country

	def get_ship_residential(self) -> bool:
		"""
		Get ShipResidential.

		:returns: bool
		"""

		return self.ship_residential

	def get_bill_first_name(self) -> str:
		"""
		Get BillFirstName.

		:returns: str
		"""

		return self.bill_first_name

	def get_bill_last_name(self) -> str:
		"""
		Get BillLastName.

		:returns: str
		"""

		return self.bill_last_name

	def get_bill_email(self) -> str:
		"""
		Get BillEmail.

		:returns: str
		"""

		return self.bill_email

	def get_bill_phone(self) -> str:
		"""
		Get BillPhone.

		:returns: str
		"""

		return self.bill_phone

	def get_bill_fax(self) -> str:
		"""
		Get BillFax.

		:returns: str
		"""

		return self.bill_fax

	def get_bill_company(self) -> str:
		"""
		Get BillCompany.

		:returns: str
		"""

		return self.bill_company

	def get_bill_address1(self) -> str:
		"""
		Get BillAddress1.

		:returns: str
		"""

		return self.bill_address1

	def get_bill_address2(self) -> str:
		"""
		Get BillAddress2.

		:returns: str
		"""

		return self.bill_address2

	def get_bill_city(self) -> str:
		"""
		Get BillCity.

		:returns: str
		"""

		return self.bill_city

	def get_bill_state(self) -> str:
		"""
		Get BillState.

		:returns: str
		"""

		return self.bill_state

	def get_bill_zip(self) -> str:
		"""
		Get BillZip.

		:returns: str
		"""

		return self.bill_zip

	def get_bill_country(self) -> str:
		"""
		Get BillCountry.

		:returns: str
		"""

		return self.bill_country

	def get_items(self) -> list:
		"""
		Get Items.

		:returns: List of OrderItem
		"""

		return self.items

	def get_products(self) -> list:
		"""
		Get Products.

		:returns: List of OrderProduct
		"""

		return self.products

	def get_charges(self) -> list:
		"""
		Get Charges.

		:returns: List of OrderCharge
		"""

		return self.charges

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def get_shipping_module_code(self) -> str:
		"""
		Get Shipping_Module_Code.

		:returns: str
		"""

		return self.shipping_module_code

	def get_shipping_module_data(self) -> str:
		"""
		Get Shipping_Module_Data.

		:returns: str
		"""

		return self.shipping_module_data

	def get_calculate_charges(self) -> bool:
		"""
		Get CalculateCharges.

		:returns: bool
		"""

		return self.calculate_charges

	def get_trigger_fulfillment_modules(self) -> bool:
		"""
		Get TriggerFulfillmentModules.

		:returns: bool
		"""

		return self.trigger_fulfillment_modules

	def set_customer_login(self, customer_login: str) -> 'OrderCreate':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: OrderCreate
		"""

		self.customer_login = customer_login
		return self

	def set_customer_id(self, customer_id: int) -> 'OrderCreate':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: OrderCreate
		"""

		self.customer_id = customer_id
		return self

	def set_ship_first_name(self, ship_first_name: str) -> 'OrderCreate':
		"""
		Set ShipFirstName.

		:param ship_first_name: str
		:returns: OrderCreate
		"""

		self.ship_first_name = ship_first_name
		return self

	def set_ship_last_name(self, ship_last_name: str) -> 'OrderCreate':
		"""
		Set ShipLastName.

		:param ship_last_name: str
		:returns: OrderCreate
		"""

		self.ship_last_name = ship_last_name
		return self

	def set_ship_email(self, ship_email: str) -> 'OrderCreate':
		"""
		Set ShipEmail.

		:param ship_email: str
		:returns: OrderCreate
		"""

		self.ship_email = ship_email
		return self

	def set_ship_phone(self, ship_phone: str) -> 'OrderCreate':
		"""
		Set ShipPhone.

		:param ship_phone: str
		:returns: OrderCreate
		"""

		self.ship_phone = ship_phone
		return self

	def set_ship_fax(self, ship_fax: str) -> 'OrderCreate':
		"""
		Set ShipFax.

		:param ship_fax: str
		:returns: OrderCreate
		"""

		self.ship_fax = ship_fax
		return self

	def set_ship_company(self, ship_company: str) -> 'OrderCreate':
		"""
		Set ShipCompany.

		:param ship_company: str
		:returns: OrderCreate
		"""

		self.ship_company = ship_company
		return self

	def set_ship_address1(self, ship_address1: str) -> 'OrderCreate':
		"""
		Set ShipAddress1.

		:param ship_address1: str
		:returns: OrderCreate
		"""

		self.ship_address1 = ship_address1
		return self

	def set_ship_address2(self, ship_address2: str) -> 'OrderCreate':
		"""
		Set ShipAddress2.

		:param ship_address2: str
		:returns: OrderCreate
		"""

		self.ship_address2 = ship_address2
		return self

	def set_ship_city(self, ship_city: str) -> 'OrderCreate':
		"""
		Set ShipCity.

		:param ship_city: str
		:returns: OrderCreate
		"""

		self.ship_city = ship_city
		return self

	def set_ship_state(self, ship_state: str) -> 'OrderCreate':
		"""
		Set ShipState.

		:param ship_state: str
		:returns: OrderCreate
		"""

		self.ship_state = ship_state
		return self

	def set_ship_zip(self, ship_zip: str) -> 'OrderCreate':
		"""
		Set ShipZip.

		:param ship_zip: str
		:returns: OrderCreate
		"""

		self.ship_zip = ship_zip
		return self

	def set_ship_country(self, ship_country: str) -> 'OrderCreate':
		"""
		Set ShipCountry.

		:param ship_country: str
		:returns: OrderCreate
		"""

		self.ship_country = ship_country
		return self

	def set_ship_residential(self, ship_residential: bool) -> 'OrderCreate':
		"""
		Set ShipResidential.

		:param ship_residential: bool
		:returns: OrderCreate
		"""

		self.ship_residential = ship_residential
		return self

	def set_bill_first_name(self, bill_first_name: str) -> 'OrderCreate':
		"""
		Set BillFirstName.

		:param bill_first_name: str
		:returns: OrderCreate
		"""

		self.bill_first_name = bill_first_name
		return self

	def set_bill_last_name(self, bill_last_name: str) -> 'OrderCreate':
		"""
		Set BillLastName.

		:param bill_last_name: str
		:returns: OrderCreate
		"""

		self.bill_last_name = bill_last_name
		return self

	def set_bill_email(self, bill_email: str) -> 'OrderCreate':
		"""
		Set BillEmail.

		:param bill_email: str
		:returns: OrderCreate
		"""

		self.bill_email = bill_email
		return self

	def set_bill_phone(self, bill_phone: str) -> 'OrderCreate':
		"""
		Set BillPhone.

		:param bill_phone: str
		:returns: OrderCreate
		"""

		self.bill_phone = bill_phone
		return self

	def set_bill_fax(self, bill_fax: str) -> 'OrderCreate':
		"""
		Set BillFax.

		:param bill_fax: str
		:returns: OrderCreate
		"""

		self.bill_fax = bill_fax
		return self

	def set_bill_company(self, bill_company: str) -> 'OrderCreate':
		"""
		Set BillCompany.

		:param bill_company: str
		:returns: OrderCreate
		"""

		self.bill_company = bill_company
		return self

	def set_bill_address1(self, bill_address1: str) -> 'OrderCreate':
		"""
		Set BillAddress1.

		:param bill_address1: str
		:returns: OrderCreate
		"""

		self.bill_address1 = bill_address1
		return self

	def set_bill_address2(self, bill_address2: str) -> 'OrderCreate':
		"""
		Set BillAddress2.

		:param bill_address2: str
		:returns: OrderCreate
		"""

		self.bill_address2 = bill_address2
		return self

	def set_bill_city(self, bill_city: str) -> 'OrderCreate':
		"""
		Set BillCity.

		:param bill_city: str
		:returns: OrderCreate
		"""

		self.bill_city = bill_city
		return self

	def set_bill_state(self, bill_state: str) -> 'OrderCreate':
		"""
		Set BillState.

		:param bill_state: str
		:returns: OrderCreate
		"""

		self.bill_state = bill_state
		return self

	def set_bill_zip(self, bill_zip: str) -> 'OrderCreate':
		"""
		Set BillZip.

		:param bill_zip: str
		:returns: OrderCreate
		"""

		self.bill_zip = bill_zip
		return self

	def set_bill_country(self, bill_country: str) -> 'OrderCreate':
		"""
		Set BillCountry.

		:param bill_country: str
		:returns: OrderCreate
		"""

		self.bill_country = bill_country
		return self

	def set_items(self, items: list) -> 'OrderCreate':
		"""
		Set Items.

		:param items: {OrderItem[]}
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in items:
			if not isinstance(e, merchantapi.model.OrderItem):
				raise Exception("")
		self.items = items
		return self

	def set_products(self, products: list) -> 'OrderCreate':
		"""
		Set Products.

		:param products: {OrderProduct[]}
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in products:
			if not isinstance(e, merchantapi.model.OrderProduct):
				raise Exception("")
		self.products = products
		return self

	def set_charges(self, charges: list) -> 'OrderCreate':
		"""
		Set Charges.

		:param charges: {OrderCharge[]}
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in charges:
			if not isinstance(e, merchantapi.model.OrderCharge):
				raise Exception("")
		self.charges = charges
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'OrderCreate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: OrderCreate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	def set_shipping_module_code(self, shipping_module_code: str) -> 'OrderCreate':
		"""
		Set Shipping_Module_Code.

		:param shipping_module_code: str
		:returns: OrderCreate
		"""

		self.shipping_module_code = shipping_module_code
		return self

	def set_shipping_module_data(self, shipping_module_data: str) -> 'OrderCreate':
		"""
		Set Shipping_Module_Data.

		:param shipping_module_data: str
		:returns: OrderCreate
		"""

		self.shipping_module_data = shipping_module_data
		return self

	def set_calculate_charges(self, calculate_charges: bool) -> 'OrderCreate':
		"""
		Set CalculateCharges.

		:param calculate_charges: bool
		:returns: OrderCreate
		"""

		self.calculate_charges = calculate_charges
		return self

	def set_trigger_fulfillment_modules(self, trigger_fulfillment_modules: bool) -> 'OrderCreate':
		"""
		Set TriggerFulfillmentModules.

		:param trigger_fulfillment_modules: bool
		:returns: OrderCreate
		"""

		self.trigger_fulfillment_modules = trigger_fulfillment_modules
		return self
	
	def add_item(self, item) -> 'OrderCreate':
		"""
		Add Items.

		:param item: OrderItem 
		:raises Exception:
		:returns: {OrderCreate}
		"""

		if isinstance(item, merchantapi.model.OrderItem):
			self.items.append(item)
		elif isinstance(item, dict):
			self.items.append(merchantapi.model.OrderItem(item))
		else:
			raise Exception('Expected instance of OrderItem or dict')
		return self

	def add_items(self, items: list) -> 'OrderCreate':
		"""
		Add many OrderItem.

		:param items: List of OrderItem
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in items:
			if not isinstance(e, merchantapi.model.OrderItem):
				raise Exception('')
			self.items.append(e)

		return self
	
	def add_product(self, product) -> 'OrderCreate':
		"""
		Add Products.

		:param product: OrderProduct 
		:raises Exception:
		:returns: {OrderCreate}
		"""

		if isinstance(product, merchantapi.model.OrderProduct):
			self.products.append(product)
		elif isinstance(product, dict):
			self.products.append(merchantapi.model.OrderProduct(product))
		else:
			raise Exception('Expected instance of OrderProduct or dict')
		return self

	def add_products(self, products: list) -> 'OrderCreate':
		"""
		Add many OrderProduct.

		:param products: List of OrderProduct
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in products:
			if not isinstance(e, merchantapi.model.OrderProduct):
				raise Exception('')
			self.products.append(e)

		return self
	
	def add_charge(self, charge) -> 'OrderCreate':
		"""
		Add Charges.

		:param charge: OrderCharge 
		:raises Exception:
		:returns: {OrderCreate}
		"""

		if isinstance(charge, merchantapi.model.OrderCharge):
			self.charges.append(charge)
		elif isinstance(charge, dict):
			self.charges.append(merchantapi.model.OrderCharge(charge))
		else:
			raise Exception('Expected instance of OrderCharge or dict')
		return self

	def add_charges(self, charges: list) -> 'OrderCreate':
		"""
		Add many OrderCharge.

		:param charges: List of OrderCharge
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in charges:
			if not isinstance(e, merchantapi.model.OrderCharge):
				raise Exception('')
			self.charges.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCreate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCreate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCreate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.ship_first_name is not None:
			data['ShipFirstName'] = self.ship_first_name
		if self.ship_last_name is not None:
			data['ShipLastName'] = self.ship_last_name
		if self.ship_email is not None:
			data['ShipEmail'] = self.ship_email
		if self.ship_phone is not None:
			data['ShipPhone'] = self.ship_phone
		if self.ship_fax is not None:
			data['ShipFax'] = self.ship_fax
		if self.ship_company is not None:
			data['ShipCompany'] = self.ship_company
		if self.ship_address1 is not None:
			data['ShipAddress1'] = self.ship_address1
		if self.ship_address2 is not None:
			data['ShipAddress2'] = self.ship_address2
		if self.ship_city is not None:
			data['ShipCity'] = self.ship_city
		if self.ship_state is not None:
			data['ShipState'] = self.ship_state
		if self.ship_zip is not None:
			data['ShipZip'] = self.ship_zip
		if self.ship_country is not None:
			data['ShipCountry'] = self.ship_country
		if self.ship_residential is not None:
			data['ShipResidential'] = self.ship_residential
		if self.bill_first_name is not None:
			data['BillFirstName'] = self.bill_first_name
		if self.bill_last_name is not None:
			data['BillLastName'] = self.bill_last_name
		if self.bill_email is not None:
			data['BillEmail'] = self.bill_email
		if self.bill_phone is not None:
			data['BillPhone'] = self.bill_phone
		if self.bill_fax is not None:
			data['BillFax'] = self.bill_fax
		if self.bill_company is not None:
			data['BillCompany'] = self.bill_company
		if self.bill_address1 is not None:
			data['BillAddress1'] = self.bill_address1
		if self.bill_address2 is not None:
			data['BillAddress2'] = self.bill_address2
		if self.bill_city is not None:
			data['BillCity'] = self.bill_city
		if self.bill_state is not None:
			data['BillState'] = self.bill_state
		if self.bill_zip is not None:
			data['BillZip'] = self.bill_zip
		if self.bill_country is not None:
			data['BillCountry'] = self.bill_country
		if len(self.items):
			data['Items'] = []

			for f in self.items:
				data['Items'].append(f.to_dict())
		if len(self.products):
			data['Products'] = []

			for f in self.products:
				data['Products'].append(f.to_dict())
		if len(self.charges):
			data['Charges'] = []

			for f in self.charges:
				data['Charges'].append(f.to_dict())
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		if self.shipping_module_code is not None:
			data['Shipping_Module_Code'] = self.shipping_module_code
		if self.shipping_module_data is not None:
			data['Shipping_Module_Data'] = self.shipping_module_data
		if self.calculate_charges is not None:
			data['CalculateCharges'] = self.calculate_charges
		if self.trigger_fulfillment_modules is not None:
			data['TriggerFulfillmentModules'] = self.trigger_fulfillment_modules
		return data


"""
Handles API Request Order_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_delete
"""


class OrderDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderDelete Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Delete'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def set_order_id(self, order_id: int) -> 'OrderDelete':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderDelete
		"""

		self.order_id = order_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.order_id
		return data


"""
Handles API Request Order_Update_Customer_Information. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_update_customer_information
"""


class OrderUpdateCustomerInformation(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderUpdateCustomerInformation Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.customer_id = None
		self.ship_residential = False
		self.ship_first_name = None
		self.ship_last_name = None
		self.ship_email = None
		self.ship_phone = None
		self.ship_fax = None
		self.ship_company = None
		self.ship_address1 = None
		self.ship_address2 = None
		self.ship_city = None
		self.ship_state = None
		self.ship_zip = None
		self.ship_country = None
		self.bill_first_name = None
		self.bill_last_name = None
		self.bill_email = None
		self.bill_phone = None
		self.bill_fax = None
		self.bill_company = None
		self.bill_address1 = None
		self.bill_address2 = None
		self.bill_city = None
		self.bill_state = None
		self.bill_zip = None
		self.bill_country = None
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Update_Customer_Information'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_ship_residential(self) -> bool:
		"""
		Get Ship_Residential.

		:returns: bool
		"""

		return self.ship_residential

	def get_ship_first_name(self) -> str:
		"""
		Get Ship_FirstName.

		:returns: str
		"""

		return self.ship_first_name

	def get_ship_last_name(self) -> str:
		"""
		Get Ship_LastName.

		:returns: str
		"""

		return self.ship_last_name

	def get_ship_email(self) -> str:
		"""
		Get Ship_Email.

		:returns: str
		"""

		return self.ship_email

	def get_ship_phone(self) -> str:
		"""
		Get Ship_Phone.

		:returns: str
		"""

		return self.ship_phone

	def get_ship_fax(self) -> str:
		"""
		Get Ship_Fax.

		:returns: str
		"""

		return self.ship_fax

	def get_ship_company(self) -> str:
		"""
		Get Ship_Company.

		:returns: str
		"""

		return self.ship_company

	def get_ship_address1(self) -> str:
		"""
		Get Ship_Address1.

		:returns: str
		"""

		return self.ship_address1

	def get_ship_address2(self) -> str:
		"""
		Get Ship_Address2.

		:returns: str
		"""

		return self.ship_address2

	def get_ship_city(self) -> str:
		"""
		Get Ship_City.

		:returns: str
		"""

		return self.ship_city

	def get_ship_state(self) -> str:
		"""
		Get Ship_State.

		:returns: str
		"""

		return self.ship_state

	def get_ship_zip(self) -> str:
		"""
		Get Ship_Zip.

		:returns: str
		"""

		return self.ship_zip

	def get_ship_country(self) -> str:
		"""
		Get Ship_Country.

		:returns: str
		"""

		return self.ship_country

	def get_bill_first_name(self) -> str:
		"""
		Get Bill_FirstName.

		:returns: str
		"""

		return self.bill_first_name

	def get_bill_last_name(self) -> str:
		"""
		Get Bill_LastName.

		:returns: str
		"""

		return self.bill_last_name

	def get_bill_email(self) -> str:
		"""
		Get Bill_Email.

		:returns: str
		"""

		return self.bill_email

	def get_bill_phone(self) -> str:
		"""
		Get Bill_Phone.

		:returns: str
		"""

		return self.bill_phone

	def get_bill_fax(self) -> str:
		"""
		Get Bill_Fax.

		:returns: str
		"""

		return self.bill_fax

	def get_bill_company(self) -> str:
		"""
		Get Bill_Company.

		:returns: str
		"""

		return self.bill_company

	def get_bill_address1(self) -> str:
		"""
		Get Bill_Address1.

		:returns: str
		"""

		return self.bill_address1

	def get_bill_address2(self) -> str:
		"""
		Get Bill_Address2.

		:returns: str
		"""

		return self.bill_address2

	def get_bill_city(self) -> str:
		"""
		Get Bill_City.

		:returns: str
		"""

		return self.bill_city

	def get_bill_state(self) -> str:
		"""
		Get Bill_State.

		:returns: str
		"""

		return self.bill_state

	def get_bill_zip(self) -> str:
		"""
		Get Bill_Zip.

		:returns: str
		"""

		return self.bill_zip

	def get_bill_country(self) -> str:
		"""
		Get Bill_Country.

		:returns: str
		"""

		return self.bill_country

	def set_order_id(self, order_id: int) -> 'OrderUpdateCustomerInformation':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderUpdateCustomerInformation
		"""

		self.order_id = order_id
		return self

	def set_customer_id(self, customer_id: int) -> 'OrderUpdateCustomerInformation':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: OrderUpdateCustomerInformation
		"""

		self.customer_id = customer_id
		return self

	def set_ship_residential(self, ship_residential: bool) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Residential.

		:param ship_residential: bool
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_residential = ship_residential
		return self

	def set_ship_first_name(self, ship_first_name: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_FirstName.

		:param ship_first_name: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_first_name = ship_first_name
		return self

	def set_ship_last_name(self, ship_last_name: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_LastName.

		:param ship_last_name: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_last_name = ship_last_name
		return self

	def set_ship_email(self, ship_email: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Email.

		:param ship_email: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_email = ship_email
		return self

	def set_ship_phone(self, ship_phone: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Phone.

		:param ship_phone: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_phone = ship_phone
		return self

	def set_ship_fax(self, ship_fax: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Fax.

		:param ship_fax: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_fax = ship_fax
		return self

	def set_ship_company(self, ship_company: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Company.

		:param ship_company: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_company = ship_company
		return self

	def set_ship_address1(self, ship_address1: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Address1.

		:param ship_address1: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_address1 = ship_address1
		return self

	def set_ship_address2(self, ship_address2: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Address2.

		:param ship_address2: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_address2 = ship_address2
		return self

	def set_ship_city(self, ship_city: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_City.

		:param ship_city: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_city = ship_city
		return self

	def set_ship_state(self, ship_state: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_State.

		:param ship_state: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_state = ship_state
		return self

	def set_ship_zip(self, ship_zip: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Zip.

		:param ship_zip: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_zip = ship_zip
		return self

	def set_ship_country(self, ship_country: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Country.

		:param ship_country: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_country = ship_country
		return self

	def set_bill_first_name(self, bill_first_name: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_FirstName.

		:param bill_first_name: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_first_name = bill_first_name
		return self

	def set_bill_last_name(self, bill_last_name: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_LastName.

		:param bill_last_name: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_last_name = bill_last_name
		return self

	def set_bill_email(self, bill_email: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Email.

		:param bill_email: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_email = bill_email
		return self

	def set_bill_phone(self, bill_phone: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Phone.

		:param bill_phone: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_phone = bill_phone
		return self

	def set_bill_fax(self, bill_fax: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Fax.

		:param bill_fax: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_fax = bill_fax
		return self

	def set_bill_company(self, bill_company: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Company.

		:param bill_company: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_company = bill_company
		return self

	def set_bill_address1(self, bill_address1: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Address1.

		:param bill_address1: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_address1 = bill_address1
		return self

	def set_bill_address2(self, bill_address2: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Address2.

		:param bill_address2: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_address2 = bill_address2
		return self

	def set_bill_city(self, bill_city: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_City.

		:param bill_city: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_city = bill_city
		return self

	def set_bill_state(self, bill_state: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_State.

		:param bill_state: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_state = bill_state
		return self

	def set_bill_zip(self, bill_zip: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Zip.

		:param bill_zip: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_zip = bill_zip
		return self

	def set_bill_country(self, bill_country: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Country.

		:param bill_country: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_country = bill_country
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderUpdateCustomerInformation':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderUpdateCustomerInformation':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderUpdateCustomerInformation(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.order_id
		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		if self.ship_residential is not None:
			data['Ship_Residential'] = self.ship_residential
		if self.ship_first_name is not None:
			data['Ship_FirstName'] = self.ship_first_name
		if self.ship_last_name is not None:
			data['Ship_LastName'] = self.ship_last_name
		if self.ship_email is not None:
			data['Ship_Email'] = self.ship_email
		if self.ship_phone is not None:
			data['Ship_Phone'] = self.ship_phone
		if self.ship_fax is not None:
			data['Ship_Fax'] = self.ship_fax
		if self.ship_company is not None:
			data['Ship_Company'] = self.ship_company
		if self.ship_address1 is not None:
			data['Ship_Address1'] = self.ship_address1
		if self.ship_address2 is not None:
			data['Ship_Address2'] = self.ship_address2
		if self.ship_city is not None:
			data['Ship_City'] = self.ship_city
		if self.ship_state is not None:
			data['Ship_State'] = self.ship_state
		if self.ship_zip is not None:
			data['Ship_Zip'] = self.ship_zip
		if self.ship_country is not None:
			data['Ship_Country'] = self.ship_country
		if self.bill_first_name is not None:
			data['Bill_FirstName'] = self.bill_first_name
		if self.bill_last_name is not None:
			data['Bill_LastName'] = self.bill_last_name
		if self.bill_email is not None:
			data['Bill_Email'] = self.bill_email
		if self.bill_phone is not None:
			data['Bill_Phone'] = self.bill_phone
		if self.bill_fax is not None:
			data['Bill_Fax'] = self.bill_fax
		if self.bill_company is not None:
			data['Bill_Company'] = self.bill_company
		if self.bill_address1 is not None:
			data['Bill_Address1'] = self.bill_address1
		if self.bill_address2 is not None:
			data['Bill_Address2'] = self.bill_address2
		if self.bill_city is not None:
			data['Bill_City'] = self.bill_city
		if self.bill_state is not None:
			data['Bill_State'] = self.bill_state
		if self.bill_zip is not None:
			data['Bill_Zip'] = self.bill_zip
		if self.bill_country is not None:
			data['Bill_Country'] = self.bill_country
		return data


"""
Handles API Request PriceGroupCustomer_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupcustomer_update_assigned
"""


class PriceGroupCustomerUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupCustomerUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.price_group_name = None
		self.edit_customer = None
		self.customer_id = None
		self.customer_login = None
		self.assigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())
			elif price_group.get_name():
				self.set_price_group_name(price_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupCustomer_Update_Assigned'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_edit_customer(self, edit_customer: str) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_id(self, customer_id: int) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.customer_login = customer_login
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupCustomerUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupCustomerUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request PriceGroupList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegrouplist_load_query
"""


class PriceGroupListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'name',
		'type',
		'module_id',
		'custscope',
		'rate',
		'discount',
		'markup',
		'dt_start',
		'dt_end',
		'priority',
		'exclusion',
		'descrip',
		'display',
		'qmn_subtot',
		'qmx_subtot',
		'qmn_quan',
		'qmx_quan',
		'qmn_weight',
		'qmx_weight',
		'bmn_subtot',
		'bmx_subtot',
		'bmn_quan',
		'bmx_quan',
		'bmn_weight',
		'bmx_weight'
	]

	available_sort_fields = [
		'id',
		'name',
		'type',
		'module_id',
		'custscope',
		'rate',
		'discount',
		'markup',
		'dt_start',
		'dt_end',
		'priority',
		'exclusion',
		'descrip',
		'display',
		'qmn_subtot',
		'qmx_subtot',
		'qmn_quan',
		'qmx_quan',
		'qmn_weight',
		'qmx_weight',
		'bmn_subtot',
		'bmx_subtot',
		'bmn_quan',
		'bmx_quan',
		'bmn_weight',
		'bmx_weight'
	]

	def __init__(self, client: Client = None):
		"""
		PriceGroupListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupListLoadQuery(self, http_response, data)


"""
Handles API Request PriceGroupProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupproduct_update_assigned
"""


class PriceGroupProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupProductUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.price_group_name = None
		self.edit_product = None
		self.product_id = None
		self.product_code = None
		self.product_sku = None
		self.assigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())
			elif price_group.get_name():
				self.set_price_group_name(price_group.get_name())

			self.set_price_group_name(price_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupProduct_Update_Assigned'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupProductUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupProductUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupProductUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupProductUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_edit_product(self, edit_product: str) -> 'PriceGroupProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: PriceGroupProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_product_id(self, product_id: int) -> 'PriceGroupProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: PriceGroupProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'PriceGroupProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: PriceGroupProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'PriceGroupProductUpdateAssigned':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: PriceGroupProductUpdateAssigned
		"""

		self.product_sku = product_sku
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupProductUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		if self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request ProductImage_Add. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productimage_add
"""


class ProductImageAdd(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductImageAdd Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_code = None
		self.product_id = None
		self.edit_product = None
		self.product_sku = None
		self.filepath = None
		self.image_type_id = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())
			elif product.get_sku():
				self.set_product_sku(product.get_sku())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductImage_Add'

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_filepath(self) -> str:
		"""
		Get Filepath.

		:returns: str
		"""

		return self.filepath

	def get_image_type_id(self) -> int:
		"""
		Get ImageType_ID.

		:returns: int
		"""

		return self.image_type_id

	def set_product_code(self, product_code: str) -> 'ProductImageAdd':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductImageAdd
		"""

		self.product_code = product_code
		return self

	def set_product_id(self, product_id: int) -> 'ProductImageAdd':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductImageAdd
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductImageAdd':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductImageAdd
		"""

		self.edit_product = edit_product
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductImageAdd':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductImageAdd
		"""

		self.product_sku = product_sku
		return self

	def set_filepath(self, filepath: str) -> 'ProductImageAdd':
		"""
		Set Filepath.

		:param filepath: str
		:returns: ProductImageAdd
		"""

		self.filepath = filepath
		return self

	def set_image_type_id(self, image_type_id: int) -> 'ProductImageAdd':
		"""
		Set ImageType_ID.

		:param image_type_id: int
		:returns: ProductImageAdd
		"""

		self.image_type_id = image_type_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductImageAdd':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductImageAdd':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductImageAdd(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		data['Filepath'] = self.filepath
		data['ImageType_ID'] = self.image_type_id
		return data


"""
Handles API Request ProductImage_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productimage_delete
"""


class ProductImageDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_image_data: merchantapi.model.ProductImageData = None):
		"""
		ProductImageDelete Constructor.

		:param client: Client
		:param product_image_data: ProductImageData
		"""

		super().__init__(client)
		self.product_image_id = None
		if isinstance(product_image_data, merchantapi.model.ProductImageData):
			self.set_product_image_id(product_image_data.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductImage_Delete'

	def get_product_image_id(self) -> int:
		"""
		Get ProductImage_ID.

		:returns: int
		"""

		return self.product_image_id

	def set_product_image_id(self, product_image_id: int) -> 'ProductImageDelete':
		"""
		Set ProductImage_ID.

		:param product_image_id: int
		:returns: ProductImageDelete
		"""

		self.product_image_id = product_image_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductImageDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductImageDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductImageDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['ProductImage_ID'] = self.product_image_id
		return data


"""
Handles API Request ProductList_Adjust_Inventory. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productlist_adjust_inventory
"""


class ProductListAdjustInventory(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProductListAdjustInventory Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.inventory_adjustments = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductList_Adjust_Inventory'

	def get_inventory_adjustments(self) -> list:
		"""
		Get Inventory_Adjustments.

		:returns: List of ProductInventoryAdjustment
		"""

		return self.inventory_adjustments

	def set_inventory_adjustments(self, inventory_adjustments: list) -> 'ProductListAdjustInventory':
		"""
		Set Inventory_Adjustments.

		:param inventory_adjustments: {ProductInventoryAdjustment[]}
		:raises Exception:
		:returns: ProductListAdjustInventory
		"""

		for e in inventory_adjustments:
			if not isinstance(e, merchantapi.model.ProductInventoryAdjustment):
				raise Exception("")
		self.inventory_adjustments = inventory_adjustments
		return self
	
	def add_inventory_adjustment(self, inventory_adjustment) -> 'ProductListAdjustInventory':
		"""
		Add Inventory_Adjustments.

		:param inventory_adjustment: ProductInventoryAdjustment 
		:raises Exception:
		:returns: {ProductListAdjustInventory}
		"""

		if isinstance(inventory_adjustment, merchantapi.model.ProductInventoryAdjustment):
			self.inventory_adjustments.append(inventory_adjustment)
		elif isinstance(inventory_adjustment, dict):
			self.inventory_adjustments.append(merchantapi.model.ProductInventoryAdjustment(inventory_adjustment))
		else:
			raise Exception('Expected instance of ProductInventoryAdjustment or dict')
		return self

	def add_inventory_adjustments(self, inventory_adjustments: list) -> 'ProductListAdjustInventory':
		"""
		Add many ProductInventoryAdjustment.

		:param inventory_adjustments: List of ProductInventoryAdjustment
		:raises Exception:
		:returns: ProductListAdjustInventory
		"""

		for e in inventory_adjustments:
			if not isinstance(e, merchantapi.model.ProductInventoryAdjustment):
				raise Exception('')
			self.inventory_adjustments.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductListAdjustInventory':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductListAdjustInventory':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductListAdjustInventory(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if len(self.inventory_adjustments):
			data['Inventory_Adjustments'] = []

			for f in self.inventory_adjustments:
				data['Inventory_Adjustments'].append(f.to_dict())
		return data


"""
Handles API Request ProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productlist_load_query
"""


class ProductListLoadQuery(ListQueryRequest):
	# PRODUCT_SHOW constants.
	PRODUCT_SHOW_ALL = 'All'
	PRODUCT_SHOW_UNCATEGORIZED = 'Uncategorized'
	PRODUCT_SHOW_ACTIVE = 'Active'

	available_search_fields = [
		'id',
		'code',
		'sku',
		'cancat_code',
		'page_code',
		'name',
		'thumbnail',
		'image',
		'price',
		'cost',
		'descrip',
		'weight',
		'taxable',
		'active',
		'page_title',
		'dt_created',
		'dt_updated',
		'category',
		'product_inventory'
	]

	available_sort_fields = [
		'id',
		'code',
		'sku',
		'cancat_code',
		'page_code',
		'name',
		'thumbnail',
		'image',
		'price',
		'cost',
		'descrip',
		'weight',
		'taxable',
		'active',
		'page_title',
		'dt_created',
		'dt_updated'
	]

	available_on_demand_columns = [
		'descrip',
		'catcount',
		'cancat_code',
		'page_code',
		'product_inventory',
		'productinventorysettings',
		'attributes',
		'productimagedata',
		'categories',
		'productshippingrules',
		'relatedproducts',
		'uris'
	]

	available_custom_filters = {
		'Product_Show': [
			PRODUCT_SHOW_ALL,
			PRODUCT_SHOW_UNCATEGORIZED,
			PRODUCT_SHOW_ACTIVE
		]
	}

	def __init__(self, client: Client = None):
		"""
		ProductListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductListLoadQuery(self, http_response, data)


"""
Handles API Request ProductVariantList_Load_Product. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariantlist_load_product
"""


class ProductVariantListLoadProduct(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantListLoadProduct Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.product_sku = None
		self.include_default_variant = False
		self.limits = []
		self.exclusions = []
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())
			elif product.get_sku():
				self.set_product_sku(product.get_sku())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariantList_Load_Product'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_include_default_variant(self) -> bool:
		"""
		Get Include_Default_Variant.

		:returns: bool
		"""

		return self.include_default_variant

	def get_limits(self) -> list:
		"""
		Get Limits.

		:returns: List of ProductVariantLimit
		"""

		return self.limits

	def get_exclusions(self) -> list:
		"""
		Get Exclusions.

		:returns: List of ProductVariantExclusion
		"""

		return self.exclusions

	def set_product_id(self, product_id: int) -> 'ProductVariantListLoadProduct':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantListLoadProduct
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantListLoadProduct':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantListLoadProduct
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantListLoadProduct':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantListLoadProduct
		"""

		self.edit_product = edit_product
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductVariantListLoadProduct':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductVariantListLoadProduct
		"""

		self.product_sku = product_sku
		return self

	def set_include_default_variant(self, include_default_variant: bool) -> 'ProductVariantListLoadProduct':
		"""
		Set Include_Default_Variant.

		:param include_default_variant: bool
		:returns: ProductVariantListLoadProduct
		"""

		self.include_default_variant = include_default_variant
		return self

	def set_limits(self, limits: list) -> 'ProductVariantListLoadProduct':
		"""
		Set Limits.

		:param limits: {ProductVariantLimit[]}
		:raises Exception:
		:returns: ProductVariantListLoadProduct
		"""

		for e in limits:
			if not isinstance(e, merchantapi.model.ProductVariantLimit):
				raise Exception("")
		self.limits = limits
		return self

	def set_exclusions(self, exclusions: list) -> 'ProductVariantListLoadProduct':
		"""
		Set Exclusions.

		:param exclusions: {ProductVariantExclusion[]}
		:raises Exception:
		:returns: ProductVariantListLoadProduct
		"""

		for e in exclusions:
			if not isinstance(e, merchantapi.model.ProductVariantExclusion):
				raise Exception("")
		self.exclusions = exclusions
		return self
	
	def add_limit(self, limit) -> 'ProductVariantListLoadProduct':
		"""
		Add Limits.

		:param limit: ProductVariantLimit 
		:raises Exception:
		:returns: {ProductVariantListLoadProduct}
		"""

		if isinstance(limit, merchantapi.model.ProductVariantLimit):
			self.limits.append(limit)
		elif isinstance(limit, dict):
			self.limits.append(merchantapi.model.ProductVariantLimit(limit))
		else:
			raise Exception('Expected instance of ProductVariantLimit or dict')
		return self

	def add_limits(self, limits: list) -> 'ProductVariantListLoadProduct':
		"""
		Add many ProductVariantLimit.

		:param limits: List of ProductVariantLimit
		:raises Exception:
		:returns: ProductVariantListLoadProduct
		"""

		for e in limits:
			if not isinstance(e, merchantapi.model.ProductVariantLimit):
				raise Exception('')
			self.limits.append(e)

		return self
	
	def add_exclusion(self, exclusion) -> 'ProductVariantListLoadProduct':
		"""
		Add Exclusions.

		:param exclusion: ProductVariantExclusion 
		:raises Exception:
		:returns: {ProductVariantListLoadProduct}
		"""

		if isinstance(exclusion, merchantapi.model.ProductVariantExclusion):
			self.exclusions.append(exclusion)
		elif isinstance(exclusion, dict):
			self.exclusions.append(merchantapi.model.ProductVariantExclusion(exclusion))
		else:
			raise Exception('Expected instance of ProductVariantExclusion or dict')
		return self

	def add_exclusions(self, exclusions: list) -> 'ProductVariantListLoadProduct':
		"""
		Add many ProductVariantExclusion.

		:param exclusions: List of ProductVariantExclusion
		:raises Exception:
		:returns: ProductVariantListLoadProduct
		"""

		for e in exclusions:
			if not isinstance(e, merchantapi.model.ProductVariantExclusion):
				raise Exception('')
			self.exclusions.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantListLoadProduct':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantListLoadProduct':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantListLoadProduct(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		if self.include_default_variant is not None:
			data['Include_Default_Variant'] = self.include_default_variant
		if len(self.limits):
			data['Limits'] = []

			for f in self.limits:
				data['Limits'].append(f.to_dict())
		if len(self.exclusions):
			data['Exclusions'] = []

			for f in self.exclusions:
				data['Exclusions'].append(f.to_dict())
		return data


"""
Handles API Request Product_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/product_insert
"""


class ProductInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductInsert Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_code = None
		self.product_sku = None
		self.product_name = None
		self.product_description = None
		self.product_canonical_category_code = None
		self.product_alternate_display_page = None
		self.product_page_title = None
		self.product_thumbnail = None
		self.product_image = None
		self.product_price = None
		self.product_cost = None
		self.product_weight = None
		self.product_inventory = None
		self.product_taxable = False
		self.product_active = False
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(product, merchantapi.model.Product):
			self.set_product_code(product.get_code())
			self.set_product_sku(product.get_sku())
			self.set_product_name(product.get_name())
			self.set_product_description(product.get_description())
			self.set_product_canonical_category_code(product.get_canonical_category_code())
			self.set_product_alternate_display_page(product.get_page_code())
			self.set_product_page_title(product.get_page_title())
			self.set_product_thumbnail(product.get_thumbnail())
			self.set_product_image(product.get_image())
			self.set_product_price(product.get_price())
			self.set_product_cost(product.get_cost())
			self.set_product_weight(product.get_weight())
			self.set_product_inventory(product.get_product_inventory())
			self.set_product_taxable(product.get_taxable())
			self.set_product_active(product.get_active())

			if product.get_custom_field_values():
				self.set_custom_field_values(product.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Product_Insert'

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_product_name(self) -> str:
		"""
		Get Product_Name.

		:returns: str
		"""

		return self.product_name

	def get_product_description(self) -> str:
		"""
		Get Product_Description.

		:returns: str
		"""

		return self.product_description

	def get_product_canonical_category_code(self) -> str:
		"""
		Get Product_Canonical_Category_Code.

		:returns: str
		"""

		return self.product_canonical_category_code

	def get_product_alternate_display_page(self) -> str:
		"""
		Get Product_Alternate_Display_Page.

		:returns: str
		"""

		return self.product_alternate_display_page

	def get_product_page_title(self) -> str:
		"""
		Get Product_Page_Title.

		:returns: str
		"""

		return self.product_page_title

	def get_product_thumbnail(self) -> str:
		"""
		Get Product_Thumbnail.

		:returns: str
		"""

		return self.product_thumbnail

	def get_product_image(self) -> str:
		"""
		Get Product_Image.

		:returns: str
		"""

		return self.product_image

	def get_product_price(self) -> float:
		"""
		Get Product_Price.

		:returns: float
		"""

		return self.product_price

	def get_product_cost(self) -> float:
		"""
		Get Product_Cost.

		:returns: float
		"""

		return self.product_cost

	def get_product_weight(self) -> float:
		"""
		Get Product_Weight.

		:returns: float
		"""

		return self.product_weight

	def get_product_inventory(self) -> int:
		"""
		Get Product_Inventory.

		:returns: int
		"""

		return self.product_inventory

	def get_product_taxable(self) -> bool:
		"""
		Get Product_Taxable.

		:returns: bool
		"""

		return self.product_taxable

	def get_product_active(self) -> bool:
		"""
		Get Product_Active.

		:returns: bool
		"""

		return self.product_active

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_product_code(self, product_code: str) -> 'ProductInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductInsert
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductInsert':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductInsert
		"""

		self.product_sku = product_sku
		return self

	def set_product_name(self, product_name: str) -> 'ProductInsert':
		"""
		Set Product_Name.

		:param product_name: str
		:returns: ProductInsert
		"""

		self.product_name = product_name
		return self

	def set_product_description(self, product_description: str) -> 'ProductInsert':
		"""
		Set Product_Description.

		:param product_description: str
		:returns: ProductInsert
		"""

		self.product_description = product_description
		return self

	def set_product_canonical_category_code(self, product_canonical_category_code: str) -> 'ProductInsert':
		"""
		Set Product_Canonical_Category_Code.

		:param product_canonical_category_code: str
		:returns: ProductInsert
		"""

		self.product_canonical_category_code = product_canonical_category_code
		return self

	def set_product_alternate_display_page(self, product_alternate_display_page: str) -> 'ProductInsert':
		"""
		Set Product_Alternate_Display_Page.

		:param product_alternate_display_page: str
		:returns: ProductInsert
		"""

		self.product_alternate_display_page = product_alternate_display_page
		return self

	def set_product_page_title(self, product_page_title: str) -> 'ProductInsert':
		"""
		Set Product_Page_Title.

		:param product_page_title: str
		:returns: ProductInsert
		"""

		self.product_page_title = product_page_title
		return self

	def set_product_thumbnail(self, product_thumbnail: str) -> 'ProductInsert':
		"""
		Set Product_Thumbnail.

		:param product_thumbnail: str
		:returns: ProductInsert
		"""

		self.product_thumbnail = product_thumbnail
		return self

	def set_product_image(self, product_image: str) -> 'ProductInsert':
		"""
		Set Product_Image.

		:param product_image: str
		:returns: ProductInsert
		"""

		self.product_image = product_image
		return self

	def set_product_price(self, product_price: float) -> 'ProductInsert':
		"""
		Set Product_Price.

		:param product_price: float
		:returns: ProductInsert
		"""

		self.product_price = product_price
		return self

	def set_product_cost(self, product_cost: float) -> 'ProductInsert':
		"""
		Set Product_Cost.

		:param product_cost: float
		:returns: ProductInsert
		"""

		self.product_cost = product_cost
		return self

	def set_product_weight(self, product_weight: float) -> 'ProductInsert':
		"""
		Set Product_Weight.

		:param product_weight: float
		:returns: ProductInsert
		"""

		self.product_weight = product_weight
		return self

	def set_product_inventory(self, product_inventory: int) -> 'ProductInsert':
		"""
		Set Product_Inventory.

		:param product_inventory: int
		:returns: ProductInsert
		"""

		self.product_inventory = product_inventory
		return self

	def set_product_taxable(self, product_taxable: bool) -> 'ProductInsert':
		"""
		Set Product_Taxable.

		:param product_taxable: bool
		:returns: ProductInsert
		"""

		self.product_taxable = product_taxable
		return self

	def set_product_active(self, product_active: bool) -> 'ProductInsert':
		"""
		Set Product_Active.

		:param product_active: bool
		:returns: ProductInsert
		"""

		self.product_active = product_active
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'ProductInsert':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: ProductInsert
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Product_Code'] = self.product_code
		data['Product_SKU'] = self.product_sku
		data['Product_Name'] = self.product_name
		if self.product_description is not None:
			data['Product_Description'] = self.product_description
		if self.product_canonical_category_code is not None:
			data['Product_Canonical_Category_Code'] = self.product_canonical_category_code
		if self.product_alternate_display_page is not None:
			data['Product_Alternate_Display_Page'] = self.product_alternate_display_page
		if self.product_page_title is not None:
			data['Product_Page_Title'] = self.product_page_title
		if self.product_thumbnail is not None:
			data['Product_Thumbnail'] = self.product_thumbnail
		if self.product_image is not None:
			data['Product_Image'] = self.product_image
		if self.product_price is not None:
			data['Product_Price'] = self.product_price
		if self.product_cost is not None:
			data['Product_Cost'] = self.product_cost
		if self.product_weight is not None:
			data['Product_Weight'] = self.product_weight
		if self.product_inventory is not None:
			data['Product_Inventory'] = self.product_inventory
		if self.product_taxable is not None:
			data['Product_Taxable'] = self.product_taxable
		if self.product_active is not None:
			data['Product_Active'] = self.product_active
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data


"""
Handles API Request Product_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/product_delete
"""


class ProductDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductDelete Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_code = None
		self.product_id = None
		self.edit_product = None
		self.product_sku = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())
			elif product.get_sku():
				self.set_product_sku(product.get_sku())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Product_Delete'

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def set_product_code(self, product_code: str) -> 'ProductDelete':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductDelete
		"""

		self.product_code = product_code
		return self

	def set_product_id(self, product_id: int) -> 'ProductDelete':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductDelete
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductDelete':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductDelete
		"""

		self.edit_product = edit_product
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductDelete':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductDelete
		"""

		self.product_sku = product_sku
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		return data


"""
Handles API Request Product_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/product_update
"""


class ProductUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductUpdate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.product_sku = None
		self.product_name = None
		self.product_description = None
		self.product_canonical_category_code = None
		self.product_alternate_display_page = None
		self.product_page_title = None
		self.product_thumbnail = None
		self.product_image = None
		self.product_price = None
		self.product_cost = None
		self.product_weight = None
		self.product_inventory = None
		self.product_taxable = False
		self.product_active = False
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

			self.set_product_code(product.get_code())
			self.set_product_sku(product.get_sku())
			self.set_product_name(product.get_name())
			self.set_product_description(product.get_description())
			self.set_product_canonical_category_code(product.get_canonical_category_code())
			self.set_product_alternate_display_page(product.get_page_code())
			self.set_product_page_title(product.get_page_title())
			self.set_product_thumbnail(product.get_thumbnail())
			self.set_product_image(product.get_image())
			self.set_product_price(product.get_price())
			self.set_product_cost(product.get_cost())
			self.set_product_weight(product.get_weight())
			self.set_product_inventory(product.get_product_inventory())
			self.set_product_taxable(product.get_taxable())
			self.set_product_active(product.get_active())

			if product.get_custom_field_values():
				self.set_custom_field_values(product.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Product_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_product_name(self) -> str:
		"""
		Get Product_Name.

		:returns: str
		"""

		return self.product_name

	def get_product_description(self) -> str:
		"""
		Get Product_Description.

		:returns: str
		"""

		return self.product_description

	def get_product_canonical_category_code(self) -> str:
		"""
		Get Product_Canonical_Category_Code.

		:returns: str
		"""

		return self.product_canonical_category_code

	def get_product_alternate_display_page(self) -> str:
		"""
		Get Product_Alternate_Display_Page.

		:returns: str
		"""

		return self.product_alternate_display_page

	def get_product_page_title(self) -> str:
		"""
		Get Product_Page_Title.

		:returns: str
		"""

		return self.product_page_title

	def get_product_thumbnail(self) -> str:
		"""
		Get Product_Thumbnail.

		:returns: str
		"""

		return self.product_thumbnail

	def get_product_image(self) -> str:
		"""
		Get Product_Image.

		:returns: str
		"""

		return self.product_image

	def get_product_price(self) -> float:
		"""
		Get Product_Price.

		:returns: float
		"""

		return self.product_price

	def get_product_cost(self) -> float:
		"""
		Get Product_Cost.

		:returns: float
		"""

		return self.product_cost

	def get_product_weight(self) -> float:
		"""
		Get Product_Weight.

		:returns: float
		"""

		return self.product_weight

	def get_product_inventory(self) -> int:
		"""
		Get Product_Inventory.

		:returns: int
		"""

		return self.product_inventory

	def get_product_taxable(self) -> bool:
		"""
		Get Product_Taxable.

		:returns: bool
		"""

		return self.product_taxable

	def get_product_active(self) -> bool:
		"""
		Get Product_Active.

		:returns: bool
		"""

		return self.product_active

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_product_id(self, product_id: int) -> 'ProductUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductUpdate':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductUpdate
		"""

		self.product_sku = product_sku
		return self

	def set_product_name(self, product_name: str) -> 'ProductUpdate':
		"""
		Set Product_Name.

		:param product_name: str
		:returns: ProductUpdate
		"""

		self.product_name = product_name
		return self

	def set_product_description(self, product_description: str) -> 'ProductUpdate':
		"""
		Set Product_Description.

		:param product_description: str
		:returns: ProductUpdate
		"""

		self.product_description = product_description
		return self

	def set_product_canonical_category_code(self, product_canonical_category_code: str) -> 'ProductUpdate':
		"""
		Set Product_Canonical_Category_Code.

		:param product_canonical_category_code: str
		:returns: ProductUpdate
		"""

		self.product_canonical_category_code = product_canonical_category_code
		return self

	def set_product_alternate_display_page(self, product_alternate_display_page: str) -> 'ProductUpdate':
		"""
		Set Product_Alternate_Display_Page.

		:param product_alternate_display_page: str
		:returns: ProductUpdate
		"""

		self.product_alternate_display_page = product_alternate_display_page
		return self

	def set_product_page_title(self, product_page_title: str) -> 'ProductUpdate':
		"""
		Set Product_Page_Title.

		:param product_page_title: str
		:returns: ProductUpdate
		"""

		self.product_page_title = product_page_title
		return self

	def set_product_thumbnail(self, product_thumbnail: str) -> 'ProductUpdate':
		"""
		Set Product_Thumbnail.

		:param product_thumbnail: str
		:returns: ProductUpdate
		"""

		self.product_thumbnail = product_thumbnail
		return self

	def set_product_image(self, product_image: str) -> 'ProductUpdate':
		"""
		Set Product_Image.

		:param product_image: str
		:returns: ProductUpdate
		"""

		self.product_image = product_image
		return self

	def set_product_price(self, product_price: float) -> 'ProductUpdate':
		"""
		Set Product_Price.

		:param product_price: float
		:returns: ProductUpdate
		"""

		self.product_price = product_price
		return self

	def set_product_cost(self, product_cost: float) -> 'ProductUpdate':
		"""
		Set Product_Cost.

		:param product_cost: float
		:returns: ProductUpdate
		"""

		self.product_cost = product_cost
		return self

	def set_product_weight(self, product_weight: float) -> 'ProductUpdate':
		"""
		Set Product_Weight.

		:param product_weight: float
		:returns: ProductUpdate
		"""

		self.product_weight = product_weight
		return self

	def set_product_inventory(self, product_inventory: int) -> 'ProductUpdate':
		"""
		Set Product_Inventory.

		:param product_inventory: int
		:returns: ProductUpdate
		"""

		self.product_inventory = product_inventory
		return self

	def set_product_taxable(self, product_taxable: bool) -> 'ProductUpdate':
		"""
		Set Product_Taxable.

		:param product_taxable: bool
		:returns: ProductUpdate
		"""

		self.product_taxable = product_taxable
		return self

	def set_product_active(self, product_active: bool) -> 'ProductUpdate':
		"""
		Set Product_Active.

		:param product_active: bool
		:returns: ProductUpdate
		"""

		self.product_active = product_active
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'ProductUpdate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: ProductUpdate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.product_code is not None:
			data['Product_Code'] = self.product_code
		if self.product_sku is not None:
			data['Product_SKU'] = self.product_sku
		if self.product_name is not None:
			data['Product_Name'] = self.product_name
		if self.product_description is not None:
			data['Product_Description'] = self.product_description
		if self.product_canonical_category_code is not None:
			data['Product_Canonical_Category_Code'] = self.product_canonical_category_code
		if self.product_alternate_display_page is not None:
			data['Product_Alternate_Display_Page'] = self.product_alternate_display_page
		if self.product_page_title is not None:
			data['Product_Page_Title'] = self.product_page_title
		if self.product_thumbnail is not None:
			data['Product_Thumbnail'] = self.product_thumbnail
		if self.product_image is not None:
			data['Product_Image'] = self.product_image
		if self.product_price is not None:
			data['Product_Price'] = self.product_price
		if self.product_cost is not None:
			data['Product_Cost'] = self.product_cost
		if self.product_weight is not None:
			data['Product_Weight'] = self.product_weight
		if self.product_inventory is not None:
			data['Product_Inventory'] = self.product_inventory
		if self.product_taxable is not None:
			data['Product_Taxable'] = self.product_taxable
		if self.product_active is not None:
			data['Product_Active'] = self.product_active
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data


"""
Handles API Request Provision_Domain. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/provision_domain
"""


class ProvisionDomain(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProvisionDomain Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN
		self.xml = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Provision_Domain'

	def get_xml(self) -> str:
		"""
		Get xml.

		:returns: str
		"""

		return self.xml

	def set_xml(self, xml: str) -> 'ProvisionDomain':
		"""
		Set xml.

		:param xml: str
		:returns: ProvisionDomain
		"""

		self.xml = xml
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProvisionDomain':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProvisionDomain':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProvisionDomain(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['XML'] = self.xml
		return data


"""
Handles API Request Provision_Store. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/provision_store
"""


class ProvisionStore(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProvisionStore Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.xml = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Provision_Store'

	def get_xml(self) -> str:
		"""
		Get xml.

		:returns: str
		"""

		return self.xml

	def set_xml(self, xml: str) -> 'ProvisionStore':
		"""
		Set xml.

		:param xml: str
		:returns: ProvisionStore
		"""

		self.xml = xml
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProvisionStore':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProvisionStore':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProvisionStore(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['XML'] = self.xml
		return data


"""
Handles API Request CustomerAddressList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddresslist_load_query
"""


class CustomerAddressListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'cust_id',
		'id',
		'descrip',
		'fname',
		'lname',
		'email',
		'comp',
		'phone',
		'fax',
		'addr1',
		'addr2',
		'city',
		'state',
		'zip',
		'cntry',
		'resdntl'
	]

	available_sort_fields = [
		'cust_id',
		'id',
		'descrip',
		'fname',
		'lname',
		'email',
		'comp',
		'phone',
		'fax',
		'addr1',
		'addr2',
		'city',
		'state',
		'zip',
		'cntry',
		'resdntl'
	]

	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerAddressListLoadQuery Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddressList_Load_Query'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def set_customer_id(self, customer_id: int) -> 'CustomerAddressListLoadQuery':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerAddressListLoadQuery
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerAddressListLoadQuery':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerAddressListLoadQuery
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerAddressListLoadQuery':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerAddressListLoadQuery
		"""

		self.customer_login = customer_login
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		return data


"""
Handles API Request PrintQueueList_Load_Query. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/printqueuelist_load_query
"""


class PrintQueueListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'descrip'
	]

	available_sort_fields = [
		'descrip'
	]

	def __init__(self, client: Client = None):
		"""
		PrintQueueListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PrintQueueList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueListLoadQuery(self, http_response, data)


"""
Handles API Request PrintQueueJobList_Load_Query. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/printqueuejoblist_load_query
"""


class PrintQueueJobListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'queue_id',
		'store_id',
		'user_id',
		'descrip',
		'job_fmt',
		'job_data',
		'dt_created'
	]

	available_sort_fields = [
		'id',
		'queue_id',
		'store_id',
		'user_id',
		'descrip',
		'job_fmt',
		'job_data',
		'dt_created'
	]

	available_on_demand_columns = [
		'job_data'
	]

	def __init__(self, client: Client = None, print_queue: merchantapi.model.PrintQueue = None):
		"""
		PrintQueueJobListLoadQuery Constructor.

		:param client: Client
		:param print_queue: PrintQueue
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN
		self.print_queue_id = None
		self.edit_print_queue = None
		self.print_queue_description = None
		if isinstance(print_queue, merchantapi.model.PrintQueue):
			if print_queue.get_id():
				self.set_print_queue_id(print_queue.get_id())
			elif print_queue.get_description():
				self.set_edit_print_queue(print_queue.get_description())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PrintQueueJobList_Load_Query'

	def get_print_queue_id(self) -> int:
		"""
		Get PrintQueue_ID.

		:returns: int
		"""

		return self.print_queue_id

	def get_edit_print_queue(self) -> str:
		"""
		Get Edit_PrintQueue.

		:returns: str
		"""

		return self.edit_print_queue

	def get_print_queue_description(self) -> str:
		"""
		Get PrintQueue_Description.

		:returns: str
		"""

		return self.print_queue_description

	def set_print_queue_id(self, print_queue_id: int) -> 'PrintQueueJobListLoadQuery':
		"""
		Set PrintQueue_ID.

		:param print_queue_id: int
		:returns: PrintQueueJobListLoadQuery
		"""

		self.print_queue_id = print_queue_id
		return self

	def set_edit_print_queue(self, edit_print_queue: str) -> 'PrintQueueJobListLoadQuery':
		"""
		Set Edit_PrintQueue.

		:param edit_print_queue: str
		:returns: PrintQueueJobListLoadQuery
		"""

		self.edit_print_queue = edit_print_queue
		return self

	def set_print_queue_description(self, print_queue_description: str) -> 'PrintQueueJobListLoadQuery':
		"""
		Set PrintQueue_Description.

		:param print_queue_description: str
		:returns: PrintQueueJobListLoadQuery
		"""

		self.print_queue_description = print_queue_description
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueJobListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueJobListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueJobListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.print_queue_id is not None:
			data['PrintQueue_ID'] = self.print_queue_id
		elif self.edit_print_queue is not None:
			data['Edit_PrintQueue'] = self.edit_print_queue
		elif self.print_queue_description is not None:
			data['PrintQueue_Description'] = self.print_queue_description

		return data


"""
Handles API Request PrintQueueJob_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/printqueuejob_delete
"""


class PrintQueueJobDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, print_queue_job: merchantapi.model.PrintQueueJob = None):
		"""
		PrintQueueJobDelete Constructor.

		:param client: Client
		:param print_queue_job: PrintQueueJob
		"""

		super().__init__(client)
		self.print_queue_job_id = None
		if isinstance(print_queue_job, merchantapi.model.PrintQueueJob):
			if print_queue_job.get_id():
				self.set_print_queue_job_id(print_queue_job.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PrintQueueJob_Delete'

	def get_print_queue_job_id(self) -> int:
		"""
		Get PrintQueueJob_ID.

		:returns: int
		"""

		return self.print_queue_job_id

	def set_print_queue_job_id(self, print_queue_job_id: int) -> 'PrintQueueJobDelete':
		"""
		Set PrintQueueJob_ID.

		:param print_queue_job_id: int
		:returns: PrintQueueJobDelete
		"""

		self.print_queue_job_id = print_queue_job_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueJobDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueJobDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueJobDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.print_queue_job_id is not None:
			data['PrintQueueJob_ID'] = self.print_queue_job_id

		return data


"""
Handles API Request PrintQueueJob_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/printqueuejob_insert
"""


class PrintQueueJobInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, print_queue: merchantapi.model.PrintQueue = None):
		"""
		PrintQueueJobInsert Constructor.

		:param client: Client
		:param print_queue: PrintQueue
		"""

		super().__init__(client)
		self.print_queue_id = None
		self.edit_print_queue = None
		self.print_queue_description = None
		self.print_queue_job_description = None
		self.print_queue_job_format = None
		self.print_queue_job_data = None
		if isinstance(print_queue, merchantapi.model.PrintQueue):
			if print_queue.get_id():
				self.set_print_queue_id(print_queue.get_id())
			elif print_queue.get_description():
				self.set_edit_print_queue(print_queue.get_description())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PrintQueueJob_Insert'

	def get_print_queue_id(self) -> int:
		"""
		Get PrintQueue_ID.

		:returns: int
		"""

		return self.print_queue_id

	def get_edit_print_queue(self) -> str:
		"""
		Get Edit_PrintQueue.

		:returns: str
		"""

		return self.edit_print_queue

	def get_print_queue_description(self) -> str:
		"""
		Get PrintQueue_Description.

		:returns: str
		"""

		return self.print_queue_description

	def get_print_queue_job_description(self) -> str:
		"""
		Get PrintQueueJob_Description.

		:returns: str
		"""

		return self.print_queue_job_description

	def get_print_queue_job_format(self) -> str:
		"""
		Get PrintQueueJob_Format.

		:returns: str
		"""

		return self.print_queue_job_format

	def get_print_queue_job_data(self) -> str:
		"""
		Get PrintQueueJob_Data.

		:returns: str
		"""

		return self.print_queue_job_data

	def set_print_queue_id(self, print_queue_id: int) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueue_ID.

		:param print_queue_id: int
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_id = print_queue_id
		return self

	def set_edit_print_queue(self, edit_print_queue: str) -> 'PrintQueueJobInsert':
		"""
		Set Edit_PrintQueue.

		:param edit_print_queue: str
		:returns: PrintQueueJobInsert
		"""

		self.edit_print_queue = edit_print_queue
		return self

	def set_print_queue_description(self, print_queue_description: str) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueue_Description.

		:param print_queue_description: str
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_description = print_queue_description
		return self

	def set_print_queue_job_description(self, print_queue_job_description: str) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueueJob_Description.

		:param print_queue_job_description: str
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_job_description = print_queue_job_description
		return self

	def set_print_queue_job_format(self, print_queue_job_format: str) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueueJob_Format.

		:param print_queue_job_format: str
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_job_format = print_queue_job_format
		return self

	def set_print_queue_job_data(self, print_queue_job_data: str) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueueJob_Data.

		:param print_queue_job_data: str
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_job_data = print_queue_job_data
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueJobInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueJobInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueJobInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.print_queue_id is not None:
			data['PrintQueue_ID'] = self.print_queue_id
		elif self.edit_print_queue is not None:
			data['Edit_PrintQueue'] = self.edit_print_queue
		elif self.print_queue_description is not None:
			data['PrintQueue_Description'] = self.print_queue_description

		if self.print_queue_job_description is not None:
			data['PrintQueueJob_Description'] = self.print_queue_job_description
		if self.print_queue_job_format is not None:
			data['PrintQueueJob_Format'] = self.print_queue_job_format
		if self.print_queue_job_data is not None:
			data['PrintQueueJob_Data'] = self.print_queue_job_data
		return data


"""
Handles API Request PrintQueueJob_Status. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/printqueuejob_status
"""


class PrintQueueJobStatus(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, print_queue_job: merchantapi.model.PrintQueueJob = None):
		"""
		PrintQueueJobStatus Constructor.

		:param client: Client
		:param print_queue_job: PrintQueueJob
		"""

		super().__init__(client)
		self.print_queue_job_id = None
		if isinstance(print_queue_job, merchantapi.model.PrintQueueJob):
			if print_queue_job.get_id():
				self.set_print_queue_job_id(print_queue_job.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PrintQueueJob_Status'

	def get_print_queue_job_id(self) -> int:
		"""
		Get PrintQueueJob_ID.

		:returns: int
		"""

		return self.print_queue_job_id

	def set_print_queue_job_id(self, print_queue_job_id: int) -> 'PrintQueueJobStatus':
		"""
		Set PrintQueueJob_ID.

		:param print_queue_job_id: int
		:returns: PrintQueueJobStatus
		"""

		self.print_queue_job_id = print_queue_job_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueJobStatus':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueJobStatus':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueJobStatus(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.print_queue_job_id is not None:
			data['PrintQueueJob_ID'] = self.print_queue_job_id

		return data


"""
Handles API Request PaymentMethodList_Load. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/paymentmethodlist_load
"""


class PaymentMethodListLoad(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		PaymentMethodListLoad Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PaymentMethodList_Load'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def set_order_id(self, order_id: int) -> 'PaymentMethodListLoad':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: PaymentMethodListLoad
		"""

		self.order_id = order_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PaymentMethodListLoad':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PaymentMethodListLoad':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PaymentMethodListLoad(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id
		return data


"""
Handles API Request Order_Create_FromOrder. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_create_fromorder
"""


class OrderCreateFromOrder(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderCreateFromOrder Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Create_FromOrder'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def set_order_id(self, order_id: int) -> 'OrderCreateFromOrder':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderCreateFromOrder
		"""

		self.order_id = order_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCreateFromOrder':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCreateFromOrder':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCreateFromOrder(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		return data


"""
Handles API Request Order_Authorize. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_authorize
"""


class OrderAuthorize(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderAuthorize Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.module_id = None
		self.module_data = None
		self.amount = None
		self.module_fields = {}
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Authorize'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_module_id(self) -> int:
		"""
		Get Module_ID.

		:returns: int
		"""

		return self.module_id

	def get_module_data(self) -> str:
		"""
		Get Module_Data.

		:returns: str
		"""

		return self.module_data

	def get_amount(self) -> float:
		"""
		Get Amount.

		:returns: float
		"""

		return self.amount

	def get_module_fields(self):
		"""
		Get Module_Fields.

		:returns: dict
		"""

		return self.module_fields

	def set_order_id(self, order_id: int) -> 'OrderAuthorize':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderAuthorize
		"""

		self.order_id = order_id
		return self

	def set_module_id(self, module_id: int) -> 'OrderAuthorize':
		"""
		Set Module_ID.

		:param module_id: int
		:returns: OrderAuthorize
		"""

		self.module_id = module_id
		return self

	def set_module_data(self, module_data: str) -> 'OrderAuthorize':
		"""
		Set Module_Data.

		:param module_data: str
		:returns: OrderAuthorize
		"""

		self.module_data = module_data
		return self

	def set_amount(self, amount: float) -> 'OrderAuthorize':
		"""
		Set Amount.

		:param amount: float
		:returns: OrderAuthorize
		"""

		self.amount = amount
		return self

	def set_module_fields(self, module_fields) -> 'OrderAuthorize':
		"""
		Set Module_Fields.

		:param module_fields: dict
		:returns: OrderAuthorize
		"""

		self.module_fields = module_fields
		return self

	def set_module_field(self, field: str, value) -> 'OrderAuthorize':
		"""
		Add custom data to the request.

		:param field: str
		:param value: mixed
		:returns: {OrderAuthorize}
		"""

		self.module_fields[field] = value
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderAuthorize':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderAuthorize':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderAuthorize(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()
		data.update(self.get_module_fields())

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.module_id is not None:
			data['Module_ID'] = self.module_id
		if self.module_data is not None:
			data['Module_Data'] = self.module_data
		data['Amount'] = self.amount
		return data


"""
Handles API Request CustomerPaymentCardList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customerpaymentcardlist_load_query
"""


class CustomerPaymentCardListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'fname',
		'lname',
		'exp_month',
		'exp_year',
		'lastfour',
		'lastused',
		'type',
		'addr1',
		'addr2',
		'city',
		'state',
		'zip',
		'cntry',
		'refcount',
		'mod_code',
		'meth_code',
		'id'
	]

	available_sort_fields = [
		'fname',
		'lname',
		'expires',
		'lastfour',
		'lastused',
		'type',
		'addr1',
		'addr2',
		'city',
		'state',
		'zip',
		'cntry',
		'refcount',
		'mod_code',
		'meth_code',
		'id'
	]

	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerPaymentCardListLoadQuery Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_customer_login(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerPaymentCardList_Load_Query'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def set_customer_id(self, customer_id: int) -> 'CustomerPaymentCardListLoadQuery':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerPaymentCardListLoadQuery
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerPaymentCardListLoadQuery':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerPaymentCardListLoadQuery
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerPaymentCardListLoadQuery':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerPaymentCardListLoadQuery
		"""

		self.customer_login = customer_login
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerPaymentCardListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerPaymentCardListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerPaymentCardListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		return data


"""
Handles API Request Branch_Copy. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branch_copy
"""


class BranchCopy(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchCopy Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.source_branch_id = None
		self.destination_branch_id = None
		self.notes = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_source_branch_id(branch.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Branch_Copy'

	def get_source_branch_id(self) -> int:
		"""
		Get Source_Branch_ID.

		:returns: int
		"""

		return self.source_branch_id

	def get_destination_branch_id(self) -> int:
		"""
		Get Destination_Branch_ID.

		:returns: int
		"""

		return self.destination_branch_id

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: str
		"""

		return self.notes

	def set_source_branch_id(self, source_branch_id: int) -> 'BranchCopy':
		"""
		Set Source_Branch_ID.

		:param source_branch_id: int
		:returns: BranchCopy
		"""

		self.source_branch_id = source_branch_id
		return self

	def set_destination_branch_id(self, destination_branch_id: int) -> 'BranchCopy':
		"""
		Set Destination_Branch_ID.

		:param destination_branch_id: int
		:returns: BranchCopy
		"""

		self.destination_branch_id = destination_branch_id
		return self

	def set_notes(self, notes: str) -> 'BranchCopy':
		"""
		Set Notes.

		:param notes: str
		:returns: BranchCopy
		"""

		self.notes = notes
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchCopy':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchCopy':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchCopy(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.source_branch_id is not None:
			data['Source_Branch_ID'] = self.source_branch_id

		if self.destination_branch_id is not None:
			data['Destination_Branch_ID'] = self.destination_branch_id

		if self.notes is not None:
			data['Notes'] = self.notes
		return data


"""
Handles API Request Branch_Create. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branch_create
"""


class BranchCreate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchCreate Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.parent_branch_id = None
		self.name = None
		self.color = None
		self.changeset_id = None
		self.tags = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_parent_branch_id(branch.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Branch_Create'

	def get_parent_branch_id(self) -> int:
		"""
		Get Parent_Branch_ID.

		:returns: int
		"""

		return self.parent_branch_id

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_color(self) -> str:
		"""
		Get Color.

		:returns: str
		"""

		return self.color

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def get_tags(self) -> str:
		"""
		Get Tags.

		:returns: str
		"""

		return self.tags

	def set_parent_branch_id(self, parent_branch_id: int) -> 'BranchCreate':
		"""
		Set Parent_Branch_ID.

		:param parent_branch_id: int
		:returns: BranchCreate
		"""

		self.parent_branch_id = parent_branch_id
		return self

	def set_name(self, name: str) -> 'BranchCreate':
		"""
		Set Name.

		:param name: str
		:returns: BranchCreate
		"""

		self.name = name
		return self

	def set_color(self, color: str) -> 'BranchCreate':
		"""
		Set Color.

		:param color: str
		:returns: BranchCreate
		"""

		self.color = color
		return self

	def set_changeset_id(self, changeset_id: int) -> 'BranchCreate':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: BranchCreate
		"""

		self.changeset_id = changeset_id
		return self

	def set_tags(self, tags: str) -> 'BranchCreate':
		"""
		Set Tags.

		:param tags: str
		:returns: BranchCreate
		"""

		self.tags = tags
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchCreate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchCreate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchCreate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.parent_branch_id is not None:
			data['Parent_Branch_ID'] = self.parent_branch_id

		if self.name is not None:
			data['Name'] = self.name
		if self.color is not None:
			data['Color'] = self.color
		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id
		if self.tags is not None:
			data['Tags'] = self.tags
		return data


"""
Handles API Request Branch_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branch_delete
"""


class BranchDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchDelete Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Branch_Delete'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def set_branch_id(self, branch_id: int) -> 'BranchDelete':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchDelete
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchDelete':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchDelete
		"""

		self.branch_name = branch_name
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		return data


"""
Handles API Request Changeset_Create. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changeset_create
"""


class ChangesetCreate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		ChangesetCreate Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		self.notes = None
		self.tags = None
		self.template_changes = []
		self.resource_group_changes = []
		self.css_resource_changes = []
		self.java_script_resource_changes = []
		self.property_changes = []
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Changeset_Create'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: str
		"""

		return self.notes

	def get_tags(self) -> str:
		"""
		Get Tags.

		:returns: str
		"""

		return self.tags

	def get_template_changes(self) -> list:
		"""
		Get Template_Changes.

		:returns: List of TemplateChange
		"""

		return self.template_changes

	def get_resource_group_changes(self) -> list:
		"""
		Get ResourceGroup_Changes.

		:returns: List of ResourceGroupChange
		"""

		return self.resource_group_changes

	def get_css_resource_changes(self) -> list:
		"""
		Get CSSResource_Changes.

		:returns: List of CSSResourceChange
		"""

		return self.css_resource_changes

	def get_java_script_resource_changes(self) -> list:
		"""
		Get JavaScriptResource_Changes.

		:returns: List of JavaScriptResourceChange
		"""

		return self.java_script_resource_changes

	def get_property_changes(self) -> list:
		"""
		Get Property_Changes.

		:returns: List of PropertyChange
		"""

		return self.property_changes

	def set_branch_id(self, branch_id: int) -> 'ChangesetCreate':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: ChangesetCreate
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'ChangesetCreate':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: ChangesetCreate
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'ChangesetCreate':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: ChangesetCreate
		"""

		self.edit_branch = edit_branch
		return self

	def set_notes(self, notes: str) -> 'ChangesetCreate':
		"""
		Set Notes.

		:param notes: str
		:returns: ChangesetCreate
		"""

		self.notes = notes
		return self

	def set_tags(self, tags: str) -> 'ChangesetCreate':
		"""
		Set Tags.

		:param tags: str
		:returns: ChangesetCreate
		"""

		self.tags = tags
		return self

	def set_template_changes(self, template_changes: list) -> 'ChangesetCreate':
		"""
		Set Template_Changes.

		:param template_changes: {TemplateChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in template_changes:
			if not isinstance(e, merchantapi.model.TemplateChange):
				raise Exception("")
		self.template_changes = template_changes
		return self

	def set_resource_group_changes(self, resource_group_changes: list) -> 'ChangesetCreate':
		"""
		Set ResourceGroup_Changes.

		:param resource_group_changes: {ResourceGroupChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in resource_group_changes:
			if not isinstance(e, merchantapi.model.ResourceGroupChange):
				raise Exception("")
		self.resource_group_changes = resource_group_changes
		return self

	def set_css_resource_changes(self, css_resource_changes: list) -> 'ChangesetCreate':
		"""
		Set CSSResource_Changes.

		:param css_resource_changes: {CSSResourceChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in css_resource_changes:
			if not isinstance(e, merchantapi.model.CSSResourceChange):
				raise Exception("")
		self.css_resource_changes = css_resource_changes
		return self

	def set_java_script_resource_changes(self, java_script_resource_changes: list) -> 'ChangesetCreate':
		"""
		Set JavaScriptResource_Changes.

		:param java_script_resource_changes: {JavaScriptResourceChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in java_script_resource_changes:
			if not isinstance(e, merchantapi.model.JavaScriptResourceChange):
				raise Exception("")
		self.java_script_resource_changes = java_script_resource_changes
		return self

	def set_property_changes(self, property_changes: list) -> 'ChangesetCreate':
		"""
		Set Property_Changes.

		:param property_changes: {PropertyChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in property_changes:
			if not isinstance(e, merchantapi.model.PropertyChange):
				raise Exception("")
		self.property_changes = property_changes
		return self
	
	def add_template_change(self, template_change) -> 'ChangesetCreate':
		"""
		Add Template_Changes.

		:param template_change: TemplateChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(template_change, merchantapi.model.TemplateChange):
			self.template_changes.append(template_change)
		elif isinstance(template_change, dict):
			self.template_changes.append(merchantapi.model.TemplateChange(template_change))
		else:
			raise Exception('Expected instance of TemplateChange or dict')
		return self

	def add_template_changes(self, template_changes: list) -> 'ChangesetCreate':
		"""
		Add many TemplateChange.

		:param template_changes: List of TemplateChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in template_changes:
			if not isinstance(e, merchantapi.model.TemplateChange):
				raise Exception('')
			self.template_changes.append(e)

		return self
	
	def add_resource_group_change(self, resource_group_change) -> 'ChangesetCreate':
		"""
		Add ResourceGroup_Changes.

		:param resource_group_change: ResourceGroupChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(resource_group_change, merchantapi.model.ResourceGroupChange):
			self.resource_group_changes.append(resource_group_change)
		elif isinstance(resource_group_change, dict):
			self.resource_group_changes.append(merchantapi.model.ResourceGroupChange(resource_group_change))
		else:
			raise Exception('Expected instance of ResourceGroupChange or dict')
		return self

	def add_resource_group_changes(self, resource_group_changes: list) -> 'ChangesetCreate':
		"""
		Add many ResourceGroupChange.

		:param resource_group_changes: List of ResourceGroupChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in resource_group_changes:
			if not isinstance(e, merchantapi.model.ResourceGroupChange):
				raise Exception('')
			self.resource_group_changes.append(e)

		return self
	
	def add_css_resource_change(self, css_resource_change) -> 'ChangesetCreate':
		"""
		Add CSSResource_Changes.

		:param css_resource_change: CSSResourceChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(css_resource_change, merchantapi.model.CSSResourceChange):
			self.css_resource_changes.append(css_resource_change)
		elif isinstance(css_resource_change, dict):
			self.css_resource_changes.append(merchantapi.model.CSSResourceChange(css_resource_change))
		else:
			raise Exception('Expected instance of CSSResourceChange or dict')
		return self

	def add_css_resource_changes(self, css_resource_changes: list) -> 'ChangesetCreate':
		"""
		Add many CSSResourceChange.

		:param css_resource_changes: List of CSSResourceChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in css_resource_changes:
			if not isinstance(e, merchantapi.model.CSSResourceChange):
				raise Exception('')
			self.css_resource_changes.append(e)

		return self
	
	def add_java_script_resource_change(self, java_script_resource_change) -> 'ChangesetCreate':
		"""
		Add JavaScriptResource_Changes.

		:param java_script_resource_change: JavaScriptResourceChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(java_script_resource_change, merchantapi.model.JavaScriptResourceChange):
			self.java_script_resource_changes.append(java_script_resource_change)
		elif isinstance(java_script_resource_change, dict):
			self.java_script_resource_changes.append(merchantapi.model.JavaScriptResourceChange(java_script_resource_change))
		else:
			raise Exception('Expected instance of JavaScriptResourceChange or dict')
		return self

	def add_java_script_resource_changes(self, java_script_resource_changes: list) -> 'ChangesetCreate':
		"""
		Add many JavaScriptResourceChange.

		:param java_script_resource_changes: List of JavaScriptResourceChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in java_script_resource_changes:
			if not isinstance(e, merchantapi.model.JavaScriptResourceChange):
				raise Exception('')
			self.java_script_resource_changes.append(e)

		return self
	
	def add_property_change(self, property_change) -> 'ChangesetCreate':
		"""
		Add Property_Changes.

		:param property_change: PropertyChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(property_change, merchantapi.model.PropertyChange):
			self.property_changes.append(property_change)
		elif isinstance(property_change, dict):
			self.property_changes.append(merchantapi.model.PropertyChange(property_change))
		else:
			raise Exception('Expected instance of PropertyChange or dict')
		return self

	def add_property_changes(self, property_changes: list) -> 'ChangesetCreate':
		"""
		Add many PropertyChange.

		:param property_changes: List of PropertyChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in property_changes:
			if not isinstance(e, merchantapi.model.PropertyChange):
				raise Exception('')
			self.property_changes.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetCreate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetCreate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetCreate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.notes is not None:
			data['Notes'] = self.notes
		if self.tags is not None:
			data['Tags'] = self.tags
		if len(self.template_changes):
			data['Template_Changes'] = []

			for f in self.template_changes:
				data['Template_Changes'].append(f.to_dict())
		if len(self.resource_group_changes):
			data['ResourceGroup_Changes'] = []

			for f in self.resource_group_changes:
				data['ResourceGroup_Changes'].append(f.to_dict())
		if len(self.css_resource_changes):
			data['CSSResource_Changes'] = []

			for f in self.css_resource_changes:
				data['CSSResource_Changes'].append(f.to_dict())
		if len(self.java_script_resource_changes):
			data['JavaScriptResource_Changes'] = []

			for f in self.java_script_resource_changes:
				data['JavaScriptResource_Changes'].append(f.to_dict())
		if len(self.property_changes):
			data['Property_Changes'] = []

			for f in self.property_changes:
				data['Property_Changes'].append(f.to_dict())
		return data


"""
Handles API Request ChangesetList_Merge. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesetlist_merge
"""


class ChangesetListMerge(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		ChangesetListMerge Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.source_changeset_ids = []
		self.destination_branch_id = None
		self.notes = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_destination_branch_id(branch.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetList_Merge'

	def get_source_changeset_ids(self):
		"""
		Get Source_Changeset_IDs.

		:returns: list
		"""

		return self.source_changeset_ids

	def get_destination_branch_id(self) -> int:
		"""
		Get Destination_Branch_ID.

		:returns: int
		"""

		return self.destination_branch_id

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: str
		"""

		return self.notes

	def set_destination_branch_id(self, destination_branch_id: int) -> 'ChangesetListMerge':
		"""
		Set Destination_Branch_ID.

		:param destination_branch_id: int
		:returns: ChangesetListMerge
		"""

		self.destination_branch_id = destination_branch_id
		return self

	def set_notes(self, notes: str) -> 'ChangesetListMerge':
		"""
		Set Notes.

		:param notes: str
		:returns: ChangesetListMerge
		"""

		self.notes = notes
		return self
	
	def add_source_changeset_id(self, source_changeset_id) -> 'ChangesetListMerge':
		"""
		Add Source_Changeset_IDs.

		:param source_changeset_id: int
		:returns: {ChangesetListMerge}
		"""

		self.source_changeset_ids.append(source_changeset_id)
		return self

	def add_changeset(self, changeset: merchantapi.model.Changeset) -> 'ChangesetListMerge':
		"""
		Add Changeset model.

		:param changeset: Changeset
		:raises Exception:
		:returns: ChangesetListMerge
		"""
		if not isinstance(changeset, merchantapi.model.Changeset):
			raise Exception('Expected an instance of Changeset')

		if changeset.get_id():
			self.source_changeset_ids.append(changeset.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetListMerge':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetListMerge':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetListMerge(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.destination_branch_id is not None:
			data['Destination_Branch_ID'] = self.destination_branch_id

		data['Source_Changeset_IDs'] = self.source_changeset_ids
		if self.notes is not None:
			data['Notes'] = self.notes
		return data


"""
Handles API Request ChangesetChangeList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesetchangelist_load_query
"""


class ChangesetChangeListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'item_type',
		'item_id',
		'item_version_id',
		'item_identifier'
	]

	available_sort_fields = [
		'item_type',
		'item_id',
		'item_version_id',
		'item_identifier'
	]

	def __init__(self, client: Client = None, changeset: merchantapi.model.Changeset = None):
		"""
		ChangesetChangeListLoadQuery Constructor.

		:param client: Client
		:param changeset: Changeset
		"""

		super().__init__(client)
		self.changeset_id = None
		if isinstance(changeset, merchantapi.model.Changeset):
			self.set_changeset_id(changeset.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetChangeList_Load_Query'

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_changeset_id(self, changeset_id: int) -> 'ChangesetChangeListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: ChangesetChangeListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetChangeListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetChangeListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetChangeListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Changeset_ID'] = self.get_changeset_id()

		return data


"""
Handles API Request BranchList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchlist_load_query
"""


class BranchListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'immutable',
		'branchkey',
		'name',
		'framework'
	]

	available_sort_fields = [
		'id',
		'immutable',
		'branchkey',
		'name',
		'framework'
	]

	def __init__(self, client: Client = None):
		"""
		BranchListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchListLoadQuery(self, http_response, data)


"""
Handles API Request BranchTemplateVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchtemplateversionlist_load_query
"""


class BranchTemplateVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'templ_id',
		'parent_id',
		'item_id',
		'prop_id',
		'sync',
		'filename',
		'dtstamp',
		'user_id',
		'user_name'
	]

	available_sort_fields = [
		'id',
		'templ_id',
		'parent_id',
		'item_id',
		'prop_id',
		'sync',
		'filename',
		'dtstamp',
		'user_id',
		'user_name'
	]

	available_on_demand_columns = [
		'notes',
		'source',
		'settings'
	]

	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchTemplateVersionListLoadQuery Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		self.changeset_id = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchTemplateVersionList_Load_Query'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_branch_id(self, branch_id: int) -> 'BranchTemplateVersionListLoadQuery':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchTemplateVersionListLoadQuery
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchTemplateVersionListLoadQuery':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchTemplateVersionListLoadQuery
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'BranchTemplateVersionListLoadQuery':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: BranchTemplateVersionListLoadQuery
		"""

		self.edit_branch = edit_branch
		return self

	def set_changeset_id(self, changeset_id: int) -> 'BranchTemplateVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: BranchTemplateVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchTemplateVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchTemplateVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchTemplateVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id
		return data


"""
Handles API Request BranchCSSResourceVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchcssresourceversionlist_load_query
"""


class BranchCSSResourceVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_sort_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_on_demand_columns = [
		'source',
		'linkedpages',
		'linkedresources',
		'source_notes'
	]

	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchCSSResourceVersionListLoadQuery Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		self.changeset_id = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchCSSResourceVersionList_Load_Query'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_branch_id(self, branch_id: int) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchCSSResourceVersionListLoadQuery
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchCSSResourceVersionListLoadQuery
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: BranchCSSResourceVersionListLoadQuery
		"""

		self.edit_branch = edit_branch
		return self

	def set_changeset_id(self, changeset_id: int) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: BranchCSSResourceVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchCSSResourceVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchCSSResourceVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id
		return data


"""
Handles API Request BranchJavaScriptResourceVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchjavascriptresourceversionlist_load_query
"""


class BranchJavaScriptResourceVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_sort_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_on_demand_columns = [
		'source',
		'linkedpages',
		'linkedresources',
		'source_notes'
	]

	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchJavaScriptResourceVersionListLoadQuery Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		self.changeset_id = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchJavaScriptResourceVersionList_Load_Query'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_branch_id(self, branch_id: int) -> 'BranchJavaScriptResourceVersionListLoadQuery':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchJavaScriptResourceVersionListLoadQuery
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchJavaScriptResourceVersionListLoadQuery':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchJavaScriptResourceVersionListLoadQuery
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'BranchJavaScriptResourceVersionListLoadQuery':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: BranchJavaScriptResourceVersionListLoadQuery
		"""

		self.edit_branch = edit_branch
		return self

	def set_changeset_id(self, changeset_id: int) -> 'BranchJavaScriptResourceVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: BranchJavaScriptResourceVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchJavaScriptResourceVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchJavaScriptResourceVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchJavaScriptResourceVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id
		return data


"""
Handles API Request ChangesetList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesetlist_load_query
"""


class ChangesetListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'branch_id',
		'user_id',
		'user_name',
		'dtstamp',
		'notes',
		'user_name'
	]

	available_sort_fields = [
		'id',
		'branch_id',
		'user_id',
		'user_name',
		'dtstamp',
		'notes',
		'user_name'
	]

	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		ChangesetListLoadQuery Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetList_Load_Query'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def set_branch_id(self, branch_id: int) -> 'ChangesetListLoadQuery':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: ChangesetListLoadQuery
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'ChangesetListLoadQuery':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: ChangesetListLoadQuery
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'ChangesetListLoadQuery':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: ChangesetListLoadQuery
		"""

		self.edit_branch = edit_branch
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		return data


"""
Handles API Request ChangesetTemplateVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesettemplateversionlist_load_query
"""


class ChangesetTemplateVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'templ_id',
		'parent_id',
		'item_id',
		'prop_id',
		'sync',
		'filename',
		'dtstamp',
		'user_id',
		'user_name'
	]

	available_sort_fields = [
		'id',
		'templ_id',
		'parent_id',
		'item_id',
		'prop_id',
		'sync',
		'filename',
		'dtstamp',
		'user_id',
		'user_name'
	]

	available_on_demand_columns = [
		'notes',
		'source',
		'settings'
	]

	def __init__(self, client: Client = None, changeset: merchantapi.model.Changeset = None):
		"""
		ChangesetTemplateVersionListLoadQuery Constructor.

		:param client: Client
		:param changeset: Changeset
		"""

		super().__init__(client)
		self.changeset_id = None
		if isinstance(changeset, merchantapi.model.Changeset):
			if changeset.get_id():
				self.set_changeset_id(changeset.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetTemplateVersionList_Load_Query'

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_changeset_id(self, changeset_id: int) -> 'ChangesetTemplateVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: ChangesetTemplateVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetTemplateVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetTemplateVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetTemplateVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id

		return data


"""
Handles API Request ChangesetCSSResourceVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesetcssresourceversionlist_load_query
"""


class ChangesetCSSResourceVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_sort_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_on_demand_columns = [
		'source',
		'source_notes'
	]

	def __init__(self, client: Client = None, changeset: merchantapi.model.Changeset = None):
		"""
		ChangesetCSSResourceVersionListLoadQuery Constructor.

		:param client: Client
		:param changeset: Changeset
		"""

		super().__init__(client)
		self.changeset_id = None
		if isinstance(changeset, merchantapi.model.Changeset):
			self.set_changeset_id(changeset.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetCSSResourceVersionList_Load_Query'

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_changeset_id(self, changeset_id: int) -> 'ChangesetCSSResourceVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: ChangesetCSSResourceVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetCSSResourceVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetCSSResourceVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetCSSResourceVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Changeset_ID'] = self.get_changeset_id()

		return data


"""
Handles API Request ChangesetJavaScriptResourceVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesetjavascriptresourceversionlist_load_query
"""


class ChangesetJavaScriptResourceVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_sort_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_on_demand_columns = [
		'source',
		'source_notes'
	]

	def __init__(self, client: Client = None, changeset: merchantapi.model.Changeset = None):
		"""
		ChangesetJavaScriptResourceVersionListLoadQuery Constructor.

		:param client: Client
		:param changeset: Changeset
		"""

		super().__init__(client)
		self.changeset_id = None
		if isinstance(changeset, merchantapi.model.Changeset):
			self.set_changeset_id(changeset.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetJavaScriptResourceVersionList_Load_Query'

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_changeset_id(self, changeset_id: int) -> 'ChangesetJavaScriptResourceVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: ChangesetJavaScriptResourceVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetJavaScriptResourceVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetJavaScriptResourceVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetJavaScriptResourceVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Changeset_ID'] = self.get_changeset_id()

		return data


"""
Handles API Request CustomerCreditHistoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customercredithistorylist_load_query
"""


class CustomerCreditHistoryListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'user_name',
		'order_id',
		'txref',
		'descrip',
		'amount',
		'dtstamp',
		'id'
	]

	available_sort_fields = [
		'user_name',
		'order_id',
		'txref',
		'descrip',
		'amount',
		'dtstamp',
		'id'
	]

	available_on_demand_columns = [
		'source'
	]

	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerCreditHistoryListLoadQuery Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerCreditHistoryList_Load_Query'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def set_customer_id(self, customer_id: int) -> 'CustomerCreditHistoryListLoadQuery':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerCreditHistoryListLoadQuery
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerCreditHistoryListLoadQuery':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerCreditHistoryListLoadQuery
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerCreditHistoryListLoadQuery':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerCreditHistoryListLoadQuery
		"""

		self.customer_login = customer_login
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerCreditHistoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerCreditHistoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerCreditHistoryListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		return data


"""
Handles API Request CustomerCreditHistory_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customercredithistory_insert
"""


class CustomerCreditHistoryInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerCreditHistoryInsert Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.amount = None
		self.description = None
		self.transaction_reference = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerCreditHistory_Insert'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_amount(self) -> float:
		"""
		Get Amount.

		:returns: float
		"""

		return self.amount

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_transaction_reference(self) -> str:
		"""
		Get TransactionReference.

		:returns: str
		"""

		return self.transaction_reference

	def set_customer_id(self, customer_id: int) -> 'CustomerCreditHistoryInsert':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerCreditHistoryInsert
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerCreditHistoryInsert':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerCreditHistoryInsert
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerCreditHistoryInsert':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerCreditHistoryInsert
		"""

		self.customer_login = customer_login
		return self

	def set_amount(self, amount: float) -> 'CustomerCreditHistoryInsert':
		"""
		Set Amount.

		:param amount: float
		:returns: CustomerCreditHistoryInsert
		"""

		self.amount = amount
		return self

	def set_description(self, description: str) -> 'CustomerCreditHistoryInsert':
		"""
		Set Description.

		:param description: str
		:returns: CustomerCreditHistoryInsert
		"""

		self.description = description
		return self

	def set_transaction_reference(self, transaction_reference: str) -> 'CustomerCreditHistoryInsert':
		"""
		Set TransactionReference.

		:param transaction_reference: str
		:returns: CustomerCreditHistoryInsert
		"""

		self.transaction_reference = transaction_reference
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerCreditHistoryInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerCreditHistoryInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerCreditHistoryInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		data['Amount'] = self.amount
		data['Description'] = self.description
		if self.transaction_reference is not None:
			data['TransactionReference'] = self.transaction_reference
		return data


"""
Handles API Request CustomerCreditHistory_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customercredithistory_delete
"""


class CustomerCreditHistoryDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer_credit_history: merchantapi.model.CustomerCreditHistory = None):
		"""
		CustomerCreditHistoryDelete Constructor.

		:param client: Client
		:param customer_credit_history: CustomerCreditHistory
		"""

		super().__init__(client)
		self.customer_credit_history_id = None
		if isinstance(customer_credit_history, merchantapi.model.CustomerCreditHistory):
			self.set_customer_credit_history_id(customer_credit_history.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerCreditHistory_Delete'

	def get_customer_credit_history_id(self) -> int:
		"""
		Get CustomerCreditHistory_ID.

		:returns: int
		"""

		return self.customer_credit_history_id

	def set_customer_credit_history_id(self, customer_credit_history_id: int) -> 'CustomerCreditHistoryDelete':
		"""
		Set CustomerCreditHistory_ID.

		:param customer_credit_history_id: int
		:returns: CustomerCreditHistoryDelete
		"""

		self.customer_credit_history_id = customer_credit_history_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerCreditHistoryDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerCreditHistoryDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerCreditHistoryDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['CustomerCreditHistory_ID'] = self.customer_credit_history_id
		return data


"""
Handles API Request OrderCoupon_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordercoupon_update_assigned
"""


class OrderCouponUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderCouponUpdateAssigned Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.assigned = False
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderCoupon_Update_Assigned'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_order_id(self, order_id: int) -> 'OrderCouponUpdateAssigned':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderCouponUpdateAssigned
		"""

		self.order_id = order_id
		return self

	def set_coupon_id(self, coupon_id: int) -> 'OrderCouponUpdateAssigned':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: OrderCouponUpdateAssigned
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'OrderCouponUpdateAssigned':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: OrderCouponUpdateAssigned
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'OrderCouponUpdateAssigned':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: OrderCouponUpdateAssigned
		"""

		self.coupon_code = coupon_code
		return self

	def set_assigned(self, assigned: bool) -> 'OrderCouponUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: OrderCouponUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCouponUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCouponUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCouponUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon
		elif self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request OrderPriceGroup_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderpricegroup_update_assigned
"""


class OrderPriceGroupUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderPriceGroupUpdateAssigned Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.price_group_id = None
		self.price_group_name = None
		self.assigned = False
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderPriceGroup_Update_Assigned'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_order_id(self, order_id: int) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderPriceGroupUpdateAssigned
		"""

		self.order_id = order_id
		return self

	def set_price_group_id(self, price_group_id: int) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: OrderPriceGroupUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: OrderPriceGroupUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: OrderPriceGroupUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderPriceGroupUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderPriceGroupUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request OrderItemList_CreateReturn. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitemlist_createreturn
"""


class OrderItemListCreateReturn(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemListCreateReturn Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.line_ids = []
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItemList_CreateReturn'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_ids(self):
		"""
		Get Line_IDs.

		:returns: list
		"""

		return self.line_ids

	def set_order_id(self, order_id: int) -> 'OrderItemListCreateReturn':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemListCreateReturn
		"""

		self.order_id = order_id
		return self
	
	def add_line_id(self, line_id) -> 'OrderItemListCreateReturn':
		"""
		Add Line_IDs.

		:param line_id: int
		:returns: {OrderItemListCreateReturn}
		"""

		self.line_ids.append(line_id)
		return self

	def add_order_item(self, order_item: merchantapi.model.OrderItem) -> 'OrderItemListCreateReturn':
		"""
		Add OrderItem model.

		:param order_item: OrderItem
		:raises Exception:
		:returns: OrderItemListCreateReturn
		"""
		if not isinstance(order_item, merchantapi.model.OrderItem):
			raise Exception('Expected an instance of OrderItem')

		if order_item.get_line_id():
			self.line_ids.append(order_item.get_line_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemListCreateReturn':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemListCreateReturn':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemListCreateReturn(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		data['Line_IDs'] = self.line_ids
		return data


"""
Handles API Request OrderReturnList_Received. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderreturnlist_received
"""


class OrderReturnListReceived(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		OrderReturnListReceived Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.returns = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderReturnList_Received'

	def get_returns(self) -> list:
		"""
		Get Returns.

		:returns: List of ReceivedReturn
		"""

		return self.returns

	def set_returns(self, returns: list) -> 'OrderReturnListReceived':
		"""
		Set Returns.

		:param returns: {ReceivedReturn[]}
		:raises Exception:
		:returns: OrderReturnListReceived
		"""

		for e in returns:
			if not isinstance(e, merchantapi.model.ReceivedReturn):
				raise Exception("")
		self.returns = returns
		return self
	
	def add_received_return(self, received_return) -> 'OrderReturnListReceived':
		"""
		Add Returns.

		:param received_return: ReceivedReturn 
		:raises Exception:
		:returns: {OrderReturnListReceived}
		"""

		if isinstance(received_return, merchantapi.model.ReceivedReturn):
			self.returns.append(received_return)
		elif isinstance(received_return, dict):
			self.returns.append(merchantapi.model.ReceivedReturn(received_return))
		else:
			raise Exception('Expected instance of ReceivedReturn or dict')
		return self

	def add_returns(self, returns: list) -> 'OrderReturnListReceived':
		"""
		Add many ReceivedReturn.

		:param returns: List of ReceivedReturn
		:raises Exception:
		:returns: OrderReturnListReceived
		"""

		for e in returns:
			if not isinstance(e, merchantapi.model.ReceivedReturn):
				raise Exception('')
			self.returns.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderReturnListReceived':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderReturnListReceived':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderReturnListReceived(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if len(self.returns):
			data['Returns'] = []

			for f in self.returns:
				data['Returns'].append(f.to_dict())
		return data


"""
Handles API Request BranchPropertyVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchpropertyversionlist_load_query
"""


class BranchPropertyVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'prop_id',
		'type',
		'code',
		'product_id',
		'cat_id',
		'sync',
		'templ_id',
		'version_id',
		'version_user_id',
		'version_user_name',
		'source_user_id',
		'source_user_name'
	]

	available_sort_fields = [
		'prop_id',
		'type',
		'code',
		'product_id',
		'cat_id',
		'sync',
		'templ_id',
		'version_id',
		'version_user_id',
		'version_user_name',
		'source_user_id',
		'source_user_name'
	]

	available_on_demand_columns = [
		'settings',
		'product',
		'category',
		'source',
		'source_notes'
	]

	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchPropertyVersionListLoadQuery Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		self.changeset_id = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchPropertyVersionList_Load_Query'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_branch_id(self, branch_id: int) -> 'BranchPropertyVersionListLoadQuery':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchPropertyVersionListLoadQuery
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchPropertyVersionListLoadQuery':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchPropertyVersionListLoadQuery
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'BranchPropertyVersionListLoadQuery':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: BranchPropertyVersionListLoadQuery
		"""

		self.edit_branch = edit_branch
		return self

	def set_changeset_id(self, changeset_id: int) -> 'BranchPropertyVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: BranchPropertyVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchPropertyVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchPropertyVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchPropertyVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id
		return data


"""
Handles API Request ChangesetPropertyVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesetpropertyversionlist_load_query
"""


class ChangesetPropertyVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'prop_id',
		'type',
		'code',
		'product_id',
		'cat_id',
		'sync',
		'version_id',
		'version_user_id',
		'version_user_name',
		'source_user_id',
		'source_user_name'
	]

	available_sort_fields = [
		'id',
		'prop_id',
		'type',
		'code',
		'product_id',
		'cat_id',
		'sync',
		'version_id',
		'version_user_id',
		'version_user_name',
		'source_user_id',
		'source_user_name'
	]

	available_on_demand_columns = [
		'settings',
		'product',
		'category',
		'source',
		'source_notes'
	]

	def __init__(self, client: Client = None, changeset: merchantapi.model.Changeset = None):
		"""
		ChangesetPropertyVersionListLoadQuery Constructor.

		:param client: Client
		:param changeset: Changeset
		"""

		super().__init__(client)
		self.changeset_id = None
		if isinstance(changeset, merchantapi.model.Changeset):
			self.set_changeset_id(changeset.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetPropertyVersionList_Load_Query'

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_changeset_id(self, changeset_id: int) -> 'ChangesetPropertyVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: ChangesetPropertyVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetPropertyVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetPropertyVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetPropertyVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Changeset_ID'] = self.get_changeset_id()

		return data


"""
Handles API Request ResourceGroupList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/resourcegrouplist_load_query
"""


class ResourceGroupListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'code'
	]

	available_sort_fields = [
		'id',
		'code'
	]

	available_on_demand_columns = [
		'linkedcssresources',
		'linkedjavascriptresources'
	]

	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		ResourceGroupListLoadQuery Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		self.changeset_id = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ResourceGroupList_Load_Query'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_branch_id(self, branch_id: int) -> 'ResourceGroupListLoadQuery':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: ResourceGroupListLoadQuery
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'ResourceGroupListLoadQuery':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: ResourceGroupListLoadQuery
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'ResourceGroupListLoadQuery':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: ResourceGroupListLoadQuery
		"""

		self.edit_branch = edit_branch
		return self

	def set_changeset_id(self, changeset_id: int) -> 'ResourceGroupListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: ResourceGroupListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ResourceGroupListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ResourceGroupListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ResourceGroupListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id
		return data


"""
Handles API Request BranchList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchlist_delete
"""


class BranchListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		BranchListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.branch_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchList_Delete'

	def get_branch_ids(self):
		"""
		Get Branch_IDs.

		:returns: list
		"""

		return self.branch_ids
	
	def add_branch_id(self, branch_id) -> 'BranchListDelete':
		"""
		Add Branch_IDs.

		:param branch_id: int
		:returns: {BranchListDelete}
		"""

		self.branch_ids.append(branch_id)
		return self

	def add_branch(self, branch: merchantapi.model.Branch) -> 'BranchListDelete':
		"""
		Add Branch model.

		:param branch: Branch
		:raises Exception:
		:returns: BranchListDelete
		"""
		if not isinstance(branch, merchantapi.model.Branch):
			raise Exception('Expected an instance of Branch')

		if branch.get_id():
			self.branch_ids.append(branch.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Branch_IDs'] = self.branch_ids
		return data


"""
Handles API Request MivaMerchantVersion. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/mivamerchantversion
"""


class MivaMerchantVersion(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		MivaMerchantVersion Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'MivaMerchantVersion'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.MivaMerchantVersion':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'MivaMerchantVersion':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.MivaMerchantVersion(self, http_response, data)


"""
Handles API Request Attribute_Load_Code. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_load_code
"""


class AttributeLoadCode(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeLoadCode Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.customer_id = None
		self.attribute_code = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_Load_Code'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def set_product_id(self, product_id: int) -> 'AttributeLoadCode':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeLoadCode
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeLoadCode':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeLoadCode
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeLoadCode':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeLoadCode
		"""

		self.edit_product = edit_product
		return self

	def set_customer_id(self, customer_id: int) -> 'AttributeLoadCode':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: AttributeLoadCode
		"""

		self.customer_id = customer_id
		return self

	def set_attribute_code(self, attribute_code: str) -> 'AttributeLoadCode':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: AttributeLoadCode
		"""

		self.attribute_code = attribute_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeLoadCode':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeLoadCode':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeLoadCode(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		data['Attribute_Code'] = self.attribute_code
		return data


"""
Handles API Request Attribute_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_insert
"""


class AttributeInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeInsert Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.code = None
		self.prompt = None
		self.type = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.copy = False
		self.required = False
		self.inventory = False
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

			self.set_product_code(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_Insert'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_type(self) -> str:
		"""
		Get Type.

		:returns: str
		"""

		return self.type

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_copy(self) -> bool:
		"""
		Get Copy.

		:returns: bool
		"""

		return self.copy

	def get_required(self) -> bool:
		"""
		Get Required.

		:returns: bool
		"""

		return self.required

	def get_inventory(self) -> bool:
		"""
		Get Inventory.

		:returns: bool
		"""

		return self.inventory

	def set_product_id(self, product_id: int) -> 'AttributeInsert':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeInsert
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeInsert
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeInsert':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeInsert
		"""

		self.edit_product = edit_product
		return self

	def set_code(self, code: str) -> 'AttributeInsert':
		"""
		Set Code.

		:param code: str
		:returns: AttributeInsert
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeInsert':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeInsert
		"""

		self.prompt = prompt
		return self

	def set_type(self, type: str) -> 'AttributeInsert':
		"""
		Set Type.

		:param type: str
		:returns: AttributeInsert
		"""

		self.type = type
		return self

	def set_image(self, image: str) -> 'AttributeInsert':
		"""
		Set Image.

		:param image: str
		:returns: AttributeInsert
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeInsert':
		"""
		Set Price.

		:param price: float
		:returns: AttributeInsert
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeInsert':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeInsert
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeInsert':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeInsert
		"""

		self.weight = weight
		return self

	def set_copy(self, copy: bool) -> 'AttributeInsert':
		"""
		Set Copy.

		:param copy: bool
		:returns: AttributeInsert
		"""

		self.copy = copy
		return self

	def set_required(self, required: bool) -> 'AttributeInsert':
		"""
		Set Required.

		:param required: bool
		:returns: AttributeInsert
		"""

		self.required = required
		return self

	def set_inventory(self, inventory: bool) -> 'AttributeInsert':
		"""
		Set Inventory.

		:param inventory: bool
		:returns: AttributeInsert
		"""

		self.inventory = inventory
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.product_code is not None:
			data['Product_Code'] = self.product_code
		data['Code'] = self.code
		if self.prompt is not None:
			data['Prompt'] = self.prompt
		data['Type'] = self.type
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.copy is not None:
			data['Copy'] = self.copy
		if self.required is not None:
			data['Required'] = self.required
		if self.inventory is not None:
			data['Inventory'] = self.inventory
		return data


"""
Handles API Request Attribute_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_update
"""


class AttributeUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_attribute: merchantapi.model.ProductAttribute = None):
		"""
		AttributeUpdate Constructor.

		:param client: Client
		:param product_attribute: ProductAttribute
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
		self.code = None
		self.prompt = None
		self.type = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.copy = False
		self.required = False
		self.inventory = False
		if isinstance(product_attribute, merchantapi.model.ProductAttribute):
			if product_attribute.get_product_id():
				self.set_product_id(product_attribute.get_product_id())

			if product_attribute.get_id():
				self.set_attribute_id(product_attribute.get_id())
			elif product_attribute.get_code():
				self.set_edit_attribute(product_attribute.get_code())
			elif product_attribute.get_code():
				self.set_attribute_code(product_attribute.get_code())

			self.set_edit_attribute(product_attribute.get_code())
			self.set_code(product_attribute.get_code())
			self.set_prompt(product_attribute.get_prompt())
			self.set_type(product_attribute.get_type())
			self.set_image(product_attribute.get_image())
			self.set_price(product_attribute.get_price())
			self.set_cost(product_attribute.get_cost())
			self.set_weight(product_attribute.get_weight())
			self.set_required(product_attribute.get_required())
			self.set_inventory(product_attribute.get_inventory())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_type(self) -> str:
		"""
		Get Type.

		:returns: str
		"""

		return self.type

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_copy(self) -> bool:
		"""
		Get Copy.

		:returns: bool
		"""

		return self.copy

	def get_required(self) -> bool:
		"""
		Get Required.

		:returns: bool
		"""

		return self.required

	def get_inventory(self) -> bool:
		"""
		Get Inventory.

		:returns: bool
		"""

		return self.inventory

	def set_product_id(self, product_id: int) -> 'AttributeUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'AttributeUpdate':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: AttributeUpdate
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'AttributeUpdate':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: AttributeUpdate
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'AttributeUpdate':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: AttributeUpdate
		"""

		self.attribute_code = attribute_code
		return self

	def set_code(self, code: str) -> 'AttributeUpdate':
		"""
		Set Code.

		:param code: str
		:returns: AttributeUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeUpdate
		"""

		self.prompt = prompt
		return self

	def set_type(self, type: str) -> 'AttributeUpdate':
		"""
		Set Type.

		:param type: str
		:returns: AttributeUpdate
		"""

		self.type = type
		return self

	def set_image(self, image: str) -> 'AttributeUpdate':
		"""
		Set Image.

		:param image: str
		:returns: AttributeUpdate
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeUpdate':
		"""
		Set Price.

		:param price: float
		:returns: AttributeUpdate
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeUpdate':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeUpdate
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeUpdate
		"""

		self.weight = weight
		return self

	def set_copy(self, copy: bool) -> 'AttributeUpdate':
		"""
		Set Copy.

		:param copy: bool
		:returns: AttributeUpdate
		"""

		self.copy = copy
		return self

	def set_required(self, required: bool) -> 'AttributeUpdate':
		"""
		Set Required.

		:param required: bool
		:returns: AttributeUpdate
		"""

		self.required = required
		return self

	def set_inventory(self, inventory: bool) -> 'AttributeUpdate':
		"""
		Set Inventory.

		:param inventory: bool
		:returns: AttributeUpdate
		"""

		self.inventory = inventory
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		if self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		if self.code is not None:
			data['Code'] = self.code
		if self.prompt is not None:
			data['Prompt'] = self.prompt
		if self.type is not None:
			data['Type'] = self.type
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.copy is not None:
			data['Copy'] = self.copy
		if self.required is not None:
			data['Required'] = self.required
		if self.inventory is not None:
			data['Inventory'] = self.inventory
		return data


"""
Handles API Request Attribute_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_delete
"""


class AttributeDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_attribute: merchantapi.model.ProductAttribute = None):
		"""
		AttributeDelete Constructor.

		:param client: Client
		:param product_attribute: ProductAttribute
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
		if isinstance(product_attribute, merchantapi.model.ProductAttribute):
			if product_attribute.get_product_id():
				self.set_product_id(product_attribute.get_product_id())

			if product_attribute.get_id():
				self.set_attribute_id(product_attribute.get_id())
			elif product_attribute.get_code():
				self.set_edit_attribute(product_attribute.get_code())

			self.set_edit_attribute(product_attribute.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_Delete'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def set_product_id(self, product_id: int) -> 'AttributeDelete':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeDelete
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeDelete':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeDelete
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeDelete':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeDelete
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'AttributeDelete':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: AttributeDelete
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'AttributeDelete':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: AttributeDelete
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'AttributeDelete':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: AttributeDelete
		"""

		self.attribute_code = attribute_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		if self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		return data


"""
Handles API Request OptionList_Load_Attribute. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/optionlist_load_attribute
"""


class OptionListLoadAttribute(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_attribute: merchantapi.model.ProductAttribute = None):
		"""
		OptionListLoadAttribute Constructor.

		:param client: Client
		:param product_attribute: ProductAttribute
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
		self.customer_id = None
		if isinstance(product_attribute, merchantapi.model.ProductAttribute):
			if product_attribute.get_product_id():
				self.set_product_id(product_attribute.get_product_id())

			if product_attribute.get_id():
				self.set_attribute_id(product_attribute.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OptionList_Load_Attribute'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def set_product_id(self, product_id: int) -> 'OptionListLoadAttribute':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: OptionListLoadAttribute
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'OptionListLoadAttribute':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: OptionListLoadAttribute
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'OptionListLoadAttribute':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: OptionListLoadAttribute
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionListLoadAttribute':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionListLoadAttribute
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'OptionListLoadAttribute':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: OptionListLoadAttribute
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'OptionListLoadAttribute':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: OptionListLoadAttribute
		"""

		self.attribute_code = attribute_code
		return self

	def set_customer_id(self, customer_id: int) -> 'OptionListLoadAttribute':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: OptionListLoadAttribute
		"""

		self.customer_id = customer_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionListLoadAttribute':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionListLoadAttribute':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionListLoadAttribute(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		return data


"""
Handles API Request Option_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/option_delete
"""


class OptionDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_option: merchantapi.model.ProductOption = None):
		"""
		OptionDelete Constructor.

		:param client: Client
		:param product_option: ProductOption
		"""

		super().__init__(client)
		self.option_id = None
		self.option_code = None
		self.attribute_id = None
		if isinstance(product_option, merchantapi.model.ProductOption):
			if product_option.get_id():
				self.set_option_id(product_option.get_id())
			elif product_option.get_code():
				self.set_option_code(product_option.get_code())

			if product_option.get_attribute_id():
				self.set_attribute_id(product_option.get_attribute_id())

			self.set_option_id(product_option.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Option_Delete'

	def get_option_id(self) -> int:
		"""
		Get Option_ID.

		:returns: int
		"""

		return self.option_id

	def get_option_code(self) -> str:
		"""
		Get Option_Code.

		:returns: str
		"""

		return self.option_code

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def set_option_id(self, option_id: int) -> 'OptionDelete':
		"""
		Set Option_ID.

		:param option_id: int
		:returns: OptionDelete
		"""

		self.option_id = option_id
		return self

	def set_option_code(self, option_code: str) -> 'OptionDelete':
		"""
		Set Option_Code.

		:param option_code: str
		:returns: OptionDelete
		"""

		self.option_code = option_code
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionDelete':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionDelete
		"""

		self.attribute_id = attribute_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.option_id is not None:
			data['Option_ID'] = self.option_id
		elif self.option_code is not None:
			data['Option_Code'] = self.option_code

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id

		if self.option_id is not None:
			data['Option_ID'] = self.option_id
		return data


"""
Handles API Request Option_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/option_insert
"""


class OptionInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_attribute: merchantapi.model.ProductAttribute = None):
		"""
		OptionInsert Constructor.

		:param client: Client
		:param product_attribute: ProductAttribute
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
		self.code = None
		self.prompt = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.default = False
		if isinstance(product_attribute, merchantapi.model.ProductAttribute):
			if product_attribute.get_product_id():
				self.set_product_id(product_attribute.get_product_id())

			if product_attribute.get_id():
				self.set_attribute_id(product_attribute.get_id())
			elif product_attribute.get_code():
				self.set_edit_attribute(product_attribute.get_code())
			elif product_attribute.get_code():
				self.set_attribute_code(product_attribute.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Option_Insert'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_default(self) -> bool:
		"""
		Get Default.

		:returns: bool
		"""

		return self.default

	def set_product_id(self, product_id: int) -> 'OptionInsert':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: OptionInsert
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'OptionInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: OptionInsert
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'OptionInsert':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: OptionInsert
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionInsert':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionInsert
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'OptionInsert':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: OptionInsert
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'OptionInsert':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: OptionInsert
		"""

		self.attribute_code = attribute_code
		return self

	def set_code(self, code: str) -> 'OptionInsert':
		"""
		Set Code.

		:param code: str
		:returns: OptionInsert
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'OptionInsert':
		"""
		Set Prompt.

		:param prompt: str
		:returns: OptionInsert
		"""

		self.prompt = prompt
		return self

	def set_image(self, image: str) -> 'OptionInsert':
		"""
		Set Image.

		:param image: str
		:returns: OptionInsert
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'OptionInsert':
		"""
		Set Price.

		:param price: float
		:returns: OptionInsert
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'OptionInsert':
		"""
		Set Cost.

		:param cost: float
		:returns: OptionInsert
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'OptionInsert':
		"""
		Set Weight.

		:param weight: float
		:returns: OptionInsert
		"""

		self.weight = weight
		return self

	def set_default(self, default: bool) -> 'OptionInsert':
		"""
		Set Default.

		:param default: bool
		:returns: OptionInsert
		"""

		self.default = default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		data['Code'] = self.code
		data['Prompt'] = self.prompt
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.default is not None:
			data['Default'] = self.default
		return data


"""
Handles API Request Option_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/option_update
"""


class OptionUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_option: merchantapi.model.ProductOption = None):
		"""
		OptionUpdate Constructor.

		:param client: Client
		:param product_option: ProductOption
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.option_id = None
		self.option_code = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
		self.code = None
		self.prompt = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.default = False
		if isinstance(product_option, merchantapi.model.ProductOption):
			if product_option.get_product_id():
				self.set_product_id(product_option.get_product_id())

			if product_option.get_attribute_id():
				self.set_attribute_id(product_option.get_attribute_id())

			if product_option.get_id():
				self.set_option_id(product_option.get_id())
			elif product_option.get_code():
				self.set_option_code(product_option.get_code())

			self.set_code(product_option.get_code())
			self.set_prompt(product_option.get_prompt())
			self.set_image(product_option.get_image())
			self.set_price(product_option.get_price())
			self.set_cost(product_option.get_cost())
			self.set_weight(product_option.get_weight())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Option_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_option_id(self) -> int:
		"""
		Get Option_ID.

		:returns: int
		"""

		return self.option_id

	def get_option_code(self) -> str:
		"""
		Get Option_Code.

		:returns: str
		"""

		return self.option_code

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_default(self) -> bool:
		"""
		Get Default.

		:returns: bool
		"""

		return self.default

	def set_product_id(self, product_id: int) -> 'OptionUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: OptionUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'OptionUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: OptionUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'OptionUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: OptionUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_option_id(self, option_id: int) -> 'OptionUpdate':
		"""
		Set Option_ID.

		:param option_id: int
		:returns: OptionUpdate
		"""

		self.option_id = option_id
		return self

	def set_option_code(self, option_code: str) -> 'OptionUpdate':
		"""
		Set Option_Code.

		:param option_code: str
		:returns: OptionUpdate
		"""

		self.option_code = option_code
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionUpdate':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionUpdate
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'OptionUpdate':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: OptionUpdate
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'OptionUpdate':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: OptionUpdate
		"""

		self.attribute_code = attribute_code
		return self

	def set_code(self, code: str) -> 'OptionUpdate':
		"""
		Set Code.

		:param code: str
		:returns: OptionUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'OptionUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: OptionUpdate
		"""

		self.prompt = prompt
		return self

	def set_image(self, image: str) -> 'OptionUpdate':
		"""
		Set Image.

		:param image: str
		:returns: OptionUpdate
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'OptionUpdate':
		"""
		Set Price.

		:param price: float
		:returns: OptionUpdate
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'OptionUpdate':
		"""
		Set Cost.

		:param cost: float
		:returns: OptionUpdate
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'OptionUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: OptionUpdate
		"""

		self.weight = weight
		return self

	def set_default(self, default: bool) -> 'OptionUpdate':
		"""
		Set Default.

		:param default: bool
		:returns: OptionUpdate
		"""

		self.default = default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		if self.option_id is not None:
			data['Option_ID'] = self.option_id
		elif self.option_code is not None:
			data['Option_Code'] = self.option_code

		if self.code is not None:
			data['Code'] = self.code
		if self.prompt is not None:
			data['Prompt'] = self.prompt
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.default is not None:
			data['Default'] = self.default
		return data


"""
Handles API Request Option_Load_Code. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/option_load_code
"""


class OptionLoadCode(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		OptionLoadCode Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.attribute_code = None
		self.edit_attribute = None
		self.option_code = None
		self.customer_id = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Option_Load_Code'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_option_code(self) -> str:
		"""
		Get Option_Code.

		:returns: str
		"""

		return self.option_code

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def set_product_id(self, product_id: int) -> 'OptionLoadCode':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: OptionLoadCode
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'OptionLoadCode':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: OptionLoadCode
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'OptionLoadCode':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: OptionLoadCode
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionLoadCode':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionLoadCode
		"""

		self.attribute_id = attribute_id
		return self

	def set_attribute_code(self, attribute_code: str) -> 'OptionLoadCode':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: OptionLoadCode
		"""

		self.attribute_code = attribute_code
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'OptionLoadCode':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: OptionLoadCode
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_option_code(self, option_code: str) -> 'OptionLoadCode':
		"""
		Set Option_Code.

		:param option_code: str
		:returns: OptionLoadCode
		"""

		self.option_code = option_code
		return self

	def set_customer_id(self, customer_id: int) -> 'OptionLoadCode':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: OptionLoadCode
		"""

		self.customer_id = customer_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionLoadCode':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionLoadCode':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionLoadCode(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute

		if self.option_code is not None:
			data['Option_Code'] = self.option_code

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		return data


"""
Handles API Request Option_Set_Default. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/option_set_default
"""


class OptionSetDefault(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_option: merchantapi.model.ProductOption = None):
		"""
		OptionSetDefault Constructor.

		:param client: Client
		:param product_option: ProductOption
		"""

		super().__init__(client)
		self.option_id = None
		self.option_code = None
		self.attribute_id = None
		self.option_default = False
		if isinstance(product_option, merchantapi.model.ProductOption):
			if product_option.get_id():
				self.set_option_id(product_option.get_id())
			elif product_option.get_code():
				self.set_option_code(product_option.get_code())

			if product_option.get_attribute_id():
				self.set_attribute_id(product_option.get_attribute_id())

			self.set_option_code(product_option.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Option_Set_Default'

	def get_option_id(self) -> int:
		"""
		Get Option_ID.

		:returns: int
		"""

		return self.option_id

	def get_option_code(self) -> str:
		"""
		Get Option_Code.

		:returns: str
		"""

		return self.option_code

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_option_default(self) -> bool:
		"""
		Get Option_Default.

		:returns: bool
		"""

		return self.option_default

	def set_option_id(self, option_id: int) -> 'OptionSetDefault':
		"""
		Set Option_ID.

		:param option_id: int
		:returns: OptionSetDefault
		"""

		self.option_id = option_id
		return self

	def set_option_code(self, option_code: str) -> 'OptionSetDefault':
		"""
		Set Option_Code.

		:param option_code: str
		:returns: OptionSetDefault
		"""

		self.option_code = option_code
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionSetDefault':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionSetDefault
		"""

		self.attribute_id = attribute_id
		return self

	def set_option_default(self, option_default: bool) -> 'OptionSetDefault':
		"""
		Set Option_Default.

		:param option_default: bool
		:returns: OptionSetDefault
		"""

		self.option_default = option_default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionSetDefault':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionSetDefault':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionSetDefault(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.option_id is not None:
			data['Option_ID'] = self.option_id
		elif self.option_code is not None:
			data['Option_Code'] = self.option_code

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id

		if self.option_code is not None:
			data['Option_Code'] = self.option_code
		if self.option_default is not None:
			data['Option_Default'] = self.option_default
		return data


"""
Handles API Request AttributeAndOptionList_Load_Product. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributeandoptionlist_load_product
"""


class AttributeAndOptionListLoadProduct(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeAndOptionListLoadProduct Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.customer_id = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())

			self.set_product_code(product.get_code())
			self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeAndOptionList_Load_Product'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def set_product_id(self, product_id: int) -> 'AttributeAndOptionListLoadProduct':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeAndOptionListLoadProduct
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeAndOptionListLoadProduct':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeAndOptionListLoadProduct
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeAndOptionListLoadProduct':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeAndOptionListLoadProduct
		"""

		self.edit_product = edit_product
		return self

	def set_customer_id(self, customer_id: int) -> 'AttributeAndOptionListLoadProduct':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: AttributeAndOptionListLoadProduct
		"""

		self.customer_id = customer_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeAndOptionListLoadProduct':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeAndOptionListLoadProduct':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeAndOptionListLoadProduct(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.product_code is not None:
			data['Product_Code'] = self.product_code
		if self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		return data


"""
Handles API Request OrderShipmentList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordershipmentlist_load_query
"""


class OrderShipmentListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'order_id',
		'code',
		'tracknum',
		'tracktype',
		'weight',
		'cost',
		'status',
		'ship_date',
		'batch_id',
		'order_batch_id',
		'order_pay_id',
		'order_status',
		'order_pay_status',
		'order_stk_status',
		'order_orderdate',
		'order_dt_instock',
		'order_cust_id',
		'order_ship_res',
		'order_ship_fname',
		'order_ship_lname',
		'order_ship_email',
		'order_ship_comp',
		'order_ship_phone',
		'order_ship_fax',
		'order_ship_addr1',
		'order_ship_addr2',
		'order_ship_city',
		'order_ship_state',
		'order_ship_zip',
		'order_ship_cntry',
		'order_bill_fname',
		'order_bill_lname',
		'order_bill_email',
		'order_bill_comp',
		'order_bill_phone',
		'order_bill_fax',
		'order_bill_addr1',
		'order_bill_addr2',
		'order_bill_city',
		'order_bill_state',
		'order_bill_zip',
		'order_bill_cntry',
		'order_ship_id',
		'order_ship_data',
		'order_source',
		'order_source_id',
		'order_total',
		'order_total_ship',
		'order_total_tax',
		'order_total_auth',
		'order_total_capt',
		'order_total_rfnd',
		'order_net_capt',
		'order_pend_count',
		'order_bord_count',
		'order_note_count'
	]

	available_sort_fields = [
		'id',
		'order_id',
		'code',
		'tracknum',
		'tracktype',
		'weight',
		'cost',
		'status',
		'ship_date',
		'batch_id',
		'order_batch_id',
		'order_pay_id',
		'order_status',
		'order_pay_status',
		'order_stk_status',
		'order_dt_instock',
		'order_orderdate',
		'order_cust_id',
		'order_ship_res',
		'order_ship_fname',
		'order_ship_lname',
		'order_ship_email',
		'order_ship_comp',
		'order_ship_phone',
		'order_ship_fax',
		'order_ship_addr1',
		'order_ship_addr2',
		'order_ship_city',
		'order_ship_state',
		'order_ship_zip',
		'order_ship_cntry',
		'order_bill_fname',
		'order_bill_lname',
		'order_bill_email',
		'order_bill_comp',
		'order_bill_phone',
		'order_bill_fax',
		'order_bill_addr1',
		'order_bill_addr2',
		'order_bill_city',
		'order_bill_state',
		'order_bill_zip',
		'order_bill_cntry',
		'order_ship_id',
		'order_ship_data',
		'order_source',
		'order_source_id',
		'order_total',
		'order_total_ship',
		'order_total_tax',
		'order_total_auth',
		'order_total_capt',
		'order_total_rfnd',
		'order_net_capt',
		'order_pend_count',
		'order_bord_count',
		'order_note_count'
	]

	available_on_demand_columns = [
		'items',
		'include_order'
	]

	def __init__(self, client: Client = None):
		"""
		OrderShipmentListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderShipmentList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderShipmentListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderShipmentListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderShipmentListLoadQuery(self, http_response, data)


"""
Handles API Request OrderItem_Split. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitem_split
"""


class OrderItemSplit(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order_item: merchantapi.model.OrderItem = None):
		"""
		OrderItemSplit Constructor.

		:param client: Client
		:param order_item: OrderItem
		"""

		super().__init__(client)
		self.order_id = None
		self.line_id = None
		self.quantity = None
		if isinstance(order_item, merchantapi.model.OrderItem):
			if order_item.get_order_id():
				self.set_order_id(order_item.get_order_id())

			if order_item.get_line_id():
				self.set_line_id(order_item.get_line_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItem_Split'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_id(self) -> int:
		"""
		Get Line_ID.

		:returns: int
		"""

		return self.line_id

	def get_quantity(self) -> int:
		"""
		Get Quantity.

		:returns: int
		"""

		return self.quantity

	def set_order_id(self, order_id: int) -> 'OrderItemSplit':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemSplit
		"""

		self.order_id = order_id
		return self

	def set_line_id(self, line_id: int) -> 'OrderItemSplit':
		"""
		Set Line_ID.

		:param line_id: int
		:returns: OrderItemSplit
		"""

		self.line_id = line_id
		return self

	def set_quantity(self, quantity: int) -> 'OrderItemSplit':
		"""
		Set Quantity.

		:param quantity: int
		:returns: OrderItemSplit
		"""

		self.quantity = quantity
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemSplit':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemSplit':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemSplit(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.line_id is not None:
			data['Line_ID'] = self.line_id

		data['Quantity'] = self.quantity
		return data


"""
Handles API Request OrderItemList_RemoveFromShipment. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitemlist_removefromshipment
"""


class OrderItemListRemoveFromShipment(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemListRemoveFromShipment Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.line_ids = []
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItemList_RemoveFromShipment'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_ids(self):
		"""
		Get Line_IDs.

		:returns: list
		"""

		return self.line_ids

	def set_order_id(self, order_id: int) -> 'OrderItemListRemoveFromShipment':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemListRemoveFromShipment
		"""

		self.order_id = order_id
		return self
	
	def add_line_id(self, line_id) -> 'OrderItemListRemoveFromShipment':
		"""
		Add Line_IDs.

		:param line_id: int
		:returns: {OrderItemListRemoveFromShipment}
		"""

		self.line_ids.append(line_id)
		return self

	def add_order_item(self, order_item: merchantapi.model.OrderItem) -> 'OrderItemListRemoveFromShipment':
		"""
		Add OrderItem model.

		:param order_item: OrderItem
		:raises Exception:
		:returns: OrderItemListRemoveFromShipment
		"""
		if not isinstance(order_item, merchantapi.model.OrderItem):
			raise Exception('Expected an instance of OrderItem')

		if order_item.get_line_id():
			self.line_ids.append(order_item.get_line_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemListRemoveFromShipment':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemListRemoveFromShipment':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemListRemoveFromShipment(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		data['Line_IDs'] = self.line_ids
		return data


"""
Handles API Request CustomerAddress_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddress_insert
"""


class CustomerAddressInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerAddressInsert Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.customer_login = None
		self.description = None
		self.first_name = None
		self.last_name = None
		self.email = None
		self.phone = None
		self.fax = None
		self.company = None
		self.address1 = None
		self.address2 = None
		self.city = None
		self.state = None
		self.zip = None
		self.country = None
		self.residential = False
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddress_Insert'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_first_name(self) -> str:
		"""
		Get FirstName.

		:returns: str
		"""

		return self.first_name

	def get_last_name(self) -> str:
		"""
		Get LastName.

		:returns: str
		"""

		return self.last_name

	def get_email(self) -> str:
		"""
		Get Email.

		:returns: str
		"""

		return self.email

	def get_phone(self) -> str:
		"""
		Get Phone.

		:returns: str
		"""

		return self.phone

	def get_fax(self) -> str:
		"""
		Get Fax.

		:returns: str
		"""

		return self.fax

	def get_company(self) -> str:
		"""
		Get Company.

		:returns: str
		"""

		return self.company

	def get_address1(self) -> str:
		"""
		Get Address1.

		:returns: str
		"""

		return self.address1

	def get_address2(self) -> str:
		"""
		Get Address2.

		:returns: str
		"""

		return self.address2

	def get_city(self) -> str:
		"""
		Get City.

		:returns: str
		"""

		return self.city

	def get_state(self) -> str:
		"""
		Get State.

		:returns: str
		"""

		return self.state

	def get_zip(self) -> str:
		"""
		Get Zip.

		:returns: str
		"""

		return self.zip

	def get_country(self) -> str:
		"""
		Get Country.

		:returns: str
		"""

		return self.country

	def get_residential(self) -> bool:
		"""
		Get Residential.

		:returns: bool
		"""

		return self.residential

	def set_customer_id(self, customer_id: int) -> 'CustomerAddressInsert':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerAddressInsert
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerAddressInsert':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerAddressInsert
		"""

		self.customer_login = customer_login
		return self

	def set_description(self, description: str) -> 'CustomerAddressInsert':
		"""
		Set Description.

		:param description: str
		:returns: CustomerAddressInsert
		"""

		self.description = description
		return self

	def set_first_name(self, first_name: str) -> 'CustomerAddressInsert':
		"""
		Set FirstName.

		:param first_name: str
		:returns: CustomerAddressInsert
		"""

		self.first_name = first_name
		return self

	def set_last_name(self, last_name: str) -> 'CustomerAddressInsert':
		"""
		Set LastName.

		:param last_name: str
		:returns: CustomerAddressInsert
		"""

		self.last_name = last_name
		return self

	def set_email(self, email: str) -> 'CustomerAddressInsert':
		"""
		Set Email.

		:param email: str
		:returns: CustomerAddressInsert
		"""

		self.email = email
		return self

	def set_phone(self, phone: str) -> 'CustomerAddressInsert':
		"""
		Set Phone.

		:param phone: str
		:returns: CustomerAddressInsert
		"""

		self.phone = phone
		return self

	def set_fax(self, fax: str) -> 'CustomerAddressInsert':
		"""
		Set Fax.

		:param fax: str
		:returns: CustomerAddressInsert
		"""

		self.fax = fax
		return self

	def set_company(self, company: str) -> 'CustomerAddressInsert':
		"""
		Set Company.

		:param company: str
		:returns: CustomerAddressInsert
		"""

		self.company = company
		return self

	def set_address1(self, address1: str) -> 'CustomerAddressInsert':
		"""
		Set Address1.

		:param address1: str
		:returns: CustomerAddressInsert
		"""

		self.address1 = address1
		return self

	def set_address2(self, address2: str) -> 'CustomerAddressInsert':
		"""
		Set Address2.

		:param address2: str
		:returns: CustomerAddressInsert
		"""

		self.address2 = address2
		return self

	def set_city(self, city: str) -> 'CustomerAddressInsert':
		"""
		Set City.

		:param city: str
		:returns: CustomerAddressInsert
		"""

		self.city = city
		return self

	def set_state(self, state: str) -> 'CustomerAddressInsert':
		"""
		Set State.

		:param state: str
		:returns: CustomerAddressInsert
		"""

		self.state = state
		return self

	def set_zip(self, zip: str) -> 'CustomerAddressInsert':
		"""
		Set Zip.

		:param zip: str
		:returns: CustomerAddressInsert
		"""

		self.zip = zip
		return self

	def set_country(self, country: str) -> 'CustomerAddressInsert':
		"""
		Set Country.

		:param country: str
		:returns: CustomerAddressInsert
		"""

		self.country = country
		return self

	def set_residential(self, residential: bool) -> 'CustomerAddressInsert':
		"""
		Set Residential.

		:param residential: bool
		:returns: CustomerAddressInsert
		"""

		self.residential = residential
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.description is not None:
			data['Description'] = self.description
		if self.first_name is not None:
			data['FirstName'] = self.first_name
		if self.last_name is not None:
			data['LastName'] = self.last_name
		if self.email is not None:
			data['Email'] = self.email
		if self.phone is not None:
			data['Phone'] = self.phone
		if self.fax is not None:
			data['Fax'] = self.fax
		if self.company is not None:
			data['Company'] = self.company
		if self.address1 is not None:
			data['Address1'] = self.address1
		if self.address2 is not None:
			data['Address2'] = self.address2
		if self.city is not None:
			data['City'] = self.city
		if self.state is not None:
			data['State'] = self.state
		if self.zip is not None:
			data['Zip'] = self.zip
		if self.country is not None:
			data['Country'] = self.country
		if self.residential is not None:
			data['Residential'] = self.residential
		return data


"""
Handles API Request CustomerAddress_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddress_update
"""


class CustomerAddressUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer_address: merchantapi.model.CustomerAddress = None):
		"""
		CustomerAddressUpdate Constructor.

		:param client: Client
		:param customer_address: CustomerAddress
		"""

		super().__init__(client)
		self.address_id = None
		self.customer_address_id = None
		self.customer_id = None
		self.customer_login = None
		self.description = None
		self.first_name = None
		self.last_name = None
		self.email = None
		self.phone = None
		self.fax = None
		self.company = None
		self.address1 = None
		self.address2 = None
		self.city = None
		self.state = None
		self.zip = None
		self.country = None
		self.residential = False
		if isinstance(customer_address, merchantapi.model.CustomerAddress):
			if customer_address.get_customer_id():
				self.set_customer_id(customer_address.get_customer_id())

			if customer_address.get_id():
				self.set_address_id(customer_address.get_id())

			self.set_description(customer_address.get_description())
			self.set_first_name(customer_address.get_first_name())
			self.set_last_name(customer_address.get_last_name())
			self.set_email(customer_address.get_email())
			self.set_phone(customer_address.get_phone())
			self.set_fax(customer_address.get_fax())
			self.set_company(customer_address.get_company())
			self.set_address1(customer_address.get_address1())
			self.set_address2(customer_address.get_address2())
			self.set_city(customer_address.get_city())
			self.set_state(customer_address.get_state())
			self.set_zip(customer_address.get_zip())
			self.set_country(customer_address.get_country())
			self.set_residential(customer_address.get_residential())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddress_Update'

	def get_address_id(self) -> int:
		"""
		Get Address_ID.

		:returns: int
		"""

		return self.address_id

	def get_customer_address_id(self) -> int:
		"""
		Get CustomerAddress_ID.

		:returns: int
		"""

		return self.customer_address_id

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_first_name(self) -> str:
		"""
		Get FirstName.

		:returns: str
		"""

		return self.first_name

	def get_last_name(self) -> str:
		"""
		Get LastName.

		:returns: str
		"""

		return self.last_name

	def get_email(self) -> str:
		"""
		Get Email.

		:returns: str
		"""

		return self.email

	def get_phone(self) -> str:
		"""
		Get Phone.

		:returns: str
		"""

		return self.phone

	def get_fax(self) -> str:
		"""
		Get Fax.

		:returns: str
		"""

		return self.fax

	def get_company(self) -> str:
		"""
		Get Company.

		:returns: str
		"""

		return self.company

	def get_address1(self) -> str:
		"""
		Get Address1.

		:returns: str
		"""

		return self.address1

	def get_address2(self) -> str:
		"""
		Get Address2.

		:returns: str
		"""

		return self.address2

	def get_city(self) -> str:
		"""
		Get City.

		:returns: str
		"""

		return self.city

	def get_state(self) -> str:
		"""
		Get State.

		:returns: str
		"""

		return self.state

	def get_zip(self) -> str:
		"""
		Get Zip.

		:returns: str
		"""

		return self.zip

	def get_country(self) -> str:
		"""
		Get Country.

		:returns: str
		"""

		return self.country

	def get_residential(self) -> bool:
		"""
		Get Residential.

		:returns: bool
		"""

		return self.residential

	def set_address_id(self, address_id: int) -> 'CustomerAddressUpdate':
		"""
		Set Address_ID.

		:param address_id: int
		:returns: CustomerAddressUpdate
		"""

		self.address_id = address_id
		return self

	def set_customer_address_id(self, customer_address_id: int) -> 'CustomerAddressUpdate':
		"""
		Set CustomerAddress_ID.

		:param customer_address_id: int
		:returns: CustomerAddressUpdate
		"""

		self.customer_address_id = customer_address_id
		return self

	def set_customer_id(self, customer_id: int) -> 'CustomerAddressUpdate':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerAddressUpdate
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerAddressUpdate':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerAddressUpdate
		"""

		self.customer_login = customer_login
		return self

	def set_description(self, description: str) -> 'CustomerAddressUpdate':
		"""
		Set Description.

		:param description: str
		:returns: CustomerAddressUpdate
		"""

		self.description = description
		return self

	def set_first_name(self, first_name: str) -> 'CustomerAddressUpdate':
		"""
		Set FirstName.

		:param first_name: str
		:returns: CustomerAddressUpdate
		"""

		self.first_name = first_name
		return self

	def set_last_name(self, last_name: str) -> 'CustomerAddressUpdate':
		"""
		Set LastName.

		:param last_name: str
		:returns: CustomerAddressUpdate
		"""

		self.last_name = last_name
		return self

	def set_email(self, email: str) -> 'CustomerAddressUpdate':
		"""
		Set Email.

		:param email: str
		:returns: CustomerAddressUpdate
		"""

		self.email = email
		return self

	def set_phone(self, phone: str) -> 'CustomerAddressUpdate':
		"""
		Set Phone.

		:param phone: str
		:returns: CustomerAddressUpdate
		"""

		self.phone = phone
		return self

	def set_fax(self, fax: str) -> 'CustomerAddressUpdate':
		"""
		Set Fax.

		:param fax: str
		:returns: CustomerAddressUpdate
		"""

		self.fax = fax
		return self

	def set_company(self, company: str) -> 'CustomerAddressUpdate':
		"""
		Set Company.

		:param company: str
		:returns: CustomerAddressUpdate
		"""

		self.company = company
		return self

	def set_address1(self, address1: str) -> 'CustomerAddressUpdate':
		"""
		Set Address1.

		:param address1: str
		:returns: CustomerAddressUpdate
		"""

		self.address1 = address1
		return self

	def set_address2(self, address2: str) -> 'CustomerAddressUpdate':
		"""
		Set Address2.

		:param address2: str
		:returns: CustomerAddressUpdate
		"""

		self.address2 = address2
		return self

	def set_city(self, city: str) -> 'CustomerAddressUpdate':
		"""
		Set City.

		:param city: str
		:returns: CustomerAddressUpdate
		"""

		self.city = city
		return self

	def set_state(self, state: str) -> 'CustomerAddressUpdate':
		"""
		Set State.

		:param state: str
		:returns: CustomerAddressUpdate
		"""

		self.state = state
		return self

	def set_zip(self, zip: str) -> 'CustomerAddressUpdate':
		"""
		Set Zip.

		:param zip: str
		:returns: CustomerAddressUpdate
		"""

		self.zip = zip
		return self

	def set_country(self, country: str) -> 'CustomerAddressUpdate':
		"""
		Set Country.

		:param country: str
		:returns: CustomerAddressUpdate
		"""

		self.country = country
		return self

	def set_residential(self, residential: bool) -> 'CustomerAddressUpdate':
		"""
		Set Residential.

		:param residential: bool
		:returns: CustomerAddressUpdate
		"""

		self.residential = residential
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id

		if self.address_id is not None:
			data['Address_ID'] = self.address_id
		elif self.customer_address_id is not None:
			data['CustomerAddress_ID'] = self.customer_address_id

		if self.description is not None:
			data['Description'] = self.description
		if self.first_name is not None:
			data['FirstName'] = self.first_name
		if self.last_name is not None:
			data['LastName'] = self.last_name
		if self.email is not None:
			data['Email'] = self.email
		if self.phone is not None:
			data['Phone'] = self.phone
		if self.fax is not None:
			data['Fax'] = self.fax
		if self.company is not None:
			data['Company'] = self.company
		if self.address1 is not None:
			data['Address1'] = self.address1
		if self.address2 is not None:
			data['Address2'] = self.address2
		if self.city is not None:
			data['City'] = self.city
		if self.state is not None:
			data['State'] = self.state
		if self.zip is not None:
			data['Zip'] = self.zip
		if self.country is not None:
			data['Country'] = self.country
		if self.residential is not None:
			data['Residential'] = self.residential
		return data


"""
Handles API Request CustomerAddress_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddress_delete
"""


class CustomerAddressDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer_address: merchantapi.model.CustomerAddress = None):
		"""
		CustomerAddressDelete Constructor.

		:param client: Client
		:param customer_address: CustomerAddress
		"""

		super().__init__(client)
		self.address_id = None
		self.customer_address_id = None
		self.customer_id = None
		self.customer_login = None
		self.edit_customer = None
		if isinstance(customer_address, merchantapi.model.CustomerAddress):
			if customer_address.get_customer_id():
				self.set_customer_id(customer_address.get_customer_id())

			if customer_address.get_id():
				self.set_address_id(customer_address.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddress_Delete'

	def get_address_id(self) -> int:
		"""
		Get Address_ID.

		:returns: int
		"""

		return self.address_id

	def get_customer_address_id(self) -> int:
		"""
		Get CustomerAddress_ID.

		:returns: int
		"""

		return self.customer_address_id

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def set_address_id(self, address_id: int) -> 'CustomerAddressDelete':
		"""
		Set Address_ID.

		:param address_id: int
		:returns: CustomerAddressDelete
		"""

		self.address_id = address_id
		return self

	def set_customer_address_id(self, customer_address_id: int) -> 'CustomerAddressDelete':
		"""
		Set CustomerAddress_ID.

		:param customer_address_id: int
		:returns: CustomerAddressDelete
		"""

		self.customer_address_id = customer_address_id
		return self

	def set_customer_id(self, customer_id: int) -> 'CustomerAddressDelete':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerAddressDelete
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerAddressDelete':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerAddressDelete
		"""

		self.customer_login = customer_login
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerAddressDelete':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerAddressDelete
		"""

		self.edit_customer = edit_customer
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer

		if self.address_id is not None:
			data['Address_ID'] = self.address_id
		elif self.customer_address_id is not None:
			data['CustomerAddress_ID'] = self.customer_address_id

		return data


"""
Handles API Request CustomerAddressList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddresslist_delete
"""


class CustomerAddressListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerAddressListDelete Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.customer_login = None
		self.edit_customer = None
		self.customer_address_ids = []
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_customer_login(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddressList_Delete'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_address_ids(self):
		"""
		Get CustomerAddress_IDs.

		:returns: list
		"""

		return self.customer_address_ids

	def set_customer_id(self, customer_id: int) -> 'CustomerAddressListDelete':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerAddressListDelete
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerAddressListDelete':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerAddressListDelete
		"""

		self.customer_login = customer_login
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerAddressListDelete':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerAddressListDelete
		"""

		self.edit_customer = edit_customer
		return self
	
	def add_customer_address_id(self, customer_address_id) -> 'CustomerAddressListDelete':
		"""
		Add CustomerAddress_IDs.

		:param customer_address_id: int
		:returns: {CustomerAddressListDelete}
		"""

		self.customer_address_ids.append(customer_address_id)
		return self

	def add_customer_address(self, customer_address: merchantapi.model.CustomerAddress) -> 'CustomerAddressListDelete':
		"""
		Add CustomerAddress model.

		:param customer_address: CustomerAddress
		:raises Exception:
		:returns: CustomerAddressListDelete
		"""
		if not isinstance(customer_address, merchantapi.model.CustomerAddress):
			raise Exception('Expected an instance of CustomerAddress')

		if customer_address.get_id():
			self.customer_address_ids.append(customer_address.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer

		data['CustomerAddress_IDs'] = self.customer_address_ids
		return data


"""
Handles API Request CustomerAddress_Update_Residential. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddress_update_residential
"""


class CustomerAddressUpdateResidential(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer_address: merchantapi.model.CustomerAddress = None):
		"""
		CustomerAddressUpdateResidential Constructor.

		:param client: Client
		:param customer_address: CustomerAddress
		"""

		super().__init__(client)
		self.address_id = None
		self.customer_address_id = None
		self.residential = False
		if isinstance(customer_address, merchantapi.model.CustomerAddress):
			if customer_address.get_id():
				self.set_address_id(customer_address.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddress_Update_Residential'

	def get_address_id(self) -> int:
		"""
		Get Address_ID.

		:returns: int
		"""

		return self.address_id

	def get_customer_address_id(self) -> int:
		"""
		Get CustomerAddress_ID.

		:returns: int
		"""

		return self.customer_address_id

	def get_residential(self) -> bool:
		"""
		Get Residential.

		:returns: bool
		"""

		return self.residential

	def set_address_id(self, address_id: int) -> 'CustomerAddressUpdateResidential':
		"""
		Set Address_ID.

		:param address_id: int
		:returns: CustomerAddressUpdateResidential
		"""

		self.address_id = address_id
		return self

	def set_customer_address_id(self, customer_address_id: int) -> 'CustomerAddressUpdateResidential':
		"""
		Set CustomerAddress_ID.

		:param customer_address_id: int
		:returns: CustomerAddressUpdateResidential
		"""

		self.customer_address_id = customer_address_id
		return self

	def set_residential(self, residential: bool) -> 'CustomerAddressUpdateResidential':
		"""
		Set Residential.

		:param residential: bool
		:returns: CustomerAddressUpdateResidential
		"""

		self.residential = residential
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressUpdateResidential':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressUpdateResidential':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressUpdateResidential(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.address_id is not None:
			data['Address_ID'] = self.address_id
		elif self.customer_address_id is not None:
			data['CustomerAddress_ID'] = self.customer_address_id

		if self.residential is not None:
			data['Residential'] = self.residential
		return data


"""
Handles API Request URIList_Load_Query. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/urilist_load_query
"""


class URIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'uri',
		'screen',
		'status',
		'canonical',
		'store_name',
		'page_code',
		'page_name',
		'category_code',
		'category_name',
		'product_code',
		'product_sku',
		'product_name',
		'feed_code',
		'feed_name'
	]

	available_sort_fields = [
		'id',
		'uri',
		'screen',
		'status',
		'canonical',
		'store_name',
		'page_code',
		'page_name',
		'category_code',
		'category_name',
		'product_code',
		'product_sku',
		'product_name',
		'feed_code',
		'feed_name'
	]

	def __init__(self, client: Client = None):
		"""
		URIListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URIList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIListLoadQuery(self, http_response, data)


"""
Handles API Request URI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/uri_insert
"""


class URIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		URIInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.uri = None
		self.destination_type = None
		self.destination = None
		self.status = None
		self.canonical = False

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URI_Insert'

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_destination_type(self) -> str:
		"""
		Get Destination_Type.

		:returns: str
		"""

		return self.destination_type

	def get_destination(self) -> str:
		"""
		Get Destination.

		:returns: str
		"""

		return self.destination

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def set_uri(self, uri: str) -> 'URIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: URIInsert
		"""

		self.uri = uri
		return self

	def set_destination_type(self, destination_type: str) -> 'URIInsert':
		"""
		Set Destination_Type.

		:param destination_type: str
		:returns: URIInsert
		"""

		self.destination_type = destination_type
		return self

	def set_destination(self, destination: str) -> 'URIInsert':
		"""
		Set Destination.

		:param destination: str
		:returns: URIInsert
		"""

		self.destination = destination
		return self

	def set_status(self, status: int) -> 'URIInsert':
		"""
		Set Status.

		:param status: int
		:returns: URIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'URIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: URIInsert
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri is not None:
			data['URI'] = self.uri
		if self.destination_type is not None:
			data['Destination_Type'] = self.destination_type
		if self.destination is not None:
			data['Destination'] = self.destination
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request ProductURI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/producturi_insert
"""


class ProductURIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductURIInsert Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.uri = None
		self.status = None
		self.canonical = False
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_product_code(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductURI_Insert'

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def set_uri(self, uri: str) -> 'ProductURIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: ProductURIInsert
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'ProductURIInsert':
		"""
		Set Status.

		:param status: int
		:returns: ProductURIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'ProductURIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: ProductURIInsert
		"""

		self.canonical = canonical
		return self

	def set_product_id(self, product_id: int) -> 'ProductURIInsert':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductURIInsert
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductURIInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductURIInsert
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductURIInsert':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductURIInsert
		"""

		self.edit_product = edit_product
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductURIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductURIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductURIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request CategoryURI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryuri_insert
"""


class CategoryURIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryURIInsert Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.uri = None
		self.status = None
		self.canonical = False
		self.category_id = None
		self.category_code = None
		self.edit_category = None
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_category_code(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryURI_Insert'

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def set_uri(self, uri: str) -> 'CategoryURIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: CategoryURIInsert
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'CategoryURIInsert':
		"""
		Set Status.

		:param status: int
		:returns: CategoryURIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'CategoryURIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: CategoryURIInsert
		"""

		self.canonical = canonical
		return self

	def set_category_id(self, category_id: int) -> 'CategoryURIInsert':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryURIInsert
		"""

		self.category_id = category_id
		return self

	def set_category_code(self, category_code: str) -> 'CategoryURIInsert':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryURIInsert
		"""

		self.category_code = category_code
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryURIInsert':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryURIInsert
		"""

		self.edit_category = edit_category
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request PageURI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pageuri_insert
"""


class PageURIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, page: merchantapi.model.Page = None):
		"""
		PageURIInsert Constructor.

		:param client: Client
		:param page: Page
		"""

		super().__init__(client)
		self.uri = None
		self.status = None
		self.canonical = False
		self.page_id = None
		self.page_code = None
		self.edit_page = None
		if isinstance(page, merchantapi.model.Page):
			if page.get_id():
				self.set_page_id(page.get_id())
			elif page.get_code():
				self.set_page_code(page.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PageURI_Insert'

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def get_page_id(self) -> int:
		"""
		Get Page_ID.

		:returns: int
		"""

		return self.page_id

	def get_page_code(self) -> str:
		"""
		Get Page_Code.

		:returns: str
		"""

		return self.page_code

	def get_edit_page(self) -> str:
		"""
		Get Edit_Page.

		:returns: str
		"""

		return self.edit_page

	def set_uri(self, uri: str) -> 'PageURIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: PageURIInsert
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'PageURIInsert':
		"""
		Set Status.

		:param status: int
		:returns: PageURIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'PageURIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: PageURIInsert
		"""

		self.canonical = canonical
		return self

	def set_page_id(self, page_id: int) -> 'PageURIInsert':
		"""
		Set Page_ID.

		:param page_id: int
		:returns: PageURIInsert
		"""

		self.page_id = page_id
		return self

	def set_page_code(self, page_code: str) -> 'PageURIInsert':
		"""
		Set Page_Code.

		:param page_code: str
		:returns: PageURIInsert
		"""

		self.page_code = page_code
		return self

	def set_edit_page(self, edit_page: str) -> 'PageURIInsert':
		"""
		Set Edit_Page.

		:param edit_page: str
		:returns: PageURIInsert
		"""

		self.edit_page = edit_page
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageURIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageURIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageURIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.page_id is not None:
			data['Page_ID'] = self.page_id
		elif self.page_code is not None:
			data['Page_Code'] = self.page_code
		elif self.edit_page is not None:
			data['Edit_Page'] = self.edit_page

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request FeedURI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/feeduri_insert
"""


class FeedURIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		FeedURIInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.feed_id = None
		self.feed_code = None
		self.uri = None
		self.status = None
		self.canonical = False

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'FeedURI_Insert'

	def get_feed_id(self) -> int:
		"""
		Get Feed_ID.

		:returns: int
		"""

		return self.feed_id

	def get_feed_code(self) -> str:
		"""
		Get Feed_Code.

		:returns: str
		"""

		return self.feed_code

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def set_feed_id(self, feed_id: int) -> 'FeedURIInsert':
		"""
		Set Feed_ID.

		:param feed_id: int
		:returns: FeedURIInsert
		"""

		self.feed_id = feed_id
		return self

	def set_feed_code(self, feed_code: str) -> 'FeedURIInsert':
		"""
		Set Feed_Code.

		:param feed_code: str
		:returns: FeedURIInsert
		"""

		self.feed_code = feed_code
		return self

	def set_uri(self, uri: str) -> 'FeedURIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: FeedURIInsert
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'FeedURIInsert':
		"""
		Set Status.

		:param status: int
		:returns: FeedURIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'FeedURIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: FeedURIInsert
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.FeedURIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'FeedURIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.FeedURIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.feed_id is not None:
			data['Feed_ID'] = self.feed_id
		elif self.feed_code is not None:
			data['Feed_Code'] = self.feed_code

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request URI_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/uri_update
"""


class URIUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		URIUpdate Constructor.

		:param client: Client
		:param uri: Uri
		"""

		super().__init__(client)
		self.uri_id = None
		self.uri = None
		self.destination_type = None
		self.destination = None
		self.status = None
		self.canonical = False
		if isinstance(uri, merchantapi.model.Uri):
			if uri.get_id():
				self.set_uri_id(uri.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URI_Update'

	def get_uri_id(self) -> int:
		"""
		Get URI_ID.

		:returns: int
		"""

		return self.uri_id

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_destination_type(self) -> str:
		"""
		Get Destination_Type.

		:returns: str
		"""

		return self.destination_type

	def get_destination(self) -> str:
		"""
		Get Destination.

		:returns: str
		"""

		return self.destination

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def set_uri_id(self, uri_id: int) -> 'URIUpdate':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: URIUpdate
		"""

		self.uri_id = uri_id
		return self

	def set_uri(self, uri: str) -> 'URIUpdate':
		"""
		Set URI.

		:param uri: str
		:returns: URIUpdate
		"""

		self.uri = uri
		return self

	def set_destination_type(self, destination_type: str) -> 'URIUpdate':
		"""
		Set Destination_Type.

		:param destination_type: str
		:returns: URIUpdate
		"""

		self.destination_type = destination_type
		return self

	def set_destination(self, destination: str) -> 'URIUpdate':
		"""
		Set Destination.

		:param destination: str
		:returns: URIUpdate
		"""

		self.destination = destination
		return self

	def set_status(self, status: int) -> 'URIUpdate':
		"""
		Set Status.

		:param status: int
		:returns: URIUpdate
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'URIUpdate':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: URIUpdate
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri_id is not None:
			data['URI_ID'] = self.uri_id

		if self.uri is not None:
			data['URI'] = self.uri
		if self.destination_type is not None:
			data['Destination_Type'] = self.destination_type
		if self.destination is not None:
			data['Destination'] = self.destination
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request ProductURI_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/producturi_update
"""


class ProductURIUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		ProductURIUpdate Constructor.

		:param client: Client
		:param uri: Uri
		"""

		super().__init__(client)
		self.uri_id = None
		self.uri = None
		self.status = None
		self.canonical = False
		if isinstance(uri, merchantapi.model.Uri):
			if uri.get_id():
				self.set_uri_id(uri.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductURI_Update'

	def get_uri_id(self) -> int:
		"""
		Get URI_ID.

		:returns: int
		"""

		return self.uri_id

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def set_uri_id(self, uri_id: int) -> 'ProductURIUpdate':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: ProductURIUpdate
		"""

		self.uri_id = uri_id
		return self

	def set_uri(self, uri: str) -> 'ProductURIUpdate':
		"""
		Set URI.

		:param uri: str
		:returns: ProductURIUpdate
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'ProductURIUpdate':
		"""
		Set Status.

		:param status: int
		:returns: ProductURIUpdate
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'ProductURIUpdate':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: ProductURIUpdate
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductURIUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductURIUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductURIUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri_id is not None:
			data['URI_ID'] = self.uri_id

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request CategoryURI_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryuri_update
"""


class CategoryURIUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		CategoryURIUpdate Constructor.

		:param client: Client
		:param uri: Uri
		"""

		super().__init__(client)
		self.uri_id = None
		self.uri = None
		self.status = None
		self.canonical = False
		if isinstance(uri, merchantapi.model.Uri):
			if uri.get_id():
				self.set_uri_id(uri.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryURI_Update'

	def get_uri_id(self) -> int:
		"""
		Get URI_ID.

		:returns: int
		"""

		return self.uri_id

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def set_uri_id(self, uri_id: int) -> 'CategoryURIUpdate':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: CategoryURIUpdate
		"""

		self.uri_id = uri_id
		return self

	def set_uri(self, uri: str) -> 'CategoryURIUpdate':
		"""
		Set URI.

		:param uri: str
		:returns: CategoryURIUpdate
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'CategoryURIUpdate':
		"""
		Set Status.

		:param status: int
		:returns: CategoryURIUpdate
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'CategoryURIUpdate':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: CategoryURIUpdate
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri_id is not None:
			data['URI_ID'] = self.uri_id

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request PageURI_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pageuri_update
"""


class PageURIUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		PageURIUpdate Constructor.

		:param client: Client
		:param uri: Uri
		"""

		super().__init__(client)
		self.uri_id = None
		self.uri = None
		self.status = None
		self.canonical = False
		if isinstance(uri, merchantapi.model.Uri):
			if uri.get_id():
				self.set_uri_id(uri.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PageURI_Update'

	def get_uri_id(self) -> int:
		"""
		Get URI_ID.

		:returns: int
		"""

		return self.uri_id

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def set_uri_id(self, uri_id: int) -> 'PageURIUpdate':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: PageURIUpdate
		"""

		self.uri_id = uri_id
		return self

	def set_uri(self, uri: str) -> 'PageURIUpdate':
		"""
		Set URI.

		:param uri: str
		:returns: PageURIUpdate
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'PageURIUpdate':
		"""
		Set Status.

		:param status: int
		:returns: PageURIUpdate
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'PageURIUpdate':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: PageURIUpdate
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageURIUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageURIUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageURIUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri_id is not None:
			data['URI_ID'] = self.uri_id

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request FeedURI_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/feeduri_update
"""


class FeedURIUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		FeedURIUpdate Constructor.

		:param client: Client
		:param uri: Uri
		"""

		super().__init__(client)
		self.uri_id = None
		self.uri = None
		self.status = None
		self.canonical = False
		if isinstance(uri, merchantapi.model.Uri):
			if uri.get_id():
				self.set_uri_id(uri.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'FeedURI_Update'

	def get_uri_id(self) -> int:
		"""
		Get URI_ID.

		:returns: int
		"""

		return self.uri_id

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def set_uri_id(self, uri_id: int) -> 'FeedURIUpdate':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: FeedURIUpdate
		"""

		self.uri_id = uri_id
		return self

	def set_uri(self, uri: str) -> 'FeedURIUpdate':
		"""
		Set URI.

		:param uri: str
		:returns: FeedURIUpdate
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'FeedURIUpdate':
		"""
		Set Status.

		:param status: int
		:returns: FeedURIUpdate
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'FeedURIUpdate':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: FeedURIUpdate
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.FeedURIUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'FeedURIUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.FeedURIUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri_id is not None:
			data['URI_ID'] = self.uri_id

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data


"""
Handles API Request URI_Delete. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/uri_delete
"""


class URIDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		URIDelete Constructor.

		:param client: Client
		:param uri: Uri
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN
		self.uri_id = None
		if isinstance(uri, merchantapi.model.Uri):
			if uri.get_id():
				self.set_uri_id(uri.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URI_Delete'

	def get_uri_id(self) -> int:
		"""
		Get URI_ID.

		:returns: int
		"""

		return self.uri_id

	def set_uri_id(self, uri_id: int) -> 'URIDelete':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: URIDelete
		"""

		self.uri_id = uri_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri_id is not None:
			data['URI_ID'] = self.uri_id

		return data


"""
Handles API Request ProductURIList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/producturilist_load_query
"""


class ProductURIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'canonical',
		'status',
		'uri'
	]

	available_sort_fields = [
		'uri'
	]

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductURIListLoadQuery Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())
			elif product.get_code():
				self.set_product_code(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductURIList_Load_Query'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def set_product_id(self, product_id: int) -> 'ProductURIListLoadQuery':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductURIListLoadQuery
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductURIListLoadQuery':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductURIListLoadQuery
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'ProductURIListLoadQuery':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductURIListLoadQuery
		"""

		self.product_code = product_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductURIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductURIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductURIListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		return data


"""
Handles API Request CategoryURIList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryurilist_load_query
"""


class CategoryURIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'canonical',
		'status',
		'uri'
	]

	available_sort_fields = [
		'uri'
	]

	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryURIListLoadQuery Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_category(category.get_code())
			elif category.get_code():
				self.set_category_code(category.get_code())

			self.set_category_code(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryURIList_Load_Query'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def set_category_id(self, category_id: int) -> 'CategoryURIListLoadQuery':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryURIListLoadQuery
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryURIListLoadQuery':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryURIListLoadQuery
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'CategoryURIListLoadQuery':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryURIListLoadQuery
		"""

		self.category_code = category_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		data['Category_Code'] = self.category_code
		return data


"""
Handles API Request PageURIList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pageurilist_load_query
"""


class PageURIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'canonical',
		'status',
		'uri'
	]

	available_sort_fields = [
		'uri'
	]

	def __init__(self, client: Client = None):
		"""
		PageURIListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.page_id = None
		self.edit_page = None
		self.page_code = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PageURIList_Load_Query'

	def get_page_id(self) -> int:
		"""
		Get Page_ID.

		:returns: int
		"""

		return self.page_id

	def get_edit_page(self) -> str:
		"""
		Get Edit_Page.

		:returns: str
		"""

		return self.edit_page

	def get_page_code(self) -> str:
		"""
		Get Page_Code.

		:returns: str
		"""

		return self.page_code

	def set_page_id(self, page_id: int) -> 'PageURIListLoadQuery':
		"""
		Set Page_ID.

		:param page_id: int
		:returns: PageURIListLoadQuery
		"""

		self.page_id = page_id
		return self

	def set_edit_page(self, edit_page: str) -> 'PageURIListLoadQuery':
		"""
		Set Edit_Page.

		:param edit_page: str
		:returns: PageURIListLoadQuery
		"""

		self.edit_page = edit_page
		return self

	def set_page_code(self, page_code: str) -> 'PageURIListLoadQuery':
		"""
		Set Page_Code.

		:param page_code: str
		:returns: PageURIListLoadQuery
		"""

		self.page_code = page_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageURIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageURIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageURIListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.page_id is not None:
			data['Page_ID'] = self.page_id
		elif self.edit_page is not None:
			data['Edit_Page'] = self.edit_page
		elif self.page_code is not None:
			data['Page_Code'] = self.page_code

		data['Page_Code'] = self.page_code
		return data


"""
Handles API Request FeedURIList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/feedurilist_load_query
"""


class FeedURIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'canonical',
		'status',
		'uri'
	]

	available_sort_fields = [
		'uri'
	]

	def __init__(self, client: Client = None):
		"""
		FeedURIListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.feed_id = None
		self.feed_code = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'FeedURIList_Load_Query'

	def get_feed_id(self) -> int:
		"""
		Get Feed_ID.

		:returns: int
		"""

		return self.feed_id

	def get_feed_code(self) -> str:
		"""
		Get Feed_Code.

		:returns: str
		"""

		return self.feed_code

	def set_feed_id(self, feed_id: int) -> 'FeedURIListLoadQuery':
		"""
		Set Feed_ID.

		:param feed_id: int
		:returns: FeedURIListLoadQuery
		"""

		self.feed_id = feed_id
		return self

	def set_feed_code(self, feed_code: str) -> 'FeedURIListLoadQuery':
		"""
		Set Feed_Code.

		:param feed_code: str
		:returns: FeedURIListLoadQuery
		"""

		self.feed_code = feed_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.FeedURIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'FeedURIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.FeedURIListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.feed_id is not None:
			data['Feed_ID'] = self.feed_id
		elif self.feed_code is not None:
			data['Feed_Code'] = self.feed_code

		return data


"""
Handles API Request ProductURIList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/producturilist_delete
"""


class ProductURIListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProductURIListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductURIList_Delete'

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids
	
	def add_uri_id(self, uri_id) -> 'ProductURIListDelete':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {ProductURIListDelete}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'ProductURIListDelete':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: ProductURIListDelete
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductURIListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductURIListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductURIListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['URI_IDs'] = self.uri_ids
		return data


"""
Handles API Request PageURIList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pageurilist_delete
"""


class PageURIListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		PageURIListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PageURIList_Delete'

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids
	
	def add_uri_id(self, uri_id) -> 'PageURIListDelete':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {PageURIListDelete}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'PageURIListDelete':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: PageURIListDelete
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageURIListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageURIListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageURIListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['URI_IDs'] = self.uri_ids
		return data


"""
Handles API Request CategoryURIList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryurilist_delete
"""


class CategoryURIListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		CategoryURIListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryURIList_Delete'

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids
	
	def add_uri_id(self, uri_id) -> 'CategoryURIListDelete':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {CategoryURIListDelete}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'CategoryURIListDelete':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: CategoryURIListDelete
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['URI_IDs'] = self.uri_ids
		return data


"""
Handles API Request FeedURIList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/feedurilist_delete
"""


class FeedURIListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		FeedURIListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'FeedURIList_Delete'

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids
	
	def add_uri_id(self, uri_id) -> 'FeedURIListDelete':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {FeedURIListDelete}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'FeedURIListDelete':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: FeedURIListDelete
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.FeedURIListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'FeedURIListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.FeedURIListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['URI_IDs'] = self.uri_ids
		return data


"""
Handles API Request URIList_Delete. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/urilist_delete
"""


class URIListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		URIListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URIList_Delete'

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids
	
	def add_uri_id(self, uri_id) -> 'URIListDelete':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {URIListDelete}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'URIListDelete':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: URIListDelete
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['URI_IDs'] = self.uri_ids
		return data


"""
Handles API Request PageURI_Redirect. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pageuri_redirect
"""


class PageURIRedirect(ListQueryRequest):
	def __init__(self, client: Client = None):
		"""
		PageURIRedirect Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.destination_store_code = None
		self.destination_type = None
		self.destination = None
		self.status = None
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PageURI_Redirect'

	def get_destination_store_code(self) -> str:
		"""
		Get Destination_Store_Code.

		:returns: str
		"""

		return self.destination_store_code

	def get_destination_type(self) -> str:
		"""
		Get Destination_Type.

		:returns: str
		"""

		return self.destination_type

	def get_destination(self) -> str:
		"""
		Get Destination.

		:returns: str
		"""

		return self.destination

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids

	def set_destination_store_code(self, destination_store_code: str) -> 'PageURIRedirect':
		"""
		Set Destination_Store_Code.

		:param destination_store_code: str
		:returns: PageURIRedirect
		"""

		self.destination_store_code = destination_store_code
		return self

	def set_destination_type(self, destination_type: str) -> 'PageURIRedirect':
		"""
		Set Destination_Type.

		:param destination_type: str
		:returns: PageURIRedirect
		"""

		self.destination_type = destination_type
		return self

	def set_destination(self, destination: str) -> 'PageURIRedirect':
		"""
		Set Destination.

		:param destination: str
		:returns: PageURIRedirect
		"""

		self.destination = destination
		return self

	def set_status(self, status: int) -> 'PageURIRedirect':
		"""
		Set Status.

		:param status: int
		:returns: PageURIRedirect
		"""

		self.status = status
		return self
	
	def add_uri_id(self, uri_id) -> 'PageURIRedirect':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {PageURIRedirect}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'PageURIRedirect':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: PageURIRedirect
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageURIRedirect':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageURIRedirect':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageURIRedirect(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.destination_store_code is not None:
			data['Destination_Store_Code'] = self.destination_store_code
		if self.destination_type is not None:
			data['Destination_Type'] = self.destination_type
		if self.destination is not None:
			data['Destination'] = self.destination
		if self.status is not None:
			data['Status'] = self.status
		data['URI_IDs'] = self.uri_ids
		return data


"""
Handles API Request ProductURI_Redirect. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/producturi_redirect
"""


class ProductURIRedirect(ListQueryRequest):
	def __init__(self, client: Client = None):
		"""
		ProductURIRedirect Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.destination_store_code = None
		self.destination_type = None
		self.destination = None
		self.status = None
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductURI_Redirect'

	def get_destination_store_code(self) -> str:
		"""
		Get Destination_Store_Code.

		:returns: str
		"""

		return self.destination_store_code

	def get_destination_type(self) -> str:
		"""
		Get Destination_Type.

		:returns: str
		"""

		return self.destination_type

	def get_destination(self) -> str:
		"""
		Get Destination.

		:returns: str
		"""

		return self.destination

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids

	def set_destination_store_code(self, destination_store_code: str) -> 'ProductURIRedirect':
		"""
		Set Destination_Store_Code.

		:param destination_store_code: str
		:returns: ProductURIRedirect
		"""

		self.destination_store_code = destination_store_code
		return self

	def set_destination_type(self, destination_type: str) -> 'ProductURIRedirect':
		"""
		Set Destination_Type.

		:param destination_type: str
		:returns: ProductURIRedirect
		"""

		self.destination_type = destination_type
		return self

	def set_destination(self, destination: str) -> 'ProductURIRedirect':
		"""
		Set Destination.

		:param destination: str
		:returns: ProductURIRedirect
		"""

		self.destination = destination
		return self

	def set_status(self, status: int) -> 'ProductURIRedirect':
		"""
		Set Status.

		:param status: int
		:returns: ProductURIRedirect
		"""

		self.status = status
		return self
	
	def add_uri_id(self, uri_id) -> 'ProductURIRedirect':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {ProductURIRedirect}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'ProductURIRedirect':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: ProductURIRedirect
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductURIRedirect':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductURIRedirect':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductURIRedirect(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.destination_store_code is not None:
			data['Destination_Store_Code'] = self.destination_store_code
		if self.destination_type is not None:
			data['Destination_Type'] = self.destination_type
		if self.destination is not None:
			data['Destination'] = self.destination
		if self.status is not None:
			data['Status'] = self.status
		data['URI_IDs'] = self.uri_ids
		return data


"""
Handles API Request CategoryURI_Redirect. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryuri_redirect
"""


class CategoryURIRedirect(ListQueryRequest):
	def __init__(self, client: Client = None):
		"""
		CategoryURIRedirect Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.destination_store_code = None
		self.destination_type = None
		self.destination = None
		self.status = None
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryURI_Redirect'

	def get_destination_store_code(self) -> str:
		"""
		Get Destination_Store_Code.

		:returns: str
		"""

		return self.destination_store_code

	def get_destination_type(self) -> str:
		"""
		Get Destination_Type.

		:returns: str
		"""

		return self.destination_type

	def get_destination(self) -> str:
		"""
		Get Destination.

		:returns: str
		"""

		return self.destination

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids

	def set_destination_store_code(self, destination_store_code: str) -> 'CategoryURIRedirect':
		"""
		Set Destination_Store_Code.

		:param destination_store_code: str
		:returns: CategoryURIRedirect
		"""

		self.destination_store_code = destination_store_code
		return self

	def set_destination_type(self, destination_type: str) -> 'CategoryURIRedirect':
		"""
		Set Destination_Type.

		:param destination_type: str
		:returns: CategoryURIRedirect
		"""

		self.destination_type = destination_type
		return self

	def set_destination(self, destination: str) -> 'CategoryURIRedirect':
		"""
		Set Destination.

		:param destination: str
		:returns: CategoryURIRedirect
		"""

		self.destination = destination
		return self

	def set_status(self, status: int) -> 'CategoryURIRedirect':
		"""
		Set Status.

		:param status: int
		:returns: CategoryURIRedirect
		"""

		self.status = status
		return self
	
	def add_uri_id(self, uri_id) -> 'CategoryURIRedirect':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {CategoryURIRedirect}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'CategoryURIRedirect':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: CategoryURIRedirect
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIRedirect':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIRedirect':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIRedirect(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.destination_store_code is not None:
			data['Destination_Store_Code'] = self.destination_store_code
		if self.destination_type is not None:
			data['Destination_Type'] = self.destination_type
		if self.destination is not None:
			data['Destination'] = self.destination
		if self.status is not None:
			data['Status'] = self.status
		data['URI_IDs'] = self.uri_ids
		return data


"""
Handles API Request AvailabilityGroup_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroup_delete
"""


class AvailabilityGroupDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupDelete Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroup_Delete'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupDelete':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupDelete
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupDelete':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupDelete
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupDelete':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupDelete
		"""

		self.availability_group_name = availability_group_name
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		return data


"""
Handles API Request AvailabilityGroup_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroup_insert
"""


class AvailabilityGroupInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		AvailabilityGroupInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.availability_group_name = None
		self.availability_group_tax_exempt = False

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroup_Insert'

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_availability_group_tax_exempt(self) -> bool:
		"""
		Get AvailabilityGroup_Tax_Exempt.

		:returns: bool
		"""

		return self.availability_group_tax_exempt

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupInsert':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupInsert
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_availability_group_tax_exempt(self, availability_group_tax_exempt: bool) -> 'AvailabilityGroupInsert':
		"""
		Set AvailabilityGroup_Tax_Exempt.

		:param availability_group_tax_exempt: bool
		:returns: AvailabilityGroupInsert
		"""

		self.availability_group_tax_exempt = availability_group_tax_exempt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['AvailabilityGroup_Name'] = self.availability_group_name
		if self.availability_group_tax_exempt is not None:
			data['AvailabilityGroup_Tax_Exempt'] = self.availability_group_tax_exempt
		return data


"""
Handles API Request AvailabilityGroup_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroup_update
"""


class AvailabilityGroupUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupUpdate Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.availability_group_tax_exempt = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())

			self.set_availability_group_tax_exempt(availability_group.get_tax_exempt())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroup_Update'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_availability_group_tax_exempt(self) -> bool:
		"""
		Get AvailabilityGroup_Tax_Exempt.

		:returns: bool
		"""

		return self.availability_group_tax_exempt

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupUpdate':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupUpdate
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupUpdate':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupUpdate
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupUpdate':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupUpdate
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_availability_group_tax_exempt(self, availability_group_tax_exempt: bool) -> 'AvailabilityGroupUpdate':
		"""
		Set AvailabilityGroup_Tax_Exempt.

		:param availability_group_tax_exempt: bool
		:returns: AvailabilityGroupUpdate
		"""

		self.availability_group_tax_exempt = availability_group_tax_exempt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group

		data['AvailabilityGroup_Name'] = self.availability_group_name
		if self.availability_group_tax_exempt is not None:
			data['AvailabilityGroup_Tax_Exempt'] = self.availability_group_tax_exempt
		return data


"""
Handles API Request AvailabilityGroupCategory_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupcategory_update_assigned
"""


class AvailabilityGroupCategoryUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		AvailabilityGroupCategoryUpdateAssigned Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.assigned = False
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())

			self.set_category_code(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupCategory_Update_Assigned'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_category_id(self, category_id: int) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.category_code = category_code
		return self

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupCategoryUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupCategoryUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		data['Category_Code'] = self.category_code
		data['AvailabilityGroup_Name'] = self.availability_group_name
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request AvailabilityGroupShippingMethodList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupshippingmethodlist_load_query
"""


class AvailabilityGroupShippingMethodListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'method_name'
	]

	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupShippingMethodListLoadQuery Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupShippingMethodList_Load_Query'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupShippingMethodListLoadQuery':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupShippingMethodListLoadQuery
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupShippingMethodListLoadQuery':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupShippingMethodListLoadQuery
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupShippingMethodListLoadQuery':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupShippingMethodListLoadQuery
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupShippingMethodListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupShippingMethodListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'AvailabilityGroupShippingMethodListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: AvailabilityGroupShippingMethodListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupShippingMethodListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupShippingMethodListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupShippingMethodListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupBusinessAccount_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupbusinessaccount_update_assigned
"""


class PriceGroupBusinessAccountUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupBusinessAccountUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupBusinessAccount_Update_Assigned'

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_edit_business_account(self) -> str:
		"""
		Get Edit_BusinessAccount.

		:returns: str
		"""

		return self.edit_business_account

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_business_account_id(self, business_account_id: int) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: str) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: str
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.business_account_title = business_account_title
		return self

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupBusinessAccountUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupBusinessAccountUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.edit_business_account is not None:
			data['Edit_BusinessAccount'] = self.edit_business_account
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request PriceGroupCategory_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupcategory_update_assigned
"""


class PriceGroupCategoryUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupCategoryUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())
			elif price_group.get_name():
				self.set_edit_price_group(price_group.get_name())
			elif price_group.get_name():
				self.set_price_group_name(price_group.get_name())

			self.set_price_group_name(price_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupCategory_Update_Assigned'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_category_id(self, category_id: int) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.category_code = category_code
		return self

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupCategoryUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupCategoryUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		data['PriceGroup_Name'] = self.price_group_name
		data['Assigned'] = self.assigned
		return data


"""
Handles API Request PriceGroupExcludedCategory_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupexcludedcategory_update_assigned
"""


class PriceGroupExcludedCategoryUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupExcludedCategoryUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_category_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupExcludedCategory_Update_Assigned'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_category_id(self, category_id: int) -> 'PriceGroupExcludedCategoryUpdateAssigned':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: PriceGroupExcludedCategoryUpdateAssigned
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'PriceGroupExcludedCategoryUpdateAssigned':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: PriceGroupExcludedCategoryUpdateAssigned
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'PriceGroupExcludedCategoryUpdateAssigned':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: PriceGroupExcludedCategoryUpdateAssigned
		"""

		self.category_code = category_code
		return self

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupExcludedCategoryUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupExcludedCategoryUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupExcludedCategoryUpdateAssigned':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupExcludedCategoryUpdateAssigned
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupExcludedCategoryUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupExcludedCategoryUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupExcludedCategoryUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupExcludedCategoryUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupExcludedCategoryUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupExcludedCategoryUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupExcludedCategoryUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		data['PriceGroup_Name'] = self.price_group_name
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request PriceGroupExcludedProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupexcludedproduct_update_assigned
"""


class PriceGroupExcludedProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupExcludedProductUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.assigned = False
		self.unassigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupExcludedProduct_Update_Assigned'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupExcludedProductUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupExcludedProductUpdateAssigned
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupExcludedProductUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_product_id(self, product_id: int) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: PriceGroupExcludedProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: PriceGroupExcludedProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: PriceGroupExcludedProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupExcludedProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupExcludedProductUpdateAssigned
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupExcludedProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupExcludedProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupExcludedProductUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupQualifyingProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupqualifyingproduct_update_assigned
"""


class PriceGroupQualifyingProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupQualifyingProductUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_product_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupQualifyingProduct_Update_Assigned'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_product_id(self, product_id: int) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupQualifyingProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupQualifyingProductUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		data['PriceGroup_Name'] = self.price_group_name
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request PriceGroup_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroup_delete
"""


class PriceGroupDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupDelete Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

			self.set_price_group_name(price_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroup_Delete'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupDelete':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupDelete
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupDelete':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupDelete
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupDelete':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupDelete
		"""

		self.price_group_name = price_group_name
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		data['PriceGroup_Name'] = self.price_group_name
		return data


"""
Handles API Request PriceGroup_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroup_insert
"""


class PriceGroupInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		PriceGroupInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.name = None
		self.customer_scope = None
		self.rate = None
		self.discount = None
		self.markup = None
		self.module_id = None
		self.edit_module = None
		self.module_code = None
		self.exclusion = False
		self.description = None
		self.display = False
		self.date_time_start = None
		self.date_time_end = None
		self.qualifying_min_subtotal = None
		self.qualifying_max_subtotal = None
		self.qualifying_min_quantity = None
		self.qualifying_max_quantity = None
		self.qualifying_min_weight = None
		self.qualifying_max_weight = None
		self.basket_min_subtotal = None
		self.basket_max_subtotal = None
		self.basket_min_quantity = None
		self.basket_max_quantity = None
		self.basket_min_weight = None
		self.basket_max_weight = None
		self.priority = None
		self.module_fields = {}

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroup_Insert'

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_customer_scope(self) -> str:
		"""
		Get CustomerScope.

		:returns: str
		"""

		return self.customer_scope

	def get_rate(self) -> str:
		"""
		Get Rate.

		:returns: str
		"""

		return self.rate

	def get_discount(self) -> float:
		"""
		Get Discount.

		:returns: float
		"""

		return self.discount

	def get_markup(self) -> float:
		"""
		Get Markup.

		:returns: float
		"""

		return self.markup

	def get_module_id(self) -> int:
		"""
		Get Module_ID.

		:returns: int
		"""

		return self.module_id

	def get_edit_module(self) -> str:
		"""
		Get Edit_Module.

		:returns: str
		"""

		return self.edit_module

	def get_module_code(self) -> str:
		"""
		Get Module_Code.

		:returns: str
		"""

		return self.module_code

	def get_exclusion(self) -> bool:
		"""
		Get Exclusion.

		:returns: bool
		"""

		return self.exclusion

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_display(self) -> bool:
		"""
		Get Display.

		:returns: bool
		"""

		return self.display

	def get_date_time_start(self) -> int:
		"""
		Get DateTime_Start.

		:returns: int
		"""

		return self.date_time_start

	def get_date_time_end(self) -> int:
		"""
		Get DateTime_End.

		:returns: int
		"""

		return self.date_time_end

	def get_qualifying_min_subtotal(self) -> float:
		"""
		Get Qualifying_Min_Subtotal.

		:returns: float
		"""

		return self.qualifying_min_subtotal

	def get_qualifying_max_subtotal(self) -> float:
		"""
		Get Qualifying_Max_Subtotal.

		:returns: float
		"""

		return self.qualifying_max_subtotal

	def get_qualifying_min_quantity(self) -> int:
		"""
		Get Qualifying_Min_Quantity.

		:returns: int
		"""

		return self.qualifying_min_quantity

	def get_qualifying_max_quantity(self) -> int:
		"""
		Get Qualifying_Max_Quantity.

		:returns: int
		"""

		return self.qualifying_max_quantity

	def get_qualifying_min_weight(self) -> float:
		"""
		Get Qualifying_Min_Weight.

		:returns: float
		"""

		return self.qualifying_min_weight

	def get_qualifying_max_weight(self) -> float:
		"""
		Get Qualifying_Max_Weight.

		:returns: float
		"""

		return self.qualifying_max_weight

	def get_basket_min_subtotal(self) -> float:
		"""
		Get Basket_Min_Subtotal.

		:returns: float
		"""

		return self.basket_min_subtotal

	def get_basket_max_subtotal(self) -> float:
		"""
		Get Basket_Max_Subtotal.

		:returns: float
		"""

		return self.basket_max_subtotal

	def get_basket_min_quantity(self) -> int:
		"""
		Get Basket_Min_Quantity.

		:returns: int
		"""

		return self.basket_min_quantity

	def get_basket_max_quantity(self) -> int:
		"""
		Get Basket_Max_Quantity.

		:returns: int
		"""

		return self.basket_max_quantity

	def get_basket_min_weight(self) -> float:
		"""
		Get Basket_Min_Weight.

		:returns: float
		"""

		return self.basket_min_weight

	def get_basket_max_weight(self) -> float:
		"""
		Get Basket_Max_Weight.

		:returns: float
		"""

		return self.basket_max_weight

	def get_priority(self) -> int:
		"""
		Get Priority.

		:returns: int
		"""

		return self.priority

	def get_module_fields(self):
		"""
		Get Module_Fields.

		:returns: dict
		"""

		return self.module_fields

	def set_name(self, name: str) -> 'PriceGroupInsert':
		"""
		Set Name.

		:param name: str
		:returns: PriceGroupInsert
		"""

		self.name = name
		return self

	def set_customer_scope(self, customer_scope: str) -> 'PriceGroupInsert':
		"""
		Set CustomerScope.

		:param customer_scope: str
		:returns: PriceGroupInsert
		"""

		self.customer_scope = customer_scope
		return self

	def set_rate(self, rate: str) -> 'PriceGroupInsert':
		"""
		Set Rate.

		:param rate: str
		:returns: PriceGroupInsert
		"""

		self.rate = rate
		return self

	def set_discount(self, discount: float) -> 'PriceGroupInsert':
		"""
		Set Discount.

		:param discount: float
		:returns: PriceGroupInsert
		"""

		self.discount = discount
		return self

	def set_markup(self, markup: float) -> 'PriceGroupInsert':
		"""
		Set Markup.

		:param markup: float
		:returns: PriceGroupInsert
		"""

		self.markup = markup
		return self

	def set_module_id(self, module_id: int) -> 'PriceGroupInsert':
		"""
		Set Module_ID.

		:param module_id: int
		:returns: PriceGroupInsert
		"""

		self.module_id = module_id
		return self

	def set_edit_module(self, edit_module: str) -> 'PriceGroupInsert':
		"""
		Set Edit_Module.

		:param edit_module: str
		:returns: PriceGroupInsert
		"""

		self.edit_module = edit_module
		return self

	def set_module_code(self, module_code: str) -> 'PriceGroupInsert':
		"""
		Set Module_Code.

		:param module_code: str
		:returns: PriceGroupInsert
		"""

		self.module_code = module_code
		return self

	def set_exclusion(self, exclusion: bool) -> 'PriceGroupInsert':
		"""
		Set Exclusion.

		:param exclusion: bool
		:returns: PriceGroupInsert
		"""

		self.exclusion = exclusion
		return self

	def set_description(self, description: str) -> 'PriceGroupInsert':
		"""
		Set Description.

		:param description: str
		:returns: PriceGroupInsert
		"""

		self.description = description
		return self

	def set_display(self, display: bool) -> 'PriceGroupInsert':
		"""
		Set Display.

		:param display: bool
		:returns: PriceGroupInsert
		"""

		self.display = display
		return self

	def set_date_time_start(self, date_time_start: int) -> 'PriceGroupInsert':
		"""
		Set DateTime_Start.

		:param date_time_start: int
		:returns: PriceGroupInsert
		"""

		self.date_time_start = date_time_start
		return self

	def set_date_time_end(self, date_time_end: int) -> 'PriceGroupInsert':
		"""
		Set DateTime_End.

		:param date_time_end: int
		:returns: PriceGroupInsert
		"""

		self.date_time_end = date_time_end
		return self

	def set_qualifying_min_subtotal(self, qualifying_min_subtotal: float) -> 'PriceGroupInsert':
		"""
		Set Qualifying_Min_Subtotal.

		:param qualifying_min_subtotal: float
		:returns: PriceGroupInsert
		"""

		self.qualifying_min_subtotal = qualifying_min_subtotal
		return self

	def set_qualifying_max_subtotal(self, qualifying_max_subtotal: float) -> 'PriceGroupInsert':
		"""
		Set Qualifying_Max_Subtotal.

		:param qualifying_max_subtotal: float
		:returns: PriceGroupInsert
		"""

		self.qualifying_max_subtotal = qualifying_max_subtotal
		return self

	def set_qualifying_min_quantity(self, qualifying_min_quantity: int) -> 'PriceGroupInsert':
		"""
		Set Qualifying_Min_Quantity.

		:param qualifying_min_quantity: int
		:returns: PriceGroupInsert
		"""

		self.qualifying_min_quantity = qualifying_min_quantity
		return self

	def set_qualifying_max_quantity(self, qualifying_max_quantity: int) -> 'PriceGroupInsert':
		"""
		Set Qualifying_Max_Quantity.

		:param qualifying_max_quantity: int
		:returns: PriceGroupInsert
		"""

		self.qualifying_max_quantity = qualifying_max_quantity
		return self

	def set_qualifying_min_weight(self, qualifying_min_weight: float) -> 'PriceGroupInsert':
		"""
		Set Qualifying_Min_Weight.

		:param qualifying_min_weight: float
		:returns: PriceGroupInsert
		"""

		self.qualifying_min_weight = qualifying_min_weight
		return self

	def set_qualifying_max_weight(self, qualifying_max_weight: float) -> 'PriceGroupInsert':
		"""
		Set Qualifying_Max_Weight.

		:param qualifying_max_weight: float
		:returns: PriceGroupInsert
		"""

		self.qualifying_max_weight = qualifying_max_weight
		return self

	def set_basket_min_subtotal(self, basket_min_subtotal: float) -> 'PriceGroupInsert':
		"""
		Set Basket_Min_Subtotal.

		:param basket_min_subtotal: float
		:returns: PriceGroupInsert
		"""

		self.basket_min_subtotal = basket_min_subtotal
		return self

	def set_basket_max_subtotal(self, basket_max_subtotal: float) -> 'PriceGroupInsert':
		"""
		Set Basket_Max_Subtotal.

		:param basket_max_subtotal: float
		:returns: PriceGroupInsert
		"""

		self.basket_max_subtotal = basket_max_subtotal
		return self

	def set_basket_min_quantity(self, basket_min_quantity: int) -> 'PriceGroupInsert':
		"""
		Set Basket_Min_Quantity.

		:param basket_min_quantity: int
		:returns: PriceGroupInsert
		"""

		self.basket_min_quantity = basket_min_quantity
		return self

	def set_basket_max_quantity(self, basket_max_quantity: int) -> 'PriceGroupInsert':
		"""
		Set Basket_Max_Quantity.

		:param basket_max_quantity: int
		:returns: PriceGroupInsert
		"""

		self.basket_max_quantity = basket_max_quantity
		return self

	def set_basket_min_weight(self, basket_min_weight: float) -> 'PriceGroupInsert':
		"""
		Set Basket_Min_Weight.

		:param basket_min_weight: float
		:returns: PriceGroupInsert
		"""

		self.basket_min_weight = basket_min_weight
		return self

	def set_basket_max_weight(self, basket_max_weight: float) -> 'PriceGroupInsert':
		"""
		Set Basket_Max_Weight.

		:param basket_max_weight: float
		:returns: PriceGroupInsert
		"""

		self.basket_max_weight = basket_max_weight
		return self

	def set_priority(self, priority: int) -> 'PriceGroupInsert':
		"""
		Set Priority.

		:param priority: int
		:returns: PriceGroupInsert
		"""

		self.priority = priority
		return self

	def set_module_fields(self, module_fields) -> 'PriceGroupInsert':
		"""
		Set Module_Fields.

		:param module_fields: dict
		:returns: PriceGroupInsert
		"""

		self.module_fields = module_fields
		return self

	def set_module_field(self, field: str, value) -> 'PriceGroupInsert':
		"""
		Add custom data to the request.

		:param field: str
		:param value: mixed
		:returns: {PriceGroupInsert}
		"""

		self.module_fields[field] = value
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()
		data.update(self.get_module_fields())

		if self.module_id is not None:
			data['Module_ID'] = self.module_id
		elif self.edit_module is not None:
			data['Edit_Module'] = self.edit_module
		elif self.module_code is not None:
			data['Module_Code'] = self.module_code

		if self.name is not None:
			data['Name'] = self.name
		if self.customer_scope is not None:
			data['CustomerScope'] = self.customer_scope
		if self.rate is not None:
			data['Rate'] = self.rate
		if self.discount is not None:
			data['Discount'] = self.discount
		if self.markup is not None:
			data['Markup'] = self.markup
		if self.exclusion is not None:
			data['Exclusion'] = self.exclusion
		if self.description is not None:
			data['Description'] = self.description
		if self.display is not None:
			data['Display'] = self.display
		if self.date_time_start is not None:
			data['DateTime_Start'] = self.date_time_start
		if self.date_time_end is not None:
			data['DateTime_End'] = self.date_time_end
		if self.qualifying_min_subtotal is not None:
			data['Qualifying_Min_Subtotal'] = self.qualifying_min_subtotal
		if self.qualifying_max_subtotal is not None:
			data['Qualifying_Max_Subtotal'] = self.qualifying_max_subtotal
		if self.qualifying_min_quantity is not None:
			data['Qualifying_Min_Quantity'] = self.qualifying_min_quantity
		if self.qualifying_max_quantity is not None:
			data['Qualifying_Max_Quantity'] = self.qualifying_max_quantity
		if self.qualifying_min_weight is not None:
			data['Qualifying_Min_Weight'] = self.qualifying_min_weight
		if self.qualifying_max_weight is not None:
			data['Qualifying_Max_Weight'] = self.qualifying_max_weight
		if self.basket_min_subtotal is not None:
			data['Basket_Min_Subtotal'] = self.basket_min_subtotal
		if self.basket_max_subtotal is not None:
			data['Basket_Max_Subtotal'] = self.basket_max_subtotal
		if self.basket_min_quantity is not None:
			data['Basket_Min_Quantity'] = self.basket_min_quantity
		if self.basket_max_quantity is not None:
			data['Basket_Max_Quantity'] = self.basket_max_quantity
		if self.basket_min_weight is not None:
			data['Basket_Min_Weight'] = self.basket_min_weight
		if self.basket_max_weight is not None:
			data['Basket_Max_Weight'] = self.basket_max_weight
		if self.priority is not None:
			data['Priority'] = self.priority
		return data


"""
Handles API Request PriceGroup_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroup_update
"""


class PriceGroupUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupUpdate Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.name = None
		self.customer_scope = None
		self.rate = None
		self.discount = None
		self.markup = None
		self.module_id = None
		self.exclusion = False
		self.description = None
		self.display = False
		self.date_time_start = None
		self.date_time_end = None
		self.qualifying_min_subtotal = None
		self.qualifying_max_subtotal = None
		self.qualifying_min_quantity = None
		self.qualifying_max_quantity = None
		self.qualifying_min_weight = None
		self.qualifying_max_weight = None
		self.basket_min_subtotal = None
		self.basket_max_subtotal = None
		self.basket_min_quantity = None
		self.basket_max_quantity = None
		self.basket_min_weight = None
		self.basket_max_weight = None
		self.priority = None
		self.exclusions = []
		self.module_fields = {}
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

			self.set_price_group_name(price_group.get_name())
			self.set_name(price_group.get_name())
			self.set_customer_scope(price_group.get_customer_scope())
			self.set_rate(price_group.get_rate())
			self.set_discount(price_group.get_discount())
			self.set_markup(price_group.get_markup())
			self.set_exclusion(price_group.get_exclusion())
			self.set_description(price_group.get_description())
			self.set_display(price_group.get_display())
			self.set_date_time_start(price_group.get_date_time_start())
			self.set_date_time_end(price_group.get_date_time_end())
			self.set_qualifying_min_subtotal(price_group.get_minimum_subtotal())
			self.set_qualifying_max_subtotal(price_group.get_maximum_subtotal())
			self.set_qualifying_min_quantity(price_group.get_minimum_quantity())
			self.set_qualifying_max_quantity(price_group.get_maximum_quantity())
			self.set_qualifying_min_weight(price_group.get_minimum_weight())
			self.set_qualifying_max_weight(price_group.get_maximum_weight())
			self.set_basket_min_subtotal(price_group.get_basket_minimum_subtotal())
			self.set_basket_max_subtotal(price_group.get_basket_maximum_subtotal())
			self.set_basket_min_quantity(price_group.get_basket_minimum_quantity())
			self.set_basket_max_quantity(price_group.get_basket_maximum_quantity())
			self.set_basket_min_weight(price_group.get_basket_minimum_weight())
			self.set_basket_max_weight(price_group.get_basket_maximum_weight())
			self.set_priority(price_group.get_priority())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroup_Update'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_customer_scope(self) -> str:
		"""
		Get CustomerScope.

		:returns: str
		"""

		return self.customer_scope

	def get_rate(self) -> str:
		"""
		Get Rate.

		:returns: str
		"""

		return self.rate

	def get_discount(self) -> float:
		"""
		Get Discount.

		:returns: float
		"""

		return self.discount

	def get_markup(self) -> float:
		"""
		Get Markup.

		:returns: float
		"""

		return self.markup

	def get_module_id(self) -> int:
		"""
		Get Module_ID.

		:returns: int
		"""

		return self.module_id

	def get_exclusion(self) -> bool:
		"""
		Get Exclusion.

		:returns: bool
		"""

		return self.exclusion

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_display(self) -> bool:
		"""
		Get Display.

		:returns: bool
		"""

		return self.display

	def get_date_time_start(self) -> int:
		"""
		Get DateTime_Start.

		:returns: int
		"""

		return self.date_time_start

	def get_date_time_end(self) -> int:
		"""
		Get DateTime_End.

		:returns: int
		"""

		return self.date_time_end

	def get_qualifying_min_subtotal(self) -> float:
		"""
		Get Qualifying_Min_Subtotal.

		:returns: float
		"""

		return self.qualifying_min_subtotal

	def get_qualifying_max_subtotal(self) -> float:
		"""
		Get Qualifying_Max_Subtotal.

		:returns: float
		"""

		return self.qualifying_max_subtotal

	def get_qualifying_min_quantity(self) -> int:
		"""
		Get Qualifying_Min_Quantity.

		:returns: int
		"""

		return self.qualifying_min_quantity

	def get_qualifying_max_quantity(self) -> int:
		"""
		Get Qualifying_Max_Quantity.

		:returns: int
		"""

		return self.qualifying_max_quantity

	def get_qualifying_min_weight(self) -> float:
		"""
		Get Qualifying_Min_Weight.

		:returns: float
		"""

		return self.qualifying_min_weight

	def get_qualifying_max_weight(self) -> float:
		"""
		Get Qualifying_Max_Weight.

		:returns: float
		"""

		return self.qualifying_max_weight

	def get_basket_min_subtotal(self) -> float:
		"""
		Get Basket_Min_Subtotal.

		:returns: float
		"""

		return self.basket_min_subtotal

	def get_basket_max_subtotal(self) -> float:
		"""
		Get Basket_Max_Subtotal.

		:returns: float
		"""

		return self.basket_max_subtotal

	def get_basket_min_quantity(self) -> int:
		"""
		Get Basket_Min_Quantity.

		:returns: int
		"""

		return self.basket_min_quantity

	def get_basket_max_quantity(self) -> int:
		"""
		Get Basket_Max_Quantity.

		:returns: int
		"""

		return self.basket_max_quantity

	def get_basket_min_weight(self) -> float:
		"""
		Get Basket_Min_Weight.

		:returns: float
		"""

		return self.basket_min_weight

	def get_basket_max_weight(self) -> float:
		"""
		Get Basket_Max_Weight.

		:returns: float
		"""

		return self.basket_max_weight

	def get_priority(self) -> int:
		"""
		Get Priority.

		:returns: int
		"""

		return self.priority

	def get_exclusions(self) -> list:
		"""
		Get Exclusions.

		:returns: List of PriceGroupExclusion
		"""

		return self.exclusions

	def get_module_fields(self):
		"""
		Get Module_Fields.

		:returns: dict
		"""

		return self.module_fields

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupUpdate':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupUpdate
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupUpdate':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupUpdate
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupUpdate':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupUpdate
		"""

		self.price_group_name = price_group_name
		return self

	def set_name(self, name: str) -> 'PriceGroupUpdate':
		"""
		Set Name.

		:param name: str
		:returns: PriceGroupUpdate
		"""

		self.name = name
		return self

	def set_customer_scope(self, customer_scope: str) -> 'PriceGroupUpdate':
		"""
		Set CustomerScope.

		:param customer_scope: str
		:returns: PriceGroupUpdate
		"""

		self.customer_scope = customer_scope
		return self

	def set_rate(self, rate: str) -> 'PriceGroupUpdate':
		"""
		Set Rate.

		:param rate: str
		:returns: PriceGroupUpdate
		"""

		self.rate = rate
		return self

	def set_discount(self, discount: float) -> 'PriceGroupUpdate':
		"""
		Set Discount.

		:param discount: float
		:returns: PriceGroupUpdate
		"""

		self.discount = discount
		return self

	def set_markup(self, markup: float) -> 'PriceGroupUpdate':
		"""
		Set Markup.

		:param markup: float
		:returns: PriceGroupUpdate
		"""

		self.markup = markup
		return self

	def set_module_id(self, module_id: int) -> 'PriceGroupUpdate':
		"""
		Set Module_ID.

		:param module_id: int
		:returns: PriceGroupUpdate
		"""

		self.module_id = module_id
		return self

	def set_exclusion(self, exclusion: bool) -> 'PriceGroupUpdate':
		"""
		Set Exclusion.

		:param exclusion: bool
		:returns: PriceGroupUpdate
		"""

		self.exclusion = exclusion
		return self

	def set_description(self, description: str) -> 'PriceGroupUpdate':
		"""
		Set Description.

		:param description: str
		:returns: PriceGroupUpdate
		"""

		self.description = description
		return self

	def set_display(self, display: bool) -> 'PriceGroupUpdate':
		"""
		Set Display.

		:param display: bool
		:returns: PriceGroupUpdate
		"""

		self.display = display
		return self

	def set_date_time_start(self, date_time_start: int) -> 'PriceGroupUpdate':
		"""
		Set DateTime_Start.

		:param date_time_start: int
		:returns: PriceGroupUpdate
		"""

		self.date_time_start = date_time_start
		return self

	def set_date_time_end(self, date_time_end: int) -> 'PriceGroupUpdate':
		"""
		Set DateTime_End.

		:param date_time_end: int
		:returns: PriceGroupUpdate
		"""

		self.date_time_end = date_time_end
		return self

	def set_qualifying_min_subtotal(self, qualifying_min_subtotal: float) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Min_Subtotal.

		:param qualifying_min_subtotal: float
		:returns: PriceGroupUpdate
		"""

		self.qualifying_min_subtotal = qualifying_min_subtotal
		return self

	def set_qualifying_max_subtotal(self, qualifying_max_subtotal: float) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Max_Subtotal.

		:param qualifying_max_subtotal: float
		:returns: PriceGroupUpdate
		"""

		self.qualifying_max_subtotal = qualifying_max_subtotal
		return self

	def set_qualifying_min_quantity(self, qualifying_min_quantity: int) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Min_Quantity.

		:param qualifying_min_quantity: int
		:returns: PriceGroupUpdate
		"""

		self.qualifying_min_quantity = qualifying_min_quantity
		return self

	def set_qualifying_max_quantity(self, qualifying_max_quantity: int) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Max_Quantity.

		:param qualifying_max_quantity: int
		:returns: PriceGroupUpdate
		"""

		self.qualifying_max_quantity = qualifying_max_quantity
		return self

	def set_qualifying_min_weight(self, qualifying_min_weight: float) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Min_Weight.

		:param qualifying_min_weight: float
		:returns: PriceGroupUpdate
		"""

		self.qualifying_min_weight = qualifying_min_weight
		return self

	def set_qualifying_max_weight(self, qualifying_max_weight: float) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Max_Weight.

		:param qualifying_max_weight: float
		:returns: PriceGroupUpdate
		"""

		self.qualifying_max_weight = qualifying_max_weight
		return self

	def set_basket_min_subtotal(self, basket_min_subtotal: float) -> 'PriceGroupUpdate':
		"""
		Set Basket_Min_Subtotal.

		:param basket_min_subtotal: float
		:returns: PriceGroupUpdate
		"""

		self.basket_min_subtotal = basket_min_subtotal
		return self

	def set_basket_max_subtotal(self, basket_max_subtotal: float) -> 'PriceGroupUpdate':
		"""
		Set Basket_Max_Subtotal.

		:param basket_max_subtotal: float
		:returns: PriceGroupUpdate
		"""

		self.basket_max_subtotal = basket_max_subtotal
		return self

	def set_basket_min_quantity(self, basket_min_quantity: int) -> 'PriceGroupUpdate':
		"""
		Set Basket_Min_Quantity.

		:param basket_min_quantity: int
		:returns: PriceGroupUpdate
		"""

		self.basket_min_quantity = basket_min_quantity
		return self

	def set_basket_max_quantity(self, basket_max_quantity: int) -> 'PriceGroupUpdate':
		"""
		Set Basket_Max_Quantity.

		:param basket_max_quantity: int
		:returns: PriceGroupUpdate
		"""

		self.basket_max_quantity = basket_max_quantity
		return self

	def set_basket_min_weight(self, basket_min_weight: float) -> 'PriceGroupUpdate':
		"""
		Set Basket_Min_Weight.

		:param basket_min_weight: float
		:returns: PriceGroupUpdate
		"""

		self.basket_min_weight = basket_min_weight
		return self

	def set_basket_max_weight(self, basket_max_weight: float) -> 'PriceGroupUpdate':
		"""
		Set Basket_Max_Weight.

		:param basket_max_weight: float
		:returns: PriceGroupUpdate
		"""

		self.basket_max_weight = basket_max_weight
		return self

	def set_priority(self, priority: int) -> 'PriceGroupUpdate':
		"""
		Set Priority.

		:param priority: int
		:returns: PriceGroupUpdate
		"""

		self.priority = priority
		return self

	def set_exclusions(self, exclusions: list) -> 'PriceGroupUpdate':
		"""
		Set Exclusions.

		:param exclusions: {PriceGroupExclusion[]}
		:raises Exception:
		:returns: PriceGroupUpdate
		"""

		for e in exclusions:
			if not isinstance(e, merchantapi.model.PriceGroupExclusion):
				raise Exception("")
		self.exclusions = exclusions
		return self

	def set_module_fields(self, module_fields) -> 'PriceGroupUpdate':
		"""
		Set Module_Fields.

		:param module_fields: dict
		:returns: PriceGroupUpdate
		"""

		self.module_fields = module_fields
		return self
	
	def add_price_group_exclusion(self, price_group_exclusion) -> 'PriceGroupUpdate':
		"""
		Add Exclusions.

		:param price_group_exclusion: PriceGroupExclusion 
		:raises Exception:
		:returns: {PriceGroupUpdate}
		"""

		if isinstance(price_group_exclusion, merchantapi.model.PriceGroupExclusion):
			self.exclusions.append(price_group_exclusion)
		elif isinstance(price_group_exclusion, dict):
			self.exclusions.append(merchantapi.model.PriceGroupExclusion(price_group_exclusion))
		else:
			raise Exception('Expected instance of PriceGroupExclusion or dict')
		return self

	def add_exclusions(self, exclusions: list) -> 'PriceGroupUpdate':
		"""
		Add many PriceGroupExclusion.

		:param exclusions: List of PriceGroupExclusion
		:raises Exception:
		:returns: PriceGroupUpdate
		"""

		for e in exclusions:
			if not isinstance(e, merchantapi.model.PriceGroupExclusion):
				raise Exception('')
			self.exclusions.append(e)

		return self

	def set_module_field(self, field: str, value) -> 'PriceGroupUpdate':
		"""
		Add custom data to the request.

		:param field: str
		:param value: mixed
		:returns: {PriceGroupUpdate}
		"""

		self.module_fields[field] = value
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()
		data.update(self.get_module_fields())

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		data['PriceGroup_Name'] = self.price_group_name
		if self.name is not None:
			data['Name'] = self.name
		if self.customer_scope is not None:
			data['CustomerScope'] = self.customer_scope
		if self.rate is not None:
			data['Rate'] = self.rate
		if self.discount is not None:
			data['Discount'] = self.discount
		if self.markup is not None:
			data['Markup'] = self.markup
		if self.module_id is not None:
			data['Module_ID'] = self.module_id
		if self.exclusion is not None:
			data['Exclusion'] = self.exclusion
		if self.description is not None:
			data['Description'] = self.description
		if self.display is not None:
			data['Display'] = self.display
		if self.date_time_start is not None:
			data['DateTime_Start'] = self.date_time_start
		if self.date_time_end is not None:
			data['DateTime_End'] = self.date_time_end
		if self.qualifying_min_subtotal is not None:
			data['Qualifying_Min_Subtotal'] = self.qualifying_min_subtotal
		if self.qualifying_max_subtotal is not None:
			data['Qualifying_Max_Subtotal'] = self.qualifying_max_subtotal
		if self.qualifying_min_quantity is not None:
			data['Qualifying_Min_Quantity'] = self.qualifying_min_quantity
		if self.qualifying_max_quantity is not None:
			data['Qualifying_Max_Quantity'] = self.qualifying_max_quantity
		if self.qualifying_min_weight is not None:
			data['Qualifying_Min_Weight'] = self.qualifying_min_weight
		if self.qualifying_max_weight is not None:
			data['Qualifying_Max_Weight'] = self.qualifying_max_weight
		if self.basket_min_subtotal is not None:
			data['Basket_Min_Subtotal'] = self.basket_min_subtotal
		if self.basket_max_subtotal is not None:
			data['Basket_Max_Subtotal'] = self.basket_max_subtotal
		if self.basket_min_quantity is not None:
			data['Basket_Min_Quantity'] = self.basket_min_quantity
		if self.basket_max_quantity is not None:
			data['Basket_Max_Quantity'] = self.basket_max_quantity
		if self.basket_min_weight is not None:
			data['Basket_Min_Weight'] = self.basket_min_weight
		if self.basket_max_weight is not None:
			data['Basket_Max_Weight'] = self.basket_max_weight
		if self.priority is not None:
			data['Priority'] = self.priority
		if len(self.exclusions):
			data['Exclusions'] = []

			for f in self.exclusions:
				data['Exclusions'].append(f.to_dict())
		return data


"""
Handles API Request CouponCustomer_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponcustomer_update_assigned
"""


class CouponCustomerUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponCustomerUpdateAssigned Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.assigned = False
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())

			self.set_coupon_code(coupon.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponCustomer_Update_Assigned'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_customer_id(self, customer_id: int) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CouponCustomerUpdateAssigned
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CouponCustomerUpdateAssigned
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CouponCustomerUpdateAssigned
		"""

		self.customer_login = customer_login
		return self

	def set_coupon_id(self, coupon_id: int) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponCustomerUpdateAssigned
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponCustomerUpdateAssigned
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponCustomerUpdateAssigned
		"""

		self.coupon_code = coupon_code
		return self

	def set_assigned(self, assigned: bool) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CouponCustomerUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponCustomerUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponCustomerUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponCustomerUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon
		elif self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		data['Customer_Login'] = self.customer_login
		data['Coupon_Code'] = self.coupon_code
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request BusinessAccountList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccountlist_load_query
"""


class BusinessAccountListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'title',
		'note_count',
		'tax_exempt',
		'order_cnt',
		'order_avg',
		'order_tot'
	]

	available_sort_fields = [
		'title',
		'note_count',
		'tax_exempt',
		'order_cnt',
		'order_avg',
		'order_tot'
	]

	def __init__(self, client: Client = None):
		"""
		BusinessAccountListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccountList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountListLoadQuery(self, http_response, data)


"""
Handles API Request BusinessAccount_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccount_insert
"""


class BusinessAccountInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		BusinessAccountInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.business_account_title = None
		self.business_account_tax_exempt = False

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccount_Insert'

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_business_account_tax_exempt(self) -> bool:
		"""
		Get BusinessAccount_Tax_Exempt.

		:returns: bool
		"""

		return self.business_account_tax_exempt

	def set_business_account_title(self, business_account_title: str) -> 'BusinessAccountInsert':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: BusinessAccountInsert
		"""

		self.business_account_title = business_account_title
		return self

	def set_business_account_tax_exempt(self, business_account_tax_exempt: bool) -> 'BusinessAccountInsert':
		"""
		Set BusinessAccount_Tax_Exempt.

		:param business_account_tax_exempt: bool
		:returns: BusinessAccountInsert
		"""

		self.business_account_tax_exempt = business_account_tax_exempt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title
		if self.business_account_tax_exempt is not None:
			data['BusinessAccount_Tax_Exempt'] = self.business_account_tax_exempt
		return data


"""
Handles API Request BusinessAccount_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccount_update
"""


class BusinessAccountUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, business_account: merchantapi.model.BusinessAccount = None):
		"""
		BusinessAccountUpdate Constructor.

		:param client: Client
		:param business_account: BusinessAccount
		"""

		super().__init__(client)
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.business_account_tax_exempt = False
		if isinstance(business_account, merchantapi.model.BusinessAccount):
			if business_account.get_id():
				self.set_business_account_id(business_account.get_id())

			self.set_business_account_title(business_account.get_title())
			self.set_business_account_tax_exempt(business_account.get_tax_exempt())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccount_Update'

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_edit_business_account(self) -> int:
		"""
		Get Edit_BusinessAccount.

		:returns: int
		"""

		return self.edit_business_account

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_business_account_tax_exempt(self) -> bool:
		"""
		Get BusinessAccount_Tax_Exempt.

		:returns: bool
		"""

		return self.business_account_tax_exempt

	def set_business_account_id(self, business_account_id: int) -> 'BusinessAccountUpdate':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: BusinessAccountUpdate
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: int) -> 'BusinessAccountUpdate':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: int
		:returns: BusinessAccountUpdate
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'BusinessAccountUpdate':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: BusinessAccountUpdate
		"""

		self.business_account_title = business_account_title
		return self

	def set_business_account_tax_exempt(self, business_account_tax_exempt: bool) -> 'BusinessAccountUpdate':
		"""
		Set BusinessAccount_Tax_Exempt.

		:param business_account_tax_exempt: bool
		:returns: BusinessAccountUpdate
		"""

		self.business_account_tax_exempt = business_account_tax_exempt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.edit_business_account is not None:
			data['Edit_BusinessAccount'] = self.edit_business_account
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title
		if self.business_account_tax_exempt is not None:
			data['BusinessAccount_Tax_Exempt'] = self.business_account_tax_exempt
		return data


"""
Handles API Request BusinessAccountList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccountlist_delete
"""


class BusinessAccountListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		BusinessAccountListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.business_account_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccountList_Delete'

	def get_business_account_ids(self):
		"""
		Get BusinessAccount_IDs.

		:returns: list
		"""

		return self.business_account_ids
	
	def add_business_account_id(self, business_account_id) -> 'BusinessAccountListDelete':
		"""
		Add BusinessAccount_IDs.

		:param business_account_id: int
		:returns: {BusinessAccountListDelete}
		"""

		self.business_account_ids.append(business_account_id)
		return self

	def add_business_account(self, business_account: merchantapi.model.BusinessAccount) -> 'BusinessAccountListDelete':
		"""
		Add BusinessAccount model.

		:param business_account: BusinessAccount
		:raises Exception:
		:returns: BusinessAccountListDelete
		"""
		if not isinstance(business_account, merchantapi.model.BusinessAccount):
			raise Exception('Expected an instance of BusinessAccount')

		if business_account.get_id():
			self.business_account_ids.append(business_account.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['BusinessAccount_IDs'] = self.business_account_ids
		return data


"""
Handles API Request BusinessAccountCustomer_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccountcustomer_update_assigned
"""


class BusinessAccountCustomerUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, business_account: merchantapi.model.BusinessAccount = None):
		"""
		BusinessAccountCustomerUpdateAssigned Constructor.

		:param client: Client
		:param business_account: BusinessAccount
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.assigned = False
		if isinstance(business_account, merchantapi.model.BusinessAccount):
			if business_account.get_id():
				self.set_business_account_id(business_account.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccountCustomer_Update_Assigned'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_edit_business_account(self) -> str:
		"""
		Get Edit_BusinessAccount.

		:returns: str
		"""

		return self.edit_business_account

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_customer_id(self, customer_id: int) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.customer_login = customer_login
		return self

	def set_business_account_id(self, business_account_id: int) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: str) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: str
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.business_account_title = business_account_title
		return self

	def set_assigned(self, assigned: bool) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountCustomerUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountCustomerUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.edit_business_account is not None:
			data['Edit_BusinessAccount'] = self.edit_business_account
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		data['Customer_Login'] = self.customer_login
		data['BusinessAccount_Title'] = self.business_account_title
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request StoreList_Load_Query. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/storelist_load_query
"""


class StoreListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'code',
		'license',
		'name',
		'owner',
		'email',
		'company',
		'address',
		'city',
		'state',
		'zip',
		'phone',
		'fax',
		'country'
	]

	available_sort_fields = [
		'id',
		'code',
		'license',
		'name',
		'owner',
		'email',
		'company',
		'address',
		'city',
		'state',
		'zip',
		'phone',
		'fax',
		'country'
	]

	def __init__(self, client: Client = None):
		"""
		StoreListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'StoreList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.StoreListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'StoreListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.StoreListLoadQuery(self, http_response, data)


"""
Handles API Request Store_Load. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/store_load
"""


class StoreLoad(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		StoreLoad Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Store_Load'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.StoreLoad':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'StoreLoad':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.StoreLoad(self, http_response, data)


"""
Handles API Request ProductVariantList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariantlist_load_query
"""


class ProductVariantListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'product_code',
		'product_name',
		'product_sku',
		'option_id',
		'option_code'
	]

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantListLoadQuery Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_product_code(product.get_code())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariantList_Load_Query'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def set_product_id(self, product_id: int) -> 'ProductVariantListLoadQuery':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantListLoadQuery
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantListLoadQuery':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantListLoadQuery
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantListLoadQuery':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantListLoadQuery
		"""

		self.edit_product = edit_product
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		return data


"""
Handles API Request ProductVariant_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariant_insert
"""


class ProductVariantInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantInsert Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attributes = []
		self.parts = []
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_product_code(product.get_code())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariant_Insert'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_attributes(self) -> list:
		"""
		Get Attributes.

		:returns: List of VariantAttribute
		"""

		return self.attributes

	def get_parts(self) -> list:
		"""
		Get Parts.

		:returns: List of VariantPart
		"""

		return self.parts

	def set_product_id(self, product_id: int) -> 'ProductVariantInsert':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantInsert
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantInsert
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantInsert':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantInsert
		"""

		self.edit_product = edit_product
		return self

	def set_attributes(self, attributes: list) -> 'ProductVariantInsert':
		"""
		Set Attributes.

		:param attributes: {VariantAttribute[]}
		:raises Exception:
		:returns: ProductVariantInsert
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.VariantAttribute):
				raise Exception("")
		self.attributes = attributes
		return self

	def set_parts(self, parts: list) -> 'ProductVariantInsert':
		"""
		Set Parts.

		:param parts: {VariantPart[]}
		:raises Exception:
		:returns: ProductVariantInsert
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.VariantPart):
				raise Exception("")
		self.parts = parts
		return self
	
	def add_variant_attribute(self, variant_attribute) -> 'ProductVariantInsert':
		"""
		Add Attributes.

		:param variant_attribute: VariantAttribute 
		:raises Exception:
		:returns: {ProductVariantInsert}
		"""

		if isinstance(variant_attribute, merchantapi.model.VariantAttribute):
			self.attributes.append(variant_attribute)
		elif isinstance(variant_attribute, dict):
			self.attributes.append(merchantapi.model.VariantAttribute(variant_attribute))
		else:
			raise Exception('Expected instance of VariantAttribute or dict')
		return self

	def add_attributes(self, attributes: list) -> 'ProductVariantInsert':
		"""
		Add many VariantAttribute.

		:param attributes: List of VariantAttribute
		:raises Exception:
		:returns: ProductVariantInsert
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.VariantAttribute):
				raise Exception('')
			self.attributes.append(e)

		return self
	
	def add_variant_part(self, variant_part) -> 'ProductVariantInsert':
		"""
		Add Parts.

		:param variant_part: VariantPart 
		:raises Exception:
		:returns: {ProductVariantInsert}
		"""

		if isinstance(variant_part, merchantapi.model.VariantPart):
			self.parts.append(variant_part)
		elif isinstance(variant_part, dict):
			self.parts.append(merchantapi.model.VariantPart(variant_part))
		else:
			raise Exception('Expected instance of VariantPart or dict')
		return self

	def add_parts(self, parts: list) -> 'ProductVariantInsert':
		"""
		Add many VariantPart.

		:param parts: List of VariantPart
		:raises Exception:
		:returns: ProductVariantInsert
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.VariantPart):
				raise Exception('')
			self.parts.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if len(self.attributes):
			data['Attributes'] = []

			for f in self.attributes:
				data['Attributes'].append(f.to_dict())
		if len(self.parts):
			data['Parts'] = []

			for f in self.parts:
				data['Parts'].append(f.to_dict())
		return data


"""
Handles API Request ProductVariant_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariant_update
"""


class ProductVariantUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_variant: merchantapi.model.ProductVariant = None):
		"""
		ProductVariantUpdate Constructor.

		:param client: Client
		:param product_variant: ProductVariant
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.variant_id = None
		self.attributes = []
		self.parts = []
		if isinstance(product_variant, merchantapi.model.ProductVariant):
			if product_variant.get_product_id():
				self.set_product_id(product_variant.get_product_id())

			if product_variant.get_variant_id():
				self.set_variant_id(product_variant.get_variant_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariant_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_variant_id(self) -> int:
		"""
		Get Variant_ID.

		:returns: int
		"""

		return self.variant_id

	def get_attributes(self) -> list:
		"""
		Get Attributes.

		:returns: List of VariantAttribute
		"""

		return self.attributes

	def get_parts(self) -> list:
		"""
		Get Parts.

		:returns: List of VariantPart
		"""

		return self.parts

	def set_product_id(self, product_id: int) -> 'ProductVariantUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_variant_id(self, variant_id: int) -> 'ProductVariantUpdate':
		"""
		Set Variant_ID.

		:param variant_id: int
		:returns: ProductVariantUpdate
		"""

		self.variant_id = variant_id
		return self

	def set_attributes(self, attributes: list) -> 'ProductVariantUpdate':
		"""
		Set Attributes.

		:param attributes: {VariantAttribute[]}
		:raises Exception:
		:returns: ProductVariantUpdate
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.VariantAttribute):
				raise Exception("")
		self.attributes = attributes
		return self

	def set_parts(self, parts: list) -> 'ProductVariantUpdate':
		"""
		Set Parts.

		:param parts: {VariantPart[]}
		:raises Exception:
		:returns: ProductVariantUpdate
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.VariantPart):
				raise Exception("")
		self.parts = parts
		return self
	
	def add_variant_attribute(self, variant_attribute) -> 'ProductVariantUpdate':
		"""
		Add Attributes.

		:param variant_attribute: VariantAttribute 
		:raises Exception:
		:returns: {ProductVariantUpdate}
		"""

		if isinstance(variant_attribute, merchantapi.model.VariantAttribute):
			self.attributes.append(variant_attribute)
		elif isinstance(variant_attribute, dict):
			self.attributes.append(merchantapi.model.VariantAttribute(variant_attribute))
		else:
			raise Exception('Expected instance of VariantAttribute or dict')
		return self

	def add_attributes(self, attributes: list) -> 'ProductVariantUpdate':
		"""
		Add many VariantAttribute.

		:param attributes: List of VariantAttribute
		:raises Exception:
		:returns: ProductVariantUpdate
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.VariantAttribute):
				raise Exception('')
			self.attributes.append(e)

		return self
	
	def add_variant_part(self, variant_part) -> 'ProductVariantUpdate':
		"""
		Add Parts.

		:param variant_part: VariantPart 
		:raises Exception:
		:returns: {ProductVariantUpdate}
		"""

		if isinstance(variant_part, merchantapi.model.VariantPart):
			self.parts.append(variant_part)
		elif isinstance(variant_part, dict):
			self.parts.append(merchantapi.model.VariantPart(variant_part))
		else:
			raise Exception('Expected instance of VariantPart or dict')
		return self

	def add_parts(self, parts: list) -> 'ProductVariantUpdate':
		"""
		Add many VariantPart.

		:param parts: List of VariantPart
		:raises Exception:
		:returns: ProductVariantUpdate
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.VariantPart):
				raise Exception('')
			self.parts.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.variant_id is not None:
			data['Variant_ID'] = self.variant_id

		if len(self.attributes):
			data['Attributes'] = []

			for f in self.attributes:
				data['Attributes'].append(f.to_dict())
		if len(self.parts):
			data['Parts'] = []

			for f in self.parts:
				data['Parts'].append(f.to_dict())
		return data


"""
Handles API Request ProductVariant_Generate. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariant_generate
"""


class ProductVariantGenerate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantGenerate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.pricing_method = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_product_code(product.get_code())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariant_Generate'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_pricing_method(self) -> int:
		"""
		Get Pricing_Method.

		:returns: int
		"""

		return self.pricing_method

	def set_product_id(self, product_id: int) -> 'ProductVariantGenerate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantGenerate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantGenerate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantGenerate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantGenerate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantGenerate
		"""

		self.edit_product = edit_product
		return self

	def set_pricing_method(self, pricing_method: int) -> 'ProductVariantGenerate':
		"""
		Set Pricing_Method.

		:param pricing_method: int
		:returns: ProductVariantGenerate
		"""

		self.pricing_method = pricing_method
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantGenerate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantGenerate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantGenerate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		data['Pricing_Method'] = self.pricing_method
		return data


"""
Handles API Request ProductVariant_Generate_Delimiter. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariant_generate_delimiter
"""


class ProductVariantGenerateDelimiter(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantGenerateDelimiter Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.pricing_method = None
		self.delimiter = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_product_code(product.get_code())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariant_Generate_Delimiter'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_pricing_method(self) -> int:
		"""
		Get Pricing_Method.

		:returns: int
		"""

		return self.pricing_method

	def get_delimiter(self) -> str:
		"""
		Get Delimiter.

		:returns: str
		"""

		return self.delimiter

	def set_product_id(self, product_id: int) -> 'ProductVariantGenerateDelimiter':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantGenerateDelimiter
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantGenerateDelimiter':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantGenerateDelimiter
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantGenerateDelimiter':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantGenerateDelimiter
		"""

		self.edit_product = edit_product
		return self

	def set_pricing_method(self, pricing_method: int) -> 'ProductVariantGenerateDelimiter':
		"""
		Set Pricing_Method.

		:param pricing_method: int
		:returns: ProductVariantGenerateDelimiter
		"""

		self.pricing_method = pricing_method
		return self

	def set_delimiter(self, delimiter: str) -> 'ProductVariantGenerateDelimiter':
		"""
		Set Delimiter.

		:param delimiter: str
		:returns: ProductVariantGenerateDelimiter
		"""

		self.delimiter = delimiter
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantGenerateDelimiter':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantGenerateDelimiter':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantGenerateDelimiter(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		data['Pricing_Method'] = self.pricing_method
		if self.delimiter is not None:
			data['Delimiter'] = self.delimiter
		return data


"""
Handles API Request ProductKitList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productkitlist_load_query
"""


class ProductKitListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'product_code',
		'product_name',
		'attr_code',
		'attr_prompt',
		'option_code',
		'option_prompt',
		'attr_code',
		'attr_prompt',
		'option_code',
		'option_prompt'
	]

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductKitListLoadQuery Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductKitList_Load_Query'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def set_product_id(self, product_id: int) -> 'ProductKitListLoadQuery':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductKitListLoadQuery
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductKitListLoadQuery':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductKitListLoadQuery
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductKitListLoadQuery':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductKitListLoadQuery
		"""

		self.edit_product = edit_product
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductKitListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductKitListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductKitListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		return data


"""
Handles API Request ProductKit_Generate_Variants. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productkit_generate_variants
"""


class ProductKitGenerateVariants(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductKitGenerateVariants Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.pricing_method = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductKit_Generate_Variants'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_pricing_method(self) -> int:
		"""
		Get Pricing_Method.

		:returns: int
		"""

		return self.pricing_method

	def set_product_id(self, product_id: int) -> 'ProductKitGenerateVariants':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductKitGenerateVariants
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductKitGenerateVariants':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductKitGenerateVariants
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductKitGenerateVariants':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductKitGenerateVariants
		"""

		self.edit_product = edit_product
		return self

	def set_pricing_method(self, pricing_method: int) -> 'ProductKitGenerateVariants':
		"""
		Set Pricing_Method.

		:param pricing_method: int
		:returns: ProductKitGenerateVariants
		"""

		self.pricing_method = pricing_method
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductKitGenerateVariants':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductKitGenerateVariants':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductKitGenerateVariants(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		data['Pricing_Method'] = self.pricing_method
		return data


"""
Handles API Request ProductKit_Update_Parts. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productkit_update_parts
"""


class ProductKitUpdateParts(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductKitUpdateParts Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.attribute_template_attribute_id = None
		self.option_id = None
		self.parts = []
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductKit_Update_Parts'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_option_id(self) -> int:
		"""
		Get Option_ID.

		:returns: int
		"""

		return self.option_id

	def get_parts(self) -> list:
		"""
		Get Parts.

		:returns: List of KitPart
		"""

		return self.parts

	def set_product_id(self, product_id: int) -> 'ProductKitUpdateParts':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductKitUpdateParts
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductKitUpdateParts':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductKitUpdateParts
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductKitUpdateParts':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductKitUpdateParts
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'ProductKitUpdateParts':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: ProductKitUpdateParts
		"""

		self.attribute_id = attribute_id
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'ProductKitUpdateParts':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: ProductKitUpdateParts
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_option_id(self, option_id: int) -> 'ProductKitUpdateParts':
		"""
		Set Option_ID.

		:param option_id: int
		:returns: ProductKitUpdateParts
		"""

		self.option_id = option_id
		return self

	def set_parts(self, parts: list) -> 'ProductKitUpdateParts':
		"""
		Set Parts.

		:param parts: {KitPart[]}
		:raises Exception:
		:returns: ProductKitUpdateParts
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.KitPart):
				raise Exception("")
		self.parts = parts
		return self
	
	def add_kit_part(self, kit_part) -> 'ProductKitUpdateParts':
		"""
		Add Parts.

		:param kit_part: KitPart 
		:raises Exception:
		:returns: {ProductKitUpdateParts}
		"""

		if isinstance(kit_part, merchantapi.model.KitPart):
			self.parts.append(kit_part)
		elif isinstance(kit_part, dict):
			self.parts.append(merchantapi.model.KitPart(kit_part))
		else:
			raise Exception('Expected instance of KitPart or dict')
		return self

	def add_parts(self, parts: list) -> 'ProductKitUpdateParts':
		"""
		Add many KitPart.

		:param parts: List of KitPart
		:raises Exception:
		:returns: ProductKitUpdateParts
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.KitPart):
				raise Exception('')
			self.parts.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductKitUpdateParts':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductKitUpdateParts':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductKitUpdateParts(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id

		if self.option_id is not None:
			data['Option_ID'] = self.option_id

		if len(self.parts):
			data['Parts'] = []

			for f in self.parts:
				data['Parts'].append(f.to_dict())
		return data


"""
Handles API Request ProductKit_Variant_Count. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productkit_variant_count
"""


class ProductKitVariantCount(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductKitVariantCount Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_product_code(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductKit_Variant_Count'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def set_product_id(self, product_id: int) -> 'ProductKitVariantCount':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductKitVariantCount
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductKitVariantCount':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductKitVariantCount
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductKitVariantCount':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductKitVariantCount
		"""

		self.edit_product = edit_product
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductKitVariantCount':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductKitVariantCount':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductKitVariantCount(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		return data


"""
Handles API Request RelatedProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/relatedproduct_update_assigned
"""


class RelatedProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		RelatedProductUpdateAssigned Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.related_product_id = None
		self.related_product_code = None
		self.edit_related_product = None
		self.assigned = False
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'RelatedProduct_Update_Assigned'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_related_product_id(self) -> int:
		"""
		Get RelatedProduct_ID.

		:returns: int
		"""

		return self.related_product_id

	def get_related_product_code(self) -> str:
		"""
		Get RelatedProduct_Code.

		:returns: str
		"""

		return self.related_product_code

	def get_edit_related_product(self) -> str:
		"""
		Get Edit_RelatedProduct.

		:returns: str
		"""

		return self.edit_related_product

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_product_id(self, product_id: int) -> 'RelatedProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: RelatedProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'RelatedProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: RelatedProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'RelatedProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: RelatedProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_related_product_id(self, related_product_id: int) -> 'RelatedProductUpdateAssigned':
		"""
		Set RelatedProduct_ID.

		:param related_product_id: int
		:returns: RelatedProductUpdateAssigned
		"""

		self.related_product_id = related_product_id
		return self

	def set_related_product_code(self, related_product_code: str) -> 'RelatedProductUpdateAssigned':
		"""
		Set RelatedProduct_Code.

		:param related_product_code: str
		:returns: RelatedProductUpdateAssigned
		"""

		self.related_product_code = related_product_code
		return self

	def set_edit_related_product(self, edit_related_product: str) -> 'RelatedProductUpdateAssigned':
		"""
		Set Edit_RelatedProduct.

		:param edit_related_product: str
		:returns: RelatedProductUpdateAssigned
		"""

		self.edit_related_product = edit_related_product
		return self

	def set_assigned(self, assigned: bool) -> 'RelatedProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: RelatedProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.RelatedProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'RelatedProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.RelatedProductUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.related_product_id is not None:
			data['RelatedProduct_ID'] = self.related_product_id
		elif self.related_product_code is not None:
			data['RelatedProduct_Code'] = self.related_product_code
		elif self.edit_related_product is not None:
			data['Edit_RelatedProduct'] = self.edit_related_product

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data


"""
Handles API Request InventoryProductSettings_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/inventoryproductsettings_update
"""


class InventoryProductSettingsUpdate(merchantapi.abstract.Request):
	# INVENTORY_CHOICE constants.
	INVENTORY_CHOICE_DEFAULT = 'd'
	INVENTORY_CHOICE_YES = 'y'
	INVENTORY_CHOICE_NO = 'n'

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		InventoryProductSettingsUpdate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.track_low_stock_level = None
		self.track_out_of_stock_level = None
		self.hide_out_of_stock_products = None
		self.low_stock_level = None
		self.out_of_stock_level = None
		self.track_product = False
		self.in_stock_message_short = None
		self.in_stock_message_long = None
		self.low_stock_message_short = None
		self.low_stock_message_long = None
		self.out_of_stock_message_short = None
		self.out_of_stock_message_long = None
		self.limited_stock_message = None
		self.adjust_stock_by = None
		self.current_stock = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'InventoryProductSettings_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_track_low_stock_level(self) -> str:
		"""
		Get TrackLowStockLevel.

		:returns: str
		"""

		return self.track_low_stock_level

	def get_track_out_of_stock_level(self) -> str:
		"""
		Get TrackOutOfStockLevel.

		:returns: str
		"""

		return self.track_out_of_stock_level

	def get_hide_out_of_stock_products(self) -> str:
		"""
		Get HideOutOfStockProducts.

		:returns: str
		"""

		return self.hide_out_of_stock_products

	def get_low_stock_level(self) -> int:
		"""
		Get LowStockLevel.

		:returns: int
		"""

		return self.low_stock_level

	def get_out_of_stock_level(self) -> int:
		"""
		Get OutOfStockLevel.

		:returns: int
		"""

		return self.out_of_stock_level

	def get_track_product(self) -> bool:
		"""
		Get TrackProduct.

		:returns: bool
		"""

		return self.track_product

	def get_in_stock_message_short(self) -> str:
		"""
		Get InStockMessageShort.

		:returns: str
		"""

		return self.in_stock_message_short

	def get_in_stock_message_long(self) -> str:
		"""
		Get InStockMessageLong.

		:returns: str
		"""

		return self.in_stock_message_long

	def get_low_stock_message_short(self) -> str:
		"""
		Get LowStockMessageShort.

		:returns: str
		"""

		return self.low_stock_message_short

	def get_low_stock_message_long(self) -> str:
		"""
		Get LowStockMessageLong.

		:returns: str
		"""

		return self.low_stock_message_long

	def get_out_of_stock_message_short(self) -> str:
		"""
		Get OutOfStockMessageShort.

		:returns: str
		"""

		return self.out_of_stock_message_short

	def get_out_of_stock_message_long(self) -> str:
		"""
		Get OutOfStockMessageLong.

		:returns: str
		"""

		return self.out_of_stock_message_long

	def get_limited_stock_message(self) -> str:
		"""
		Get LimitedStockMessage.

		:returns: str
		"""

		return self.limited_stock_message

	def get_adjust_stock_by(self) -> int:
		"""
		Get AdjustStockBy.

		:returns: int
		"""

		return self.adjust_stock_by

	def get_current_stock(self) -> int:
		"""
		Get CurrentStock.

		:returns: int
		"""

		return self.current_stock

	def set_product_id(self, product_id: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_track_low_stock_level(self, track_low_stock_level: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set TrackLowStockLevel.

		:param track_low_stock_level: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.track_low_stock_level = track_low_stock_level
		return self

	def set_track_out_of_stock_level(self, track_out_of_stock_level: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set TrackOutOfStockLevel.

		:param track_out_of_stock_level: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.track_out_of_stock_level = track_out_of_stock_level
		return self

	def set_hide_out_of_stock_products(self, hide_out_of_stock_products: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set HideOutOfStockProducts.

		:param hide_out_of_stock_products: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.hide_out_of_stock_products = hide_out_of_stock_products
		return self

	def set_low_stock_level(self, low_stock_level: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set LowStockLevel.

		:param low_stock_level: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.low_stock_level = low_stock_level
		return self

	def set_out_of_stock_level(self, out_of_stock_level: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set OutOfStockLevel.

		:param out_of_stock_level: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.out_of_stock_level = out_of_stock_level
		return self

	def set_track_product(self, track_product: bool) -> 'InventoryProductSettingsUpdate':
		"""
		Set TrackProduct.

		:param track_product: bool
		:returns: InventoryProductSettingsUpdate
		"""

		self.track_product = track_product
		return self

	def set_in_stock_message_short(self, in_stock_message_short: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set InStockMessageShort.

		:param in_stock_message_short: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.in_stock_message_short = in_stock_message_short
		return self

	def set_in_stock_message_long(self, in_stock_message_long: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set InStockMessageLong.

		:param in_stock_message_long: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.in_stock_message_long = in_stock_message_long
		return self

	def set_low_stock_message_short(self, low_stock_message_short: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set LowStockMessageShort.

		:param low_stock_message_short: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.low_stock_message_short = low_stock_message_short
		return self

	def set_low_stock_message_long(self, low_stock_message_long: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set LowStockMessageLong.

		:param low_stock_message_long: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.low_stock_message_long = low_stock_message_long
		return self

	def set_out_of_stock_message_short(self, out_of_stock_message_short: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set OutOfStockMessageShort.

		:param out_of_stock_message_short: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.out_of_stock_message_short = out_of_stock_message_short
		return self

	def set_out_of_stock_message_long(self, out_of_stock_message_long: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set OutOfStockMessageLong.

		:param out_of_stock_message_long: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.out_of_stock_message_long = out_of_stock_message_long
		return self

	def set_limited_stock_message(self, limited_stock_message: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set LimitedStockMessage.

		:param limited_stock_message: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.limited_stock_message = limited_stock_message
		return self

	def set_adjust_stock_by(self, adjust_stock_by: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set AdjustStockBy.

		:param adjust_stock_by: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.adjust_stock_by = adjust_stock_by
		return self

	def set_current_stock(self, current_stock: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set CurrentStock.

		:param current_stock: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.current_stock = current_stock
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.InventoryProductSettingsUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'InventoryProductSettingsUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.InventoryProductSettingsUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.track_low_stock_level is not None:
			data['TrackLowStockLevel'] = self.track_low_stock_level
		if self.track_out_of_stock_level is not None:
			data['TrackOutOfStockLevel'] = self.track_out_of_stock_level
		if self.hide_out_of_stock_products is not None:
			data['HideOutOfStockProducts'] = self.hide_out_of_stock_products
		if self.low_stock_level is not None:
			data['LowStockLevel'] = self.low_stock_level
		if self.out_of_stock_level is not None:
			data['OutOfStockLevel'] = self.out_of_stock_level
		if self.track_product is not None:
			data['TrackProduct'] = self.track_product
		if self.in_stock_message_short is not None:
			data['InStockMessageShort'] = self.in_stock_message_short
		if self.in_stock_message_long is not None:
			data['InStockMessageLong'] = self.in_stock_message_long
		if self.low_stock_message_short is not None:
			data['LowStockMessageShort'] = self.low_stock_message_short
		if self.low_stock_message_long is not None:
			data['LowStockMessageLong'] = self.low_stock_message_long
		if self.out_of_stock_message_short is not None:
			data['OutOfStockMessageShort'] = self.out_of_stock_message_short
		if self.out_of_stock_message_long is not None:
			data['OutOfStockMessageLong'] = self.out_of_stock_message_long
		if self.limited_stock_message is not None:
			data['LimitedStockMessage'] = self.limited_stock_message
		if self.adjust_stock_by is not None:
			data['AdjustStockBy'] = self.adjust_stock_by
		if self.current_stock is not None:
			data['CurrentStock'] = self.current_stock
		return data


"""
Handles API Request ProductVariantList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariantlist_delete
"""


class ProductVariantListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantListDelete Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.product_variant_ids = []
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariantList_Delete'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_variant_ids(self):
		"""
		Get ProductVariant_IDs.

		:returns: list
		"""

		return self.product_variant_ids

	def set_product_id(self, product_id: int) -> 'ProductVariantListDelete':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantListDelete
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantListDelete':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantListDelete
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantListDelete':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantListDelete
		"""

		self.edit_product = edit_product
		return self
	
	def add_variant_id(self, variant_id) -> 'ProductVariantListDelete':
		"""
		Add ProductVariant_IDs.

		:param variant_id: int
		:returns: {ProductVariantListDelete}
		"""

		self.product_variant_ids.append(variant_id)
		return self

	def add_product_variant(self, product_variant: merchantapi.model.ProductVariant) -> 'ProductVariantListDelete':
		"""
		Add ProductVariant model.

		:param product_variant: ProductVariant
		:raises Exception:
		:returns: ProductVariantListDelete
		"""
		if not isinstance(product_variant, merchantapi.model.ProductVariant):
			raise Exception('Expected an instance of ProductVariant')

		if product_variant.get_variant_id():
			self.product_variant_ids.append(product_variant.get_variant_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		data['ProductVariant_IDs'] = self.product_variant_ids
		return data


"""
Handles API Request ImageTypeList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/imagetypelist_load_query
"""


class ImageTypeListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'code',
		'descrip'
	]

	def __init__(self, client: Client = None):
		"""
		ImageTypeListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ImageTypeList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ImageTypeListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ImageTypeListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ImageTypeListLoadQuery(self, http_response, data)


"""
Handles API Request ProductImage_Update_Type. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productimage_update_type
"""


class ProductImageUpdateType(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProductImageUpdateType Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.product_image_id = None
		self.image_type_id = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductImage_Update_Type'

	def get_product_image_id(self) -> int:
		"""
		Get ProductImage_ID.

		:returns: int
		"""

		return self.product_image_id

	def get_image_type_id(self) -> int:
		"""
		Get ImageType_ID.

		:returns: int
		"""

		return self.image_type_id

	def set_product_image_id(self, product_image_id: int) -> 'ProductImageUpdateType':
		"""
		Set ProductImage_ID.

		:param product_image_id: int
		:returns: ProductImageUpdateType
		"""

		self.product_image_id = product_image_id
		return self

	def set_image_type_id(self, image_type_id: int) -> 'ProductImageUpdateType':
		"""
		Set ImageType_ID.

		:param image_type_id: int
		:returns: ProductImageUpdateType
		"""

		self.image_type_id = image_type_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductImageUpdateType':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductImageUpdateType':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductImageUpdateType(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['ProductImage_ID'] = self.product_image_id
		if self.image_type_id is not None:
			data['ImageType_ID'] = self.image_type_id
		return data


"""
Handles API Request AttributeTemplateList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplatelist_load_query
"""


class AttributeTemplateListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'code',
		'prompt',
		'refcount'
	]

	available_sort_fields = [
		'id',
		'code',
		'prompt',
		'refcount'
	]

	def __init__(self, client: Client = None):
		"""
		AttributeTemplateListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateListLoadQuery(self, http_response, data)


"""
Handles API Request AttributeTemplateAttributeList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateattributelist_load_query
"""


class AttributeTemplateAttributeListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'attr_code',
		'attr_prompt',
		'attr_price',
		'attr_cost',
		'attr_weight',
		'attr_image',
		'opt_code',
		'opt_prompt',
		'opt_price',
		'opt_cost',
		'opt_weight',
		'opt_image',
		'code',
		'prompt',
		'price',
		'cost',
		'weight',
		'image',
		'required',
		'inventory'
	]

	available_sort_fields = [
		'id',
		'code',
		'type',
		'prompt',
		'price',
		'cost',
		'weight',
		'image',
		'required',
		'inventory',
		'attr_code',
		'attr_prompt',
		'attr_price',
		'attr_cost',
		'attr_weight',
		'attr_image',
		'opt_code',
		'opt_prompt',
		'opt_price',
		'opt_cost',
		'opt_weight',
		'opt_image'
	]

	def __init__(self, client: Client = None, attribute_template: merchantapi.model.AttributeTemplate = None):
		"""
		AttributeTemplateAttributeListLoadQuery Constructor.

		:param client: Client
		:param attribute_template: AttributeTemplate
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		if isinstance(attribute_template, merchantapi.model.AttributeTemplate):
			if attribute_template.get_id():
				self.set_attribute_template_id(attribute_template.get_id())
			elif attribute_template.get_code():
				self.set_attribute_template_code(attribute_template.get_code())
			elif attribute_template.get_code():
				self.set_edit_attribute_template(attribute_template.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateAttributeList_Load_Query'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateAttributeListLoadQuery':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateAttributeListLoadQuery
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateAttributeListLoadQuery':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateAttributeListLoadQuery
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateAttributeListLoadQuery':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateAttributeListLoadQuery
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateAttributeListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateAttributeListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateAttributeListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		return data


"""
Handles API Request AttributeTemplateOptionList_Load_Attribute. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateoptionlist_load_attribute
"""


class AttributeTemplateOptionListLoadAttribute(ListQueryRequest):
	def __init__(self, client: Client = None, attribute_template_attribute: merchantapi.model.AttributeTemplateAttribute = None):
		"""
		AttributeTemplateOptionListLoadAttribute Constructor.

		:param client: Client
		:param attribute_template_attribute: AttributeTemplateAttribute
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
		if isinstance(attribute_template_attribute, merchantapi.model.AttributeTemplateAttribute):
			if attribute_template_attribute.get_id():
				self.set_attribute_template_attribute_id(attribute_template_attribute.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateOptionList_Load_Attribute'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get AttributeTemplateAttribute_Code.

		:returns: str
		"""

		return self.attribute_template_attribute_code

	def get_edit_attribute_template_attribute(self) -> str:
		"""
		Get Edit_AttributeTemplateAttribute.

		:returns: str
		"""

		return self.edit_attribute_template_attribute

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateOptionListLoadAttribute':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateOptionListLoadAttribute
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateOptionListLoadAttribute':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateOptionListLoadAttribute
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateOptionListLoadAttribute':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateOptionListLoadAttribute
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateOptionListLoadAttribute':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateOptionListLoadAttribute
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateOptionListLoadAttribute':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateOptionListLoadAttribute
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateOptionListLoadAttribute':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateOptionListLoadAttribute
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateOptionListLoadAttribute':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateOptionListLoadAttribute':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateOptionListLoadAttribute(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id
		elif self.attribute_template_attribute_code is not None:
			data['AttributeTemplateAttribute_Code'] = self.attribute_template_attribute_code
		elif self.edit_attribute_template_attribute is not None:
			data['Edit_AttributeTemplateAttribute'] = self.edit_attribute_template_attribute

		return data


"""
Handles API Request AttributeTemplateAttribute_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_delete
"""


class AttributeTemplateAttributeDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_attribute: merchantapi.model.AttributeTemplateAttribute = None):
		"""
		AttributeTemplateAttributeDelete Constructor.

		:param client: Client
		:param attribute_template_attribute: AttributeTemplateAttribute
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
		if isinstance(attribute_template_attribute, merchantapi.model.AttributeTemplateAttribute):
			if attribute_template_attribute.get_id():
				self.set_attribute_template_attribute_id(attribute_template_attribute.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateAttribute_Delete'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get AttributeTemplateAttribute_Code.

		:returns: str
		"""

		return self.attribute_template_attribute_code

	def get_edit_attribute_template_attribute(self) -> str:
		"""
		Get Edit_AttributeTemplateAttribute.

		:returns: str
		"""

		return self.edit_attribute_template_attribute

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateAttributeDelete':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateAttributeDelete
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateAttributeDelete':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateAttributeDelete
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateAttributeDelete':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateAttributeDelete
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateAttributeDelete':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateAttributeDelete
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateAttributeDelete':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateAttributeDelete
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateAttributeDelete':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateAttributeDelete
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateAttributeDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateAttributeDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateAttributeDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id
		elif self.attribute_template_attribute_code is not None:
			data['AttributeTemplateAttribute_Code'] = self.attribute_template_attribute_code
		elif self.edit_attribute_template_attribute is not None:
			data['Edit_AttributeTemplateAttribute'] = self.edit_attribute_template_attribute

		return data


"""
Handles API Request AttributeTemplateAttribute_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_insert
"""


class AttributeTemplateAttributeInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template: merchantapi.model.AttributeTemplate = None):
		"""
		AttributeTemplateAttributeInsert Constructor.

		:param client: Client
		:param attribute_template: AttributeTemplate
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.code = None
		self.prompt = None
		self.type = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.copy = False
		self.required = False
		self.inventory = False
		if isinstance(attribute_template, merchantapi.model.AttributeTemplate):
			if attribute_template.get_id():
				self.set_attribute_template_id(attribute_template.get_id())
			elif attribute_template.get_code():
				self.set_attribute_template_code(attribute_template.get_code())
			elif attribute_template.get_code():
				self.set_edit_attribute_template(attribute_template.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateAttribute_Insert'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_type(self) -> str:
		"""
		Get Type.

		:returns: str
		"""

		return self.type

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_copy(self) -> bool:
		"""
		Get Copy.

		:returns: bool
		"""

		return self.copy

	def get_required(self) -> bool:
		"""
		Get Required.

		:returns: bool
		"""

		return self.required

	def get_inventory(self) -> bool:
		"""
		Get Inventory.

		:returns: bool
		"""

		return self.inventory

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateAttributeInsert':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateAttributeInsert
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_code(self, code: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.prompt = prompt
		return self

	def set_type(self, type: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Type.

		:param type: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.type = type
		return self

	def set_image(self, image: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Image.

		:param image: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Price.

		:param price: float
		:returns: AttributeTemplateAttributeInsert
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeTemplateAttributeInsert
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeTemplateAttributeInsert
		"""

		self.weight = weight
		return self

	def set_copy(self, copy: bool) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Copy.

		:param copy: bool
		:returns: AttributeTemplateAttributeInsert
		"""

		self.copy = copy
		return self

	def set_required(self, required: bool) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Required.

		:param required: bool
		:returns: AttributeTemplateAttributeInsert
		"""

		self.required = required
		return self

	def set_inventory(self, inventory: bool) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Inventory.

		:param inventory: bool
		:returns: AttributeTemplateAttributeInsert
		"""

		self.inventory = inventory
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateAttributeInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateAttributeInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateAttributeInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		data['Code'] = self.code
		if self.prompt is not None:
			data['Prompt'] = self.prompt
		data['Type'] = self.type
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.copy is not None:
			data['Copy'] = self.copy
		if self.required is not None:
			data['Required'] = self.required
		if self.inventory is not None:
			data['Inventory'] = self.inventory
		return data


"""
Handles API Request AttributeTemplateAttribute_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_update
"""


class AttributeTemplateAttributeUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_attribute: merchantapi.model.AttributeTemplateAttribute = None):
		"""
		AttributeTemplateAttributeUpdate Constructor.

		:param client: Client
		:param attribute_template_attribute: AttributeTemplateAttribute
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
		self.code = None
		self.prompt = None
		self.type = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.copy = False
		self.required = False
		self.inventory = False
		if isinstance(attribute_template_attribute, merchantapi.model.AttributeTemplateAttribute):
			if attribute_template_attribute.get_id():
				self.set_attribute_template_attribute_id(attribute_template_attribute.get_id())
			elif attribute_template_attribute.get_code():
				self.set_attribute_template_attribute_code(attribute_template_attribute.get_code())
			elif attribute_template_attribute.get_code():
				self.set_edit_attribute_template_attribute(attribute_template_attribute.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateAttribute_Update'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get AttributeTemplateAttribute_Code.

		:returns: str
		"""

		return self.attribute_template_attribute_code

	def get_edit_attribute_template_attribute(self) -> str:
		"""
		Get Edit_AttributeTemplateAttribute.

		:returns: str
		"""

		return self.edit_attribute_template_attribute

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_type(self) -> str:
		"""
		Get Type.

		:returns: str
		"""

		return self.type

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_copy(self) -> bool:
		"""
		Get Copy.

		:returns: bool
		"""

		return self.copy

	def get_required(self) -> bool:
		"""
		Get Required.

		:returns: bool
		"""

		return self.required

	def get_inventory(self) -> bool:
		"""
		Get Inventory.

		:returns: bool
		"""

		return self.inventory

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	def set_code(self, code: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.prompt = prompt
		return self

	def set_type(self, type: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Type.

		:param type: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.type = type
		return self

	def set_image(self, image: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Image.

		:param image: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Price.

		:param price: float
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.weight = weight
		return self

	def set_copy(self, copy: bool) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Copy.

		:param copy: bool
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.copy = copy
		return self

	def set_required(self, required: bool) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Required.

		:param required: bool
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.required = required
		return self

	def set_inventory(self, inventory: bool) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Inventory.

		:param inventory: bool
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.inventory = inventory
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateAttributeUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateAttributeUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateAttributeUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id
		elif self.attribute_template_attribute_code is not None:
			data['AttributeTemplateAttribute_Code'] = self.attribute_template_attribute_code
		elif self.edit_attribute_template_attribute is not None:
			data['Edit_AttributeTemplateAttribute'] = self.edit_attribute_template_attribute

		data['Code'] = self.code
		if self.prompt is not None:
			data['Prompt'] = self.prompt
		if self.type is not None:
			data['Type'] = self.type
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.copy is not None:
			data['Copy'] = self.copy
		if self.required is not None:
			data['Required'] = self.required
		if self.inventory is not None:
			data['Inventory'] = self.inventory
		return data


"""
Handles API Request AttributeTemplateOption_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateoption_delete
"""


class AttributeTemplateOptionDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_option: merchantapi.model.AttributeTemplateOption = None):
		"""
		AttributeTemplateOptionDelete Constructor.

		:param client: Client
		:param attribute_template_option: AttributeTemplateOption
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
		self.attribute_template_option_id = None
		self.attribute_template_option_code = None
		self.edit_attribute_template_option = None
		if isinstance(attribute_template_option, merchantapi.model.AttributeTemplateOption):
			if attribute_template_option.get_id():
				self.set_attribute_template_option_id(attribute_template_option.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateOption_Delete'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get AttributeTemplateAttribute_Code.

		:returns: str
		"""

		return self.attribute_template_attribute_code

	def get_edit_attribute_template_attribute(self) -> str:
		"""
		Get Edit_AttributeTemplateAttribute.

		:returns: str
		"""

		return self.edit_attribute_template_attribute

	def get_attribute_template_option_id(self) -> int:
		"""
		Get AttributeTemplateOption_ID.

		:returns: int
		"""

		return self.attribute_template_option_id

	def get_attribute_template_option_code(self) -> str:
		"""
		Get AttributeTemplateOption_Code.

		:returns: str
		"""

		return self.attribute_template_option_code

	def get_edit_attribute_template_option(self) -> str:
		"""
		Get Edit_AttributeTemplateOption.

		:returns: str
		"""

		return self.edit_attribute_template_option

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	def set_attribute_template_option_id(self, attribute_template_option_id: int) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplateOption_ID.

		:param attribute_template_option_id: int
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_option_id = attribute_template_option_id
		return self

	def set_attribute_template_option_code(self, attribute_template_option_code: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplateOption_Code.

		:param attribute_template_option_code: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_option_code = attribute_template_option_code
		return self

	def set_edit_attribute_template_option(self, edit_attribute_template_option: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set Edit_AttributeTemplateOption.

		:param edit_attribute_template_option: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.edit_attribute_template_option = edit_attribute_template_option
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateOptionDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateOptionDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateOptionDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id
		elif self.attribute_template_attribute_code is not None:
			data['AttributeTemplateAttribute_Code'] = self.attribute_template_attribute_code
		elif self.edit_attribute_template_attribute is not None:
			data['Edit_AttributeTemplateAttribute'] = self.edit_attribute_template_attribute

		if self.attribute_template_option_id is not None:
			data['AttributeTemplateOption_ID'] = self.attribute_template_option_id
		elif self.attribute_template_option_code is not None:
			data['AttributeTemplateOption_Code'] = self.attribute_template_option_code
		elif self.edit_attribute_template_option is not None:
			data['Edit_AttributeTemplateOption'] = self.edit_attribute_template_option

		return data


"""
Handles API Request AttributeTemplateOption_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateoption_insert
"""


class AttributeTemplateOptionInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_attribute: merchantapi.model.AttributeTemplateAttribute = None):
		"""
		AttributeTemplateOptionInsert Constructor.

		:param client: Client
		:param attribute_template_attribute: AttributeTemplateAttribute
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
		self.code = None
		self.prompt = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.default = False
		if isinstance(attribute_template_attribute, merchantapi.model.AttributeTemplateAttribute):
			if attribute_template_attribute.get_id():
				self.set_attribute_template_attribute_id(attribute_template_attribute.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateOption_Insert'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get AttributeTemplateAttribute_Code.

		:returns: str
		"""

		return self.attribute_template_attribute_code

	def get_edit_attribute_template_attribute(self) -> str:
		"""
		Get Edit_AttributeTemplateAttribute.

		:returns: str
		"""

		return self.edit_attribute_template_attribute

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_default(self) -> bool:
		"""
		Get Default.

		:returns: bool
		"""

		return self.default

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateOptionInsert':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateOptionInsert
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateOptionInsert':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateOptionInsert
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateOptionInsert':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateOptionInsert
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateOptionInsert':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateOptionInsert
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateOptionInsert':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateOptionInsert
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateOptionInsert':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateOptionInsert
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	def set_code(self, code: str) -> 'AttributeTemplateOptionInsert':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateOptionInsert
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateOptionInsert':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateOptionInsert
		"""

		self.prompt = prompt
		return self

	def set_image(self, image: str) -> 'AttributeTemplateOptionInsert':
		"""
		Set Image.

		:param image: str
		:returns: AttributeTemplateOptionInsert
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeTemplateOptionInsert':
		"""
		Set Price.

		:param price: float
		:returns: AttributeTemplateOptionInsert
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeTemplateOptionInsert':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeTemplateOptionInsert
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeTemplateOptionInsert':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeTemplateOptionInsert
		"""

		self.weight = weight
		return self

	def set_default(self, default: bool) -> 'AttributeTemplateOptionInsert':
		"""
		Set Default.

		:param default: bool
		:returns: AttributeTemplateOptionInsert
		"""

		self.default = default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateOptionInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateOptionInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateOptionInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id
		elif self.attribute_template_attribute_code is not None:
			data['AttributeTemplateAttribute_Code'] = self.attribute_template_attribute_code
		elif self.edit_attribute_template_attribute is not None:
			data['Edit_AttributeTemplateAttribute'] = self.edit_attribute_template_attribute

		data['Code'] = self.code
		data['Prompt'] = self.prompt
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.default is not None:
			data['Default'] = self.default
		return data


"""
Handles API Request AttributeTemplateOption_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateoption_update
"""


class AttributeTemplateOptionUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_option: merchantapi.model.AttributeTemplateOption = None):
		"""
		AttributeTemplateOptionUpdate Constructor.

		:param client: Client
		:param attribute_template_option: AttributeTemplateOption
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
		self.attribute_template_option_id = None
		self.attribute_template_option_code = None
		self.edit_attribute_template_option = None
		self.code = None
		self.prompt = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.default = False
		if isinstance(attribute_template_option, merchantapi.model.AttributeTemplateOption):
			if attribute_template_option.get_id():
				self.set_attribute_template_option_id(attribute_template_option.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateOption_Update'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get AttributeTemplateAttribute_Code.

		:returns: str
		"""

		return self.attribute_template_attribute_code

	def get_edit_attribute_template_attribute(self) -> str:
		"""
		Get Edit_AttributeTemplateAttribute.

		:returns: str
		"""

		return self.edit_attribute_template_attribute

	def get_attribute_template_option_id(self) -> int:
		"""
		Get AttributeTemplateOption_ID.

		:returns: int
		"""

		return self.attribute_template_option_id

	def get_attribute_template_option_code(self) -> str:
		"""
		Get AttributeTemplateOption_Code.

		:returns: str
		"""

		return self.attribute_template_option_code

	def get_edit_attribute_template_option(self) -> str:
		"""
		Get Edit_AttributeTemplateOption.

		:returns: str
		"""

		return self.edit_attribute_template_option

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_default(self) -> bool:
		"""
		Get Default.

		:returns: bool
		"""

		return self.default

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	def set_attribute_template_option_id(self, attribute_template_option_id: int) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplateOption_ID.

		:param attribute_template_option_id: int
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_option_id = attribute_template_option_id
		return self

	def set_attribute_template_option_code(self, attribute_template_option_code: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplateOption_Code.

		:param attribute_template_option_code: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_option_code = attribute_template_option_code
		return self

	def set_edit_attribute_template_option(self, edit_attribute_template_option: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Edit_AttributeTemplateOption.

		:param edit_attribute_template_option: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.edit_attribute_template_option = edit_attribute_template_option
		return self

	def set_code(self, code: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.prompt = prompt
		return self

	def set_image(self, image: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Image.

		:param image: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Price.

		:param price: float
		:returns: AttributeTemplateOptionUpdate
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeTemplateOptionUpdate
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeTemplateOptionUpdate
		"""

		self.weight = weight
		return self

	def set_default(self, default: bool) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Default.

		:param default: bool
		:returns: AttributeTemplateOptionUpdate
		"""

		self.default = default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateOptionUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateOptionUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateOptionUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id
		elif self.attribute_template_attribute_code is not None:
			data['AttributeTemplateAttribute_Code'] = self.attribute_template_attribute_code
		elif self.edit_attribute_template_attribute is not None:
			data['Edit_AttributeTemplateAttribute'] = self.edit_attribute_template_attribute

		if self.attribute_template_option_id is not None:
			data['AttributeTemplateOption_ID'] = self.attribute_template_option_id
		elif self.attribute_template_option_code is not None:
			data['AttributeTemplateOption_Code'] = self.attribute_template_option_code
		elif self.edit_attribute_template_option is not None:
			data['Edit_AttributeTemplateOption'] = self.edit_attribute_template_option

		data['Code'] = self.code
		data['Prompt'] = self.prompt
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.default is not None:
			data['Default'] = self.default
		return data


"""
Handles API Request AttributeTemplate_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplate_insert
"""


class AttributeTemplateInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		AttributeTemplateInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.code = None
		self.prompt = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplate_Insert'

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def set_code(self, code: str) -> 'AttributeTemplateInsert':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateInsert
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateInsert':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateInsert
		"""

		self.prompt = prompt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Code'] = self.code
		data['Prompt'] = self.prompt
		return data


"""
Handles API Request AttributeTemplate_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplate_update
"""


class AttributeTemplateUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template: merchantapi.model.AttributeTemplate = None):
		"""
		AttributeTemplateUpdate Constructor.

		:param client: Client
		:param attribute_template: AttributeTemplate
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.code = None
		self.prompt = None
		if isinstance(attribute_template, merchantapi.model.AttributeTemplate):
			if attribute_template.get_id():
				self.set_attribute_template_id(attribute_template.get_id())
			elif attribute_template.get_code():
				self.set_attribute_template_code(attribute_template.get_code())
			elif attribute_template.get_code():
				self.set_edit_attribute_template(attribute_template.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplate_Update'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateUpdate':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateUpdate
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateUpdate':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateUpdate
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateUpdate':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateUpdate
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_code(self, code: str) -> 'AttributeTemplateUpdate':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateUpdate
		"""

		self.prompt = prompt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		data['Code'] = self.code
		data['Prompt'] = self.prompt
		return data


"""
Handles API Request AttributeTemplate_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplate_delete
"""


class AttributeTemplateDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template: merchantapi.model.AttributeTemplate = None):
		"""
		AttributeTemplateDelete Constructor.

		:param client: Client
		:param attribute_template: AttributeTemplate
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		if isinstance(attribute_template, merchantapi.model.AttributeTemplate):
			if attribute_template.get_id():
				self.set_attribute_template_id(attribute_template.get_id())
			elif attribute_template.get_code():
				self.set_attribute_template_code(attribute_template.get_code())
			elif attribute_template.get_code():
				self.set_edit_attribute_template(attribute_template.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplate_Delete'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateDelete':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateDelete
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateDelete':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateDelete
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateDelete':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateDelete
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		return data


"""
Handles API Request AttributeTemplateOption_Set_Default. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateoption_set_default
"""


class AttributeTemplateOptionSetDefault(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_option: merchantapi.model.AttributeTemplateOption = None):
		"""
		AttributeTemplateOptionSetDefault Constructor.

		:param client: Client
		:param attribute_template_option: AttributeTemplateOption
		"""

		super().__init__(client)
		self.attribute_template_option_id = None
		self.attribute_template_option_code = None
		self.edit_attribute_template_option = None
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
		self.attribute_template_option_default = False
		if isinstance(attribute_template_option, merchantapi.model.AttributeTemplateOption):
			if attribute_template_option.get_id():
				self.set_attribute_template_option_id(attribute_template_option.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateOption_Set_Default'

	def get_attribute_template_option_id(self) -> int:
		"""
		Get AttributeTemplateOption_ID.

		:returns: int
		"""

		return self.attribute_template_option_id

	def get_attribute_template_option_code(self) -> str:
		"""
		Get AttributeTemplateOption_Code.

		:returns: str
		"""

		return self.attribute_template_option_code

	def get_edit_attribute_template_option(self) -> str:
		"""
		Get Edit_AttributeTemplateOption.

		:returns: str
		"""

		return self.edit_attribute_template_option

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get AttributeTemplateAttribute_Code.

		:returns: str
		"""

		return self.attribute_template_attribute_code

	def get_edit_attribute_template_attribute(self) -> str:
		"""
		Get Edit_AttributeTemplateAttribute.

		:returns: str
		"""

		return self.edit_attribute_template_attribute

	def get_attribute_template_option_default(self) -> bool:
		"""
		Get AttributeTemplateOption_Default.

		:returns: bool
		"""

		return self.attribute_template_option_default

	def set_attribute_template_option_id(self, attribute_template_option_id: int) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set AttributeTemplateOption_ID.

		:param attribute_template_option_id: int
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.attribute_template_option_id = attribute_template_option_id
		return self

	def set_attribute_template_option_code(self, attribute_template_option_code: str) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set AttributeTemplateOption_Code.

		:param attribute_template_option_code: str
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.attribute_template_option_code = attribute_template_option_code
		return self

	def set_edit_attribute_template_option(self, edit_attribute_template_option: str) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set Edit_AttributeTemplateOption.

		:param edit_attribute_template_option: str
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.edit_attribute_template_option = edit_attribute_template_option
		return self

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	def set_attribute_template_option_default(self, attribute_template_option_default: bool) -> 'AttributeTemplateOptionSetDefault':
		"""
		Set AttributeTemplateOption_Default.

		:param attribute_template_option_default: bool
		:returns: AttributeTemplateOptionSetDefault
		"""

		self.attribute_template_option_default = attribute_template_option_default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateOptionSetDefault':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateOptionSetDefault':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateOptionSetDefault(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id
		elif self.attribute_template_attribute_code is not None:
			data['AttributeTemplateAttribute_Code'] = self.attribute_template_attribute_code
		elif self.edit_attribute_template_attribute is not None:
			data['Edit_AttributeTemplateAttribute'] = self.edit_attribute_template_attribute

		if self.attribute_template_option_id is not None:
			data['AttributeTemplateOption_ID'] = self.attribute_template_option_id
		elif self.attribute_template_option_code is not None:
			data['AttributeTemplateOption_Code'] = self.attribute_template_option_code
		elif self.edit_attribute_template_option is not None:
			data['Edit_AttributeTemplateOption'] = self.edit_attribute_template_option

		data['AttributeTemplateOption_Default'] = self.attribute_template_option_default
		return data


"""
Handles API Request AttributeTemplateProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateproduct_update_assigned
"""


class AttributeTemplateProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template: merchantapi.model.AttributeTemplate = None):
		"""
		AttributeTemplateProductUpdateAssigned Constructor.

		:param client: Client
		:param attribute_template: AttributeTemplate
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.assigned = False
		if isinstance(attribute_template, merchantapi.model.AttributeTemplate):
			if attribute_template.get_id():
				self.set_attribute_template_id(attribute_template.get_id())
			elif attribute_template.get_code():
				self.set_attribute_template_code(attribute_template.get_code())
			elif attribute_template.get_code():
				self.set_edit_attribute_template(attribute_template.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateProduct_Update_Assigned'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateProductUpdateAssigned':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateProductUpdateAssigned
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateProductUpdateAssigned':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateProductUpdateAssigned
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateProductUpdateAssigned':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateProductUpdateAssigned
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_product_id(self, product_id: int) -> 'AttributeTemplateProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeTemplateProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeTemplateProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeTemplateProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeTemplateProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeTemplateProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_assigned(self, assigned: bool) -> 'AttributeTemplateProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AttributeTemplateProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateProductUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		data['Assigned'] = self.assigned
		return data


"""
Handles API Request Branch_SetPrimary. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branch_setprimary
"""


class BranchSetPrimary(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchSetPrimary Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.edit_branch = None
		self.branch_name = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())
			elif branch.get_name():
				self.set_edit_branch(branch.get_name())
			elif branch.get_name():
				self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Branch_SetPrimary'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def set_branch_id(self, branch_id: int) -> 'BranchSetPrimary':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchSetPrimary
		"""

		self.branch_id = branch_id
		return self

	def set_edit_branch(self, edit_branch: str) -> 'BranchSetPrimary':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: BranchSetPrimary
		"""

		self.edit_branch = edit_branch
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchSetPrimary':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchSetPrimary
		"""

		self.branch_name = branch_name
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchSetPrimary':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchSetPrimary':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchSetPrimary(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name

		return data


"""
Handles API Request Branch_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branch_update
"""


class BranchUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchUpdate Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.edit_branch = None
		self.branch_name = None
		self.branch_color = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())
			elif branch.get_name():
				self.set_edit_branch(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Branch_Update'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_branch_color(self) -> str:
		"""
		Get Branch_Color.

		:returns: str
		"""

		return self.branch_color

	def set_branch_id(self, branch_id: int) -> 'BranchUpdate':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchUpdate
		"""

		self.branch_id = branch_id
		return self

	def set_edit_branch(self, edit_branch: str) -> 'BranchUpdate':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: BranchUpdate
		"""

		self.edit_branch = edit_branch
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchUpdate':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchUpdate
		"""

		self.branch_name = branch_name
		return self

	def set_branch_color(self, branch_color: str) -> 'BranchUpdate':
		"""
		Set Branch_Color.

		:param branch_color: str
		:returns: BranchUpdate
		"""

		self.branch_color = branch_color
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.branch_color is not None:
			data['Branch_Color'] = self.branch_color
		return data


"""
Handles API Request Attribute_CopyTemplate. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_copytemplate
"""


class AttributeCopyTemplate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeCopyTemplate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.attribute_template_id = None
		self.edit_attribute_template = None
		self.attribute_template_code = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_CopyTemplate'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def set_product_id(self, product_id: int) -> 'AttributeCopyTemplate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeCopyTemplate
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeCopyTemplate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeCopyTemplate
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'AttributeCopyTemplate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeCopyTemplate
		"""

		self.product_code = product_code
		return self

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeCopyTemplate':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeCopyTemplate
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeCopyTemplate':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeCopyTemplate
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeCopyTemplate':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeCopyTemplate
		"""

		self.attribute_template_code = attribute_template_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeCopyTemplate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeCopyTemplate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeCopyTemplate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code

		return data


"""
Handles API Request Attribute_CopyLinkedTemplate. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_copylinkedtemplate
"""


class AttributeCopyLinkedTemplate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeCopyLinkedTemplate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_CopyLinkedTemplate'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def set_product_id(self, product_id: int) -> 'AttributeCopyLinkedTemplate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeCopyLinkedTemplate
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeCopyLinkedTemplate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeCopyLinkedTemplate
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'AttributeCopyLinkedTemplate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeCopyLinkedTemplate
		"""

		self.product_code = product_code
		return self

	def set_attribute_id(self, attribute_id: int) -> 'AttributeCopyLinkedTemplate':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: AttributeCopyLinkedTemplate
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'AttributeCopyLinkedTemplate':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: AttributeCopyLinkedTemplate
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'AttributeCopyLinkedTemplate':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: AttributeCopyLinkedTemplate
		"""

		self.attribute_code = attribute_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeCopyLinkedTemplate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeCopyLinkedTemplate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeCopyLinkedTemplate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		return data


"""
Handles API Request ProductAttributeAndOptionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productattributeandoptionlist_load_query
"""


class ProductAttributeAndOptionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'code',
		'prompt',
		'price',
		'cost',
		'weight',
		'image',
		'type',
		'template',
		'required',
		'inventory',
		'attr_code',
		'attr_prompt',
		'attr_price',
		'attr_cost',
		'attr_weight',
		'attr_image',
		'opt_code',
		'opt_prompt',
		'opt_price',
		'opt_cost',
		'opt_weight',
		'opt_image'
	]

	available_sort_fields = [
		'code',
		'prompt',
		'price',
		'cost',
		'weight',
		'image',
		'type',
		'required',
		'inventory',
		'attr_code',
		'attr_prompt',
		'attr_price',
		'attr_cost',
		'attr_weight',
		'attr_image',
		'opt_code',
		'opt_prompt',
		'opt_price',
		'opt_cost',
		'opt_weight',
		'opt_image',
		'disporder'
	]

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductAttributeAndOptionListLoadQuery Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductAttributeAndOptionList_Load_Query'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def set_product_id(self, product_id: int) -> 'ProductAttributeAndOptionListLoadQuery':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductAttributeAndOptionListLoadQuery
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductAttributeAndOptionListLoadQuery':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductAttributeAndOptionListLoadQuery
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'ProductAttributeAndOptionListLoadQuery':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductAttributeAndOptionListLoadQuery
		"""

		self.product_code = product_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductAttributeAndOptionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductAttributeAndOptionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductAttributeAndOptionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		return data


"""
Handles API Request CategoryProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryproductlist_load_query
"""


class CategoryProductListLoadQuery(ProductListLoadQuery):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryProductListLoadQuery Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.category_code = None
		self.edit_category = None
		self.assigned = False
		self.unassigned = False
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_category(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryProductList_Load_Query'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_category_id(self, category_id: int) -> 'CategoryProductListLoadQuery':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryProductListLoadQuery
		"""

		self.category_id = category_id
		return self

	def set_category_code(self, category_code: str) -> 'CategoryProductListLoadQuery':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryProductListLoadQuery
		"""

		self.category_code = category_code
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryProductListLoadQuery':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryProductListLoadQuery
		"""

		self.edit_category = edit_category
		return self

	def set_assigned(self, assigned: bool) -> 'CategoryProductListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CategoryProductListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'CategoryProductListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: CategoryProductListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryProductListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request CouponPriceGroupList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponpricegrouplist_load_query
"""


class CouponPriceGroupListLoadQuery(PriceGroupListLoadQuery):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponPriceGroupListLoadQuery Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.assigned = False
		self.unassigned = False
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())
			elif coupon.get_code():
				self.set_edit_coupon(coupon.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponPriceGroupList_Load_Query'

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_coupon_id(self, coupon_id: int) -> 'CouponPriceGroupListLoadQuery':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponPriceGroupListLoadQuery
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponPriceGroupListLoadQuery':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponPriceGroupListLoadQuery
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponPriceGroupListLoadQuery':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponPriceGroupListLoadQuery
		"""

		self.coupon_code = coupon_code
		return self

	def set_assigned(self, assigned: bool) -> 'CouponPriceGroupListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CouponPriceGroupListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'CouponPriceGroupListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: CouponPriceGroupListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponPriceGroupListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponPriceGroupListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponPriceGroupListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon
		elif self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupCustomerList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupcustomerlist_load_query
"""


class PriceGroupCustomerListLoadQuery(CustomerListLoadQuery):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupCustomerListLoadQuery Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.price_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())
			elif price_group.get_name():
				self.set_price_group_name(price_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupCustomerList_Load_Query'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupCustomerListLoadQuery':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupCustomerListLoadQuery
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupCustomerListLoadQuery':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupCustomerListLoadQuery
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupCustomerListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupCustomerListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupCustomerListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupCustomerListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupCustomerListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupCustomerListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupCustomerListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupproductlist_load_query
"""


class PriceGroupProductListLoadQuery(ProductListLoadQuery):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupProductListLoadQuery Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.price_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())
			elif price_group.get_name():
				self.set_price_group_name(price_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupProductList_Load_Query'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupProductListLoadQuery':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupProductListLoadQuery
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupProductListLoadQuery':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupProductListLoadQuery
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupProductListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupProductListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupProductListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupProductListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupProductListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request CustomerPriceGroupList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customerpricegrouplist_load_query
"""


class CustomerPriceGroupListLoadQuery(PriceGroupListLoadQuery):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerPriceGroupListLoadQuery Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.assigned = False
		self.unassigned = False
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerPriceGroupList_Load_Query'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_customer_id(self, customer_id: int) -> 'CustomerPriceGroupListLoadQuery':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerPriceGroupListLoadQuery
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerPriceGroupListLoadQuery':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerPriceGroupListLoadQuery
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerPriceGroupListLoadQuery':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerPriceGroupListLoadQuery
		"""

		self.customer_login = customer_login
		return self

	def set_assigned(self, assigned: bool) -> 'CustomerPriceGroupListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CustomerPriceGroupListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'CustomerPriceGroupListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: CustomerPriceGroupListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerPriceGroupListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerPriceGroupListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerPriceGroupListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request OrderPriceGroupList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderpricegrouplist_load_query
"""


class OrderPriceGroupListLoadQuery(PriceGroupListLoadQuery):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderPriceGroupListLoadQuery Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.assigned = False
		self.unassigned = False
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderPriceGroupList_Load_Query'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_order_id(self, order_id: int) -> 'OrderPriceGroupListLoadQuery':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderPriceGroupListLoadQuery
		"""

		self.order_id = order_id
		return self

	def set_assigned(self, assigned: bool) -> 'OrderPriceGroupListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: OrderPriceGroupListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'OrderPriceGroupListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: OrderPriceGroupListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderPriceGroupListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderPriceGroupListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderPriceGroupListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request OrderCouponList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordercouponlist_load_query
"""


class OrderCouponListLoadQuery(CouponListLoadQuery):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderCouponListLoadQuery Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.assigned = False
		self.unassigned = False
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderCouponList_Load_Query'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_order_id(self, order_id: int) -> 'OrderCouponListLoadQuery':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderCouponListLoadQuery
		"""

		self.order_id = order_id
		return self

	def set_assigned(self, assigned: bool) -> 'OrderCouponListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: OrderCouponListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'OrderCouponListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: OrderCouponListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCouponListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCouponListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCouponListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.get_order_id()

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request ChildCategoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/childcategorylist_load_query
"""


class ChildCategoryListLoadQuery(CategoryListLoadQuery):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		ChildCategoryListLoadQuery Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.parent_category_id = None
		self.parent_category_code = None
		self.edit_parent_category = None
		self.assigned = False
		self.unassigned = False
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_parent_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_parent_category(category.get_code())
			elif category.get_code():
				self.set_parent_category_code(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChildCategoryList_Load_Query'

	def get_parent_category_id(self) -> int:
		"""
		Get ParentCategory_ID.

		:returns: int
		"""

		return self.parent_category_id

	def get_parent_category_code(self) -> str:
		"""
		Get ParentCategory_Code.

		:returns: str
		"""

		return self.parent_category_code

	def get_edit_parent_category(self) -> str:
		"""
		Get Edit_ParentCategory.

		:returns: str
		"""

		return self.edit_parent_category

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_parent_category_id(self, parent_category_id: int) -> 'ChildCategoryListLoadQuery':
		"""
		Set ParentCategory_ID.

		:param parent_category_id: int
		:returns: ChildCategoryListLoadQuery
		"""

		self.parent_category_id = parent_category_id
		return self

	def set_parent_category_code(self, parent_category_code: str) -> 'ChildCategoryListLoadQuery':
		"""
		Set ParentCategory_Code.

		:param parent_category_code: str
		:returns: ChildCategoryListLoadQuery
		"""

		self.parent_category_code = parent_category_code
		return self

	def set_edit_parent_category(self, edit_parent_category: str) -> 'ChildCategoryListLoadQuery':
		"""
		Set Edit_ParentCategory.

		:param edit_parent_category: str
		:returns: ChildCategoryListLoadQuery
		"""

		self.edit_parent_category = edit_parent_category
		return self

	def set_assigned(self, assigned: bool) -> 'ChildCategoryListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: ChildCategoryListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'ChildCategoryListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: ChildCategoryListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChildCategoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChildCategoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChildCategoryListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.parent_category_id is not None:
			data['ParentCategory_ID'] = self.parent_category_id
		elif self.parent_category_code is not None:
			data['ParentCategory_Code'] = self.parent_category_code
		elif self.edit_parent_category is not None:
			data['Edit_ParentCategory'] = self.edit_parent_category

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request AvailabilityGroupCustomerList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupcustomerlist_load_query
"""


class AvailabilityGroupCustomerListLoadQuery(CustomerListLoadQuery):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupCustomerListLoadQuery Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupCustomerList_Load_Query'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupCustomerListLoadQuery':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupCustomerListLoadQuery
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupCustomerListLoadQuery':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupCustomerListLoadQuery
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupCustomerListLoadQuery':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupCustomerListLoadQuery
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupCustomerListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupCustomerListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'AvailabilityGroupCustomerListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: AvailabilityGroupCustomerListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupCustomerListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupCustomerListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupCustomerListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request AvailabilityGroupProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupproductlist_load_query
"""


class AvailabilityGroupProductListLoadQuery(ProductListLoadQuery):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupProductListLoadQuery Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupProductList_Load_Query'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupProductListLoadQuery':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupProductListLoadQuery
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupProductListLoadQuery':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupProductListLoadQuery
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupProductListLoadQuery':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupProductListLoadQuery
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupProductListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupProductListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'AvailabilityGroupProductListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: AvailabilityGroupProductListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupProductListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request AvailabilityGroupCategoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupcategorylist_load_query
"""


class AvailabilityGroupCategoryListLoadQuery(CategoryListLoadQuery):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupCategoryListLoadQuery Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupCategoryList_Load_Query'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupCategoryListLoadQuery':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupCategoryListLoadQuery
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupCategoryListLoadQuery':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupCategoryListLoadQuery
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupCategoryListLoadQuery':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupCategoryListLoadQuery
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupCategoryListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupCategoryListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'AvailabilityGroupCategoryListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: AvailabilityGroupCategoryListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupCategoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupCategoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupCategoryListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request AvailabilityGroupBusinessAccountList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupbusinessaccountlist_load_query
"""


class AvailabilityGroupBusinessAccountListLoadQuery(BusinessAccountListLoadQuery):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupBusinessAccountListLoadQuery Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupBusinessAccountList_Load_Query'

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupBusinessAccountListLoadQuery':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupBusinessAccountListLoadQuery
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupBusinessAccountListLoadQuery':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupBusinessAccountListLoadQuery
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupBusinessAccountListLoadQuery':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupBusinessAccountListLoadQuery
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupBusinessAccountListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupBusinessAccountListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'AvailabilityGroupBusinessAccountListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: AvailabilityGroupBusinessAccountListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupBusinessAccountListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupBusinessAccountListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupBusinessAccountListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupBusinessAccountList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupbusinessaccountlist_load_query
"""


class PriceGroupBusinessAccountListLoadQuery(BusinessAccountListLoadQuery):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupBusinessAccountListLoadQuery Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupBusinessAccountList_Load_Query'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupBusinessAccountListLoadQuery':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupBusinessAccountListLoadQuery
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupBusinessAccountListLoadQuery':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupBusinessAccountListLoadQuery
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupBusinessAccountListLoadQuery':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupBusinessAccountListLoadQuery
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupBusinessAccountListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupBusinessAccountListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupBusinessAccountListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupBusinessAccountListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupBusinessAccountListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupBusinessAccountListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupBusinessAccountListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupCategoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupcategorylist_load_query
"""


class PriceGroupCategoryListLoadQuery(CategoryListLoadQuery):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupCategoryListLoadQuery Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupCategoryList_Load_Query'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupCategoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupCategoryListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupExcludedCategoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupexcludedcategorylist_load_query
"""


class PriceGroupExcludedCategoryListLoadQuery(CategoryListLoadQuery):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupExcludedCategoryListLoadQuery Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupExcludedCategoryList_Load_Query'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupExcludedCategoryListLoadQuery':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupExcludedCategoryListLoadQuery
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupExcludedCategoryListLoadQuery':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupExcludedCategoryListLoadQuery
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupExcludedCategoryListLoadQuery':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupExcludedCategoryListLoadQuery
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupExcludedCategoryListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupExcludedCategoryListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupExcludedCategoryListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupExcludedCategoryListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupExcludedCategoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupExcludedCategoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupExcludedCategoryListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupExcludedProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupexcludedproductlist_load_query
"""


class PriceGroupExcludedProductListLoadQuery(ProductListLoadQuery):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupExcludedProductListLoadQuery Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupExcludedProductList_Load_Query'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupExcludedProductListLoadQuery':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupExcludedProductListLoadQuery
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupExcludedProductListLoadQuery':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupExcludedProductListLoadQuery
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupExcludedProductListLoadQuery':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupExcludedProductListLoadQuery
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupExcludedProductListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupExcludedProductListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupExcludedProductListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupExcludedProductListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupExcludedProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupExcludedProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupExcludedProductListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request PriceGroupQualifyingProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupqualifyingproductlist_load_query
"""


class PriceGroupQualifyingProductListLoadQuery(ProductListLoadQuery):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupQualifyingProductListLoadQuery Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = False
		self.unassigned = False
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupQualifyingProductList_Load_Query'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupQualifyingProductListLoadQuery':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupQualifyingProductListLoadQuery
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupQualifyingProductListLoadQuery':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupQualifyingProductListLoadQuery
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupQualifyingProductListLoadQuery':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupQualifyingProductListLoadQuery
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupQualifyingProductListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupQualifyingProductListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupQualifyingProductListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupQualifyingProductListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupQualifyingProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupQualifyingProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupQualifyingProductListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request CouponCustomerList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponcustomerlist_load_query
"""


class CouponCustomerListLoadQuery(CustomerListLoadQuery):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponCustomerListLoadQuery Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.assigned = False
		self.unassigned = False
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponCustomerList_Load_Query'

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_coupon_id(self, coupon_id: int) -> 'CouponCustomerListLoadQuery':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponCustomerListLoadQuery
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponCustomerListLoadQuery':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponCustomerListLoadQuery
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponCustomerListLoadQuery':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponCustomerListLoadQuery
		"""

		self.coupon_code = coupon_code
		return self

	def set_assigned(self, assigned: bool) -> 'CouponCustomerListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CouponCustomerListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'CouponCustomerListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: CouponCustomerListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponCustomerListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponCustomerListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponCustomerListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon
		elif self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request BusinessAccountCustomerList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccountcustomerlist_load_query
"""


class BusinessAccountCustomerListLoadQuery(CustomerListLoadQuery):
	def __init__(self, client: Client = None):
		"""
		BusinessAccountCustomerListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.assigned = False
		self.unassigned = False

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccountCustomerList_Load_Query'

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_edit_business_account(self) -> int:
		"""
		Get Edit_BusinessAccount.

		:returns: int
		"""

		return self.edit_business_account

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_business_account_id(self, business_account_id: int) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: int) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: int
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.business_account_title = business_account_title
		return self

	def set_assigned(self, assigned: bool) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountCustomerListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountCustomerListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.edit_business_account is not None:
			data['Edit_BusinessAccount'] = self.edit_business_account
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request RelatedProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/relatedproductlist_load_query
"""


class RelatedProductListLoadQuery(ProductListLoadQuery):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		RelatedProductListLoadQuery Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.assigned = False
		self.unassigned = False
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'RelatedProductList_Load_Query'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_product_id(self, product_id: int) -> 'RelatedProductListLoadQuery':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: RelatedProductListLoadQuery
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'RelatedProductListLoadQuery':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: RelatedProductListLoadQuery
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'RelatedProductListLoadQuery':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: RelatedProductListLoadQuery
		"""

		self.edit_product = edit_product
		return self

	def set_assigned(self, assigned: bool) -> 'RelatedProductListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: RelatedProductListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'RelatedProductListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: RelatedProductListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.RelatedProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'RelatedProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.RelatedProductListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
Handles API Request AttributeTemplateProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateproductlist_load_query
"""


class AttributeTemplateProductListLoadQuery(ProductListLoadQuery):
	def __init__(self, client: Client = None, attribute_template: merchantapi.model.AttributeTemplate = None):
		"""
		AttributeTemplateProductListLoadQuery Constructor.

		:param client: Client
		:param attribute_template: AttributeTemplate
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.assigned = False
		self.unassigned = False
		if isinstance(attribute_template, merchantapi.model.AttributeTemplate):
			if attribute_template.get_id():
				self.set_attribute_template_id(attribute_template.get_id())
			elif attribute_template.get_code():
				self.set_attribute_template_code(attribute_template.get_code())
			elif attribute_template.get_code():
				self.set_edit_attribute_template(attribute_template.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateProductList_Load_Query'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateProductListLoadQuery':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateProductListLoadQuery
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateProductListLoadQuery':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateProductListLoadQuery
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateProductListLoadQuery':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateProductListLoadQuery
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_assigned(self, assigned: bool) -> 'AttributeTemplateProductListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AttributeTemplateProductListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'AttributeTemplateProductListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: AttributeTemplateProductListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateProductListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data


"""
RequestBuilder can be used to build out custom request objects to send to the API
"""


class RequestBuilder(merchantapi.abstract.Request):
	def __init__(self, client: Client, function: str, data: dict = None):
		"""
		RequestBuilder Constructor.

		:param client: Client
		:param function: str
		:param data: dict
		"""

		if data is None:
			data = {}
		self.set_scope(merchantapi.abstract.Request.SCOPE_STORE)
		self.set_function(function)

	def set_function(self, function: str) -> 'RequestBuilder':
		"""
		Set the request function

		:param function: str
		"""

		self.function = function
		return self

	def set_scope(self, scope: int) -> 'RequestBuilder':
		"""
		Set the request scope

		:param scope: int
		"""

		self.scope = scope
		return self

	def set(self, field: str, value) -> 'RequestBuilder':
		"""
		Set a field value

		:param field: str
		:param value: mixed
		"""

		self.data[field] = value
		return self

	def get(self, field: str, default_value=None):
		"""
		Get a field value

		:param field: str
		:param default_value: mixed
		:returns: mixed
		"""

		if field in self.data:
			return self.data[field]
		return default_value

	def has(self, field: str) -> bool:
		"""
		Check if a field exists

		:param field: str
		:returns: bool
		"""

		return field in self.data

	def remove(self, field: str) -> 'RequestBuilder':
		"""
		Remove a field if it exists

		:param field: str
		"""

		if field in self.data:
			self.data.pop(field, None)
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.RequestBuilder':
		return super().send()

	def create_response(self, data) -> 'merchantapi.response.RequestBuilder':
		"""
		Create a response object from the response data

		:param data:
		:returns: Response
		"""

		return merchantapi.response.RequestBuilder(self, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		return super().to_dict().update(self.data)