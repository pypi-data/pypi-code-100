"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from merchantapi.abstract import Model

"""
AvailabilityGroup data model.
"""


class AvailabilityGroup(Model):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroup Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_tax_exempt(self) -> bool:
		"""
		Get tax_exempt.

		:returns: bool
		"""

		return self.get_field('tax_exempt', False)


"""
AvailabilityGroupShippingMethod data model.
"""


class AvailabilityGroupShippingMethod(Model):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroupShippingMethod Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_module_code(self) -> str:
		"""
		Get mod_code.

		:returns: string
		"""

		return self.get_field('mod_code')

	def get_method_code(self) -> str:
		"""
		Get meth_code.

		:returns: string
		"""

		return self.get_field('meth_code')

	def get_method_name(self) -> str:
		"""
		Get method_name.

		:returns: string
		"""

		return self.get_field('method_name')

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
BusinessAccount data model.
"""


class BusinessAccount(Model):
	def __init__(self, data: dict = None):
		"""
		BusinessAccount Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_title(self) -> str:
		"""
		Get title.

		:returns: string
		"""

		return self.get_field('title')

	def get_tax_exempt(self) -> bool:
		"""
		Get tax_exempt.

		:returns: bool
		"""

		return self.get_field('tax_exempt', False)

	def get_order_count(self) -> int:
		"""
		Get order_cnt.

		:returns: int
		"""

		return self.get_field('order_cnt', 0)

	def get_order_average(self) -> float:
		"""
		Get order_avg.

		:returns: float
		"""

		return self.get_field('order_avg', 0.00)

	def get_formatted_order_average(self) -> str:
		"""
		Get formatted_order_avg.

		:returns: string
		"""

		return self.get_field('formatted_order_avg')

	def get_order_total(self) -> float:
		"""
		Get order_tot.

		:returns: float
		"""

		return self.get_field('order_tot', 0.00)

	def get_formatted_order_total(self) -> str:
		"""
		Get formatted_order_tot.

		:returns: string
		"""

		return self.get_field('formatted_order_tot')

	def get_note_count(self) -> int:
		"""
		Get note_count.

		:returns: int
		"""

		return self.get_field('note_count', 0)


"""
Customer data model.
"""


class Customer(Model):
	def __init__(self, data: dict = None):
		"""
		Customer Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_account_id(self) -> int:
		"""
		Get account_id.

		:returns: int
		"""

		return self.get_field('account_id', 0)

	def get_login(self) -> str:
		"""
		Get login.

		:returns: string
		"""

		return self.get_field('login')

	def get_password_email(self) -> str:
		"""
		Get pw_email.

		:returns: string
		"""

		return self.get_field('pw_email')

	def get_ship_id(self) -> int:
		"""
		Get ship_id.

		:returns: int
		"""

		return self.get_field('ship_id', 0)

	def get_shipping_residential(self) -> bool:
		"""
		Get ship_res.

		:returns: bool
		"""

		return self.get_field('ship_res', False)

	def get_ship_first_name(self) -> str:
		"""
		Get ship_fname.

		:returns: string
		"""

		return self.get_field('ship_fname')

	def get_ship_last_name(self) -> str:
		"""
		Get ship_lname.

		:returns: string
		"""

		return self.get_field('ship_lname')

	def get_ship_email(self) -> str:
		"""
		Get ship_email.

		:returns: string
		"""

		return self.get_field('ship_email')

	def get_ship_company(self) -> str:
		"""
		Get ship_comp.

		:returns: string
		"""

		return self.get_field('ship_comp')

	def get_ship_phone(self) -> str:
		"""
		Get ship_phone.

		:returns: string
		"""

		return self.get_field('ship_phone')

	def get_ship_fax(self) -> str:
		"""
		Get ship_fax.

		:returns: string
		"""

		return self.get_field('ship_fax')

	def get_ship_address1(self) -> str:
		"""
		Get ship_addr1.

		:returns: string
		"""

		return self.get_field('ship_addr1')

	def get_ship_address2(self) -> str:
		"""
		Get ship_addr2.

		:returns: string
		"""

		return self.get_field('ship_addr2')

	def get_ship_city(self) -> str:
		"""
		Get ship_city.

		:returns: string
		"""

		return self.get_field('ship_city')

	def get_ship_state(self) -> str:
		"""
		Get ship_state.

		:returns: string
		"""

		return self.get_field('ship_state')

	def get_ship_zip(self) -> str:
		"""
		Get ship_zip.

		:returns: string
		"""

		return self.get_field('ship_zip')

	def get_ship_country(self) -> str:
		"""
		Get ship_cntry.

		:returns: string
		"""

		return self.get_field('ship_cntry')

	def get_bill_id(self) -> int:
		"""
		Get bill_id.

		:returns: int
		"""

		return self.get_field('bill_id', 0)

	def get_bill_first_name(self) -> str:
		"""
		Get bill_fname.

		:returns: string
		"""

		return self.get_field('bill_fname')

	def get_bill_last_name(self) -> str:
		"""
		Get bill_lname.

		:returns: string
		"""

		return self.get_field('bill_lname')

	def get_bill_email(self) -> str:
		"""
		Get bill_email.

		:returns: string
		"""

		return self.get_field('bill_email')

	def get_bill_company(self) -> str:
		"""
		Get bill_comp.

		:returns: string
		"""

		return self.get_field('bill_comp')

	def get_bill_phone(self) -> str:
		"""
		Get bill_phone.

		:returns: string
		"""

		return self.get_field('bill_phone')

	def get_bill_fax(self) -> str:
		"""
		Get bill_fax.

		:returns: string
		"""

		return self.get_field('bill_fax')

	def get_bill_address1(self) -> str:
		"""
		Get bill_addr1.

		:returns: string
		"""

		return self.get_field('bill_addr1')

	def get_bill_address2(self) -> str:
		"""
		Get bill_addr2.

		:returns: string
		"""

		return self.get_field('bill_addr2')

	def get_bill_city(self) -> str:
		"""
		Get bill_city.

		:returns: string
		"""

		return self.get_field('bill_city')

	def get_bill_state(self) -> str:
		"""
		Get bill_state.

		:returns: string
		"""

		return self.get_field('bill_state')

	def get_bill_zip(self) -> str:
		"""
		Get bill_zip.

		:returns: string
		"""

		return self.get_field('bill_zip')

	def get_bill_country(self) -> str:
		"""
		Get bill_cntry.

		:returns: string
		"""

		return self.get_field('bill_cntry')

	def get_tax_exempt(self) -> bool:
		"""
		Get tax_exempt.

		:returns: bool
		"""

		return self.get_field('tax_exempt', False)

	def get_order_count(self) -> int:
		"""
		Get order_cnt.

		:returns: int
		"""

		return self.get_field('order_cnt', 0)

	def get_order_average(self) -> float:
		"""
		Get order_avg.

		:returns: float
		"""

		return self.get_field('order_avg', 0.00)

	def get_formatted_order_average(self) -> str:
		"""
		Get formatted_order_avg.

		:returns: string
		"""

		return self.get_field('formatted_order_avg')

	def get_order_total(self) -> float:
		"""
		Get order_tot.

		:returns: float
		"""

		return self.get_field('order_tot', 0.00)

	def get_formatted_order_total(self) -> str:
		"""
		Get formatted_order_tot.

		:returns: string
		"""

		return self.get_field('formatted_order_tot')

	def get_note_count(self) -> int:
		"""
		Get note_count.

		:returns: int
		"""

		return self.get_field('note_count', 0)

	def get_created_on(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_field('dt_created', 0)

	def get_last_login(self) -> int:
		"""
		Get dt_login.

		:returns: int
		"""

		return self.get_field('dt_login', 0)

	def get_password_change_date_time(self) -> int:
		"""
		Get dt_pwchg.

		:returns: int
		"""

		return self.get_field('dt_pwchg', 0)

	def get_credit(self) -> float:
		"""
		Get credit.

		:returns: float
		"""

		return self.get_field('credit', 0.00)

	def get_formatted_credit(self) -> str:
		"""
		Get formatted_credit.

		:returns: string
		"""

		return self.get_field('formatted_credit')

	def get_business_title(self) -> str:
		"""
		Get business_title.

		:returns: string
		"""

		return self.get_field('business_title')

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		return ret


"""
Coupon data model.
"""


class Coupon(Model):
	# CUSTOMER_SCOPE constants.
	CUSTOMER_SCOPE_ALL_SHOPPERS = 'A'
	CUSTOMER_SCOPE_SPECIFIC_CUSTOMERS = 'X'
	CUSTOMER_SCOPE_ALL_LOGGED_IN = 'L'

	def __init__(self, data: dict = None):
		"""
		Coupon Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_customer_scope(self) -> str:
		"""
		Get custscope.

		:returns: string
		"""

		return self.get_field('custscope')

	def get_date_time_start(self) -> int:
		"""
		Get dt_start.

		:returns: int
		"""

		return self.get_field('dt_start', 0)

	def get_date_time_end(self) -> int:
		"""
		Get dt_end.

		:returns: int
		"""

		return self.get_field('dt_end', 0)

	def get_max_use(self) -> int:
		"""
		Get max_use.

		:returns: int
		"""

		return self.get_field('max_use', 0)

	def get_max_per(self) -> int:
		"""
		Get max_per.

		:returns: int
		"""

		return self.get_field('max_per', 0)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_use_count(self) -> int:
		"""
		Get use_count.

		:returns: int
		"""

		return self.get_field('use_count', 0)


"""
CustomFieldValues data model.
"""


class CustomFieldValues(Model):
	def __init__(self, data: dict = None):
		"""
		CustomFieldValues Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_value(self, code: str, module : str = 'customfields'):
		"""
		Get a value for a module by its code.

		:param code: str
		:param module: str
		:returns: mixed
		"""

		return self[module][code] if self.has_value(code, module) else None

	def has_value(self, code: str, module: str = 'customfields'):
		"""
		Check if a value for code and module exists.

		:param code: {string}
		:param module: {string}
		:returns: bool
		"""

		if self.has_field(module):
			return code in self.get_field(module)

	def has_module(self, module: str):
		"""
		Check if a specific module is defined.

		:param module: str
		:returns: boolean
		"""

		return self.has_field(module)

	def get_module(self, module: str):
		"""
		Get a specific modules custom field values.

		:param module: str
		:returns: dict
		"""

		return self.get_field(module, {})

	def add_value(self, field: str, value, module: str = 'customfields') -> 'CustomFieldValues':
		"""
		Add a custom field value.

		:param field: str
		:param value: mixed
		:param module: std
		:returns: CustomFieldValues
		"""

		if not self.has_module(module):
			self.set_field(module, {})
		self[module][field] = value
		return self


"""
Module data model.
"""


class Module(Model):
	def __init__(self, data: dict = None):
		"""
		Module Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_provider(self) -> str:
		"""
		Get provider.

		:returns: string
		"""

		return self.get_field('provider')

	def get_api_version(self) -> str:
		"""
		Get api_ver.

		:returns: string
		"""

		return self.get_field('api_ver')

	def get_version(self) -> str:
		"""
		Get version.

		:returns: string
		"""

		return self.get_field('version')

	def get_module(self) -> str:
		"""
		Get module.

		:returns: string
		"""

		return self.get_field('module')

	def get_reference_count(self) -> int:
		"""
		Get refcount.

		:returns: int
		"""

		return self.get_field('refcount', 0)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)


"""
Note data model.
"""


class Note(Model):
	def __init__(self, data: dict = None):
		"""
		Note Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_account_id(self) -> int:
		"""
		Get account_id.

		:returns: int
		"""

		return self.get_field('account_id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_note_text(self) -> str:
		"""
		Get notetext.

		:returns: string
		"""

		return self.get_field('notetext')

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_field('dtstamp', 0)

	def get_customer_login(self) -> str:
		"""
		Get cust_login.

		:returns: string
		"""

		return self.get_field('cust_login')

	def get_business_title(self) -> str:
		"""
		Get business_title.

		:returns: string
		"""

		return self.get_field('business_title')

	def get_admin_user(self) -> str:
		"""
		Get admin_user.

		:returns: string
		"""

		return self.get_field('admin_user')


"""
PriceGroup data model.
"""


class PriceGroup(Model):
	# ELIGIBILITY constants.
	ELIGIBILITY_COUPON = 'C'
	ELIGIBILITY_ALL = 'A'
	ELIGIBILITY_CUSTOMER = 'X'
	ELIGIBILITY_LOGGED_IN = 'L'

	# DISCOUNT_TYPE constants.
	DISCOUNT_TYPE_RETAIL = 'R'
	DISCOUNT_TYPE_COST = 'C'
	DISCOUNT_TYPE_DISCOUNT_RETAIL = 'D'
	DISCOUNT_TYPE_MARKUP_COST = 'M'

	def __init__(self, data: dict = None):
		"""
		PriceGroup Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('module'):
			value = self.get_field('module')
			if isinstance(value, dict):
				if not isinstance(value, Module):
					self.set_field('module', Module(value))
			else:
				raise Exception('Expected Module or a dict')

		if self.has_field('capabilities'):
			value = self.get_field('capabilities')
			if isinstance(value, dict):
				if not isinstance(value, DiscountModuleCapabilities):
					self.set_field('capabilities', DiscountModuleCapabilities(value))
			else:
				raise Exception('Expected DiscountModuleCapabilities or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_customer_scope(self) -> str:
		"""
		Get custscope.

		:returns: string
		"""

		return self.get_field('custscope')

	def get_rate(self) -> str:
		"""
		Get rate.

		:returns: string
		"""

		return self.get_field('rate')

	def get_discount(self) -> float:
		"""
		Get discount.

		:returns: float
		"""

		return self.get_field('discount', 0.00)

	def get_markup(self) -> float:
		"""
		Get markup.

		:returns: float
		"""

		return self.get_field('markup', 0.00)

	def get_date_time_start(self) -> int:
		"""
		Get dt_start.

		:returns: int
		"""

		return self.get_field('dt_start', 0)

	def get_date_time_end(self) -> int:
		"""
		Get dt_end.

		:returns: int
		"""

		return self.get_field('dt_end', 0)

	def get_minimum_subtotal(self) -> float:
		"""
		Get qmn_subtot.

		:returns: float
		"""

		return self.get_field('qmn_subtot', 0.00)

	def get_maximum_subtotal(self) -> float:
		"""
		Get qmx_subtot.

		:returns: float
		"""

		return self.get_field('qmx_subtot', 0.00)

	def get_minimum_quantity(self) -> int:
		"""
		Get qmn_quan.

		:returns: int
		"""

		return self.get_field('qmn_quan', 0)

	def get_maximum_quantity(self) -> int:
		"""
		Get qmx_quan.

		:returns: int
		"""

		return self.get_field('qmx_quan', 0)

	def get_minimum_weight(self) -> float:
		"""
		Get qmn_weight.

		:returns: float
		"""

		return self.get_field('qmn_weight', 0.00)

	def get_maximum_weight(self) -> float:
		"""
		Get qmx_weight.

		:returns: float
		"""

		return self.get_field('qmx_weight', 0.00)

	def get_basket_minimum_subtotal(self) -> float:
		"""
		Get bmn_subtot.

		:returns: float
		"""

		return self.get_field('bmn_subtot', 0.00)

	def get_basket_maximum_subtotal(self) -> float:
		"""
		Get bmx_subtot.

		:returns: float
		"""

		return self.get_field('bmx_subtot', 0.00)

	def get_basket_minimum_quantity(self) -> int:
		"""
		Get bmn_quan.

		:returns: int
		"""

		return self.get_field('bmn_quan', 0)

	def get_basket_maximum_quantity(self) -> int:
		"""
		Get bmx_quan.

		:returns: int
		"""

		return self.get_field('bmx_quan', 0)

	def get_basket_minimum_weight(self) -> float:
		"""
		Get bmn_weight.

		:returns: float
		"""

		return self.get_field('bmn_weight', 0.00)

	def get_basket_maximum_weight(self) -> float:
		"""
		Get bmx_weight.

		:returns: float
		"""

		return self.get_field('bmx_weight', 0.00)

	def get_priority(self) -> int:
		"""
		Get priority.

		:returns: int
		"""

		return self.get_field('priority', 0)

	def get_module(self):
		"""
		Get module.

		:returns: Module|None
		"""

		return self.get_field('module', None)

	def get_capabilities(self):
		"""
		Get capabilities.

		:returns: DiscountModuleCapabilities|None
		"""

		return self.get_field('capabilities', None)

	def get_exclusion(self) -> bool:
		"""
		Get exclusion.

		:returns: bool
		"""

		return self.get_field('exclusion', False)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_display(self) -> bool:
		"""
		Get display.

		:returns: bool
		"""

		return self.get_field('display', False)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'module' in ret and isinstance(ret['module'], Module):
			ret['module'] = ret['module'].to_dict()

		if 'capabilities' in ret and isinstance(ret['capabilities'], DiscountModuleCapabilities):
			ret['capabilities'] = ret['capabilities'].to_dict()

		return ret


"""
DiscountModuleCapabilities data model.
"""


class DiscountModuleCapabilities(Model):
	def __init__(self, data: dict = None):
		"""
		DiscountModuleCapabilities Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_preitems(self) -> bool:
		"""
		Get preitems.

		:returns: bool
		"""

		return self.get_field('preitems', False)

	def get_items(self) -> bool:
		"""
		Get items.

		:returns: bool
		"""

		return self.get_field('items', False)

	def get_eligibility(self) -> str:
		"""
		Get eligibility.

		:returns: string
		"""

		return self.get_field('eligibility')

	def get_basket(self) -> bool:
		"""
		Get basket.

		:returns: bool
		"""

		return self.get_field('basket', False)

	def get_shipping(self) -> bool:
		"""
		Get shipping.

		:returns: bool
		"""

		return self.get_field('shipping', False)

	def get_qualifying(self) -> bool:
		"""
		Get qualifying.

		:returns: bool
		"""

		return self.get_field('qualifying', False)


"""
Product data model.
"""


class Product(Model):
	def __init__(self, data: dict = None):
		"""
		Product Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('productinventorysettings'):
			value = self.get_field('productinventorysettings')
			if isinstance(value, dict):
				if not isinstance(value, ProductInventorySettings):
					self.set_field('productinventorysettings', ProductInventorySettings(value))
			else:
				raise Exception('Expected ProductInventorySettings or a dict')

		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

		if self.has_field('uris'):
			value = self.get_field('uris')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Uri):
							value[i] = Uri(e)
					else:
						raise Exception('Expected list of Uri or dict')
			else:
				raise Exception('Expected list of Uri or dict')

		if self.has_field('relatedproducts'):
			value = self.get_field('relatedproducts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, RelatedProduct):
							value[i] = RelatedProduct(e)
					else:
						raise Exception('Expected list of RelatedProduct or dict')
			else:
				raise Exception('Expected list of RelatedProduct or dict')

		if self.has_field('categories'):
			value = self.get_field('categories')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Category):
							value[i] = Category(e)
					else:
						raise Exception('Expected list of Category or dict')
			else:
				raise Exception('Expected list of Category or dict')

		if self.has_field('productshippingrules'):
			value = self.get_field('productshippingrules')
			if isinstance(value, dict):
				if not isinstance(value, ProductShippingRules):
					self.set_field('productshippingrules', ProductShippingRules(value))
			else:
				raise Exception('Expected ProductShippingRules or a dict')

		if self.has_field('productimagedata'):
			value = self.get_field('productimagedata')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductImageData):
							value[i] = ProductImageData(e)
					else:
						raise Exception('Expected list of ProductImageData or dict')
			else:
				raise Exception('Expected list of ProductImageData or dict')

		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductAttribute):
							value[i] = ProductAttribute(e)
					else:
						raise Exception('Expected list of ProductAttribute or dict')
			else:
				raise Exception('Expected list of ProductAttribute or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_thumbnail(self) -> str:
		"""
		Get thumbnail.

		:returns: string
		"""

		return self.get_field('thumbnail')

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_formatted_price(self) -> str:
		"""
		Get formatted_price.

		:returns: string
		"""

		return self.get_field('formatted_price')

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_category_count(self) -> int:
		"""
		Get catcount.

		:returns: int
		"""

		return self.get_field('catcount', 0)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_page_title(self) -> str:
		"""
		Get page_title.

		:returns: string
		"""

		return self.get_field('page_title')

	def get_taxable(self) -> bool:
		"""
		Get taxable.

		:returns: bool
		"""

		return self.get_field('taxable', False)

	def get_date_time_created(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_field('dt_created', 0)

	def get_date_time_update(self) -> int:
		"""
		Get dt_updated.

		:returns: int
		"""

		return self.get_field('dt_updated', 0)

	def get_product_inventory_settings(self):
		"""
		Get productinventorysettings.

		:returns: ProductInventorySettings|None
		"""

		return self.get_field('productinventorysettings', None)

	def get_product_inventory_active(self) -> bool:
		"""
		Get product_inventory_active.

		:returns: bool
		"""

		return self.get_field('product_inventory_active', False)

	def get_product_inventory(self) -> int:
		"""
		Get product_inventory.

		:returns: int
		"""

		return self.get_field('product_inventory', 0)

	def get_canonical_category_code(self) -> str:
		"""
		Get cancat_code.

		:returns: string
		"""

		return self.get_field('cancat_code')

	def get_page_code(self) -> str:
		"""
		Get page_code.

		:returns: string
		"""

		return self.get_field('page_code')

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def get_uris(self):
		"""
		Get uris.

		:returns: List of Uri
		"""

		return self.get_field('uris', [])

	def get_related_products(self):
		"""
		Get relatedproducts.

		:returns: List of RelatedProduct
		"""

		return self.get_field('relatedproducts', [])

	def get_categories(self):
		"""
		Get categories.

		:returns: List of Category
		"""

		return self.get_field('categories', [])

	def get_product_shipping_rules(self):
		"""
		Get productshippingrules.

		:returns: ProductShippingRules|None
		"""

		return self.get_field('productshippingrules', None)

	def get_product_image_data(self):
		"""
		Get productimagedata.

		:returns: List of ProductImageData
		"""

		return self.get_field('productimagedata', [])

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of ProductAttribute
		"""

		return self.get_field('attributes', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'productinventorysettings' in ret and isinstance(ret['productinventorysettings'], ProductInventorySettings):
			ret['productinventorysettings'] = ret['productinventorysettings'].to_dict()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		if 'uris' in ret and isinstance(ret['uris'], list):
			for i, e in enumerate(ret['uris']):
				if isinstance(e, Uri):
					ret['uris'][i] = ret['uris'][i].to_dict()

		if 'relatedproducts' in ret and isinstance(ret['relatedproducts'], list):
			for i, e in enumerate(ret['relatedproducts']):
				if isinstance(e, RelatedProduct):
					ret['relatedproducts'][i] = ret['relatedproducts'][i].to_dict()

		if 'categories' in ret and isinstance(ret['categories'], list):
			for i, e in enumerate(ret['categories']):
				if isinstance(e, Category):
					ret['categories'][i] = ret['categories'][i].to_dict()

		if 'productshippingrules' in ret and isinstance(ret['productshippingrules'], ProductShippingRules):
			ret['productshippingrules'] = ret['productshippingrules'].to_dict()

		if 'productimagedata' in ret and isinstance(ret['productimagedata'], list):
			for i, e in enumerate(ret['productimagedata']):
				if isinstance(e, ProductImageData):
					ret['productimagedata'][i] = ret['productimagedata'][i].to_dict()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, ProductAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		return ret


"""
RelatedProduct data model.
"""


class RelatedProduct(Model):
	def __init__(self, data: dict = None):
		"""
		RelatedProduct Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_thumbnail(self) -> str:
		"""
		Get thumbnail.

		:returns: string
		"""

		return self.get_field('thumbnail')

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_formatted_price(self) -> str:
		"""
		Get formatted_price.

		:returns: string
		"""

		return self.get_field('formatted_price')

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_page_title(self) -> str:
		"""
		Get page_title.

		:returns: string
		"""

		return self.get_field('page_title')

	def get_taxable(self) -> bool:
		"""
		Get taxable.

		:returns: bool
		"""

		return self.get_field('taxable', False)

	def get_date_time_created(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_field('dt_created', 0)

	def get_date_time_updated(self) -> int:
		"""
		Get dt_updated.

		:returns: int
		"""

		return self.get_field('dt_updated', 0)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
ProductImageData data model.
"""


class ProductImageData(Model):
	def __init__(self, data: dict = None):
		"""
		ProductImageData Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_image_id(self) -> int:
		"""
		Get image_id.

		:returns: int
		"""

		return self.get_field('image_id', 0)

	def get_type_id(self) -> int:
		"""
		Get type_id.

		:returns: int
		"""

		return self.get_field('type_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type_description(self) -> str:
		"""
		Get type_desc.

		:returns: string
		"""

		return self.get_field('type_desc')

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_width(self) -> int:
		"""
		Get width.

		:returns: int
		"""

		return self.get_field('width', 0)

	def get_height(self) -> int:
		"""
		Get height.

		:returns: int
		"""

		return self.get_field('height', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		return self.get_field('disp_order', 0)


"""
ProductAttribute data model.
"""


class ProductAttribute(Model):
	# PRODUCT_ATTRIBUTE_TYPE constants.
	PRODUCT_ATTRIBUTE_TYPE_CHECKBOX = 'checkbox'
	PRODUCT_ATTRIBUTE_TYPE_RADIO = 'radio'
	PRODUCT_ATTRIBUTE_TYPE_TEXT = 'text'
	PRODUCT_ATTRIBUTE_TYPE_SELECT = 'select'
	PRODUCT_ATTRIBUTE_TYPE_MEMO = 'memo'
	PRODUCT_ATTRIBUTE_TYPE_TEMPLATE = 'template'
	PRODUCT_ATTRIBUTE_TYPE_SWATCH_SELECT = 'swatch-select'

	def __init__(self, data: dict = None):
		"""
		ProductAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductAttribute):
							value[i] = ProductAttribute(e)
					else:
						raise Exception('Expected list of ProductAttribute or dict')
			else:
				raise Exception('Expected list of ProductAttribute or dict')

		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductOption):
							value[i] = ProductOption(e)
					else:
						raise Exception('Expected list of ProductOption or dict')
			else:
				raise Exception('Expected list of ProductOption or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_default_id(self) -> int:
		"""
		Get default_id.

		:returns: int
		"""

		return self.get_field('default_id', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		if self.has_field('disp_order'):
			return self.get_field('disp_order', 0)
		elif self.has_field('disporder'):
			return self.get_field('disporder', 0)

		return 0

	def get_attribute_template_id(self) -> int:
		"""
		Get attemp_id.

		:returns: int
		"""

		return self.get_field('attemp_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_required(self) -> bool:
		"""
		Get required.

		:returns: bool
		"""

		return self.get_field('required', False)

	def get_inventory(self) -> bool:
		"""
		Get inventory.

		:returns: bool
		"""

		return self.get_field('inventory', False)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_template_attributes(self):
		"""
		Get attributes.

		:returns: List of ProductAttribute
		"""

		return self.get_field('attributes', [])

	def get_options(self):
		"""
		Get options.

		:returns: List of ProductOption
		"""

		return self.get_field('options', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, ProductAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, ProductOption):
					ret['options'][i] = ret['options'][i].to_dict()

		return ret


"""
ProductOption data model.
"""


class ProductOption(Model):
	def __init__(self, data: dict = None):
		"""
		ProductOption Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_id(self) -> int:
		"""
		Get attemp_id.

		:returns: int
		"""

		return self.get_field('attemp_id', 0)

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		if self.has_field('disp_order'):
			return self.get_field('disp_order', 0)
		elif self.has_field('disporder'):
			return self.get_field('disporder', 0)

		return 0

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_formatted_price(self) -> str:
		"""
		Get formatted_price.

		:returns: string
		"""

		return self.get_field('formatted_price')

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')


"""
ProductShippingMethod data model.
"""


class ProductShippingMethod(Model):
	def __init__(self, data: dict = None):
		"""
		ProductShippingMethod Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_module_code(self) -> str:
		"""
		Get mod_code.

		:returns: string
		"""

		return self.get_field('mod_code')

	def get_method_code(self) -> str:
		"""
		Get meth_code.

		:returns: string
		"""

		return self.get_field('meth_code')


"""
ProductShippingRules data model.
"""


class ProductShippingRules(Model):
	def __init__(self, data: dict = None):
		"""
		ProductShippingRules Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('methods'):
			value = self.get_field('methods')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductShippingMethod):
							value[i] = ProductShippingMethod(e)
					else:
						raise Exception('Expected list of ProductShippingMethod or dict')
			else:
				raise Exception('Expected list of ProductShippingMethod or dict')

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_own_package(self) -> bool:
		"""
		Get ownpackage.

		:returns: bool
		"""

		return self.get_field('ownpackage', False)

	def get_width(self) -> float:
		"""
		Get width.

		:returns: float
		"""

		return self.get_field('width', 0.00)

	def get_length(self) -> float:
		"""
		Get length.

		:returns: float
		"""

		return self.get_field('length', 0.00)

	def get_height(self) -> float:
		"""
		Get height.

		:returns: float
		"""

		return self.get_field('height', 0.00)

	def get_limit_methods(self) -> bool:
		"""
		Get limitmeths.

		:returns: bool
		"""

		return self.get_field('limitmeths', False)

	def get_methods(self):
		"""
		Get methods.

		:returns: List of ProductShippingMethod
		"""

		return self.get_field('methods', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'methods' in ret and isinstance(ret['methods'], list):
			for i, e in enumerate(ret['methods']):
				if isinstance(e, ProductShippingMethod):
					ret['methods'][i] = ret['methods'][i].to_dict()

		return ret


"""
Uri data model.
"""


class Uri(Model):
	# DESTINATION_TYPE constants.
	DESTINATION_TYPE_SCREEN = 'screen'
	DESTINATION_TYPE_PAGE = 'page'
	DESTINATION_TYPE_CATEGORY = 'category'
	DESTINATION_TYPE_PRODUCT = 'product'
	DESTINATION_TYPE_FEED = 'feed'

	def __init__(self, data: dict = None):
		"""
		Uri Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('store'):
			value = self.get_field('store')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('store', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

		if self.has_field('product'):
			value = self.get_field('product')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('product', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

		if self.has_field('category'):
			value = self.get_field('category')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('category', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

		if self.has_field('page'):
			value = self.get_field('page')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('page', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

		if self.has_field('feed'):
			value = self.get_field('feed')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('feed', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_uri(self) -> str:
		"""
		Get uri.

		:returns: string
		"""

		return self.get_field('uri')

	def get_store_id(self) -> int:
		"""
		Get store_id.

		:returns: int
		"""

		return self.get_field('store_id', 0)

	def get_screen(self) -> str:
		"""
		Get screen.

		:returns: string
		"""

		return self.get_field('screen')

	def get_page_id(self) -> int:
		"""
		Get page_id.

		:returns: int
		"""

		return self.get_field('page_id', 0)

	def get_category_id(self) -> int:
		"""
		Get cat_id.

		:returns: int
		"""

		return self.get_field('cat_id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_feed_id(self) -> int:
		"""
		Get feed_id.

		:returns: int
		"""

		return self.get_field('feed_id', 0)

	def get_canonical(self) -> bool:
		"""
		Get canonical.

		:returns: bool
		"""

		return self.get_field('canonical', False)

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_store(self):
		"""
		Get store.

		:returns: UriDetail|None
		"""

		return self.get_field('store', None)

	def get_product(self):
		"""
		Get product.

		:returns: UriDetail|None
		"""

		return self.get_field('product', None)

	def get_category(self):
		"""
		Get category.

		:returns: UriDetail|None
		"""

		return self.get_field('category', None)

	def get_page(self):
		"""
		Get page.

		:returns: UriDetail|None
		"""

		return self.get_field('page', None)

	def get_feed(self):
		"""
		Get feed.

		:returns: UriDetail|None
		"""

		return self.get_field('feed', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'store' in ret and isinstance(ret['store'], UriDetail):
			ret['store'] = ret['store'].to_dict()

		if 'product' in ret and isinstance(ret['product'], UriDetail):
			ret['product'] = ret['product'].to_dict()

		if 'category' in ret and isinstance(ret['category'], UriDetail):
			ret['category'] = ret['category'].to_dict()

		if 'page' in ret and isinstance(ret['page'], UriDetail):
			ret['page'] = ret['page'].to_dict()

		if 'feed' in ret and isinstance(ret['feed'], UriDetail):
			ret['feed'] = ret['feed'].to_dict()

		return ret


"""
UriDetail data model.
"""


class UriDetail(Model):
	def __init__(self, data: dict = None):
		"""
		UriDetail Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')


"""
ProductVariant data model.
"""


class ProductVariant(Model):
	def __init__(self, data: dict = None):
		"""
		ProductVariant Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('parts'):
			value = self.get_field('parts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductVariantPart):
							value[i] = ProductVariantPart(e)
					else:
						raise Exception('Expected list of ProductVariantPart or dict')
			else:
				raise Exception('Expected list of ProductVariantPart or dict')

		if self.has_field('dimensions'):
			value = self.get_field('dimensions')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductVariantDimension):
							value[i] = ProductVariantDimension(e)
					else:
						raise Exception('Expected list of ProductVariantDimension or dict')
			else:
				raise Exception('Expected list of ProductVariantDimension or dict')

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_variant_id(self) -> int:
		"""
		Get variant_id.

		:returns: int
		"""

		return self.get_field('variant_id', 0)

	def get_parts(self):
		"""
		Get parts.

		:returns: List of ProductVariantPart
		"""

		return self.get_field('parts', [])

	def get_dimensions(self):
		"""
		Get dimensions.

		:returns: List of ProductVariantDimension
		"""

		return self.get_field('dimensions', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'parts' in ret and isinstance(ret['parts'], list):
			for i, e in enumerate(ret['parts']):
				if isinstance(e, ProductVariantPart):
					ret['parts'][i] = ret['parts'][i].to_dict()

		if 'dimensions' in ret and isinstance(ret['dimensions'], list):
			for i, e in enumerate(ret['dimensions']):
				if isinstance(e, ProductVariantDimension):
					ret['dimensions'][i] = ret['dimensions'][i].to_dict()

		return ret


"""
ProductKit data model.
"""


class ProductKit(Model):
	def __init__(self, data: dict = None):
		"""
		ProductKit Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('parts'):
			value = self.get_field('parts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductKitPart):
							value[i] = ProductKitPart(e)
					else:
						raise Exception('Expected list of ProductKitPart or dict')
			else:
				raise Exception('Expected list of ProductKitPart or dict')

	def get_attr_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attr_type(self) -> str:
		"""
		Get attr_type.

		:returns: string
		"""

		return self.get_field('attr_type')

	def get_attr_code(self) -> str:
		"""
		Get attr_code.

		:returns: string
		"""

		return self.get_field('attr_code')

	def get_attr_prompt(self) -> str:
		"""
		Get attr_prompt.

		:returns: string
		"""

		return self.get_field('attr_prompt')

	def get_attmpat_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def get_option_code(self) -> str:
		"""
		Get option_code.

		:returns: string
		"""

		return self.get_field('option_code')

	def get_option_prompt(self) -> str:
		"""
		Get option_prompt.

		:returns: string
		"""

		return self.get_field('option_prompt')

	def get_parts(self):
		"""
		Get parts.

		:returns: List of ProductKitPart
		"""

		return self.get_field('parts', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'parts' in ret and isinstance(ret['parts'], list):
			for i, e in enumerate(ret['parts']):
				if isinstance(e, ProductKitPart):
					ret['parts'][i] = ret['parts'][i].to_dict()

		return ret


"""
ProductKitPart data model.
"""


class ProductKitPart(Model):
	def __init__(self, data: dict = None):
		"""
		ProductKitPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_product_code(self) -> str:
		"""
		Get product_code.

		:returns: string
		"""

		return self.get_field('product_code')

	def get_product_name(self) -> str:
		"""
		Get product_name.

		:returns: string
		"""

		return self.get_field('product_name')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)


"""
KitPart data model.
"""


class KitPart(Model):
	def __init__(self, data: dict = None):
		"""
		KitPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_part_id(self) -> int:
		"""
		Get part_id.

		:returns: int
		"""

		return self.get_field('part_id', 0)

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def set_part_id(self, part_id: int) -> 'KitPart':
		"""
		Set part_id.

		:param part_id: int
		:returns: KitPart
		"""

		return self.set_field('part_id', part_id)

	def set_quantity(self, quantity: int) -> 'KitPart':
		"""
		Set quantity.

		:param quantity: int
		:returns: KitPart
		"""

		return self.set_field('quantity', quantity)


"""
Category data model.
"""


class Category(Model):
	def __init__(self, data: dict = None):
		"""
		Category Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('uris'):
			value = self.get_field('uris')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Uri):
							value[i] = Uri(e)
					else:
						raise Exception('Expected list of Uri or dict')
			else:
				raise Exception('Expected list of Uri or dict')

		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_parent_id(self) -> int:
		"""
		Get parent_id.

		:returns: int
		"""

		return self.get_field('parent_id', 0)

	def get_availability_group_count(self) -> int:
		"""
		Get agrpcount.

		:returns: int
		"""

		return self.get_field('agrpcount', 0)

	def get_depth(self) -> int:
		"""
		Get depth.

		:returns: int
		"""

		return self.get_field('depth', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		return self.get_field('disp_order', 0)

	def get_page_id(self) -> int:
		"""
		Get page_id.

		:returns: int
		"""

		return self.get_field('page_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_page_title(self) -> str:
		"""
		Get page_title.

		:returns: string
		"""

		return self.get_field('page_title')

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_date_time_created(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_field('dt_created', 0)

	def get_date_time_updated(self) -> int:
		"""
		Get dt_updated.

		:returns: int
		"""

		return self.get_field('dt_updated', 0)

	def get_page_code(self) -> str:
		"""
		Get page_code.

		:returns: string
		"""

		return self.get_field('page_code')

	def get_parent_category(self) -> str:
		"""
		Get parent_category.

		:returns: string
		"""

		return self.get_field('parent_category')

	def get_uris(self):
		"""
		Get uris.

		:returns: List of Uri
		"""

		return self.get_field('uris', [])

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'uris' in ret and isinstance(ret['uris'], list):
			for i, e in enumerate(ret['uris']):
				if isinstance(e, Uri):
					ret['uris'][i] = ret['uris'][i].to_dict()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		return ret


"""
Order data model.
"""


class Order(Model):
	# ORDER_STATUS constants.
	ORDER_STATUS_PENDING = 0
	ORDER_STATUS_PROCESSING = 100
	ORDER_STATUS_SHIPPED = 200
	ORDER_STATUS_PARTIALLY_SHIPPED = 201
	ORDER_STATUS_CANCELLED = 300
	ORDER_STATUS_BACKORDERED = 400
	ORDER_STATUS_RMA_ISSUED = 500
	ORDER_STATUS_RETURNED = 600

	# ORDER_PAYMENT_STATUS constants.
	ORDER_PAYMENT_STATUS_PENDING = 0
	ORDER_PAYMENT_STATUS_AUTHORIZED = 100
	ORDER_PAYMENT_STATUS_CAPTURED = 200
	ORDER_PAYMENT_STATUS_PARTIALLY_CAPTURED = 201

	# ORDER_STOCK_STATUS constants.
	ORDER_STOCK_STATUS_AVAILABLE = 100
	ORDER_STOCK_STATUS_UNAVAILABLE = 200
	ORDER_STOCK_STATUS_PARTIAL = 201

	def __init__(self, data: dict = None):
		"""
		Order Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('customer'):
			value = self.get_field('customer')
			if isinstance(value, dict):
				if not isinstance(value, Customer):
					self.set_field('customer', Customer(value))
			else:
				raise Exception('Expected Customer or a dict')

		if self.has_field('items'):
			value = self.get_field('items')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItem):
							value[i] = OrderItem(e)
					else:
						raise Exception('Expected list of OrderItem or dict')
			else:
				raise Exception('Expected list of OrderItem or dict')

		if self.has_field('charges'):
			value = self.get_field('charges')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderCharge):
							value[i] = OrderCharge(e)
					else:
						raise Exception('Expected list of OrderCharge or dict')
			else:
				raise Exception('Expected list of OrderCharge or dict')

		if self.has_field('coupons'):
			value = self.get_field('coupons')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderCoupon):
							value[i] = OrderCoupon(e)
					else:
						raise Exception('Expected list of OrderCoupon or dict')
			else:
				raise Exception('Expected list of OrderCoupon or dict')

		if self.has_field('discounts'):
			value = self.get_field('discounts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderDiscountTotal):
							value[i] = OrderDiscountTotal(e)
					else:
						raise Exception('Expected list of OrderDiscountTotal or dict')
			else:
				raise Exception('Expected list of OrderDiscountTotal or dict')

		if self.has_field('payments'):
			value = self.get_field('payments')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderPayment):
							value[i] = OrderPayment(e)
					else:
						raise Exception('Expected list of OrderPayment or dict')
			else:
				raise Exception('Expected list of OrderPayment or dict')

		if self.has_field('notes'):
			value = self.get_field('notes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderNote):
							value[i] = OrderNote(e)
					else:
						raise Exception('Expected list of OrderNote or dict')
			else:
				raise Exception('Expected list of OrderNote or dict')

		if self.has_field('parts'):
			value = self.get_field('parts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderPart):
							value[i] = OrderPart(e)
					else:
						raise Exception('Expected list of OrderPart or dict')
			else:
				raise Exception('Expected list of OrderPart or dict')

		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_payment_id(self) -> int:
		"""
		Get pay_id.

		:returns: int
		"""

		return self.get_field('pay_id', 0)

	def get_batch_id(self) -> int:
		"""
		Get batch_id.

		:returns: int
		"""

		return self.get_field('batch_id', 0)

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_payment_status(self) -> int:
		"""
		Get pay_status.

		:returns: int
		"""

		return self.get_field('pay_status', 0)

	def get_stock_status(self) -> int:
		"""
		Get stk_status.

		:returns: int
		"""

		return self.get_field('stk_status', 0)

	def get_date_in_stock(self) -> int:
		"""
		Get dt_instock.

		:returns: int
		"""

		return self.get_field('dt_instock', 0)

	def get_order_date(self) -> int:
		"""
		Get orderdate.

		:returns: int
		"""

		return self.get_field('orderdate', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_ship_residential(self) -> bool:
		"""
		Get ship_res.

		:returns: bool
		"""

		return self.get_field('ship_res', False)

	def get_ship_first_name(self) -> str:
		"""
		Get ship_fname.

		:returns: string
		"""

		return self.get_field('ship_fname')

	def get_ship_last_name(self) -> str:
		"""
		Get ship_lname.

		:returns: string
		"""

		return self.get_field('ship_lname')

	def get_ship_email(self) -> str:
		"""
		Get ship_email.

		:returns: string
		"""

		return self.get_field('ship_email')

	def get_ship_company(self) -> str:
		"""
		Get ship_comp.

		:returns: string
		"""

		return self.get_field('ship_comp')

	def get_ship_phone(self) -> str:
		"""
		Get ship_phone.

		:returns: string
		"""

		return self.get_field('ship_phone')

	def get_ship_fax(self) -> str:
		"""
		Get ship_fax.

		:returns: string
		"""

		return self.get_field('ship_fax')

	def get_ship_address1(self) -> str:
		"""
		Get ship_addr1.

		:returns: string
		"""

		return self.get_field('ship_addr1')

	def get_ship_address2(self) -> str:
		"""
		Get ship_addr2.

		:returns: string
		"""

		return self.get_field('ship_addr2')

	def get_ship_city(self) -> str:
		"""
		Get ship_city.

		:returns: string
		"""

		return self.get_field('ship_city')

	def get_ship_state(self) -> str:
		"""
		Get ship_state.

		:returns: string
		"""

		return self.get_field('ship_state')

	def get_ship_zip(self) -> str:
		"""
		Get ship_zip.

		:returns: string
		"""

		return self.get_field('ship_zip')

	def get_ship_country(self) -> str:
		"""
		Get ship_cntry.

		:returns: string
		"""

		return self.get_field('ship_cntry')

	def get_bill_first_name(self) -> str:
		"""
		Get bill_fname.

		:returns: string
		"""

		return self.get_field('bill_fname')

	def get_bill_last_name(self) -> str:
		"""
		Get bill_lname.

		:returns: string
		"""

		return self.get_field('bill_lname')

	def get_bill_email(self) -> str:
		"""
		Get bill_email.

		:returns: string
		"""

		return self.get_field('bill_email')

	def get_bill_company(self) -> str:
		"""
		Get bill_comp.

		:returns: string
		"""

		return self.get_field('bill_comp')

	def get_bill_phone(self) -> str:
		"""
		Get bill_phone.

		:returns: string
		"""

		return self.get_field('bill_phone')

	def get_bill_fax(self) -> str:
		"""
		Get bill_fax.

		:returns: string
		"""

		return self.get_field('bill_fax')

	def get_bill_address1(self) -> str:
		"""
		Get bill_addr1.

		:returns: string
		"""

		return self.get_field('bill_addr1')

	def get_bill_address2(self) -> str:
		"""
		Get bill_addr2.

		:returns: string
		"""

		return self.get_field('bill_addr2')

	def get_bill_city(self) -> str:
		"""
		Get bill_city.

		:returns: string
		"""

		return self.get_field('bill_city')

	def get_bill_state(self) -> str:
		"""
		Get bill_state.

		:returns: string
		"""

		return self.get_field('bill_state')

	def get_bill_zip(self) -> str:
		"""
		Get bill_zip.

		:returns: string
		"""

		return self.get_field('bill_zip')

	def get_bill_country(self) -> str:
		"""
		Get bill_cntry.

		:returns: string
		"""

		return self.get_field('bill_cntry')

	def get_shipment_id(self) -> int:
		"""
		Get ship_id.

		:returns: int
		"""

		return self.get_field('ship_id', 0)

	def get_ship_data(self) -> str:
		"""
		Get ship_data.

		:returns: string
		"""

		return self.get_field('ship_data')

	def get_ship_method(self) -> str:
		"""
		Get ship_method.

		:returns: string
		"""

		return self.get_field('ship_method')

	def get_customer_login(self) -> str:
		"""
		Get cust_login.

		:returns: string
		"""

		return self.get_field('cust_login')

	def get_customer_password_email(self) -> str:
		"""
		Get cust_pw_email.

		:returns: string
		"""

		return self.get_field('cust_pw_email')

	def get_business_title(self) -> str:
		"""
		Get business_title.

		:returns: string
		"""

		return self.get_field('business_title')

	def get_payment_module(self) -> str:
		"""
		Get payment_module.

		:returns: string
		"""

		return self.get_field('payment_module')

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_source_id(self) -> int:
		"""
		Get source_id.

		:returns: int
		"""

		return self.get_field('source_id', 0)

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_formatted_total(self) -> str:
		"""
		Get formatted_total.

		:returns: string
		"""

		return self.get_field('formatted_total')

	def get_total_ship(self) -> float:
		"""
		Get total_ship.

		:returns: float
		"""

		return self.get_field('total_ship', 0.00)

	def get_formatted_total_ship(self) -> str:
		"""
		Get formatted_total_ship.

		:returns: string
		"""

		return self.get_field('formatted_total_ship')

	def get_total_tax(self) -> float:
		"""
		Get total_tax.

		:returns: float
		"""

		return self.get_field('total_tax', 0.00)

	def get_formatted_total_tax(self) -> str:
		"""
		Get formatted_total_tax.

		:returns: string
		"""

		return self.get_field('formatted_total_tax')

	def get_total_authorized(self) -> float:
		"""
		Get total_auth.

		:returns: float
		"""

		return self.get_field('total_auth', 0.00)

	def get_formatted_total_authorized(self) -> str:
		"""
		Get formatted_total_auth.

		:returns: string
		"""

		return self.get_field('formatted_total_auth')

	def get_total_captured(self) -> float:
		"""
		Get total_capt.

		:returns: float
		"""

		return self.get_field('total_capt', 0.00)

	def get_formatted_total_captured(self) -> str:
		"""
		Get formatted_total_capt.

		:returns: string
		"""

		return self.get_field('formatted_total_capt')

	def get_total_refunded(self) -> float:
		"""
		Get total_rfnd.

		:returns: float
		"""

		return self.get_field('total_rfnd', 0.00)

	def get_formatted_total_refunded(self) -> str:
		"""
		Get formatted_total_rfnd.

		:returns: string
		"""

		return self.get_field('formatted_total_rfnd')

	def get_net_captured(self) -> float:
		"""
		Get net_capt.

		:returns: float
		"""

		return self.get_field('net_capt', 0.00)

	def get_formatted_net_captured(self) -> str:
		"""
		Get formatted_net_capt.

		:returns: string
		"""

		return self.get_field('formatted_net_capt')

	def get_pending_count(self) -> int:
		"""
		Get pend_count.

		:returns: int
		"""

		return self.get_field('pend_count', 0)

	def get_backorder_count(self) -> int:
		"""
		Get bord_count.

		:returns: int
		"""

		return self.get_field('bord_count', 0)

	def get_note_count(self) -> int:
		"""
		Get note_count.

		:returns: int
		"""

		return self.get_field('note_count', 0)

	def get_customer(self):
		"""
		Get customer.

		:returns: Customer|None
		"""

		return self.get_field('customer', None)

	def get_items(self):
		"""
		Get items.

		:returns: List of OrderItem
		"""

		return self.get_field('items', [])

	def get_charges(self):
		"""
		Get charges.

		:returns: List of OrderCharge
		"""

		return self.get_field('charges', [])

	def get_coupons(self):
		"""
		Get coupons.

		:returns: List of OrderCoupon
		"""

		return self.get_field('coupons', [])

	def get_discounts(self):
		"""
		Get discounts.

		:returns: List of OrderDiscountTotal
		"""

		return self.get_field('discounts', [])

	def get_payments(self):
		"""
		Get payments.

		:returns: List of OrderPayment
		"""

		return self.get_field('payments', [])

	def get_notes(self):
		"""
		Get notes.

		:returns: List of OrderNote
		"""

		return self.get_field('notes', [])

	def get_parts(self):
		"""
		Get parts.

		:returns: List of OrderPart
		"""

		return self.get_field('parts', [])

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'customer' in ret and isinstance(ret['customer'], Customer):
			ret['customer'] = ret['customer'].to_dict()

		if 'items' in ret and isinstance(ret['items'], list):
			for i, e in enumerate(ret['items']):
				if isinstance(e, OrderItem):
					ret['items'][i] = ret['items'][i].to_dict()

		if 'charges' in ret and isinstance(ret['charges'], list):
			for i, e in enumerate(ret['charges']):
				if isinstance(e, OrderCharge):
					ret['charges'][i] = ret['charges'][i].to_dict()

		if 'coupons' in ret and isinstance(ret['coupons'], list):
			for i, e in enumerate(ret['coupons']):
				if isinstance(e, OrderCoupon):
					ret['coupons'][i] = ret['coupons'][i].to_dict()

		if 'discounts' in ret and isinstance(ret['discounts'], list):
			for i, e in enumerate(ret['discounts']):
				if isinstance(e, OrderDiscountTotal):
					ret['discounts'][i] = ret['discounts'][i].to_dict()

		if 'payments' in ret and isinstance(ret['payments'], list):
			for i, e in enumerate(ret['payments']):
				if isinstance(e, OrderPayment):
					ret['payments'][i] = ret['payments'][i].to_dict()

		if 'notes' in ret and isinstance(ret['notes'], list):
			for i, e in enumerate(ret['notes']):
				if isinstance(e, OrderNote):
					ret['notes'][i] = ret['notes'][i].to_dict()

		if 'parts' in ret and isinstance(ret['parts'], list):
			for i, e in enumerate(ret['parts']):
				if isinstance(e, OrderPart):
					ret['parts'][i] = ret['parts'][i].to_dict()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		return ret


"""
OrderShipment data model.
"""


class OrderShipment(Model):
	# ORDER_SHIPMENT_STATUS constants.
	ORDER_SHIPMENT_STATUS_PENDING = 0
	ORDER_SHIPMENT_STATUS_PICKING = 100
	ORDER_SHIPMENT_STATUS_SHIPPED = 200

	def __init__(self, data: dict = None):
		"""
		OrderShipment Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('order'):
			value = self.get_field('order')
			if isinstance(value, dict):
				if not isinstance(value, Order):
					self.set_field('order', Order(value))
			else:
				raise Exception('Expected Order or a dict')

		if self.has_field('items'):
			value = self.get_field('items')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItem):
							value[i] = OrderItem(e)
					else:
						raise Exception('Expected list of OrderItem or dict')
			else:
				raise Exception('Expected list of OrderItem or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_batch_id(self) -> int:
		"""
		Get batch_id.

		:returns: int
		"""

		return self.get_field('batch_id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_label_count(self) -> int:
		"""
		Get labelcount.

		:returns: int
		"""

		return self.get_field('labelcount', 0)

	def get_ship_date(self) -> int:
		"""
		Get ship_date.

		:returns: int
		"""

		return self.get_field('ship_date', 0)

	def get_tracking_number(self) -> str:
		"""
		Get tracknum.

		:returns: string
		"""

		return self.get_field('tracknum')

	def get_tracking_type(self) -> str:
		"""
		Get tracktype.

		:returns: string
		"""

		return self.get_field('tracktype')

	def get_tracking_link(self) -> str:
		"""
		Get tracklink.

		:returns: string
		"""

		return self.get_field('tracklink')

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')

	def get_order(self):
		"""
		Get order.

		:returns: Order|None
		"""

		return self.get_field('order', None)

	def get_items(self):
		"""
		Get items.

		:returns: List of OrderItem
		"""

		return self.get_field('items', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'order' in ret and isinstance(ret['order'], Order):
			ret['order'] = ret['order'].to_dict()

		if 'items' in ret and isinstance(ret['items'], list):
			for i, e in enumerate(ret['items']):
				if isinstance(e, OrderItem):
					ret['items'][i] = ret['items'][i].to_dict()

		return ret


"""
OrderItemOption data model.
"""


class OrderItemOption(Model):
	def __init__(self, data: dict = None):
		"""
		OrderItemOption Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_line_id(self) -> int:
		"""
		Get line_id.

		:returns: int
		"""

		return self.get_field('line_id', 0)

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def get_option_code(self) -> str:
		"""
		Get opt_code.

		:returns: string
		"""

		return self.get_field('opt_code')

	def get_attribute_code(self) -> str:
		"""
		Get attr_code.

		:returns: string
		"""

		return self.get_field('attr_code')

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_value(self) -> str:
		"""
		Get value.

		:returns: string
		"""

		return self.get_field('value')

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_retail(self) -> float:
		"""
		Get retail.

		:returns: float
		"""

		return self.get_field('retail', 0.00)

	def get_base_price(self) -> float:
		"""
		Get base_price.

		:returns: float
		"""

		return self.get_field('base_price', 0.00)

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_option_data(self) -> str:
		"""
		Get data.

		:returns: string
		"""

		return self.get_field('data')

	def get_option_data_long(self) -> str:
		"""
		Get data_long.

		:returns: string
		"""

		return self.get_field('data_long')

	def get_attribute_prompt(self) -> str:
		"""
		Get attr_prompt.

		:returns: string
		"""

		return self.get_field('attr_prompt')

	def get_option_prompt(self) -> str:
		"""
		Get opt_prompt.

		:returns: string
		"""

		return self.get_field('opt_prompt')

	def set_attribute_code(self, attribute_code: str) -> 'OrderItemOption':
		"""
		Set attr_code.

		:param attribute_code: string
		:returns: OrderItemOption
		"""

		return self.set_field('attr_code', attribute_code)

	def set_attribute_id(self, attribute_id: int) -> 'OrderItemOption':
		"""
		Set attr_id.

		:param attribute_id: int
		:returns: OrderItemOption
		"""

		return self.set_field('attr_id', attribute_id)

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'OrderItemOption':
		"""
		Set attmpat_id.

		:param attribute_template_attribute_id: int
		:returns: OrderItemOption
		"""

		return self.set_field('attmpat_id', attribute_template_attribute_id)

	def set_value(self, value: str) -> 'OrderItemOption':
		"""
		Set value.

		:param value: string
		:returns: OrderItemOption
		"""

		return self.set_field('value', value)

	def set_weight(self, weight: float) -> 'OrderItemOption':
		"""
		Set weight.

		:param weight: int
		:returns: OrderItemOption
		"""

		return self.set_field('weight', weight)

	def set_retail(self, retail: float) -> 'OrderItemOption':
		"""
		Set retail.

		:param retail: int
		:returns: OrderItemOption
		"""

		return self.set_field('retail', retail)

	def set_base_price(self, base_price: float) -> 'OrderItemOption':
		"""
		Set base_price.

		:param base_price: int
		:returns: OrderItemOption
		"""

		return self.set_field('base_price', base_price)

	def set_price(self, price: float) -> 'OrderItemOption':
		"""
		Set price.

		:param price: int
		:returns: OrderItemOption
		"""

		return self.set_field('price', price)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = {}

		if self.has_field('attr_code'):
			ret['attr_code'] = self.get_field('attr_code')

		if self.has_field('attr_id'):
			ret['attr_id'] = self.get_field('attr_id')

		if self.has_field('attmpat_id'):
			ret['attmpat_id'] = self.get_field('attmpat_id')

		if self.has_field('value'):
			ret['opt_code_or_data'] = self.get_field('value')

		if self.has_field('price'):
			ret['price'] = self.get_field('price')

		if self.has_field('weight'):
			ret['weight'] = self.get_field('weight')

		return ret


"""
OrderItem data model.
"""


class OrderItem(Model):
	# ORDER_ITEM_STATUS constants.
	ORDER_ITEM_STATUS_PENDING = 0
	ORDER_ITEM_STATUS_PROCESSING = 100
	ORDER_ITEM_STATUS_SHIPPED = 200
	ORDER_ITEM_STATUS_PARTIALLY_SHIPPED = 201
	ORDER_ITEM_STATUS_GIFT_CERT_NOT_REDEEMED = 210
	ORDER_ITEM_STATUS_GIFT_CERT_REDEEMED = 211
	ORDER_ITEM_STATUS_DIGITAL_NOT_DOWNLOADED = 220
	ORDER_ITEM_STATUS_DIGITAL_DOWNLOADED = 221
	ORDER_ITEM_STATUS_CANCELLED = 300
	ORDER_ITEM_STATUS_BACKORDERED = 400
	ORDER_ITEM_STATUS_RMA_ISSUED = 500
	ORDER_ITEM_STATUS_RETURNED = 600

	def __init__(self, data: dict = None):
		"""
		OrderItem Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('shipment'):
			value = self.get_field('shipment')
			if isinstance(value, dict):
				if not isinstance(value, OrderShipment):
					self.set_field('shipment', OrderShipment(value))
			else:
				raise Exception('Expected OrderShipment or a dict')

		if self.has_field('discounts'):
			value = self.get_field('discounts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItemDiscount):
							value[i] = OrderItemDiscount(e)
					else:
						raise Exception('Expected list of OrderItemDiscount or dict')
			else:
				raise Exception('Expected list of OrderItemDiscount or dict')

		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItemOption):
							value[i] = OrderItemOption(e)
					else:
						raise Exception('Expected list of OrderItemOption or dict')
			else:
				raise Exception('Expected list of OrderItemOption or dict')

		if self.has_field('subscription'):
			value = self.get_field('subscription')
			if isinstance(value, dict):
				if not isinstance(value, OrderItemSubscription):
					self.set_field('subscription', OrderItemSubscription(value))
			else:
				raise Exception('Expected OrderItemSubscription or a dict')

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_line_id(self) -> int:
		"""
		Get line_id.

		:returns: int
		"""

		return self.get_field('line_id', 0)

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_subscription_id(self) -> int:
		"""
		Get subscrp_id.

		:returns: int
		"""

		return self.get_field('subscrp_id', 0)

	def get_subscription_term_id(self) -> int:
		"""
		Get subterm_id.

		:returns: int
		"""

		return self.get_field('subterm_id', 0)

	def get_rma_id(self) -> int:
		"""
		Get rma_id.

		:returns: int
		"""

		return self.get_field('rma_id', 0)

	def get_rma_code(self) -> str:
		"""
		Get rma_code.

		:returns: string
		"""

		return self.get_field('rma_code')

	def get_rma_data_time_issued(self) -> int:
		"""
		Get rma_dt_issued.

		:returns: int
		"""

		return self.get_field('rma_dt_issued', 0)

	def get_rma_date_time_received(self) -> int:
		"""
		Get rma_dt_recvd.

		:returns: int
		"""

		return self.get_field('rma_dt_recvd', 0)

	def get_date_in_stock(self) -> int:
		"""
		Get dt_instock.

		:returns: int
		"""

		return self.get_field('dt_instock', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_retail(self) -> float:
		"""
		Get retail.

		:returns: float
		"""

		return self.get_field('retail', 0.00)

	def get_base_price(self) -> float:
		"""
		Get base_price.

		:returns: float
		"""

		return self.get_field('base_price', 0.00)

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_tax(self) -> float:
		"""
		Get tax.

		:returns: float
		"""

		return self.get_field('tax', 0.00)

	def get_formatted_tax(self) -> str:
		"""
		Get formatted_tax.

		:returns: string
		"""

		return self.get_field('formatted_tax')

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_taxable(self) -> bool:
		"""
		Get taxable.

		:returns: bool
		"""

		return self.get_field('taxable', False)

	def get_upsold(self) -> bool:
		"""
		Get upsold.

		:returns: bool
		"""

		return self.get_field('upsold', False)

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_shipment(self):
		"""
		Get shipment.

		:returns: OrderShipment|None
		"""

		return self.get_field('shipment', None)

	def get_discounts(self):
		"""
		Get discounts.

		:returns: List of OrderItemDiscount
		"""

		return self.get_field('discounts', [])

	def get_options(self):
		"""
		Get options.

		:returns: List of OrderItemOption
		"""

		return self.get_field('options', [])

	def get_subscription(self):
		"""
		Get subscription.

		:returns: OrderItemSubscription|None
		"""

		return self.get_field('subscription', None)

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_tracking_type(self) -> str:
		"""
		Get tracktype.

		:returns: string
		"""

		return self.get_field('tracktype')

	def get_tracking_number(self) -> str:
		"""
		Get tracknum.

		:returns: string
		"""

		return self.get_field('tracknum')

	def get_shipment_id(self) -> int:
		"""
		Get shpmnt_id.

		:returns: int
		"""

		return self.get_field('shpmnt_id', 0)

	def set_code(self, code: str) -> 'OrderItem':
		"""
		Set code.

		:param code: string
		:returns: OrderItem
		"""

		return self.set_field('code', code)

	def set_name(self, name: str) -> 'OrderItem':
		"""
		Set name.

		:param name: string
		:returns: OrderItem
		"""

		return self.set_field('name', name)

	def set_sku(self, sku: str) -> 'OrderItem':
		"""
		Set sku.

		:param sku: string
		:returns: OrderItem
		"""

		return self.set_field('sku', sku)

	def set_price(self, price: float) -> 'OrderItem':
		"""
		Set price.

		:param price: int
		:returns: OrderItem
		"""

		return self.set_field('price', price)

	def set_tax(self, tax: float) -> 'OrderItem':
		"""
		Set tax.

		:param tax: int
		:returns: OrderItem
		"""

		return self.set_field('tax', tax)

	def set_weight(self, weight: float) -> 'OrderItem':
		"""
		Set weight.

		:param weight: int
		:returns: OrderItem
		"""

		return self.set_field('weight', weight)

	def set_taxable(self, taxable: bool) -> 'OrderItem':
		"""
		Set taxable.

		:param taxable: bool
		:returns: OrderItem
		"""

		return self.set_field('taxable', taxable)

	def set_upsold(self, upsold: bool) -> 'OrderItem':
		"""
		Set upsold.

		:param upsold: bool
		:returns: OrderItem
		"""

		return self.set_field('upsold', upsold)

	def set_quantity(self, quantity: int) -> 'OrderItem':
		"""
		Set quantity.

		:param quantity: int
		:returns: OrderItem
		"""

		return self.set_field('quantity', quantity)

	def set_options(self, options: list) -> 'OrderItem':
		"""
		Set options.

		:param options: List of OrderItemOption 
		:raises Exception:
		:returns: OrderItem
		"""

		for i, e in enumerate(options, 0):
			if isinstance(e, OrderItemOption):
				continue
			elif isinstance(e, dict):
				options[i] = OrderItemOption(e)
			else:
				raise Exception('Expected instance of OrderItemOption or dict')
		return self.set_field('options', options)

	def set_tracking_type(self, tracking_type: str) -> 'OrderItem':
		"""
		Set tracktype.

		:param tracking_type: string
		:returns: OrderItem
		"""

		return self.set_field('tracktype', tracking_type)

	def set_tracking_number(self, tracking_number: str) -> 'OrderItem':
		"""
		Set tracknum.

		:param tracking_number: string
		:returns: OrderItem
		"""

		return self.set_field('tracknum', tracking_number)
	
	def add_option(self, option: 'OrderItemOption') -> 'OrderItem':
		"""
		Add a OrderItemOption.
		
		:param option: OrderItemOption
		:returns: OrderItem
		"""

		if 'options' not in self:
			self['options'] = []
		self['options'].append(option)
		return self

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'shipment' in ret and isinstance(ret['shipment'], OrderShipment):
			ret['shipment'] = ret['shipment'].to_dict()

		if 'discounts' in ret and isinstance(ret['discounts'], list):
			for i, e in enumerate(ret['discounts']):
				if isinstance(e, OrderItemDiscount):
					ret['discounts'][i] = ret['discounts'][i].to_dict()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, OrderItemOption):
					ret['options'][i] = ret['options'][i].to_dict()

		if 'subscription' in ret and isinstance(ret['subscription'], OrderItemSubscription):
			ret['subscription'] = ret['subscription'].to_dict()

		return ret


"""
OrderCharge data model.
"""


class OrderCharge(Model):
	def __init__(self, data: dict = None):
		"""
		OrderCharge Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_charge_id(self) -> int:
		"""
		Get charge_id.

		:returns: int
		"""

		return self.get_field('charge_id', 0)

	def get_module_id(self) -> int:
		"""
		Get module_id.

		:returns: int
		"""

		return self.get_field('module_id', 0)

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_amount(self) -> float:
		"""
		Get amount.

		:returns: float
		"""

		return self.get_field('amount', 0.00)

	def get_formatted_amount(self) -> str:
		"""
		Get formatted_amount.

		:returns: string
		"""

		return self.get_field('formatted_amount')

	def get_display_amount(self) -> float:
		"""
		Get disp_amt.

		:returns: float
		"""

		return self.get_field('disp_amt', 0.00)

	def get_formatted_display_amount(self) -> str:
		"""
		Get formatted_disp_amt.

		:returns: string
		"""

		return self.get_field('formatted_disp_amt')

	def get_tax_exempt(self) -> bool:
		"""
		Get tax_exempt.

		:returns: bool
		"""

		return self.get_field('tax_exempt', False)

	def get_tax(self) -> float:
		"""
		Get tax.

		:returns: float
		"""

		return self.get_field('tax', 0.00)

	def get_formatted_tax(self) -> str:
		"""
		Get formatted_tax.

		:returns: string
		"""

		return self.get_field('formatted_tax')

	def set_type(self, type: str) -> 'OrderCharge':
		"""
		Set type.

		:param type: string
		:returns: OrderCharge
		"""

		return self.set_field('type', type)

	def set_description(self, description: str) -> 'OrderCharge':
		"""
		Set descrip.

		:param description: string
		:returns: OrderCharge
		"""

		return self.set_field('descrip', description)

	def set_amount(self, amount: float) -> 'OrderCharge':
		"""
		Set amount.

		:param amount: int
		:returns: OrderCharge
		"""

		return self.set_field('amount', amount)

	def set_display_amount(self, display_amount: float) -> 'OrderCharge':
		"""
		Set disp_amt.

		:param display_amount: int
		:returns: OrderCharge
		"""

		return self.set_field('disp_amt', display_amount)

	def set_tax_exempt(self, tax_exempt: bool) -> 'OrderCharge':
		"""
		Set tax_exempt.

		:param tax_exempt: bool
		:returns: OrderCharge
		"""

		return self.set_field('tax_exempt', tax_exempt)


"""
OrderCoupon data model.
"""


class OrderCoupon(Model):
	def __init__(self, data: dict = None):
		"""
		OrderCoupon Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_coupon_id(self) -> int:
		"""
		Get coupon_id.

		:returns: int
		"""

		return self.get_field('coupon_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
OrderItemDiscount data model.
"""


class OrderItemDiscount(Model):
	def __init__(self, data: dict = None):
		"""
		OrderItemDiscount Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_line_id(self) -> int:
		"""
		Get line_id.

		:returns: int
		"""

		return self.get_field('line_id', 0)

	def get_price_group_id(self) -> int:
		"""
		Get pgrp_id.

		:returns: int
		"""

		return self.get_field('pgrp_id', 0)

	def get_display(self) -> bool:
		"""
		Get display.

		:returns: bool
		"""

		return self.get_field('display', False)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_discount(self) -> float:
		"""
		Get discount.

		:returns: float
		"""

		return self.get_field('discount', 0.00)


"""
OrderDiscountTotal data model.
"""


class OrderDiscountTotal(Model):
	def __init__(self, data: dict = None):
		"""
		OrderDiscountTotal Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_price_group_id(self) -> int:
		"""
		Get pgrp_id.

		:returns: int
		"""

		return self.get_field('pgrp_id', 0)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)


"""
OrderPayment data model.
"""


class OrderPayment(Model):
	# ORDER_PAYMENT_TYPE constants.
	ORDER_PAYMENT_TYPE_DECLINED = 0
	ORDER_PAYMENT_TYPE_LEGACY_AUTH = 1
	ORDER_PAYMENT_TYPE_LEGACY_CAPTURE = 2
	ORDER_PAYMENT_TYPE_AUTH = 3
	ORDER_PAYMENT_TYPE_CAPTURE = 4
	ORDER_PAYMENT_TYPE_AUTH_CAPTURE = 5
	ORDER_PAYMENT_TYPE_REFUND = 6
	ORDER_PAYMENT_TYPE_VOID = 7

	def __init__(self, data: dict = None):
		"""
		OrderPayment Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_type(self) -> int:
		"""
		Get type.

		:returns: int
		"""

		return self.get_field('type', 0)

	def get_reference_number(self) -> str:
		"""
		Get refnum.

		:returns: string
		"""

		return self.get_field('refnum')

	def get_amount(self) -> float:
		"""
		Get amount.

		:returns: float
		"""

		return self.get_field('amount', 0.00)

	def get_formatted_amount(self) -> str:
		"""
		Get formatted_amount.

		:returns: string
		"""

		return self.get_field('formatted_amount')

	def get_available(self) -> float:
		"""
		Get available.

		:returns: float
		"""

		return self.get_field('available', 0.00)

	def get_formatted_available(self) -> str:
		"""
		Get formatted_available.

		:returns: string
		"""

		return self.get_field('formatted_available')

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_field('dtstamp', 0)

	def get_expires(self) -> str:
		"""
		Get expires.

		:returns: string
		"""

		return self.get_field('expires')

	def get_payment_id(self) -> int:
		"""
		Get pay_id.

		:returns: int
		"""

		return self.get_field('pay_id', 0)

	def get_payment_sec_id(self) -> int:
		"""
		Get pay_secid.

		:returns: int
		"""

		return self.get_field('pay_secid', 0)

	def get_decrypt_status(self) -> str:
		"""
		Get decrypt_status.

		:returns: string
		"""

		return self.get_field('decrypt_status')

	def get_decrypt_error(self) -> str:
		"""
		Get decrypt_error.

		:returns: string
		"""

		return self.get_field('decrypt_error')

	def get_description(self) -> str:
		"""
		Get description.

		:returns: string
		"""

		return self.get_field('description')

	def get_payment_data(self) -> dict:
		"""
		Get data.

		:returns: dict
		"""

		return self.get_field('data', {})


"""
Subscription data model.
"""


class Subscription(Model):
	def __init__(self, data: dict = None):
		"""
		Subscription Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_line_id(self) -> int:
		"""
		Get line_id.

		:returns: int
		"""

		return self.get_field('line_id', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_customer_payment_card_id(self) -> int:
		"""
		Get custpc_id.

		:returns: int
		"""

		return self.get_field('custpc_id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_subscription_term_id(self) -> int:
		"""
		Get subterm_id.

		:returns: int
		"""

		return self.get_field('subterm_id', 0)

	def get_address_id(self) -> int:
		"""
		Get addr_id.

		:returns: int
		"""

		return self.get_field('addr_id', 0)

	def get_ship_id(self) -> int:
		"""
		Get ship_id.

		:returns: int
		"""

		return self.get_field('ship_id', 0)

	def get_ship_data(self) -> str:
		"""
		Get ship_data.

		:returns: string
		"""

		return self.get_field('ship_data')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_term_remaining(self) -> int:
		"""
		Get termrem.

		:returns: int
		"""

		return self.get_field('termrem', 0)

	def get_term_processed(self) -> int:
		"""
		Get termproc.

		:returns: int
		"""

		return self.get_field('termproc', 0)

	def get_first_date(self) -> int:
		"""
		Get firstdate.

		:returns: int
		"""

		return self.get_field('firstdate', 0)

	def get_last_date(self) -> int:
		"""
		Get lastdate.

		:returns: int
		"""

		return self.get_field('lastdate', 0)

	def get_next_date(self) -> int:
		"""
		Get nextdate.

		:returns: int
		"""

		return self.get_field('nextdate', 0)

	def get_status(self) -> str:
		"""
		Get status.

		:returns: string
		"""

		return self.get_field('status')

	def get_message(self) -> str:
		"""
		Get message.

		:returns: string
		"""

		return self.get_field('message')

	def get_cancel_date(self) -> str:
		"""
		Get cncldate.

		:returns: string
		"""

		return self.get_field('cncldate')

	def get_tax(self) -> float:
		"""
		Get tax.

		:returns: float
		"""

		return self.get_field('tax', 0.00)

	def get_formatted_tax(self) -> str:
		"""
		Get formatted_tax.

		:returns: string
		"""

		return self.get_field('formatted_tax')

	def get_shipping(self) -> float:
		"""
		Get shipping.

		:returns: float
		"""

		return self.get_field('shipping', 0.00)

	def get_formatted_shipping(self) -> str:
		"""
		Get formatted_shipping.

		:returns: string
		"""

		return self.get_field('formatted_shipping')

	def get_subtotal(self) -> float:
		"""
		Get subtotal.

		:returns: float
		"""

		return self.get_field('subtotal', 0.00)

	def get_formatted_subtotal(self) -> str:
		"""
		Get formatted_subtotal.

		:returns: string
		"""

		return self.get_field('formatted_subtotal')

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_formatted_total(self) -> str:
		"""
		Get formatted_total.

		:returns: string
		"""

		return self.get_field('formatted_total')


"""
ProductSubscriptionTerm data model.
"""


class ProductSubscriptionTerm(Model):
	# TERM_FREQUENCY constants.
	TERM_FREQUENCY_N_DAYS = 'n'
	TERM_FREQUENCY_N_MONTHS = 'n_months'
	TERM_FREQUENCY_DAILY = 'daily'
	TERM_FREQUENCY_WEEKLY = 'weekly'
	TERM_FREQUENCY_BIWEEKLY = 'biweekly'
	TERM_FREQUENCY_QUARTERLY = 'quarterly'
	TERM_FREQUENCY_SEMIANNUALLY = 'semiannually'
	TERM_FREQUENCY_ANNUALLY = 'annually'
	TERM_FREQUENCY_FIXED_WEEKLY = 'fixedweekly'
	TERM_FREQUENCY_FIXED_MONTHLY = 'fixedmonthly'
	TERM_FREQUENCY_DATES = 'dates'

	def __init__(self, data: dict = None):
		"""
		ProductSubscriptionTerm Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_frequency(self) -> str:
		"""
		Get frequency.

		:returns: string
		"""

		return self.get_field('frequency')

	def get_term(self) -> int:
		"""
		Get term.

		:returns: int
		"""

		return self.get_field('term', 0)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_n(self) -> int:
		"""
		Get n.

		:returns: int
		"""

		return self.get_field('n', 0)

	def get_fixed_day_of_week(self) -> int:
		"""
		Get fixed_dow.

		:returns: int
		"""

		return self.get_field('fixed_dow', 0)

	def get_fixed_day_of_month(self) -> int:
		"""
		Get fixed_dom.

		:returns: int
		"""

		return self.get_field('fixed_dom', 0)

	def get_subscription_count(self) -> int:
		"""
		Get sub_count.

		:returns: int
		"""

		return self.get_field('sub_count', 0)


"""
OrderCustomField data model.
"""


class OrderCustomField(Model):
	def __init__(self, data: dict = None):
		"""
		OrderCustomField Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('module'):
			value = self.get_field('module')
			if isinstance(value, dict):
				if not isinstance(value, Module):
					self.set_field('module', Module(value))
			else:
				raise Exception('Expected Module or a dict')

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_searchable(self) -> bool:
		"""
		Get searchable.

		:returns: bool
		"""

		return self.get_field('searchable', False)

	def get_sortable(self) -> bool:
		"""
		Get sortable.

		:returns: bool
		"""

		return self.get_field('sortable', False)

	def get_module(self):
		"""
		Get module.

		:returns: Module|None
		"""

		return self.get_field('module', None)

	def get_choices(self) -> dict:
		"""
		Get choices.

		:returns: dict
		"""

		return self.get_field('choices', {})

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'module' in ret and isinstance(ret['module'], Module):
			ret['module'] = ret['module'].to_dict()

		return ret


"""
CustomerPaymentCard data model.
"""


class CustomerPaymentCard(Model):
	def __init__(self, data: dict = None):
		"""
		CustomerPaymentCard Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_first_name(self) -> str:
		"""
		Get fname.

		:returns: string
		"""

		return self.get_field('fname')

	def get_last_name(self) -> str:
		"""
		Get lname.

		:returns: string
		"""

		return self.get_field('lname')

	def get_expiration_month(self) -> int:
		"""
		Get exp_month.

		:returns: int
		"""

		return self.get_field('exp_month', 0)

	def get_expiration_year(self) -> int:
		"""
		Get exp_year.

		:returns: int
		"""

		return self.get_field('exp_year', 0)

	def get_last_four(self) -> str:
		"""
		Get lastfour.

		:returns: string
		"""

		return self.get_field('lastfour')

	def get_address1(self) -> str:
		"""
		Get addr1.

		:returns: string
		"""

		return self.get_field('addr1')

	def get_address2(self) -> str:
		"""
		Get addr2.

		:returns: string
		"""

		return self.get_field('addr2')

	def get_city(self) -> str:
		"""
		Get city.

		:returns: string
		"""

		return self.get_field('city')

	def get_state(self) -> str:
		"""
		Get state.

		:returns: string
		"""

		return self.get_field('state')

	def get_zip(self) -> str:
		"""
		Get zip.

		:returns: string
		"""

		return self.get_field('zip')

	def get_country(self) -> str:
		"""
		Get cntry.

		:returns: string
		"""

		return self.get_field('cntry')

	def get_last_used(self) -> str:
		"""
		Get lastused.

		:returns: string
		"""

		return self.get_field('lastused')

	def get_token(self) -> str:
		"""
		Get token.

		:returns: string
		"""

		return self.get_field('token')

	def get_type_id(self) -> int:
		"""
		Get type_id.

		:returns: int
		"""

		return self.get_field('type_id', 0)

	def get_reference_count(self) -> int:
		"""
		Get refcount.

		:returns: int
		"""

		return self.get_field('refcount', 0)

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_module_code(self) -> str:
		"""
		Get mod_code.

		:returns: string
		"""

		return self.get_field('mod_code')

	def get_method_code(self) -> str:
		"""
		Get meth_code.

		:returns: string
		"""

		return self.get_field('meth_code')


"""
OrderProductAttribute data model.
"""


class OrderProductAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		OrderProductAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_template_code(self) -> str:
		"""
		Get template_code.

		:returns: string
		"""

		return self.get_field('template_code')

	def get_value(self) -> str:
		"""
		Get value.

		:returns: string
		"""

		return self.get_field('value')

	def set_code(self, code: str) -> 'OrderProductAttribute':
		"""
		Set code.

		:param code: string
		:returns: OrderProductAttribute
		"""

		return self.set_field('code', code)

	def set_template_code(self, template_code: str) -> 'OrderProductAttribute':
		"""
		Set template_code.

		:param template_code: string
		:returns: OrderProductAttribute
		"""

		return self.set_field('template_code', template_code)

	def set_value(self, value: str) -> 'OrderProductAttribute':
		"""
		Set value.

		:param value: string
		:returns: OrderProductAttribute
		"""

		return self.set_field('value', value)


"""
OrderProduct data model.
"""


class OrderProduct(Model):
	def __init__(self, data: dict = None):
		"""
		OrderProduct Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderProductAttribute):
							value[i] = OrderProductAttribute(e)
					else:
						raise Exception('Expected list of OrderProductAttribute or dict')
			else:
				raise Exception('Expected list of OrderProductAttribute or dict')

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_tracking_number(self) -> str:
		"""
		Get tracknum.

		:returns: string
		"""

		return self.get_field('tracknum')

	def get_tracking_type(self) -> str:
		"""
		Get tracktype.

		:returns: string
		"""

		return self.get_field('tracktype')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of OrderProductAttribute
		"""

		return self.get_field('attributes', [])

	def set_status(self, status: int) -> 'OrderProduct':
		"""
		Set status.

		:param status: int
		:returns: OrderProduct
		"""

		return self.set_field('status', status)

	def set_code(self, code: str) -> 'OrderProduct':
		"""
		Set code.

		:param code: string
		:returns: OrderProduct
		"""

		return self.set_field('code', code)

	def set_sku(self, sku: str) -> 'OrderProduct':
		"""
		Set sku.

		:param sku: string
		:returns: OrderProduct
		"""

		return self.set_field('sku', sku)

	def set_tracking_number(self, tracking_number: str) -> 'OrderProduct':
		"""
		Set tracknum.

		:param tracking_number: string
		:returns: OrderProduct
		"""

		return self.set_field('tracknum', tracking_number)

	def set_tracking_type(self, tracking_type: str) -> 'OrderProduct':
		"""
		Set tracktype.

		:param tracking_type: string
		:returns: OrderProduct
		"""

		return self.set_field('tracktype', tracking_type)

	def set_quantity(self, quantity: int) -> 'OrderProduct':
		"""
		Set quantity.

		:param quantity: int
		:returns: OrderProduct
		"""

		return self.set_field('quantity', quantity)

	def set_attributes(self, attributes: list) -> 'OrderProduct':
		"""
		Set attributes.

		:param attributes: List of OrderProductAttribute 
		:raises Exception:
		:returns: OrderProduct
		"""

		for i, e in enumerate(attributes, 0):
			if isinstance(e, OrderProductAttribute):
				continue
			elif isinstance(e, dict):
				attributes[i] = OrderProductAttribute(e)
			else:
				raise Exception('Expected instance of OrderProductAttribute or dict')
		return self.set_field('attributes', attributes)
	
	def add_attribute(self, attribute: 'OrderProductAttribute') -> 'OrderProduct':
		"""
		Add a OrderProductAttribute.
		
		:param attribute: OrderProductAttribute
		:returns: OrderProduct
		"""

		if 'attributes' not in self:
			self['attributes'] = []
		self['attributes'].append(attribute)
		return self

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, OrderProductAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		return ret


"""
ProductInventorySettings data model.
"""


class ProductInventorySettings(Model):
	def __init__(self, data: dict = None):
		"""
		ProductInventorySettings Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_in_stock_message_short(self) -> str:
		"""
		Get in_short.

		:returns: string
		"""

		return self.get_field('in_short')

	def get_in_stock_message_long(self) -> str:
		"""
		Get in_long.

		:returns: string
		"""

		return self.get_field('in_long')

	def get_track_low_stock_level(self) -> str:
		"""
		Get low_track.

		:returns: string
		"""

		return self.get_field('low_track')

	def get_low_stock_level(self) -> int:
		"""
		Get low_level.

		:returns: int
		"""

		return self.get_field('low_level', 0)

	def get_low_stock_level_default(self) -> bool:
		"""
		Get low_lvl_d.

		:returns: bool
		"""

		return self.get_field('low_lvl_d', False)

	def get_low_stock_message_short(self) -> str:
		"""
		Get low_short.

		:returns: string
		"""

		return self.get_field('low_short')

	def get_low_stock_message_long(self) -> str:
		"""
		Get low_long.

		:returns: string
		"""

		return self.get_field('low_long')

	def get_track_out_of_stock_level(self) -> str:
		"""
		Get out_track.

		:returns: string
		"""

		return self.get_field('out_track')

	def get_hide_out_of_stock(self) -> str:
		"""
		Get out_hide.

		:returns: string
		"""

		return self.get_field('out_hide')

	def get_out_of_stock_level(self) -> int:
		"""
		Get out_level.

		:returns: int
		"""

		return self.get_field('out_level', 0)

	def get_out_of_stock_level_default(self) -> bool:
		"""
		Get out_lvl_d.

		:returns: bool
		"""

		return self.get_field('out_lvl_d', False)

	def get_out_of_stock_message_short(self) -> str:
		"""
		Get out_short.

		:returns: string
		"""

		return self.get_field('out_short')

	def get_out_of_stock_message_long(self) -> str:
		"""
		Get out_long.

		:returns: string
		"""

		return self.get_field('out_long')

	def get_limited_stock_message(self) -> str:
		"""
		Get ltd_long.

		:returns: string
		"""

		return self.get_field('ltd_long')


"""
ProductVariantPart data model.
"""


class ProductVariantPart(Model):
	def __init__(self, data: dict = None):
		"""
		ProductVariantPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_product_code(self) -> str:
		"""
		Get product_code.

		:returns: string
		"""

		return self.get_field('product_code')

	def get_product_name(self) -> str:
		"""
		Get product_name.

		:returns: string
		"""

		return self.get_field('product_name')

	def get_product_sku(self) -> str:
		"""
		Get product_sku.

		:returns: string
		"""

		return self.get_field('product_sku')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_offset(self) -> int:
		"""
		Get offset.

		:returns: int
		"""

		return self.get_field('offset', 0)


"""
ProductVariantDimension data model.
"""


class ProductVariantDimension(Model):
	def __init__(self, data: dict = None):
		"""
		ProductVariantDimension Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def get_option_code(self) -> str:
		"""
		Get option_code.

		:returns: string
		"""

		return self.get_field('option_code')


"""
OrderItemSubscription data model.
"""


class OrderItemSubscription(Model):
	def __init__(self, data: dict = None):
		"""
		OrderItemSubscription Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('productsubscriptionterm'):
			value = self.get_field('productsubscriptionterm')
			if isinstance(value, dict):
				if not isinstance(value, ProductSubscriptionTerm):
					self.set_field('productsubscriptionterm', ProductSubscriptionTerm(value))
			else:
				raise Exception('Expected ProductSubscriptionTerm or a dict')

		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, SubscriptionOption):
							value[i] = SubscriptionOption(e)
					else:
						raise Exception('Expected list of SubscriptionOption or dict')
			else:
				raise Exception('Expected list of SubscriptionOption or dict')

	def get_method(self) -> str:
		"""
		Get method.

		:returns: string
		"""

		return self.get_field('method')

	def get_product_subscription_term(self):
		"""
		Get productsubscriptionterm.

		:returns: ProductSubscriptionTerm|None
		"""

		return self.get_field('productsubscriptionterm', None)

	def get_options(self):
		"""
		Get options.

		:returns: List of SubscriptionOption
		"""

		return self.get_field('options', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'productsubscriptionterm' in ret and isinstance(ret['productsubscriptionterm'], ProductSubscriptionTerm):
			ret['productsubscriptionterm'] = ret['productsubscriptionterm'].to_dict()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, SubscriptionOption):
					ret['options'][i] = ret['options'][i].to_dict()

		return ret


"""
SubscriptionOption data model.
"""


class SubscriptionOption(Model):
	def __init__(self, data: dict = None):
		"""
		SubscriptionOption Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_subscription_id(self) -> int:
		"""
		Get subscrp_id.

		:returns: int
		"""

		return self.get_field('subscrp_id', 0)

	def get_template_code(self) -> str:
		"""
		Get templ_code.

		:returns: string
		"""

		return self.get_field('templ_code')

	def get_attribute_code(self) -> str:
		"""
		Get attr_code.

		:returns: string
		"""

		return self.get_field('attr_code')

	def get_value(self) -> str:
		"""
		Get value.

		:returns: string
		"""

		return self.get_field('value')


"""
ProductInventoryAdjustment data model.
"""


class ProductInventoryAdjustment(Model):
	def __init__(self, data: dict = None):
		"""
		ProductInventoryAdjustment Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_product_code(self) -> str:
		"""
		Get product_code.

		:returns: string
		"""

		return self.get_field('product_code')

	def get_product_sku(self) -> str:
		"""
		Get product_sku.

		:returns: string
		"""

		return self.get_field('product_sku')

	def get_adjustment(self) -> float:
		"""
		Get adjustment.

		:returns: float
		"""

		return self.get_field('adjustment', 0.00)

	def set_product_id(self, product_id: int) -> 'ProductInventoryAdjustment':
		"""
		Set product_id.

		:param product_id: int
		:returns: ProductInventoryAdjustment
		"""

		return self.set_field('product_id', product_id)

	def set_product_code(self, product_code: str) -> 'ProductInventoryAdjustment':
		"""
		Set product_code.

		:param product_code: string
		:returns: ProductInventoryAdjustment
		"""

		return self.set_field('product_code', product_code)

	def set_product_sku(self, product_sku: str) -> 'ProductInventoryAdjustment':
		"""
		Set product_sku.

		:param product_sku: string
		:returns: ProductInventoryAdjustment
		"""

		return self.set_field('product_sku', product_sku)

	def set_adjustment(self, adjustment: float) -> 'ProductInventoryAdjustment':
		"""
		Set adjustment.

		:param adjustment: int
		:returns: ProductInventoryAdjustment
		"""

		return self.set_field('adjustment', adjustment)


"""
OrderShipmentUpdate data model.
"""


class OrderShipmentUpdate(Model):
	def __init__(self, data: dict = None):
		"""
		OrderShipmentUpdate Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_shipment_id(self) -> int:
		"""
		Get shpmnt_id.

		:returns: int
		"""

		return self.get_field('shpmnt_id', 0)

	def get_mark_shipped(self) -> bool:
		"""
		Get mark_shipped.

		:returns: bool
		"""

		return self.get_field('mark_shipped', False)

	def get_tracking_number(self) -> str:
		"""
		Get tracknum.

		:returns: string
		"""

		return self.get_field('tracknum')

	def get_tracking_type(self) -> str:
		"""
		Get tracktype.

		:returns: string
		"""

		return self.get_field('tracktype')

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def set_shipment_id(self, shipment_id: int) -> 'OrderShipmentUpdate':
		"""
		Set shpmnt_id.

		:param shipment_id: int
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('shpmnt_id', shipment_id)

	def set_mark_shipped(self, mark_shipped: bool) -> 'OrderShipmentUpdate':
		"""
		Set mark_shipped.

		:param mark_shipped: bool
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('mark_shipped', mark_shipped)

	def set_tracking_number(self, tracking_number: str) -> 'OrderShipmentUpdate':
		"""
		Set tracknum.

		:param tracking_number: string
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('tracknum', tracking_number)

	def set_tracking_type(self, tracking_type: str) -> 'OrderShipmentUpdate':
		"""
		Set tracktype.

		:param tracking_type: string
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('tracktype', tracking_type)

	def set_cost(self, cost: float) -> 'OrderShipmentUpdate':
		"""
		Set cost.

		:param cost: int
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('cost', cost)


"""
ProductVariantLimit data model.
"""


class ProductVariantLimit(Model):
	def __init__(self, data: dict = None):
		"""
		ProductVariantLimit Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def set_attribute_id(self, attribute_id: int) -> 'ProductVariantLimit':
		"""
		Set attr_id.

		:param attribute_id: int
		:returns: ProductVariantLimit
		"""

		return self.set_field('attr_id', attribute_id)

	def set_attribute_template_id(self, attribute_template_id: int) -> 'ProductVariantLimit':
		"""
		Set attmpat_id.

		:param attribute_template_id: int
		:returns: ProductVariantLimit
		"""

		return self.set_field('attmpat_id', attribute_template_id)

	def set_option_id(self, option_id: int) -> 'ProductVariantLimit':
		"""
		Set option_id.

		:param option_id: int
		:returns: ProductVariantLimit
		"""

		return self.set_field('option_id', option_id)


"""
ProductVariantExclusion data model.
"""


class ProductVariantExclusion(Model):
	def __init__(self, data: dict = None):
		"""
		ProductVariantExclusion Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def set_attribute_id(self, attribute_id: int) -> 'ProductVariantExclusion':
		"""
		Set attr_id.

		:param attribute_id: int
		:returns: ProductVariantExclusion
		"""

		return self.set_field('attr_id', attribute_id)

	def set_attribute_template_id(self, attribute_template_id: int) -> 'ProductVariantExclusion':
		"""
		Set attmpat_id.

		:param attribute_template_id: int
		:returns: ProductVariantExclusion
		"""

		return self.set_field('attmpat_id', attribute_template_id)

	def set_option_id(self, option_id: int) -> 'ProductVariantExclusion':
		"""
		Set option_id.

		:param option_id: int
		:returns: ProductVariantExclusion
		"""

		return self.set_field('option_id', option_id)


"""
ProvisionMessage data model.
"""


class ProvisionMessage(Model):
	def __init__(self, data: dict = None):
		"""
		ProvisionMessage Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_date_time_stamp(self) -> str:
		"""
		Get dtstamp.

		:returns: string
		"""

		return self.get_field('dtstamp')

	def get_line_number(self) -> int:
		"""
		Get lineno.

		:returns: int
		"""

		return self.get_field('lineno', 0)

	def get_tag(self) -> str:
		"""
		Get tag.

		:returns: string
		"""

		return self.get_field('tag')

	def get_message(self) -> str:
		"""
		Get message.

		:returns: string
		"""

		return self.get_field('message')


"""
CustomerAddress data model.
"""


class CustomerAddress(Model):
	def __init__(self, data: dict = None):
		"""
		CustomerAddress Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_first_name(self) -> str:
		"""
		Get fname.

		:returns: string
		"""

		return self.get_field('fname')

	def get_last_name(self) -> str:
		"""
		Get lname.

		:returns: string
		"""

		return self.get_field('lname')

	def get_email(self) -> str:
		"""
		Get email.

		:returns: string
		"""

		return self.get_field('email')

	def get_company(self) -> str:
		"""
		Get comp.

		:returns: string
		"""

		return self.get_field('comp')

	def get_phone(self) -> str:
		"""
		Get phone.

		:returns: string
		"""

		return self.get_field('phone')

	def get_fax(self) -> str:
		"""
		Get fax.

		:returns: string
		"""

		return self.get_field('fax')

	def get_address1(self) -> str:
		"""
		Get addr1.

		:returns: string
		"""

		return self.get_field('addr1')

	def get_address2(self) -> str:
		"""
		Get addr2.

		:returns: string
		"""

		return self.get_field('addr2')

	def get_city(self) -> str:
		"""
		Get city.

		:returns: string
		"""

		return self.get_field('city')

	def get_state(self) -> str:
		"""
		Get state.

		:returns: string
		"""

		return self.get_field('state')

	def get_zip(self) -> str:
		"""
		Get zip.

		:returns: string
		"""

		return self.get_field('zip')

	def get_country(self) -> str:
		"""
		Get cntry.

		:returns: string
		"""

		return self.get_field('cntry')

	def get_residential(self) -> bool:
		"""
		Get resdntl.

		:returns: bool
		"""

		return self.get_field('resdntl', False)


"""
OrderTotal data model.
"""


class OrderTotal(Model):
	def __init__(self, data: dict = None):
		"""
		OrderTotal Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_formatted_total(self) -> str:
		"""
		Get formatted_total.

		:returns: string
		"""

		return self.get_field('formatted_total')


"""
OrderPaymentTotal data model.
"""


class OrderPaymentTotal(Model):
	def __init__(self, data: dict = None):
		"""
		OrderPaymentTotal Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_total_authorized(self) -> float:
		"""
		Get total_auth.

		:returns: float
		"""

		return self.get_field('total_auth', 0.00)

	def get_formatted_total_authorized(self) -> str:
		"""
		Get formatted_total_auth.

		:returns: string
		"""

		return self.get_field('formatted_total_auth')

	def get_total_captured(self) -> float:
		"""
		Get total_capt.

		:returns: float
		"""

		return self.get_field('total_capt', 0.00)

	def get_formatted_total_captured(self) -> str:
		"""
		Get formatted_total_capt.

		:returns: string
		"""

		return self.get_field('formatted_total_capt')

	def get_total_refunded(self) -> float:
		"""
		Get total_rfnd.

		:returns: float
		"""

		return self.get_field('total_rfnd', 0.00)

	def get_formatted_total_refunded(self) -> str:
		"""
		Get formatted_total_rfnd.

		:returns: string
		"""

		return self.get_field('formatted_total_rfnd')

	def get_net_captured(self) -> float:
		"""
		Get net_capt.

		:returns: float
		"""

		return self.get_field('net_capt', 0.00)

	def get_formatted_net_captured(self) -> str:
		"""
		Get formatted_net_capt.

		:returns: string
		"""

		return self.get_field('formatted_net_capt')


"""
PrintQueue data model.
"""


class PrintQueue(Model):
	def __init__(self, data: dict = None):
		"""
		PrintQueue Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')


"""
PrintQueueJob data model.
"""


class PrintQueueJob(Model):
	def __init__(self, data: dict = None):
		"""
		PrintQueueJob Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_queue_id(self) -> int:
		"""
		Get queue_id.

		:returns: int
		"""

		return self.get_field('queue_id', 0)

	def get_store_id(self) -> int:
		"""
		Get store_id.

		:returns: int
		"""

		return self.get_field('store_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_job_format(self) -> str:
		"""
		Get job_fmt.

		:returns: string
		"""

		return self.get_field('job_fmt')

	def get_job_data(self) -> str:
		"""
		Get job_data.

		:returns: string
		"""

		return self.get_field('job_data')

	def get_date_time_created(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_field('dt_created', 0)

	def get_print_queue_description(self) -> str:
		"""
		Get printqueue_descrip.

		:returns: string
		"""

		return self.get_field('printqueue_descrip')

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_store_code(self) -> str:
		"""
		Get store_code.

		:returns: string
		"""

		return self.get_field('store_code')

	def get_store_name(self) -> str:
		"""
		Get store_name.

		:returns: string
		"""

		return self.get_field('store_name')


"""
PaymentMethod data model.
"""


class PaymentMethod(Model):
	def __init__(self, data: dict = None):
		"""
		PaymentMethod Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('paymentcard'):
			value = self.get_field('paymentcard')
			if isinstance(value, dict):
				if not isinstance(value, CustomerPaymentCard):
					self.set_field('paymentcard', CustomerPaymentCard(value))
			else:
				raise Exception('Expected CustomerPaymentCard or a dict')

		if self.has_field('orderpaymentcard'):
			value = self.get_field('orderpaymentcard')
			if isinstance(value, dict):
				if not isinstance(value, OrderPaymentCard):
					self.set_field('orderpaymentcard', OrderPaymentCard(value))
			else:
				raise Exception('Expected OrderPaymentCard or a dict')

		if self.has_field('paymentcardtype'):
			value = self.get_field('paymentcardtype')
			if isinstance(value, dict):
				if not isinstance(value, PaymentCardType):
					self.set_field('paymentcardtype', PaymentCardType(value))
			else:
				raise Exception('Expected PaymentCardType or a dict')

	def get_module_id(self) -> int:
		"""
		Get module_id.

		:returns: int
		"""

		return self.get_field('module_id', 0)

	def get_module_api(self) -> float:
		"""
		Get module_api.

		:returns: float
		"""

		return self.get_field('module_api', 0.00)

	def get_method_code(self) -> str:
		"""
		Get method_code.

		:returns: string
		"""

		return self.get_field('method_code')

	def get_method_name(self) -> str:
		"""
		Get method_name.

		:returns: string
		"""

		return self.get_field('method_name')

	def get_mivapay(self) -> bool:
		"""
		Get mivapay.

		:returns: bool
		"""

		return self.get_field('mivapay', False)

	def get_payment_card(self):
		"""
		Get paymentcard.

		:returns: CustomerPaymentCard|None
		"""

		return self.get_field('paymentcard', None)

	def get_order_payment_card(self):
		"""
		Get orderpaymentcard.

		:returns: OrderPaymentCard|None
		"""

		return self.get_field('orderpaymentcard', None)

	def get_payment_card_type(self):
		"""
		Get paymentcardtype.

		:returns: PaymentCardType|None
		"""

		return self.get_field('paymentcardtype', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'paymentcard' in ret and isinstance(ret['paymentcard'], CustomerPaymentCard):
			ret['paymentcard'] = ret['paymentcard'].to_dict()

		if 'orderpaymentcard' in ret and isinstance(ret['orderpaymentcard'], OrderPaymentCard):
			ret['orderpaymentcard'] = ret['orderpaymentcard'].to_dict()

		if 'paymentcardtype' in ret and isinstance(ret['paymentcardtype'], PaymentCardType):
			ret['paymentcardtype'] = ret['paymentcardtype'].to_dict()

		return ret


"""
PaymentCardType data model.
"""


class PaymentCardType(Model):
	def __init__(self, data: dict = None):
		"""
		PaymentCardType Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_prefixes(self) -> str:
		"""
		Get prefixes.

		:returns: string
		"""

		return self.get_field('prefixes')

	def get_lengths(self) -> str:
		"""
		Get lengths.

		:returns: string
		"""

		return self.get_field('lengths')

	def get_cvv(self) -> bool:
		"""
		Get cvv.

		:returns: bool
		"""

		return self.get_field('cvv', False)


"""
OrderPaymentAuthorize data model.
"""


class OrderPaymentAuthorize(Model):
	def __init__(self, data: dict = None):
		"""
		OrderPaymentAuthorize Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_valid(self) -> bool:
		"""
		Get valid.

		:returns: bool
		"""

		return self.get_field('valid', False)

	def get_total_authorized(self) -> float:
		"""
		Get total_auth.

		:returns: float
		"""

		return self.get_field('total_auth', 0.00)

	def get_formatted_total_authorized(self) -> str:
		"""
		Get formatted_total_auth.

		:returns: string
		"""

		return self.get_field('formatted_total_auth')

	def get_total_captured(self) -> float:
		"""
		Get total_capt.

		:returns: float
		"""

		return self.get_field('total_capt', 0.00)

	def get_formatted_total_captured(self) -> str:
		"""
		Get formatted_total_capt.

		:returns: string
		"""

		return self.get_field('formatted_total_capt')

	def get_total_refunded(self) -> float:
		"""
		Get total_rfnd.

		:returns: float
		"""

		return self.get_field('total_rfnd', 0.00)

	def get_formatted_total_refunded(self) -> str:
		"""
		Get formatted_total_rfnd.

		:returns: string
		"""

		return self.get_field('formatted_total_rfnd')

	def get_net_captured(self) -> float:
		"""
		Get net_capt.

		:returns: float
		"""

		return self.get_field('net_capt', 0.00)

	def get_formatted_net_captured(self) -> str:
		"""
		Get formatted_net_capt.

		:returns: string
		"""

		return self.get_field('formatted_net_capt')


"""
Branch data model.
"""


class Branch(Model):
	def __init__(self, data: dict = None):
		"""
		Branch Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_immutable(self) -> bool:
		"""
		Get immutable.

		:returns: bool
		"""

		return self.get_field('immutable', False)

	def get_branch_key(self) -> str:
		"""
		Get branchkey.

		:returns: string
		"""

		return self.get_field('branchkey')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_color(self) -> str:
		"""
		Get color.

		:returns: string
		"""

		return self.get_field('color')

	def get_framework(self) -> str:
		"""
		Get framework.

		:returns: string
		"""

		return self.get_field('framework')

	def get_is_primary(self) -> bool:
		"""
		Get is_primary.

		:returns: bool
		"""

		return self.get_field('is_primary', False)

	def get_is_working(self) -> bool:
		"""
		Get is_working.

		:returns: bool
		"""

		return self.get_field('is_working', False)

	def get_preview_url(self) -> str:
		"""
		Get preview_url.

		:returns: string
		"""

		return self.get_field('preview_url')


"""
BranchTemplateVersion data model.
"""


class BranchTemplateVersion(Model):
	def __init__(self, data: dict = None):
		"""
		BranchTemplateVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('settings'):
			value = self.get_field('settings')
			if not isinstance(value, TemplateVersionSettings):
				self.set_field('settings', TemplateVersionSettings(value))

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_parent_id(self) -> int:
		"""
		Get parent_id.

		:returns: int
		"""

		return self.get_field('parent_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_user_icon(self) -> str:
		"""
		Get user_icon.

		:returns: string
		"""

		return self.get_field('user_icon')

	def get_item_id(self) -> int:
		"""
		Get item_id.

		:returns: int
		"""

		return self.get_field('item_id', 0)

	def get_property_id(self) -> int:
		"""
		Get prop_id.

		:returns: int
		"""

		return self.get_field('prop_id', 0)

	def get_sync(self) -> bool:
		"""
		Get sync.

		:returns: bool
		"""

		return self.get_field('sync', False)

	def get_filename(self) -> str:
		"""
		Get filename.

		:returns: string
		"""

		return self.get_field('filename')

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_field('dtstamp', 0)

	def get_notes(self) -> str:
		"""
		Get notes.

		:returns: string
		"""

		return self.get_field('notes')

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_settings(self):
		"""
		Get settings.

		:returns: TemplateVersionSettings|None
		"""

		return self.get_field('settings', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'settings' in ret and isinstance(ret['settings'], TemplateVersionSettings):
			ret['settings'] = ret['settings'].to_dict()

		return ret


"""
TemplateVersionSettings data model.
"""


class TemplateVersionSettings(Model):
	def __init__(self, data: dict = None):
		"""
		TemplateVersionSettings Constructor

		:param data: dict
		"""

		self.data = data
	
	def is_scalar(self) -> bool:
		"""
		Check if the underlying data is a scalar value

		:returns: bool
		"""

		return not isinstance(self.data, dict) and not isinstance(self.data, list)

	def is_list(self) -> bool:
		"""
		Check if the underlying data is a list

		:returns: bool
		"""

		return isinstance(self.data, list)

	def is_dict(self) -> bool:
		"""
		Check if the underlying data is a dictionary

		:returns: bool
		"""

		return isinstance(self.data, dict)

	def has_item(self, item: str) -> bool:
		"""
		Check if an item exists in the dictionary

		:param item: {string}
		:returns: bool
		"""

		return self.is_dict() and item in self.data;
	
	def item_has_property(self, item: str, item_property: str) -> bool:
		"""
		Check if an item has a property

		:param item: {string}
		:param item_property: {string}
		:returns: bool
		"""
		
		if not self.is_dict() or not self.has_item(item):
			return False

		return item_property in self.data[item];

	def get_item(self, item: str):
		"""
		Get a items dictionary.

		:param item: str
		:returns: dict
		"""

		return self.data[item] if self.is_dict() and self.has_item(item) else None

	def get_item_property(self, item: str, item_property: str):
		"""
		Get a items dictionary.

		:param item: str
		:param item_property: str
		:returns: dict
		"""

		return self.data[item][item_property] if self.is_dict() and self.item_has_property(item, item_property) else None

	def get_data(self):
		"""
		Get the underlying data

		:returns: mixed
		"""

		return self.data

	def to_dict(self):
		"""
		Reduce the model to a dict.
		"""

		return self.data


	def set_item(self, item: str, value: dict) -> 'TemplateVersionSettings':
		"""
		Set a item settings dictionary

		:param item: str
		:param value: dict
		:returns: TemplateVersionSettings
		"""

		self[item] = value		
		return self

	def set_item_property(self, item: str, item_property: str, value) -> 'TemplateVersionSettings':
		"""
		Set a item property value for a specific item

		:param item: str
		:param item_property: str
		:param value: mixed
		:returns: TemplateVersionSettings
		"""

		if not self.has_item(item):
			self[item] = {}

		self[item][item_property] = value


"""
Changeset data model.
"""


class Changeset(Model):
	def __init__(self, data: dict = None):
		"""
		Changeset Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_branch_id(self) -> int:
		"""
		Get branch_id.

		:returns: int
		"""

		return self.get_field('branch_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_field('dtstamp', 0)

	def get_notes(self) -> str:
		"""
		Get notes.

		:returns: string
		"""

		return self.get_field('notes')

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_user_icon(self) -> str:
		"""
		Get user_icon.

		:returns: string
		"""

		return self.get_field('user_icon')

	def get_tags(self) -> dict:
		"""
		Get tags.

		:returns: dict
		"""

		return self.get_field('tags', {})

	def get_formatted_tags(self) -> str:
		"""
		Get formatted_tags.

		:returns: string
		"""

		return self.get_field('formatted_tags')


"""
TemplateChange data model.
"""


class TemplateChange(Model):
	def __init__(self, data: dict = None):
		"""
		TemplateChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Settings'):
			value = self.get_field('Settings')
			if not isinstance(value, TemplateVersionSettings):
				self.set_field('Settings', TemplateVersionSettings(value))

	def get_template_id(self) -> int:
		"""
		Get Template_ID.

		:returns: int
		"""

		return self.get_field('Template_ID', 0)

	def get_template_filename(self) -> str:
		"""
		Get Template_Filename.

		:returns: string
		"""

		return self.get_field('Template_Filename')

	def get_source(self) -> str:
		"""
		Get Source.

		:returns: string
		"""

		return self.get_field('Source')

	def get_settings(self):
		"""
		Get Settings.

		:returns: TemplateVersionSettings|None
		"""

		return self.get_field('Settings', None)

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: string
		"""

		return self.get_field('Notes')

	def set_template_id(self, template_id: int) -> 'TemplateChange':
		"""
		Set Template_ID.

		:param template_id: int
		:returns: TemplateChange
		"""

		return self.set_field('Template_ID', template_id)

	def set_template_filename(self, template_filename: str) -> 'TemplateChange':
		"""
		Set Template_Filename.

		:param template_filename: string
		:returns: TemplateChange
		"""

		return self.set_field('Template_Filename', template_filename)

	def set_source(self, source: str) -> 'TemplateChange':
		"""
		Set Source.

		:param source: string
		:returns: TemplateChange
		"""

		return self.set_field('Source', source)

	def set_settings(self, settings) -> 'TemplateChange':
		"""
		Set Settings.

		:param settings: TemplateVersionSettings|dict
		:returns: TemplateChange
		:raises Exception:
		"""

		if settings is None or isinstance(settings, TemplateVersionSettings):
			return self.set_field('Settings', settings)
		return self.set_field('Settings', TemplateVersionSettings(settings))

	def set_notes(self, notes: str) -> 'TemplateChange':
		"""
		Set Notes.

		:param notes: string
		:returns: TemplateChange
		"""

		return self.set_field('Notes', notes)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Settings' in ret and isinstance(ret['Settings'], TemplateVersionSettings):
			ret['Settings'] = ret['Settings'].to_dict()

		return ret


"""
ResourceGroupChange data model.
"""


class ResourceGroupChange(Model):
	def __init__(self, data: dict = None):
		"""
		ResourceGroupChange Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_resource_group_id(self) -> int:
		"""
		Get ResourceGroup_ID.

		:returns: int
		"""

		return self.get_field('ResourceGroup_ID', 0)

	def get_resource_group_code(self) -> str:
		"""
		Get ResourceGroup_Code.

		:returns: string
		"""

		return self.get_field('ResourceGroup_Code')

	def get_linked_css_resources(self) -> dict:
		"""
		Get LinkedCSSResources.

		:returns: dict
		"""

		return self.get_field('LinkedCSSResources', {})

	def get_linked_java_script_resources(self) -> dict:
		"""
		Get LinkedJavaScriptResources.

		:returns: dict
		"""

		return self.get_field('LinkedJavaScriptResources', {})

	def set_resource_group_id(self, resource_group_id: int) -> 'ResourceGroupChange':
		"""
		Set ResourceGroup_ID.

		:param resource_group_id: int
		:returns: ResourceGroupChange
		"""

		return self.set_field('ResourceGroup_ID', resource_group_id)

	def set_resource_group_code(self, resource_group_code: str) -> 'ResourceGroupChange':
		"""
		Set ResourceGroup_Code.

		:param resource_group_code: string
		:returns: ResourceGroupChange
		"""

		return self.set_field('ResourceGroup_Code', resource_group_code)

	def set_linked_css_resources(self, linked_css_resources) -> 'ResourceGroupChange':
		"""
		Set LinkedCSSResources.

		:param linked_css_resources: list
		:returns: ResourceGroupChange
		"""

		return self.set_field('LinkedCSSResources', linked_css_resources)

	def set_linked_java_script_resources(self, linked_java_script_resources) -> 'ResourceGroupChange':
		"""
		Set LinkedJavaScriptResources.

		:param linked_java_script_resources: list
		:returns: ResourceGroupChange
		"""

		return self.set_field('LinkedJavaScriptResources', linked_java_script_resources)


"""
CSSResourceChange data model.
"""


class CSSResourceChange(Model):
	def __init__(self, data: dict = None):
		"""
		CSSResourceChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Attributes'):
			value = self.get_field('Attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResourceVersionAttribute):
							value[i] = CSSResourceVersionAttribute(e)
					else:
						raise Exception('Expected list of CSSResourceVersionAttribute or dict')
			else:
				raise Exception('Expected list of CSSResourceVersionAttribute or dict')

	def get_css_resource_id(self) -> int:
		"""
		Get CSSResource_ID.

		:returns: int
		"""

		return self.get_field('CSSResource_ID', 0)

	def get_css_resource_code(self) -> str:
		"""
		Get CSSResource_Code.

		:returns: string
		"""

		return self.get_field('CSSResource_Code')

	def get_type(self) -> str:
		"""
		Get Type.

		:returns: string
		"""

		return self.get_field('Type')

	def get_is_global(self) -> bool:
		"""
		Get Global.

		:returns: bool
		"""

		return self.get_field('Global', False)

	def get_active(self) -> bool:
		"""
		Get Active.

		:returns: bool
		"""

		return self.get_field('Active', False)

	def get_file_path(self) -> str:
		"""
		Get File_Path.

		:returns: string
		"""

		return self.get_field('File_Path')

	def get_branchless_file_path(self) -> str:
		"""
		Get Branchless_File_Path.

		:returns: string
		"""

		return self.get_field('Branchless_File_Path')

	def get_source(self) -> str:
		"""
		Get Source.

		:returns: string
		"""

		return self.get_field('Source')

	def get_linked_pages(self) -> dict:
		"""
		Get LinkedPages.

		:returns: dict
		"""

		return self.get_field('LinkedPages', {})

	def get_linked_resources(self) -> dict:
		"""
		Get LinkedResources.

		:returns: dict
		"""

		return self.get_field('LinkedResources', {})

	def get_attributes(self):
		"""
		Get Attributes.

		:returns: List of CSSResourceVersionAttribute
		"""

		return self.get_field('Attributes', [])

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: string
		"""

		return self.get_field('Notes')

	def set_css_resource_id(self, css_resource_id: int) -> 'CSSResourceChange':
		"""
		Set CSSResource_ID.

		:param css_resource_id: int
		:returns: CSSResourceChange
		"""

		return self.set_field('CSSResource_ID', css_resource_id)

	def set_css_resource_code(self, css_resource_code: str) -> 'CSSResourceChange':
		"""
		Set CSSResource_Code.

		:param css_resource_code: string
		:returns: CSSResourceChange
		"""

		return self.set_field('CSSResource_Code', css_resource_code)

	def set_type(self, type: str) -> 'CSSResourceChange':
		"""
		Set Type.

		:param type: string
		:returns: CSSResourceChange
		"""

		return self.set_field('Type', type)

	def set_is_global(self, is_global: bool) -> 'CSSResourceChange':
		"""
		Set Global.

		:param is_global: bool
		:returns: CSSResourceChange
		"""

		return self.set_field('Global', is_global)

	def set_active(self, active: bool) -> 'CSSResourceChange':
		"""
		Set Active.

		:param active: bool
		:returns: CSSResourceChange
		"""

		return self.set_field('Active', active)

	def set_file_path(self, file_path: str) -> 'CSSResourceChange':
		"""
		Set File_Path.

		:param file_path: string
		:returns: CSSResourceChange
		"""

		return self.set_field('File_Path', file_path)

	def set_branchless_file_path(self, branchless_file_path: str) -> 'CSSResourceChange':
		"""
		Set Branchless_File_Path.

		:param branchless_file_path: string
		:returns: CSSResourceChange
		"""

		return self.set_field('Branchless_File_Path', branchless_file_path)

	def set_source(self, source: str) -> 'CSSResourceChange':
		"""
		Set Source.

		:param source: string
		:returns: CSSResourceChange
		"""

		return self.set_field('Source', source)

	def set_linked_pages(self, linked_pages) -> 'CSSResourceChange':
		"""
		Set LinkedPages.

		:param linked_pages: list
		:returns: CSSResourceChange
		"""

		return self.set_field('LinkedPages', linked_pages)

	def set_linked_resources(self, linked_resources) -> 'CSSResourceChange':
		"""
		Set LinkedResources.

		:param linked_resources: list
		:returns: CSSResourceChange
		"""

		return self.set_field('LinkedResources', linked_resources)

	def set_attributes(self, attributes: list) -> 'CSSResourceChange':
		"""
		Set Attributes.

		:param attributes: List of CSSResourceVersionAttribute 
		:raises Exception:
		:returns: CSSResourceChange
		"""

		for i, e in enumerate(attributes, 0):
			if isinstance(e, CSSResourceVersionAttribute):
				continue
			elif isinstance(e, dict):
				attributes[i] = CSSResourceVersionAttribute(e)
			else:
				raise Exception('Expected instance of CSSResourceVersionAttribute or dict')
		return self.set_field('Attributes', attributes)

	def set_notes(self, notes: str) -> 'CSSResourceChange':
		"""
		Set Notes.

		:param notes: string
		:returns: CSSResourceChange
		"""

		return self.set_field('Notes', notes)
	
	def add_attribute(self, attribute: 'CSSResourceVersionAttribute') -> 'CSSResourceChange':
		"""
		Add a CSSResourceVersionAttribute.
		
		:param attribute: CSSResourceVersionAttribute
		:returns: CSSResourceChange
		"""

		if 'Attributes' not in self:
			self['Attributes'] = []
		self['Attributes'].append(attribute)
		return self

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Attributes' in ret and isinstance(ret['Attributes'], list):
			for i, e in enumerate(ret['Attributes']):
				if isinstance(e, CSSResourceVersionAttribute):
					ret['Attributes'][i] = ret['Attributes'][i].to_dict()

		return ret


"""
JavaScriptResourceChange data model.
"""


class JavaScriptResourceChange(Model):
	def __init__(self, data: dict = None):
		"""
		JavaScriptResourceChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Attributes'):
			value = self.get_field('Attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, JavaScriptResourceVersionAttribute):
							value[i] = JavaScriptResourceVersionAttribute(e)
					else:
						raise Exception('Expected list of JavaScriptResourceVersionAttribute or dict')
			else:
				raise Exception('Expected list of JavaScriptResourceVersionAttribute or dict')

	def get_java_script_resource_id(self) -> int:
		"""
		Get JavaScriptResource_ID.

		:returns: int
		"""

		return self.get_field('JavaScriptResource_ID', 0)

	def get_java_script_resource_code(self) -> str:
		"""
		Get JavaScriptResource_Code.

		:returns: string
		"""

		return self.get_field('JavaScriptResource_Code')

	def get_type(self) -> str:
		"""
		Get Type.

		:returns: string
		"""

		return self.get_field('Type')

	def get_is_global(self) -> bool:
		"""
		Get Global.

		:returns: bool
		"""

		return self.get_field('Global', False)

	def get_active(self) -> bool:
		"""
		Get Active.

		:returns: bool
		"""

		return self.get_field('Active', False)

	def get_file_path(self) -> str:
		"""
		Get File_Path.

		:returns: string
		"""

		return self.get_field('File_Path')

	def get_branchless_file_path(self) -> str:
		"""
		Get Branchless_File_Path.

		:returns: string
		"""

		return self.get_field('Branchless_File_Path')

	def get_source(self) -> str:
		"""
		Get Source.

		:returns: string
		"""

		return self.get_field('Source')

	def get_linked_pages(self) -> dict:
		"""
		Get LinkedPages.

		:returns: dict
		"""

		return self.get_field('LinkedPages', {})

	def get_linked_resources(self) -> dict:
		"""
		Get LinkedResources.

		:returns: dict
		"""

		return self.get_field('LinkedResources', {})

	def get_attributes(self):
		"""
		Get Attributes.

		:returns: List of JavaScriptResourceVersionAttribute
		"""

		return self.get_field('Attributes', [])

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: string
		"""

		return self.get_field('Notes')

	def set_java_script_resource_id(self, java_script_resource_id: int) -> 'JavaScriptResourceChange':
		"""
		Set JavaScriptResource_ID.

		:param java_script_resource_id: int
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('JavaScriptResource_ID', java_script_resource_id)

	def set_java_script_resource_code(self, java_script_resource_code: str) -> 'JavaScriptResourceChange':
		"""
		Set JavaScriptResource_Code.

		:param java_script_resource_code: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('JavaScriptResource_Code', java_script_resource_code)

	def set_type(self, type: str) -> 'JavaScriptResourceChange':
		"""
		Set Type.

		:param type: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Type', type)

	def set_is_global(self, is_global: bool) -> 'JavaScriptResourceChange':
		"""
		Set Global.

		:param is_global: bool
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Global', is_global)

	def set_active(self, active: bool) -> 'JavaScriptResourceChange':
		"""
		Set Active.

		:param active: bool
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Active', active)

	def set_file_path(self, file_path: str) -> 'JavaScriptResourceChange':
		"""
		Set File_Path.

		:param file_path: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('File_Path', file_path)

	def set_branchless_file_path(self, branchless_file_path: str) -> 'JavaScriptResourceChange':
		"""
		Set Branchless_File_Path.

		:param branchless_file_path: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Branchless_File_Path', branchless_file_path)

	def set_source(self, source: str) -> 'JavaScriptResourceChange':
		"""
		Set Source.

		:param source: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Source', source)

	def set_linked_pages(self, linked_pages) -> 'JavaScriptResourceChange':
		"""
		Set LinkedPages.

		:param linked_pages: list
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('LinkedPages', linked_pages)

	def set_linked_resources(self, linked_resources) -> 'JavaScriptResourceChange':
		"""
		Set LinkedResources.

		:param linked_resources: list
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('LinkedResources', linked_resources)

	def set_attributes(self, attributes: list) -> 'JavaScriptResourceChange':
		"""
		Set Attributes.

		:param attributes: List of JavaScriptResourceVersionAttribute 
		:raises Exception:
		:returns: JavaScriptResourceChange
		"""

		for i, e in enumerate(attributes, 0):
			if isinstance(e, JavaScriptResourceVersionAttribute):
				continue
			elif isinstance(e, dict):
				attributes[i] = JavaScriptResourceVersionAttribute(e)
			else:
				raise Exception('Expected instance of JavaScriptResourceVersionAttribute or dict')
		return self.set_field('Attributes', attributes)

	def set_notes(self, notes: str) -> 'JavaScriptResourceChange':
		"""
		Set Notes.

		:param notes: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Notes', notes)
	
	def add_attribute(self, attribute: 'JavaScriptResourceVersionAttribute') -> 'JavaScriptResourceChange':
		"""
		Add a JavaScriptResourceVersionAttribute.
		
		:param attribute: JavaScriptResourceVersionAttribute
		:returns: JavaScriptResourceChange
		"""

		if 'Attributes' not in self:
			self['Attributes'] = []
		self['Attributes'].append(attribute)
		return self

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Attributes' in ret and isinstance(ret['Attributes'], list):
			for i, e in enumerate(ret['Attributes']):
				if isinstance(e, JavaScriptResourceVersionAttribute):
					ret['Attributes'][i] = ret['Attributes'][i].to_dict()

		return ret


"""
ChangesetChange data model.
"""


class ChangesetChange(Model):
	def __init__(self, data: dict = None):
		"""
		ChangesetChange Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_item_type(self) -> str:
		"""
		Get item_type.

		:returns: string
		"""

		return self.get_field('item_type')

	def get_item_id(self) -> int:
		"""
		Get item_id.

		:returns: int
		"""

		return self.get_field('item_id', 0)

	def get_item_version_id(self) -> int:
		"""
		Get item_version_id.

		:returns: int
		"""

		return self.get_field('item_version_id', 0)

	def get_item_identifier(self) -> str:
		"""
		Get item_identifier.

		:returns: string
		"""

		return self.get_field('item_identifier')


"""
PropertyChange data model.
"""


class PropertyChange(Model):
	def __init__(self, data: dict = None):
		"""
		PropertyChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Settings'):
			value = self.get_field('Settings')
			if not isinstance(value, TemplateVersionSettings):
				self.set_field('Settings', TemplateVersionSettings(value))

	def get_property_id(self) -> int:
		"""
		Get Property_ID.

		:returns: int
		"""

		return self.get_field('Property_ID', 0)

	def get_property_type(self) -> str:
		"""
		Get Property_Type.

		:returns: string
		"""

		return self.get_field('Property_Type')

	def get_property_code(self) -> str:
		"""
		Get Property_Code.

		:returns: string
		"""

		return self.get_field('Property_Code')

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.get_field('Product_ID', 0)

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: string
		"""

		return self.get_field('Product_Code')

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: string
		"""

		return self.get_field('Edit_Product')

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.get_field('Category_ID', 0)

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: string
		"""

		return self.get_field('Category_Code')

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: string
		"""

		return self.get_field('Edit_Category')

	def get_source(self) -> str:
		"""
		Get Source.

		:returns: string
		"""

		return self.get_field('Source')

	def get_settings(self):
		"""
		Get Settings.

		:returns: TemplateVersionSettings|None
		"""

		return self.get_field('Settings', None)

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: string
		"""

		return self.get_field('Notes')

	def set_property_id(self, property_id: int) -> 'PropertyChange':
		"""
		Set Property_ID.

		:param property_id: int
		:returns: PropertyChange
		"""

		return self.set_field('Property_ID', property_id)

	def set_property_type(self, property_type: str) -> 'PropertyChange':
		"""
		Set Property_Type.

		:param property_type: string
		:returns: PropertyChange
		"""

		return self.set_field('Property_Type', property_type)

	def set_property_code(self, property_code: str) -> 'PropertyChange':
		"""
		Set Property_Code.

		:param property_code: string
		:returns: PropertyChange
		"""

		return self.set_field('Property_Code', property_code)

	def set_product_id(self, product_id: int) -> 'PropertyChange':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: PropertyChange
		"""

		return self.set_field('Product_ID', product_id)

	def set_product_code(self, product_code: str) -> 'PropertyChange':
		"""
		Set Product_Code.

		:param product_code: string
		:returns: PropertyChange
		"""

		return self.set_field('Product_Code', product_code)

	def set_edit_product(self, edit_product: str) -> 'PropertyChange':
		"""
		Set Edit_Product.

		:param edit_product: string
		:returns: PropertyChange
		"""

		return self.set_field('Edit_Product', edit_product)

	def set_category_id(self, category_id: int) -> 'PropertyChange':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: PropertyChange
		"""

		return self.set_field('Category_ID', category_id)

	def set_category_code(self, category_code: str) -> 'PropertyChange':
		"""
		Set Category_Code.

		:param category_code: string
		:returns: PropertyChange
		"""

		return self.set_field('Category_Code', category_code)

	def set_edit_category(self, edit_category: str) -> 'PropertyChange':
		"""
		Set Edit_Category.

		:param edit_category: string
		:returns: PropertyChange
		"""

		return self.set_field('Edit_Category', edit_category)

	def set_source(self, source: str) -> 'PropertyChange':
		"""
		Set Source.

		:param source: string
		:returns: PropertyChange
		"""

		return self.set_field('Source', source)

	def set_settings(self, settings) -> 'PropertyChange':
		"""
		Set Settings.

		:param settings: TemplateVersionSettings|dict
		:returns: PropertyChange
		:raises Exception:
		"""

		if settings is None or isinstance(settings, TemplateVersionSettings):
			return self.set_field('Settings', settings)
		return self.set_field('Settings', TemplateVersionSettings(settings))

	def set_notes(self, notes: str) -> 'PropertyChange':
		"""
		Set Notes.

		:param notes: string
		:returns: PropertyChange
		"""

		return self.set_field('Notes', notes)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Settings' in ret and isinstance(ret['Settings'], TemplateVersionSettings):
			ret['Settings'] = ret['Settings'].to_dict()

		return ret


"""
ChangesetTemplateVersion data model.
"""


class ChangesetTemplateVersion(Model):
	def __init__(self, data: dict = None):
		"""
		ChangesetTemplateVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('settings'):
			value = self.get_field('settings')
			if not isinstance(value, TemplateVersionSettings):
				self.set_field('settings', TemplateVersionSettings(value))

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_parent_id(self) -> int:
		"""
		Get parent_id.

		:returns: int
		"""

		return self.get_field('parent_id', 0)

	def get_item_id(self) -> int:
		"""
		Get item_id.

		:returns: int
		"""

		return self.get_field('item_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_user_icon(self) -> str:
		"""
		Get user_icon.

		:returns: string
		"""

		return self.get_field('user_icon')

	def get_property_id(self) -> int:
		"""
		Get prop_id.

		:returns: int
		"""

		return self.get_field('prop_id', 0)

	def get_sync(self) -> bool:
		"""
		Get sync.

		:returns: bool
		"""

		return self.get_field('sync', False)

	def get_filename(self) -> str:
		"""
		Get filename.

		:returns: string
		"""

		return self.get_field('filename')

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_field('dtstamp', 0)

	def get_notes(self) -> str:
		"""
		Get notes.

		:returns: string
		"""

		return self.get_field('notes')

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_settings(self):
		"""
		Get settings.

		:returns: TemplateVersionSettings|None
		"""

		return self.get_field('settings', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'settings' in ret and isinstance(ret['settings'], TemplateVersionSettings):
			ret['settings'] = ret['settings'].to_dict()

		return ret


"""
CSSResourceVersion data model.
"""


class CSSResourceVersion(Model):
	def __init__(self, data: dict = None):
		"""
		CSSResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResourceVersionAttribute):
							value[i] = CSSResourceVersionAttribute(e)
					else:
						raise Exception('Expected list of CSSResourceVersionAttribute or dict')
			else:
				raise Exception('Expected list of CSSResourceVersionAttribute or dict')

		if self.has_field('linkedpages'):
			value = self.get_field('linkedpages')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Page):
							value[i] = Page(e)
					else:
						raise Exception('Expected list of Page or dict')
			else:
				raise Exception('Expected list of Page or dict')

		if self.has_field('linkedresources'):
			value = self.get_field('linkedresources')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResource):
							value[i] = CSSResource(e)
					else:
						raise Exception('Expected list of CSSResource or dict')
			else:
				raise Exception('Expected list of CSSResource or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_resource_id(self) -> int:
		"""
		Get res_id.

		:returns: int
		"""

		return self.get_field('res_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_is_global(self) -> bool:
		"""
		Get is_global.

		:returns: bool
		"""

		return self.get_field('is_global', False)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_file(self) -> str:
		"""
		Get file.

		:returns: string
		"""

		return self.get_field('file')

	def get_branchless_file(self) -> str:
		"""
		Get branchless_file.

		:returns: string
		"""

		return self.get_field('branchless_file')

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_user_icon(self) -> str:
		"""
		Get user_icon.

		:returns: string
		"""

		return self.get_field('user_icon')

	def get_source_user_id(self) -> int:
		"""
		Get source_user_id.

		:returns: int
		"""

		return self.get_field('source_user_id', 0)

	def get_source_user_name(self) -> str:
		"""
		Get source_user_name.

		:returns: string
		"""

		return self.get_field('source_user_name')

	def get_source_user_icon(self) -> str:
		"""
		Get source_user_icon.

		:returns: string
		"""

		return self.get_field('source_user_icon')

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of CSSResourceVersionAttribute
		"""

		return self.get_field('attributes', [])

	def get_linked_pages(self):
		"""
		Get linkedpages.

		:returns: List of Page
		"""

		return self.get_field('linkedpages', [])

	def get_linked_resources(self):
		"""
		Get linkedresources.

		:returns: List of CSSResource
		"""

		return self.get_field('linkedresources', [])

	def get_source_notes(self) -> str:
		"""
		Get source_notes.

		:returns: string
		"""

		return self.get_field('source_notes')

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, CSSResourceVersionAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		if 'linkedpages' in ret and isinstance(ret['linkedpages'], list):
			for i, e in enumerate(ret['linkedpages']):
				if isinstance(e, Page):
					ret['linkedpages'][i] = ret['linkedpages'][i].to_dict()

		if 'linkedresources' in ret and isinstance(ret['linkedresources'], list):
			for i, e in enumerate(ret['linkedresources']):
				if isinstance(e, CSSResource):
					ret['linkedresources'][i] = ret['linkedresources'][i].to_dict()

		return ret


"""
CSSResource data model.
"""


class CSSResource(Model):
	def __init__(self, data: dict = None):
		"""
		CSSResource Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResourceAttribute):
							value[i] = CSSResourceAttribute(e)
					else:
						raise Exception('Expected list of CSSResourceAttribute or dict')
			else:
				raise Exception('Expected list of CSSResourceAttribute or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_is_global(self) -> bool:
		"""
		Get is_global.

		:returns: bool
		"""

		return self.get_field('is_global', False)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_file(self) -> int:
		"""
		Get file.

		:returns: int
		"""

		return self.get_field('file', 0)

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of CSSResourceAttribute
		"""

		return self.get_field('attributes', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, CSSResourceAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		return ret


"""
Page data model.
"""


class Page(Model):
	def __init__(self, data: dict = None):
		"""
		Page Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_secure(self) -> bool:
		"""
		Get secure.

		:returns: bool
		"""

		return self.get_field('secure', False)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_title(self) -> str:
		"""
		Get title.

		:returns: string
		"""

		return self.get_field('title')

	def get_ui_id(self) -> int:
		"""
		Get ui_id.

		:returns: int
		"""

		return self.get_field('ui_id', 0)


"""
JavaScriptResourceVersion data model.
"""


class JavaScriptResourceVersion(Model):
	def __init__(self, data: dict = None):
		"""
		JavaScriptResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, JavaScriptResourceVersionAttribute):
							value[i] = JavaScriptResourceVersionAttribute(e)
					else:
						raise Exception('Expected list of JavaScriptResourceVersionAttribute or dict')
			else:
				raise Exception('Expected list of JavaScriptResourceVersionAttribute or dict')

		if self.has_field('linkedpages'):
			value = self.get_field('linkedpages')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Page):
							value[i] = Page(e)
					else:
						raise Exception('Expected list of Page or dict')
			else:
				raise Exception('Expected list of Page or dict')

		if self.has_field('linkedresources'):
			value = self.get_field('linkedresources')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, JavaScriptResource):
							value[i] = JavaScriptResource(e)
					else:
						raise Exception('Expected list of JavaScriptResource or dict')
			else:
				raise Exception('Expected list of JavaScriptResource or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_resource_id(self) -> int:
		"""
		Get res_id.

		:returns: int
		"""

		return self.get_field('res_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_is_global(self) -> bool:
		"""
		Get is_global.

		:returns: bool
		"""

		return self.get_field('is_global', False)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_file(self) -> str:
		"""
		Get file.

		:returns: string
		"""

		return self.get_field('file')

	def get_branchless_file(self) -> str:
		"""
		Get branchless_file.

		:returns: string
		"""

		return self.get_field('branchless_file')

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_user_icon(self) -> str:
		"""
		Get user_icon.

		:returns: string
		"""

		return self.get_field('user_icon')

	def get_source_user_id(self) -> int:
		"""
		Get source_user_id.

		:returns: int
		"""

		return self.get_field('source_user_id', 0)

	def get_source_user_name(self) -> str:
		"""
		Get source_user_name.

		:returns: string
		"""

		return self.get_field('source_user_name')

	def get_source_user_icon(self) -> str:
		"""
		Get source_user_icon.

		:returns: string
		"""

		return self.get_field('source_user_icon')

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of JavaScriptResourceVersionAttribute
		"""

		return self.get_field('attributes', [])

	def get_linked_pages(self):
		"""
		Get linkedpages.

		:returns: List of Page
		"""

		return self.get_field('linkedpages', [])

	def get_linked_resources(self):
		"""
		Get linkedresources.

		:returns: List of JavaScriptResource
		"""

		return self.get_field('linkedresources', [])

	def get_source_notes(self) -> str:
		"""
		Get source_notes.

		:returns: string
		"""

		return self.get_field('source_notes')

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, JavaScriptResourceVersionAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		if 'linkedpages' in ret and isinstance(ret['linkedpages'], list):
			for i, e in enumerate(ret['linkedpages']):
				if isinstance(e, Page):
					ret['linkedpages'][i] = ret['linkedpages'][i].to_dict()

		if 'linkedresources' in ret and isinstance(ret['linkedresources'], list):
			for i, e in enumerate(ret['linkedresources']):
				if isinstance(e, JavaScriptResource):
					ret['linkedresources'][i] = ret['linkedresources'][i].to_dict()

		return ret


"""
JavaScriptResource data model.
"""


class JavaScriptResource(Model):
	def __init__(self, data: dict = None):
		"""
		JavaScriptResource Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, JavaScriptResourceAttribute):
							value[i] = JavaScriptResourceAttribute(e)
					else:
						raise Exception('Expected list of JavaScriptResourceAttribute or dict')
			else:
				raise Exception('Expected list of JavaScriptResourceAttribute or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_is_global(self) -> bool:
		"""
		Get is_global.

		:returns: bool
		"""

		return self.get_field('is_global', False)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_file(self) -> int:
		"""
		Get file.

		:returns: int
		"""

		return self.get_field('file', 0)

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of JavaScriptResourceAttribute
		"""

		return self.get_field('attributes', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, JavaScriptResourceAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		return ret


"""
ResourceAttribute data model.
"""


class ResourceAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		ResourceAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_value(self) -> str:
		"""
		Get value.

		:returns: string
		"""

		return self.get_field('value')

	def set_name(self, name: str) -> 'ResourceAttribute':
		"""
		Set name.

		:param name: string
		:returns: ResourceAttribute
		"""

		return self.set_field('name', name)

	def set_value(self, value: str) -> 'ResourceAttribute':
		"""
		Set value.

		:param value: string
		:returns: ResourceAttribute
		"""

		return self.set_field('value', value)


"""
CustomerCreditHistory data model.
"""


class CustomerCreditHistory(Model):
	def __init__(self, data: dict = None):
		"""
		CustomerCreditHistory Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_transaction_reference(self) -> str:
		"""
		Get txref.

		:returns: string
		"""

		return self.get_field('txref')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_amount(self) -> float:
		"""
		Get amount.

		:returns: float
		"""

		return self.get_field('amount', 0.00)

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_field('dtstamp', 0)

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')


"""
OrderReturn data model.
"""


class OrderReturn(Model):
	# ORDER_RETURN_STATUS constants.
	ORDER_RETURN_STATUS_ISSUED = 500
	ORDER_RETURN_STATUS_RECEIVED = 600

	def __init__(self, data: dict = None):
		"""
		OrderReturn Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_date_time_issued(self) -> int:
		"""
		Get dt_issued.

		:returns: int
		"""

		return self.get_field('dt_issued', 0)

	def get_date_time_received(self) -> int:
		"""
		Get dt_recvd.

		:returns: int
		"""

		return self.get_field('dt_recvd', 0)


"""
ReceivedReturn data model.
"""


class ReceivedReturn(Model):
	def __init__(self, data: dict = None):
		"""
		ReceivedReturn Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_return_id(self) -> int:
		"""
		Get return_id.

		:returns: int
		"""

		return self.get_field('return_id', 0)

	def get_adjust_inventory(self) -> int:
		"""
		Get adjust_inventory.

		:returns: int
		"""

		return self.get_field('adjust_inventory', 0)

	def set_return_id(self, return_id: int) -> 'ReceivedReturn':
		"""
		Set return_id.

		:param return_id: int
		:returns: ReceivedReturn
		"""

		return self.set_field('return_id', return_id)

	def set_adjust_inventory(self, adjust_inventory: int) -> 'ReceivedReturn':
		"""
		Set adjust_inventory.

		:param adjust_inventory: int
		:returns: ReceivedReturn
		"""

		return self.set_field('adjust_inventory', adjust_inventory)


"""
PropertyVersion data model.
"""


class PropertyVersion(Model):
	def __init__(self, data: dict = None):
		"""
		PropertyVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('settings'):
			value = self.get_field('settings')
			if not isinstance(value, TemplateVersionSettings):
				self.set_field('settings', TemplateVersionSettings(value))

		if self.has_field('product'):
			value = self.get_field('product')
			if isinstance(value, dict):
				if not isinstance(value, Product):
					self.set_field('product', Product(value))
			else:
				raise Exception('Expected Product or a dict')

		if self.has_field('category'):
			value = self.get_field('category')
			if isinstance(value, dict):
				if not isinstance(value, Category):
					self.set_field('category', Category(value))
			else:
				raise Exception('Expected Category or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_property_id(self) -> int:
		"""
		Get prop_id.

		:returns: int
		"""

		return self.get_field('prop_id', 0)

	def get_version_id(self) -> int:
		"""
		Get version_id.

		:returns: int
		"""

		return self.get_field('version_id', 0)

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_category_id(self) -> int:
		"""
		Get cat_id.

		:returns: int
		"""

		return self.get_field('cat_id', 0)

	def get_version_user_id(self) -> int:
		"""
		Get version_user_id.

		:returns: int
		"""

		return self.get_field('version_user_id', 0)

	def get_version_user_name(self) -> str:
		"""
		Get version_user_name.

		:returns: string
		"""

		return self.get_field('version_user_name')

	def get_version_user_icon(self) -> str:
		"""
		Get version_user_icon.

		:returns: string
		"""

		return self.get_field('version_user_icon')

	def get_source_user_id(self) -> int:
		"""
		Get source_user_id.

		:returns: int
		"""

		return self.get_field('source_user_id', 0)

	def get_source_user_name(self) -> str:
		"""
		Get source_user_name.

		:returns: string
		"""

		return self.get_field('source_user_name')

	def get_source_user_icon(self) -> str:
		"""
		Get source_user_icon.

		:returns: string
		"""

		return self.get_field('source_user_icon')

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_settings(self):
		"""
		Get settings.

		:returns: TemplateVersionSettings|None
		"""

		return self.get_field('settings', None)

	def get_product(self):
		"""
		Get product.

		:returns: Product|None
		"""

		return self.get_field('product', None)

	def get_category(self):
		"""
		Get category.

		:returns: Category|None
		"""

		return self.get_field('category', None)

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_sync(self) -> bool:
		"""
		Get sync.

		:returns: bool
		"""

		return self.get_field('sync', False)

	def get_source_notes(self) -> str:
		"""
		Get source_notes.

		:returns: string
		"""

		return self.get_field('source_notes')

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'settings' in ret and isinstance(ret['settings'], TemplateVersionSettings):
			ret['settings'] = ret['settings'].to_dict()

		if 'product' in ret and isinstance(ret['product'], Product):
			ret['product'] = ret['product'].to_dict()

		if 'category' in ret and isinstance(ret['category'], Category):
			ret['category'] = ret['category'].to_dict()

		return ret


"""
ResourceGroup data model.
"""


class ResourceGroup(Model):
	def __init__(self, data: dict = None):
		"""
		ResourceGroup Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('linkedcssresources'):
			value = self.get_field('linkedcssresources')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResource):
							value[i] = CSSResource(e)
					else:
						raise Exception('Expected list of CSSResource or dict')
			else:
				raise Exception('Expected list of CSSResource or dict')

		if self.has_field('linkedjavascriptresources'):
			value = self.get_field('linkedjavascriptresources')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, JavaScriptResource):
							value[i] = JavaScriptResource(e)
					else:
						raise Exception('Expected list of JavaScriptResource or dict')
			else:
				raise Exception('Expected list of JavaScriptResource or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_linked_css_resources(self):
		"""
		Get linkedcssresources.

		:returns: List of CSSResource
		"""

		return self.get_field('linkedcssresources', [])

	def get_linked_java_script_resources(self):
		"""
		Get linkedjavascriptresources.

		:returns: List of JavaScriptResource
		"""

		return self.get_field('linkedjavascriptresources', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'linkedcssresources' in ret and isinstance(ret['linkedcssresources'], list):
			for i, e in enumerate(ret['linkedcssresources']):
				if isinstance(e, CSSResource):
					ret['linkedcssresources'][i] = ret['linkedcssresources'][i].to_dict()

		if 'linkedjavascriptresources' in ret and isinstance(ret['linkedjavascriptresources'], list):
			for i, e in enumerate(ret['linkedjavascriptresources']):
				if isinstance(e, JavaScriptResource):
					ret['linkedjavascriptresources'][i] = ret['linkedjavascriptresources'][i].to_dict()

		return ret


"""
MerchantVersion data model.
"""


class MerchantVersion(Model):
	def __init__(self, data: dict = None):
		"""
		MerchantVersion Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_version(self) -> str:
		"""
		Get version.

		:returns: string
		"""

		return self.get_field('version')

	def get_major(self) -> int:
		"""
		Get major.

		:returns: int
		"""

		return self.get_field('major', 0)

	def get_minor(self) -> int:
		"""
		Get minor.

		:returns: int
		"""

		return self.get_field('minor', 0)

	def get_bugfix(self) -> int:
		"""
		Get bugfix.

		:returns: int
		"""

		return self.get_field('bugfix', 0)


"""
Store data model.
"""


class Store(Model):
	# CACHE_TYPE constants.
	CACHE_TYPE_NONE = ''
	CACHE_TYPE_REDIS = 'redis'

	def __init__(self, data: dict = None):
		"""
		Store Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_manager_id(self) -> int:
		"""
		Get manager_id.

		:returns: int
		"""

		return self.get_field('manager_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_license(self) -> str:
		"""
		Get license.

		:returns: string
		"""

		return self.get_field('license')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_owner(self) -> str:
		"""
		Get owner.

		:returns: string
		"""

		return self.get_field('owner')

	def get_email(self) -> str:
		"""
		Get email.

		:returns: string
		"""

		return self.get_field('email')

	def get_company(self) -> str:
		"""
		Get company.

		:returns: string
		"""

		return self.get_field('company')

	def get_address(self) -> str:
		"""
		Get address.

		:returns: string
		"""

		return self.get_field('address')

	def get_city(self) -> str:
		"""
		Get city.

		:returns: string
		"""

		return self.get_field('city')

	def get_state(self) -> str:
		"""
		Get state.

		:returns: string
		"""

		return self.get_field('state')

	def get_zip(self) -> str:
		"""
		Get zip.

		:returns: string
		"""

		return self.get_field('zip')

	def get_phone(self) -> str:
		"""
		Get phone.

		:returns: string
		"""

		return self.get_field('phone')

	def get_fax(self) -> str:
		"""
		Get fax.

		:returns: string
		"""

		return self.get_field('fax')

	def get_country(self) -> str:
		"""
		Get country.

		:returns: string
		"""

		return self.get_field('country')

	def get_weight_units(self) -> str:
		"""
		Get wtunits.

		:returns: string
		"""

		return self.get_field('wtunits')

	def get_weight_unit_code(self) -> str:
		"""
		Get wtunitcode.

		:returns: string
		"""

		return self.get_field('wtunitcode')

	def get_dimension_units(self) -> str:
		"""
		Get dmunitcode.

		:returns: string
		"""

		return self.get_field('dmunitcode')

	def get_basket_expiration(self) -> int:
		"""
		Get baskexp.

		:returns: int
		"""

		return self.get_field('baskexp', 0)

	def get_price_group_overlap_resolution(self) -> str:
		"""
		Get pgrp_ovlp.

		:returns: string
		"""

		return self.get_field('pgrp_ovlp')

	def get_user_interface_id(self) -> int:
		"""
		Get ui_id.

		:returns: int
		"""

		return self.get_field('ui_id', 0)

	def get_tax_id(self) -> int:
		"""
		Get tax_id.

		:returns: int
		"""

		return self.get_field('tax_id', 0)

	def get_currency_id(self) -> int:
		"""
		Get currncy_id.

		:returns: int
		"""

		return self.get_field('currncy_id', 0)

	def get_maintenance_warning_message(self) -> str:
		"""
		Get mnt_warn.

		:returns: string
		"""

		return self.get_field('mnt_warn')

	def get_maintenance_closed_message(self) -> str:
		"""
		Get mnt_close.

		:returns: string
		"""

		return self.get_field('mnt_close')

	def get_maintenance_time(self) -> int:
		"""
		Get mnt_time.

		:returns: int
		"""

		return self.get_field('mnt_time', 0)

	def get_maintenance_no_new_customers_before(self) -> int:
		"""
		Get mnt_no_new.

		:returns: int
		"""

		return self.get_field('mnt_no_new', 0)

	def get_order_minimum_quantity(self) -> int:
		"""
		Get omin_quant.

		:returns: int
		"""

		return self.get_field('omin_quant', 0)

	def get_order_minimum_price(self):
		"""
		Get omin_price.

		:returns: foat
		"""

		# Missing foat

	def get_order_minimum_required_all(self) -> bool:
		"""
		Get omin_all.

		:returns: bool
		"""

		return self.get_field('omin_all', False)

	def get_order_minimum_message(self) -> str:
		"""
		Get omin_msg.

		:returns: string
		"""

		return self.get_field('omin_msg')

	def get_crypt_id(self) -> int:
		"""
		Get crypt_id.

		:returns: int
		"""

		return self.get_field('crypt_id', 0)

	def get_require_shipping(self) -> bool:
		"""
		Get req_ship.

		:returns: bool
		"""

		return self.get_field('req_ship', False)

	def get_require_tax(self) -> bool:
		"""
		Get req_tax.

		:returns: bool
		"""

		return self.get_field('req_tax', False)

	def get_require_free_order_shipping(self) -> bool:
		"""
		Get req_frship.

		:returns: bool
		"""

		return self.get_field('req_frship', False)

	def get_item_module_uninstallable(self) -> bool:
		"""
		Get item_adel.

		:returns: bool
		"""

		return self.get_field('item_adel', False)

	def get_cache_type(self) -> str:
		"""
		Get cache_type.

		:returns: string
		"""

		return self.get_field('cache_type')

	def get_redis_host(self) -> str:
		"""
		Get redishost.

		:returns: string
		"""

		return self.get_field('redishost')

	def get_redis_port(self) -> int:
		"""
		Get redisport.

		:returns: int
		"""

		return self.get_field('redisport', 0)

	def get_redis_timeout(self) -> int:
		"""
		Get redisto.

		:returns: int
		"""

		return self.get_field('redisto', 0)

	def get_redis_expiration(self) -> int:
		"""
		Get redisex.

		:returns: int
		"""

		return self.get_field('redisex', 0)


"""
CustomerAddressList data model.
"""


class CustomerAddressList(Model):
	def __init__(self, data: dict = None):
		"""
		CustomerAddressList Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('addresses'):
			value = self.get_field('addresses')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CustomerAddress):
							value[i] = CustomerAddress(e)
					else:
						raise Exception('Expected list of CustomerAddress or dict')
			else:
				raise Exception('Expected list of CustomerAddress or dict')

	def get_ship_id(self) -> int:
		"""
		Get ship_id.

		:returns: int
		"""

		return self.get_field('ship_id', 0)

	def get_bill_id(self) -> int:
		"""
		Get bill_id.

		:returns: int
		"""

		return self.get_field('bill_id', 0)

	def get_addresses(self):
		"""
		Get addresses.

		:returns: List of CustomerAddress
		"""

		return self.get_field('addresses', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'addresses' in ret and isinstance(ret['addresses'], list):
			for i, e in enumerate(ret['addresses']):
				if isinstance(e, CustomerAddress):
					ret['addresses'][i] = ret['addresses'][i].to_dict()

		return ret


"""
VariantAttribute data model.
"""


class VariantAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		VariantAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def set_attribute_id(self, attribute_id: int) -> 'VariantAttribute':
		"""
		Set attr_id.

		:param attribute_id: int
		:returns: VariantAttribute
		"""

		return self.set_field('attr_id', attribute_id)

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'VariantAttribute':
		"""
		Set attmpat_id.

		:param attribute_template_attribute_id: int
		:returns: VariantAttribute
		"""

		return self.set_field('attmpat_id', attribute_template_attribute_id)

	def set_option_id(self, option_id: int) -> 'VariantAttribute':
		"""
		Set option_id.

		:param option_id: int
		:returns: VariantAttribute
		"""

		return self.set_field('option_id', option_id)


"""
VariantPart data model.
"""


class VariantPart(Model):
	def __init__(self, data: dict = None):
		"""
		VariantPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_part_id(self) -> int:
		"""
		Get part_id.

		:returns: int
		"""

		return self.get_field('part_id', 0)

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def set_part_id(self, part_id: int) -> 'VariantPart':
		"""
		Set part_id.

		:param part_id: int
		:returns: VariantPart
		"""

		return self.set_field('part_id', part_id)

	def set_quantity(self, quantity: int) -> 'VariantPart':
		"""
		Set quantity.

		:param quantity: int
		:returns: VariantPart
		"""

		return self.set_field('quantity', quantity)


"""
ImageType data model.
"""


class ImageType(Model):
	def __init__(self, data: dict = None):
		"""
		ImageType Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')


"""
PriceGroupExclusion data model.
"""


class PriceGroupExclusion(Model):
	# EXCLUSION_SCOPE constants.
	EXCLUSION_SCOPE_BASKET = 'basket'
	EXCLUSION_SCOPE_GROUP = 'group'
	EXCLUSION_SCOPE_ITEM = 'item'

	def __init__(self, data: dict = None):
		"""
		PriceGroupExclusion Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_scope(self) -> str:
		"""
		Get scope.

		:returns: string
		"""

		return self.get_field('scope')

	def set_id(self, id: int) -> 'PriceGroupExclusion':
		"""
		Set id.

		:param id: int
		:returns: PriceGroupExclusion
		"""

		return self.set_field('id', id)

	def set_scope(self, scope: str) -> 'PriceGroupExclusion':
		"""
		Set scope.

		:param scope: string
		:returns: PriceGroupExclusion
		"""

		return self.set_field('scope', scope)


"""
AttributeTemplate data model.
"""


class AttributeTemplate(Model):
	def __init__(self, data: dict = None):
		"""
		AttributeTemplate Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_refcount(self) -> int:
		"""
		Get refcount.

		:returns: int
		"""

		return self.get_field('refcount', 0)


"""
AttributeTemplateAttribute data model.
"""


class AttributeTemplateAttribute(Model):
	# TEMPLATE_ATTRIBUTE_TYPE constants.
	TEMPLATE_ATTRIBUTE_TYPE_CHECKBOX = 'checkbox'
	TEMPLATE_ATTRIBUTE_TYPE_RADIO = 'radio'
	TEMPLATE_ATTRIBUTE_TYPE_TEXT = 'text'
	TEMPLATE_ATTRIBUTE_TYPE_SELECT = 'select'
	TEMPLATE_ATTRIBUTE_TYPE_MEMO = 'memo'
	TEMPLATE_ATTRIBUTE_TYPE_TEMPLATE = 'template'
	TEMPLATE_ATTRIBUTE_TYPE_SWATCH_SELECT = 'swatch-select'

	def __init__(self, data: dict = None):
		"""
		AttributeTemplateAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, AttributeTemplateOption):
							value[i] = AttributeTemplateOption(e)
					else:
						raise Exception('Expected list of AttributeTemplateOption or dict')
			else:
				raise Exception('Expected list of AttributeTemplateOption or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_attribute_template_id(self) -> int:
		"""
		Get attemp_id.

		:returns: int
		"""

		return self.get_field('attemp_id', 0)

	def get_default_id(self) -> int:
		"""
		Get default_id.

		:returns: int
		"""

		return self.get_field('default_id', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		if self.has_field('disp_order'):
			return self.get_field('disp_order', 0)
		elif self.has_field('disporder'):
			return self.get_field('disporder', 0)

		return 0

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_required(self) -> bool:
		"""
		Get required.

		:returns: bool
		"""

		return self.get_field('required', False)

	def get_inventory(self) -> bool:
		"""
		Get inventory.

		:returns: bool
		"""

		return self.get_field('inventory', False)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_options(self):
		"""
		Get options.

		:returns: List of AttributeTemplateOption
		"""

		return self.get_field('options', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, AttributeTemplateOption):
					ret['options'][i] = ret['options'][i].to_dict()

		return ret


"""
AttributeTemplateOption data model.
"""


class AttributeTemplateOption(Model):
	def __init__(self, data: dict = None):
		"""
		AttributeTemplateOption Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_attribute_template_id(self):
		"""
		Get attemp_id.

		:returns: 
		"""

		# Missing 

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_display_order(self) -> int:
		"""
		Get disporder.

		:returns: int
		"""

		if self.has_field('disporder'):
			return self.get_field('disporder', 0)
		elif self.has_field('disp_order'):
			return self.get_field('disp_order', 0)

		return 0

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_formatted_price(self) -> str:
		"""
		Get formatted_price.

		:returns: string
		"""

		return self.get_field('formatted_price')

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')

	def get_default_opt(self) -> bool:
		"""
		Get default_opt.

		:returns: bool
		"""

		return self.get_field('default_opt', False)


"""
OrderPart data model.
"""


class OrderPart(Model):
	def __init__(self, data: dict = None):
		"""
		OrderPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_total_quantity(self) -> int:
		"""
		Get total_quantity.

		:returns: int
		"""

		return self.get_field('total_quantity', 0)

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)


"""
ProductAttributeListAttribute data model.
"""


class ProductAttributeListAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		ProductAttributeListAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductAttributeListAttribute):
							value[i] = ProductAttributeListAttribute(e)
					else:
						raise Exception('Expected list of ProductAttributeListAttribute or dict')
			else:
				raise Exception('Expected list of ProductAttributeListAttribute or dict')

		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductOption):
							value[i] = ProductOption(e)
					else:
						raise Exception('Expected list of ProductOption or dict')
			else:
				raise Exception('Expected list of ProductOption or dict')

		if self.has_field('template'):
			value = self.get_field('template')
			if isinstance(value, dict):
				if not isinstance(value, ProductAttributeListTemplate):
					self.set_field('template', ProductAttributeListTemplate(value))
			else:
				raise Exception('Expected ProductAttributeListTemplate or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_default_id(self) -> int:
		"""
		Get default_id.

		:returns: int
		"""

		return self.get_field('default_id', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		if self.has_field('disp_order'):
			return self.get_field('disp_order', 0)
		elif self.has_field('disporder'):
			return self.get_field('disporder', 0)

		return 0

	def get_attribute_template_id(self) -> int:
		"""
		Get attemp_id.

		:returns: int
		"""

		return self.get_field('attemp_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_required(self) -> bool:
		"""
		Get required.

		:returns: bool
		"""

		return self.get_field('required', False)

	def get_inventory(self) -> bool:
		"""
		Get inventory.

		:returns: bool
		"""

		return self.get_field('inventory', False)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_template_attributes(self):
		"""
		Get attributes.

		:returns: List of ProductAttributeListAttribute
		"""

		return self.get_field('attributes', [])

	def get_options(self):
		"""
		Get options.

		:returns: List of ProductOption
		"""

		return self.get_field('options', [])

	def get_has_variant_parts(self) -> bool:
		"""
		Get has_variant_parts.

		:returns: bool
		"""

		return self.get_field('has_variant_parts', False)

	def get_template(self):
		"""
		Get template.

		:returns: ProductAttributeListTemplate|None
		"""

		return self.get_field('template', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, ProductAttributeListAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, ProductOption):
					ret['options'][i] = ret['options'][i].to_dict()

		if 'template' in ret and isinstance(ret['template'], ProductAttributeListTemplate):
			ret['template'] = ret['template'].to_dict()

		return ret


"""
ProductAttributeListOption data model.
"""


class ProductAttributeListOption(Model):
	def __init__(self, data: dict = None):
		"""
		ProductAttributeListOption Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_id(self) -> int:
		"""
		Get attemp_id.

		:returns: int
		"""

		return self.get_field('attemp_id', 0)

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		if self.has_field('disp_order'):
			return self.get_field('disp_order', 0)
		elif self.has_field('disporder'):
			return self.get_field('disporder', 0)

		return 0

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_default_option(self) -> bool:
		"""
		Get default_opt.

		:returns: bool
		"""

		return self.get_field('default_opt', False)


"""
ProductAttributeListTemplate data model.
"""


class ProductAttributeListTemplate(Model):
	def __init__(self, data: dict = None):
		"""
		ProductAttributeListTemplate Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_reference_count(self) -> int:
		"""
		Get refcount.

		:returns: int
		"""

		return self.get_field('refcount', 0)


"""
AvailabilityGroupCustomer data model.
"""


class AvailabilityGroupCustomer(Customer):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroupCustomer Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
AvailabilityGroupCategory data model.
"""


class AvailabilityGroupCategory(Category):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroupCategory Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
AvailabilityGroupProduct data model.
"""


class AvailabilityGroupProduct(Product):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroupProduct Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
AvailabilityGroupBusinessAccount data model.
"""


class AvailabilityGroupBusinessAccount(BusinessAccount):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroupBusinessAccount Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
BusinessAccountCustomer data model.
"""


class BusinessAccountCustomer(Customer):
	def __init__(self, data: dict = None):
		"""
		BusinessAccountCustomer Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
OrderNote data model.
"""


class OrderNote(Note):
	def __init__(self, data: dict = None):
		"""
		OrderNote Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
CategoryProduct data model.
"""


class CategoryProduct(Product):
	def __init__(self, data: dict = None):
		"""
		CategoryProduct Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
AttributeTemplateProduct data model.
"""


class AttributeTemplateProduct(Product):
	def __init__(self, data: dict = None):
		"""
		AttributeTemplateProduct Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
CouponPriceGroup data model.
"""


class CouponPriceGroup(PriceGroup):
	def __init__(self, data: dict = None):
		"""
		CouponPriceGroup Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
CouponCustomer data model.
"""


class CouponCustomer(Customer):
	def __init__(self, data: dict = None):
		"""
		CouponCustomer Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
OrderPaymentCard data model.
"""


class OrderPaymentCard(CustomerPaymentCard):
	def __init__(self, data: dict = None):
		"""
		OrderPaymentCard Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
PriceGroupCustomer data model.
"""


class PriceGroupCustomer(Customer):
	def __init__(self, data: dict = None):
		"""
		PriceGroupCustomer Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
PriceGroupProduct data model.
"""


class PriceGroupProduct(Product):
	def __init__(self, data: dict = None):
		"""
		PriceGroupProduct Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
PriceGroupCategory data model.
"""


class PriceGroupCategory(Category):
	def __init__(self, data: dict = None):
		"""
		PriceGroupCategory Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
PriceGroupBusinessAccount data model.
"""


class PriceGroupBusinessAccount(BusinessAccount):
	def __init__(self, data: dict = None):
		"""
		PriceGroupBusinessAccount Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
CustomerPriceGroup data model.
"""


class CustomerPriceGroup(PriceGroup):
	def __init__(self, data: dict = None):
		"""
		CustomerPriceGroup Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
BranchCSSResourceVersion data model.
"""


class BranchCSSResourceVersion(CSSResourceVersion):
	def __init__(self, data: dict = None):
		"""
		BranchCSSResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
ChangesetCSSResourceVersion data model.
"""


class ChangesetCSSResourceVersion(CSSResourceVersion):
	def __init__(self, data: dict = None):
		"""
		ChangesetCSSResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
BranchCSSResource data model.
"""


class BranchCSSResource(CSSResource):
	def __init__(self, data: dict = None):
		"""
		BranchCSSResource Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
ChangesetCSSResource data model.
"""


class ChangesetCSSResource(CSSResource):
	def __init__(self, data: dict = None):
		"""
		ChangesetCSSResource Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
BranchJavaScriptResourceVersion data model.
"""


class BranchJavaScriptResourceVersion(JavaScriptResourceVersion):
	def __init__(self, data: dict = None):
		"""
		BranchJavaScriptResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
ChangesetJavaScriptResourceVersion data model.
"""


class ChangesetJavaScriptResourceVersion(JavaScriptResourceVersion):
	def __init__(self, data: dict = None):
		"""
		ChangesetJavaScriptResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
CSSResourceVersionAttribute data model.
"""


class CSSResourceVersionAttribute(ResourceAttribute):
	def __init__(self, data: dict = None):
		"""
		CSSResourceVersionAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
CSSResourceAttribute data model.
"""


class CSSResourceAttribute(ResourceAttribute):
	def __init__(self, data: dict = None):
		"""
		CSSResourceAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
JavaScriptResourceVersionAttribute data model.
"""


class JavaScriptResourceVersionAttribute(ResourceAttribute):
	def __init__(self, data: dict = None):
		"""
		JavaScriptResourceVersionAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
JavaScriptResourceAttribute data model.
"""


class JavaScriptResourceAttribute(ResourceAttribute):
	def __init__(self, data: dict = None):
		"""
		JavaScriptResourceAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
OrderPriceGroup data model.
"""


class OrderPriceGroup(PriceGroup):
	def __init__(self, data: dict = None):
		"""
		OrderPriceGroup Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)


"""
BranchPropertyVersion data model.
"""


class BranchPropertyVersion(PropertyVersion):
	def __init__(self, data: dict = None):
		"""
		BranchPropertyVersion Constructor

		:param data: dict
		"""

		super().__init__(data)


"""
ChangesetPropertyVersion data model.
"""


class ChangesetPropertyVersion(PropertyVersion):
	def __init__(self, data: dict = None):
		"""
		ChangesetPropertyVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
