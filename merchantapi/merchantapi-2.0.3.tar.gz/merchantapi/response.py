"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.model
import merchantapi.request
from merchantapi.abstract import Request
from merchantapi.abstract import Response
from merchantapi.listquery import ListQueryRequest
from merchantapi.listquery import ListQueryResponse
from requests.models import Response as HttpResponse


"""
API Response for AvailabilityGroupBusinessAccount_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/availabilitygroupbusinessaccount_update_assigned
"""

class AvailabilityGroupBusinessAccountUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupBusinessAccountUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AvailabilityGroupCustomer_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/availabilitygroupcustomer_update_assigned
"""

class AvailabilityGroupCustomerUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupCustomerUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AvailabilityGroupList_Load_Query.

:see: https://docs.miva.com/json-api/functions/availabilitygrouplist_load_query
"""

class AvailabilityGroupListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AvailabilityGroup(e)

	def get_availability_groups(self):
		"""
		Get availability_groups.

		:returns: list of AvailabilityGroup
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AvailabilityGroupPaymentMethod_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/availabilitygrouppaymentmethod_update_assigned
"""

class AvailabilityGroupPaymentMethodUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupPaymentMethodUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AvailabilityGroupProduct_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/availabilitygroupproduct_update_assigned
"""

class AvailabilityGroupProductUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupProductUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AvailabilityGroupShippingMethod_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/availabilitygroupshippingmethod_update_assigned
"""

class AvailabilityGroupShippingMethodUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupShippingMethodUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CategoryList_Load_Parent.

:see: https://docs.miva.com/json-api/functions/categorylist_load_parent
"""

class CategoryListLoadParent(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryListLoadParent Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.Category(e)

	def get_categories(self):
		"""
		Get categories.

		:returns: list of Category
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for CategoryList_Load_Query.

:see: https://docs.miva.com/json-api/functions/categorylist_load_query
"""

class CategoryListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		CategoryListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Category(e)

	def get_categories(self):
		"""
		Get categories.

		:returns: list of Category
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CategoryProduct_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/categoryproduct_update_assigned
"""

class CategoryProductUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryProductUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Category_Insert.

:see: https://docs.miva.com/json-api/functions/category_insert
"""

class CategoryInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Category_Delete.

:see: https://docs.miva.com/json-api/functions/category_delete
"""

class CategoryDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Category_Update.

:see: https://docs.miva.com/json-api/functions/category_update
"""

class CategoryUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CouponList_Delete.

:see: https://docs.miva.com/json-api/functions/couponlist_delete
"""

class CouponListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CouponListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_processed(self):
		"""
		Get processed.

		:returns: int
		"""

		if 'processed' in self.data:
			return self.data['processed']
		return 0


"""
API Response for CouponList_Load_Query.

:see: https://docs.miva.com/json-api/functions/couponlist_load_query
"""

class CouponListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		CouponListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Coupon(e)

	def get_coupons(self):
		"""
		Get coupons.

		:returns: list of Coupon
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CouponPriceGroup_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/couponpricegroup_update_assigned
"""

class CouponPriceGroupUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CouponPriceGroupUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Coupon_Insert.

:see: https://docs.miva.com/json-api/functions/coupon_insert
"""

class CouponInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CouponInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_id(self):
		"""
		Get id.

		:returns: int
		"""

		if 'data' in self.data and 'id' in self.data['data']:
			return self.data['data']['id']
		return 0


"""
API Response for Coupon_Update.

:see: https://docs.miva.com/json-api/functions/coupon_update
"""

class CouponUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CouponUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CustomerList_Load_Query.

:see: https://docs.miva.com/json-api/functions/customerlist_load_query
"""

class CustomerListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		CustomerListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Customer(e)

	def get_customers(self):
		"""
		Get customers.

		:returns: list of Customer
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for Customer_Delete.

:see: https://docs.miva.com/json-api/functions/customer_delete
"""

class CustomerDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Customer_Insert.

:see: https://docs.miva.com/json-api/functions/customer_insert
"""

class CustomerInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Customer(self.data['data'])

	def get_customer(self) -> merchantapi.model.Customer:
		"""
		Get customer.

		:returns: Customer
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Customer_Update.

:see: https://docs.miva.com/json-api/functions/customer_update
"""

class CustomerUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CustomerPaymentCard_Register.

:see: https://docs.miva.com/json-api/functions/customerpaymentcard_register
"""

class CustomerPaymentCardRegister(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerPaymentCardRegister Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.CustomerPaymentCard(self.data['data'])

	def get_customer_payment_card(self) -> merchantapi.model.CustomerPaymentCard:
		"""
		Get customer_payment_card.

		:returns: CustomerPaymentCard
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Module.

:see: https://docs.miva.com/json-api/functions/module
"""

class Module(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		Module Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for NoteList_Load_Query.

:see: https://docs.miva.com/json-api/functions/notelist_load_query
"""

class NoteListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		NoteListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Note(e)

	def get_notes(self):
		"""
		Get notes.

		:returns: list of Note
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for Note_Delete.

:see: https://docs.miva.com/json-api/functions/note_delete
"""

class NoteDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		NoteDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Note_Insert.

:see: https://docs.miva.com/json-api/functions/note_insert
"""

class NoteInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		NoteInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Note_Update.

:see: https://docs.miva.com/json-api/functions/note_update
"""

class NoteUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		NoteUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderCustomFieldList_Load.

:see: https://docs.miva.com/json-api/functions/ordercustomfieldlist_load
"""

class OrderCustomFieldListLoad(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderCustomFieldListLoad Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.OrderCustomField(e)

	def get_order_custom_fields(self):
		"""
		Get order_custom_fields.

		:returns: list of OrderCustomField
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for OrderCustomFields_Update.

:see: https://docs.miva.com/json-api/functions/ordercustomfields_update
"""

class OrderCustomFieldsUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderCustomFieldsUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderItemList_BackOrder.

:see: https://docs.miva.com/json-api/functions/orderitemlist_backorder
"""

class OrderItemListBackOrder(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemListBackOrder Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderItemList_Cancel.

:see: https://docs.miva.com/json-api/functions/orderitemlist_cancel
"""

class OrderItemListCancel(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemListCancel Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderItemList_CreateShipment.

:see: https://docs.miva.com/json-api/functions/orderitemlist_createshipment
"""

class OrderItemListCreateShipment(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemListCreateShipment Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderShipment(self.data['data'])

	def get_order_shipment(self) -> merchantapi.model.OrderShipment:
		"""
		Get order_shipment.

		:returns: OrderShipment
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for OrderItemList_Delete.

:see: https://docs.miva.com/json-api/functions/orderitemlist_delete
"""

class OrderItemListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderItem_Add.

:see: https://docs.miva.com/json-api/functions/orderitem_add
"""

class OrderItemAdd(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemAdd Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderTotal(self.data['data'])

	def get_order_total(self) -> merchantapi.model.OrderTotal:
		"""
		Get order_total.

		:returns: OrderTotal
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for OrderItem_Update.

:see: https://docs.miva.com/json-api/functions/orderitem_update
"""

class OrderItemUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderTotal(self.data['data'])

	def get_order_total(self) -> merchantapi.model.OrderTotal:
		"""
		Get order_total.

		:returns: OrderTotal
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for OrderList_Load_Query.

:see: https://docs.miva.com/json-api/functions/orderlist_load_query
"""

class OrderListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		OrderListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Order(e)

	def get_orders(self):
		"""
		Get orders.

		:returns: list of Order
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for OrderPayment_Capture.

:see: https://docs.miva.com/json-api/functions/orderpayment_capture
"""

class OrderPaymentCapture(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderPaymentCapture Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderPaymentTotal(self.data['data'])

	def get_order_payment_total(self) -> merchantapi.model.OrderPaymentTotal:
		"""
		Get order_payment_total.

		:returns: OrderPaymentTotal
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for OrderPayment_Refund.

:see: https://docs.miva.com/json-api/functions/orderpayment_refund
"""

class OrderPaymentRefund(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderPaymentRefund Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderPaymentTotal(self.data['data'])

	def get_order_payment_total(self) -> merchantapi.model.OrderPaymentTotal:
		"""
		Get order_payment_total.

		:returns: OrderPaymentTotal
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for OrderPayment_VOID.

:see: https://docs.miva.com/json-api/functions/orderpayment_void
"""

class OrderPaymentVoid(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderPaymentVoid Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderPaymentTotal(self.data['data'])

	def get_order_payment_total(self) -> merchantapi.model.OrderPaymentTotal:
		"""
		Get order_payment_total.

		:returns: OrderPaymentTotal
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for OrderShipmentList_Update.

:see: https://docs.miva.com/json-api/functions/ordershipmentlist_update
"""

class OrderShipmentListUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderShipmentListUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Order_Create.

:see: https://docs.miva.com/json-api/functions/order_create
"""

class OrderCreate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderCreate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Order(self.data['data'])

	def get_order(self) -> merchantapi.model.Order:
		"""
		Get order.

		:returns: Order
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Order_Delete.

:see: https://docs.miva.com/json-api/functions/order_delete
"""

class OrderDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Order_Update_Customer_Information.

:see: https://docs.miva.com/json-api/functions/order_update_customer_information
"""

class OrderUpdateCustomerInformation(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderUpdateCustomerInformation Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PriceGroupCustomer_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/pricegroupcustomer_update_assigned
"""

class PriceGroupCustomerUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupCustomerUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PriceGroupList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pricegrouplist_load_query
"""

class PriceGroupListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		PriceGroupListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PriceGroup(e)

	def get_price_groups(self):
		"""
		Get price_groups.

		:returns: list of PriceGroup
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupProduct_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/pricegroupproduct_update_assigned
"""

class PriceGroupProductUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupProductUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductImage_Add.

:see: https://docs.miva.com/json-api/functions/productimage_add
"""

class ProductImageAdd(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductImageAdd Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductImage_Delete.

:see: https://docs.miva.com/json-api/functions/productimage_delete
"""

class ProductImageDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductImageDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductList_Adjust_Inventory.

:see: https://docs.miva.com/json-api/functions/productlist_adjust_inventory
"""

class ProductListAdjustInventory(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductListAdjustInventory Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductList_Load_Query.

:see: https://docs.miva.com/json-api/functions/productlist_load_query
"""

class ProductListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ProductListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Product(e)

	def get_products(self):
		"""
		Get products.

		:returns: list of Product
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ProductVariantList_Load_Product.

:see: https://docs.miva.com/json-api/functions/productvariantlist_load_product
"""

class ProductVariantListLoadProduct(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductVariantListLoadProduct Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.ProductVariant(e)

	def get_product_variants(self):
		"""
		Get product_variants.

		:returns: list of ProductVariant
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for Product_Insert.

:see: https://docs.miva.com/json-api/functions/product_insert
"""

class ProductInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Product_Delete.

:see: https://docs.miva.com/json-api/functions/product_delete
"""

class ProductDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Product_Update.

:see: https://docs.miva.com/json-api/functions/product_update
"""

class ProductUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Provision_Domain.

:see: https://docs.miva.com/json-api/functions/provision_domain
"""

class ProvisionDomain(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProvisionDomain Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.ProvisionMessage(e)

	def get_provision_messages(self):
		"""
		Get provision_messages.

		:returns: list of ProvisionMessage
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for Provision_Store.

:see: https://docs.miva.com/json-api/functions/provision_store
"""

class ProvisionStore(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProvisionStore Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.ProvisionMessage(e)

	def get_provision_messages(self):
		"""
		Get provision_messages.

		:returns: list of ProvisionMessage
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for CustomerAddressList_Load_Query.

:see: https://docs.miva.com/json-api/functions/customeraddresslist_load_query
"""

class CustomerAddressListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		CustomerAddressListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.CustomerAddress(e)

	def get_customer_addresses(self):
		"""
		Get customer_addresses.

		:returns: list of CustomerAddress
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PrintQueueList_Load_Query.

:see: https://docs.miva.com/json-api/functions/printqueuelist_load_query
"""

class PrintQueueListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		PrintQueueListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PrintQueue(e)

	def get_print_queues(self):
		"""
		Get print_queues.

		:returns: list of PrintQueue
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PrintQueueJobList_Load_Query.

:see: https://docs.miva.com/json-api/functions/printqueuejoblist_load_query
"""

class PrintQueueJobListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		PrintQueueJobListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PrintQueueJob(e)

	def get_print_queue_jobs(self):
		"""
		Get print_queue_jobs.

		:returns: list of PrintQueueJob
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PrintQueueJob_Delete.

:see: https://docs.miva.com/json-api/functions/printqueuejob_delete
"""

class PrintQueueJobDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PrintQueueJobDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PrintQueueJob_Insert.

:see: https://docs.miva.com/json-api/functions/printqueuejob_insert
"""

class PrintQueueJobInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PrintQueueJobInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_id(self):
		"""
		Get id.

		:returns: int
		"""

		if 'data' in self.data and 'id' in self.data['data']:
			return self.data['data']['id']
		return 0


"""
API Response for PrintQueueJob_Status.

:see: https://docs.miva.com/json-api/functions/printqueuejob_status
"""

class PrintQueueJobStatus(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PrintQueueJobStatus Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_status(self):
		"""
		Get status.

		:returns: string
		"""

		if 'data' in self.data and 'status' in self.data['data']:
			return self.data['data']['status']
		return None


"""
API Response for PaymentMethodList_Load.

:see: https://docs.miva.com/json-api/functions/paymentmethodlist_load
"""

class PaymentMethodListLoad(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PaymentMethodListLoad Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.PaymentMethod(e)

	def get_payment_methods(self):
		"""
		Get payment_methods.

		:returns: list of PaymentMethod
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for Order_Create_FromOrder.

:see: https://docs.miva.com/json-api/functions/order_create_fromorder
"""

class OrderCreateFromOrder(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderCreateFromOrder Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Order(self.data['data'])

	def get_order(self) -> merchantapi.model.Order:
		"""
		Get order.

		:returns: Order
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Order_Authorize.

:see: https://docs.miva.com/json-api/functions/order_authorize
"""

class OrderAuthorize(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderAuthorize Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderPaymentAuthorize(self.data['data'])

	def get_order_payment_authorize(self) -> merchantapi.model.OrderPaymentAuthorize:
		"""
		Get order_payment_authorize.

		:returns: OrderPaymentAuthorize
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for CustomerPaymentCardList_Load_Query.

:see: https://docs.miva.com/json-api/functions/customerpaymentcardlist_load_query
"""

class CustomerPaymentCardListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		CustomerPaymentCardListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.CustomerPaymentCard(e)

	def get_customer_payment_cards(self):
		"""
		Get customer_payment_cards.

		:returns: list of CustomerPaymentCard
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for Branch_Copy.

:see: https://docs.miva.com/json-api/functions/branch_copy
"""

class BranchCopy(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BranchCopy Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Changeset(self.data['data'])

	def get_changeset(self) -> merchantapi.model.Changeset:
		"""
		Get changeset.

		:returns: Changeset
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Branch_Create.

:see: https://docs.miva.com/json-api/functions/branch_create
"""

class BranchCreate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BranchCreate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Branch(self.data['data'])

	def get_branch(self) -> merchantapi.model.Branch:
		"""
		Get branch.

		:returns: Branch
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Branch_Delete.

:see: https://docs.miva.com/json-api/functions/branch_delete
"""

class BranchDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BranchDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Changeset_Create.

:see: https://docs.miva.com/json-api/functions/changeset_create
"""

class ChangesetCreate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ChangesetCreate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Changeset(self.data['data'])

	def get_changeset(self) -> merchantapi.model.Changeset:
		"""
		Get changeset.

		:returns: Changeset
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for ChangesetList_Merge.

:see: https://docs.miva.com/json-api/functions/changesetlist_merge
"""

class ChangesetListMerge(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ChangesetListMerge Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Changeset(self.data['data'])

	def get_changeset(self) -> merchantapi.model.Changeset:
		"""
		Get changeset.

		:returns: Changeset
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for ChangesetChangeList_Load_Query.

:see: https://docs.miva.com/json-api/functions/changesetchangelist_load_query
"""

class ChangesetChangeListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ChangesetChangeListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ChangesetChange(e)

	def get_changeset_changes(self):
		"""
		Get changeset_changes.

		:returns: list of ChangesetChange
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for BranchList_Load_Query.

:see: https://docs.miva.com/json-api/functions/branchlist_load_query
"""

class BranchListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		BranchListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Branch(e)

	def get_branches(self):
		"""
		Get branches.

		:returns: list of Branch
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for BranchTemplateVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/branchtemplateversionlist_load_query
"""

class BranchTemplateVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		BranchTemplateVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.BranchTemplateVersion(e)

	def get_branch_template_versions(self):
		"""
		Get branch_template_versions.

		:returns: list of BranchTemplateVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for BranchCSSResourceVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/branchcssresourceversionlist_load_query
"""

class BranchCSSResourceVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		BranchCSSResourceVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.BranchCSSResourceVersion(e)

	def get_branch_css_resource_versions(self):
		"""
		Get branch_css_resource_versions.

		:returns: list of BranchCSSResourceVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for BranchJavaScriptResourceVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/branchjavascriptresourceversionlist_load_query
"""

class BranchJavaScriptResourceVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		BranchJavaScriptResourceVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.BranchJavaScriptResourceVersion(e)

	def get_branch_java_script_resource_versions(self):
		"""
		Get branch_java_script_resource_versions.

		:returns: list of BranchJavaScriptResourceVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ChangesetList_Load_Query.

:see: https://docs.miva.com/json-api/functions/changesetlist_load_query
"""

class ChangesetListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ChangesetListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Changeset(e)

	def get_changesets(self):
		"""
		Get changesets.

		:returns: list of Changeset
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ChangesetTemplateVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/changesettemplateversionlist_load_query
"""

class ChangesetTemplateVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ChangesetTemplateVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ChangesetTemplateVersion(e)

	def get_changeset_template_versions(self):
		"""
		Get changeset_template_versions.

		:returns: list of ChangesetTemplateVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ChangesetCSSResourceVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/changesetcssresourceversionlist_load_query
"""

class ChangesetCSSResourceVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ChangesetCSSResourceVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ChangesetCSSResourceVersion(e)

	def get_changeset_css_resource_versions(self):
		"""
		Get changeset_css_resource_versions.

		:returns: list of ChangesetCSSResourceVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ChangesetJavaScriptResourceVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/changesetjavascriptresourceversionlist_load_query
"""

class ChangesetJavaScriptResourceVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ChangesetJavaScriptResourceVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ChangesetJavaScriptResourceVersion(e)

	def get_changeset_java_script_resource_versions(self):
		"""
		Get changeset_java_script_resource_versions.

		:returns: list of ChangesetJavaScriptResourceVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CustomerCreditHistoryList_Load_Query.

:see: https://docs.miva.com/json-api/functions/customercredithistorylist_load_query
"""

class CustomerCreditHistoryListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		CustomerCreditHistoryListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.CustomerCreditHistory(e)

	def get_customer_credit_history(self):
		"""
		Get customer_credit_history.

		:returns: list of CustomerCreditHistory
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CustomerCreditHistory_Insert.

:see: https://docs.miva.com/json-api/functions/customercredithistory_insert
"""

class CustomerCreditHistoryInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerCreditHistoryInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CustomerCreditHistory_Delete.

:see: https://docs.miva.com/json-api/functions/customercredithistory_delete
"""

class CustomerCreditHistoryDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerCreditHistoryDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderCoupon_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/ordercoupon_update_assigned
"""

class OrderCouponUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderCouponUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderPriceGroup_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/orderpricegroup_update_assigned
"""

class OrderPriceGroupUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderPriceGroupUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderItemList_CreateReturn.

:see: https://docs.miva.com/json-api/functions/orderitemlist_createreturn
"""

class OrderItemListCreateReturn(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemListCreateReturn Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderReturn(self.data['data'])

	def get_order_return(self) -> merchantapi.model.OrderReturn:
		"""
		Get order_return.

		:returns: OrderReturn
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for OrderReturnList_Received.

:see: https://docs.miva.com/json-api/functions/orderreturnlist_received
"""

class OrderReturnListReceived(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderReturnListReceived Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for BranchPropertyVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/branchpropertyversionlist_load_query
"""

class BranchPropertyVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		BranchPropertyVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.BranchPropertyVersion(e)

	def get_branch_property_versions(self):
		"""
		Get branch_property_versions.

		:returns: list of BranchPropertyVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ChangesetPropertyVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/changesetpropertyversionlist_load_query
"""

class ChangesetPropertyVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ChangesetPropertyVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ChangesetPropertyVersion(e)

	def get_changeset_property_versions(self):
		"""
		Get changeset_property_versions.

		:returns: list of ChangesetPropertyVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ResourceGroupList_Load_Query.

:see: https://docs.miva.com/json-api/functions/resourcegrouplist_load_query
"""

class ResourceGroupListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ResourceGroupListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ResourceGroup(e)

	def get_resource_groups(self):
		"""
		Get resource_groups.

		:returns: list of ResourceGroup
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for BranchList_Delete.

:see: https://docs.miva.com/json-api/functions/branchlist_delete
"""

class BranchListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BranchListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_processed(self):
		"""
		Get processed.

		:returns: int
		"""

		if 'processed' in self.data:
			return self.data['processed']
		return 0


"""
API Response for MivaMerchantVersion.

:see: https://docs.miva.com/json-api/functions/mivamerchantversion
"""

class MivaMerchantVersion(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		MivaMerchantVersion Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.MerchantVersion(self.data['data'])

	def get_merchant_version(self) -> merchantapi.model.MerchantVersion:
		"""
		Get merchant_version.

		:returns: MerchantVersion
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Attribute_Load_Code.

:see: https://docs.miva.com/json-api/functions/attribute_load_code
"""

class AttributeLoadCode(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeLoadCode Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.ProductAttribute(self.data['data'])

	def get_product_attribute(self) -> merchantapi.model.ProductAttribute:
		"""
		Get product_attribute.

		:returns: ProductAttribute
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Attribute_Insert.

:see: https://docs.miva.com/json-api/functions/attribute_insert
"""

class AttributeInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Attribute_Update.

:see: https://docs.miva.com/json-api/functions/attribute_update
"""

class AttributeUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Attribute_Delete.

:see: https://docs.miva.com/json-api/functions/attribute_delete
"""

class AttributeDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OptionList_Load_Attribute.

:see: https://docs.miva.com/json-api/functions/optionlist_load_attribute
"""

class OptionListLoadAttribute(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OptionListLoadAttribute Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.ProductOption(e)

	def get_product_options(self):
		"""
		Get product_options.

		:returns: list of ProductOption
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for Option_Delete.

:see: https://docs.miva.com/json-api/functions/option_delete
"""

class OptionDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OptionDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Option_Insert.

:see: https://docs.miva.com/json-api/functions/option_insert
"""

class OptionInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OptionInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Option_Update.

:see: https://docs.miva.com/json-api/functions/option_update
"""

class OptionUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OptionUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Option_Load_Code.

:see: https://docs.miva.com/json-api/functions/option_load_code
"""

class OptionLoadCode(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OptionLoadCode Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.ProductOption(self.data['data'])

	def get_product_option(self) -> merchantapi.model.ProductOption:
		"""
		Get product_option.

		:returns: ProductOption
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for Option_Set_Default.

:see: https://docs.miva.com/json-api/functions/option_set_default
"""

class OptionSetDefault(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OptionSetDefault Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeAndOptionList_Load_Product.

:see: https://docs.miva.com/json-api/functions/attributeandoptionlist_load_product
"""

class AttributeAndOptionListLoadProduct(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeAndOptionListLoadProduct Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.ProductAttribute(e)

	def get_product_attributes(self):
		"""
		Get product_attributes.

		:returns: list of ProductAttribute
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for OrderShipmentList_Load_Query.

:see: https://docs.miva.com/json-api/functions/ordershipmentlist_load_query
"""

class OrderShipmentListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		OrderShipmentListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.OrderShipment(e)

	def get_order_shipments(self):
		"""
		Get order_shipments.

		:returns: list of OrderShipment
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for OrderItem_Split.

:see: https://docs.miva.com/json-api/functions/orderitem_split
"""

class OrderItemSplit(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemSplit Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for OrderItemList_RemoveFromShipment.

:see: https://docs.miva.com/json-api/functions/orderitemlist_removefromshipment
"""

class OrderItemListRemoveFromShipment(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemListRemoveFromShipment Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CustomerAddress_Insert.

:see: https://docs.miva.com/json-api/functions/customeraddress_insert
"""

class CustomerAddressInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerAddressInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CustomerAddress_Update.

:see: https://docs.miva.com/json-api/functions/customeraddress_update
"""

class CustomerAddressUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerAddressUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CustomerAddress_Delete.

:see: https://docs.miva.com/json-api/functions/customeraddress_delete
"""

class CustomerAddressDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerAddressDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CustomerAddressList_Delete.

:see: https://docs.miva.com/json-api/functions/customeraddresslist_delete
"""

class CustomerAddressListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerAddressListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CustomerAddress_Update_Residential.

:see: https://docs.miva.com/json-api/functions/customeraddress_update_residential
"""

class CustomerAddressUpdateResidential(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerAddressUpdateResidential Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for URIList_Load_Query.

:see: https://docs.miva.com/json-api/functions/urilist_load_query
"""

class URIListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		URIListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for URI_Insert.

:see: https://docs.miva.com/json-api/functions/uri_insert
"""

class URIInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		URIInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductURI_Insert.

:see: https://docs.miva.com/json-api/functions/producturi_insert
"""

class ProductURIInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductURIInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CategoryURI_Insert.

:see: https://docs.miva.com/json-api/functions/categoryuri_insert
"""

class CategoryURIInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryURIInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PageURI_Insert.

:see: https://docs.miva.com/json-api/functions/pageuri_insert
"""

class PageURIInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PageURIInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for FeedURI_Insert.

:see: https://docs.miva.com/json-api/functions/feeduri_insert
"""

class FeedURIInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		FeedURIInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for URI_Update.

:see: https://docs.miva.com/json-api/functions/uri_update
"""

class URIUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		URIUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductURI_Update.

:see: https://docs.miva.com/json-api/functions/producturi_update
"""

class ProductURIUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductURIUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CategoryURI_Update.

:see: https://docs.miva.com/json-api/functions/categoryuri_update
"""

class CategoryURIUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryURIUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PageURI_Update.

:see: https://docs.miva.com/json-api/functions/pageuri_update
"""

class PageURIUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PageURIUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for FeedURI_Update.

:see: https://docs.miva.com/json-api/functions/feeduri_update
"""

class FeedURIUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		FeedURIUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for URI_Delete.

:see: https://docs.miva.com/json-api/functions/uri_delete
"""

class URIDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		URIDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductURIList_Load_Query.

:see: https://docs.miva.com/json-api/functions/producturilist_load_query
"""

class ProductURIListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ProductURIListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CategoryURIList_Load_Query.

:see: https://docs.miva.com/json-api/functions/categoryurilist_load_query
"""

class CategoryURIListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		CategoryURIListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PageURIList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pageurilist_load_query
"""

class PageURIListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		PageURIListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for FeedURIList_Load_Query.

:see: https://docs.miva.com/json-api/functions/feedurilist_load_query
"""

class FeedURIListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		FeedURIListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ProductURIList_Delete.

:see: https://docs.miva.com/json-api/functions/producturilist_delete
"""

class ProductURIListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductURIListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for PageURIList_Delete.

:see: https://docs.miva.com/json-api/functions/pageurilist_delete
"""

class PageURIListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PageURIListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for CategoryURIList_Delete.

:see: https://docs.miva.com/json-api/functions/categoryurilist_delete
"""

class CategoryURIListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryURIListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for FeedURIList_Delete.

:see: https://docs.miva.com/json-api/functions/feedurilist_delete
"""

class FeedURIListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		FeedURIListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for URIList_Delete.

:see: https://docs.miva.com/json-api/functions/urilist_delete
"""

class URIListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		URIListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for PageURI_Redirect.

:see: https://docs.miva.com/json-api/functions/pageuri_redirect
"""

class PageURIRedirect(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		PageURIRedirect Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ProductURI_Redirect.

:see: https://docs.miva.com/json-api/functions/producturi_redirect
"""

class ProductURIRedirect(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ProductURIRedirect Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CategoryURI_Redirect.

:see: https://docs.miva.com/json-api/functions/categoryuri_redirect
"""

class CategoryURIRedirect(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		CategoryURIRedirect Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AvailabilityGroup_Delete.

:see: https://docs.miva.com/json-api/functions/availabilitygroup_delete
"""

class AvailabilityGroupDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AvailabilityGroup_Insert.

:see: https://docs.miva.com/json-api/functions/availabilitygroup_insert
"""

class AvailabilityGroupInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AvailabilityGroup_Update.

:see: https://docs.miva.com/json-api/functions/availabilitygroup_update
"""

class AvailabilityGroupUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AvailabilityGroupCategory_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/availabilitygroupcategory_update_assigned
"""

class AvailabilityGroupCategoryUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupCategoryUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AvailabilityGroupShippingMethodList_Load_Query.

:see: https://docs.miva.com/json-api/functions/availabilitygroupshippingmethodlist_load_query
"""

class AvailabilityGroupShippingMethodListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupShippingMethodListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AvailabilityGroupShippingMethod(e)

	def get_availability_group_shipping_methods(self):
		"""
		Get availability_group_shipping_methods.

		:returns: list of AvailabilityGroupShippingMethod
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupBusinessAccount_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/pricegroupbusinessaccount_update_assigned
"""

class PriceGroupBusinessAccountUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupBusinessAccountUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PriceGroupCategory_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/pricegroupcategory_update_assigned
"""

class PriceGroupCategoryUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupCategoryUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PriceGroupExcludedCategory_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/pricegroupexcludedcategory_update_assigned
"""

class PriceGroupExcludedCategoryUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupExcludedCategoryUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PriceGroupExcludedProduct_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/pricegroupexcludedproduct_update_assigned
"""

class PriceGroupExcludedProductUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupExcludedProductUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.PriceGroupProduct(e)

	def get_price_group_products(self):
		"""
		Get price_group_products.

		:returns: list of PriceGroupProduct
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for PriceGroupQualifyingProduct_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/pricegroupqualifyingproduct_update_assigned
"""

class PriceGroupQualifyingProductUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupQualifyingProductUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PriceGroup_Delete.

:see: https://docs.miva.com/json-api/functions/pricegroup_delete
"""

class PriceGroupDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for PriceGroup_Insert.

:see: https://docs.miva.com/json-api/functions/pricegroup_insert
"""

class PriceGroupInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_id(self):
		"""
		Get id.

		:returns: int
		"""

		if 'id' in self.data:
			return self.data['id']
		return 0


"""
API Response for PriceGroup_Update.

:see: https://docs.miva.com/json-api/functions/pricegroup_update
"""

class PriceGroupUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for CouponCustomer_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/couponcustomer_update_assigned
"""

class CouponCustomerUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CouponCustomerUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for BusinessAccountList_Load_Query.

:see: https://docs.miva.com/json-api/functions/businessaccountlist_load_query
"""

class BusinessAccountListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		BusinessAccountListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.BusinessAccount(e)

	def get_business_accounts(self):
		"""
		Get business_accounts.

		:returns: list of BusinessAccount
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for BusinessAccount_Insert.

:see: https://docs.miva.com/json-api/functions/businessaccount_insert
"""

class BusinessAccountInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BusinessAccountInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for BusinessAccount_Update.

:see: https://docs.miva.com/json-api/functions/businessaccount_update
"""

class BusinessAccountUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BusinessAccountUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for BusinessAccountList_Delete.

:see: https://docs.miva.com/json-api/functions/businessaccountlist_delete
"""

class BusinessAccountListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BusinessAccountListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_processed(self):
		"""
		Get processed.

		:returns: int
		"""

		if 'processed' in self.data:
			return self.data['processed']
		return 0


"""
API Response for BusinessAccountCustomer_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/businessaccountcustomer_update_assigned
"""

class BusinessAccountCustomerUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BusinessAccountCustomerUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for StoreList_Load_Query.

:see: https://docs.miva.com/json-api/functions/storelist_load_query
"""

class StoreListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		StoreListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Store(e)

	def get_stores(self):
		"""
		Get stores.

		:returns: list of Store
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for Store_Load.

:see: https://docs.miva.com/json-api/functions/store_load
"""

class StoreLoad(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		StoreLoad Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Store(self.data['data'])

	def get_store(self) -> merchantapi.model.Store:
		"""
		Get store.

		:returns: Store
		"""

		return {} if 'data' not in self.data else self.data['data']


"""
API Response for ProductVariantList_Load_Query.

:see: https://docs.miva.com/json-api/functions/productvariantlist_load_query
"""

class ProductVariantListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ProductVariantListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ProductVariant(e)

	def get_product_variants(self):
		"""
		Get product_variants.

		:returns: list of ProductVariant
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ProductVariant_Insert.

:see: https://docs.miva.com/json-api/functions/productvariant_insert
"""

class ProductVariantInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductVariantInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_product_id(self):
		"""
		Get product_id.

		:returns: int
		"""

		if 'data' in self.data and 'product_id' in self.data['data']:
			return self.data['data']['product_id']
		return 0

	def get_variant_id(self):
		"""
		Get variant_id.

		:returns: int
		"""

		if 'data' in self.data and 'variant_id' in self.data['data']:
			return self.data['data']['variant_id']
		return 0


"""
API Response for ProductVariant_Update.

:see: https://docs.miva.com/json-api/functions/productvariant_update
"""

class ProductVariantUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductVariantUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_product_id(self):
		"""
		Get product_id.

		:returns: int
		"""

		if 'product_id' in self.data:
			return self.data['product_id']
		return 0

	def get_variant_id(self):
		"""
		Get variant_id.

		:returns: int
		"""

		if 'variant_id' in self.data:
			return self.data['variant_id']
		return 0


"""
API Response for ProductVariant_Generate.

:see: https://docs.miva.com/json-api/functions/productvariant_generate
"""

class ProductVariantGenerate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductVariantGenerate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductVariant_Generate_Delimiter.

:see: https://docs.miva.com/json-api/functions/productvariant_generate_delimiter
"""

class ProductVariantGenerateDelimiter(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductVariantGenerateDelimiter Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductKitList_Load_Query.

:see: https://docs.miva.com/json-api/functions/productkitlist_load_query
"""

class ProductKitListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ProductKitListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ProductKit(e)

	def get_product_kits(self):
		"""
		Get product_kits.

		:returns: list of ProductKit
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ProductKit_Generate_Variants.

:see: https://docs.miva.com/json-api/functions/productkit_generate_variants
"""

class ProductKitGenerateVariants(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductKitGenerateVariants Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductKit_Update_Parts.

:see: https://docs.miva.com/json-api/functions/productkit_update_parts
"""

class ProductKitUpdateParts(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductKitUpdateParts Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductKit_Variant_Count.

:see: https://docs.miva.com/json-api/functions/productkit_variant_count
"""

class ProductKitVariantCount(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductKitVariantCount Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_variants(self):
		"""
		Get variants.

		:returns: int
		"""

		if 'data' in self.data and 'variants' in self.data['data']:
			return self.data['data']['variants']
		return 0


"""
API Response for RelatedProduct_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/relatedproduct_update_assigned
"""

class RelatedProductUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		RelatedProductUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.RelatedProduct(e)

	def get_related_products(self):
		"""
		Get related_products.

		:returns: list of RelatedProduct
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for InventoryProductSettings_Update.

:see: https://docs.miva.com/json-api/functions/inventoryproductsettings_update
"""

class InventoryProductSettingsUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		InventoryProductSettingsUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductVariantList_Delete.

:see: https://docs.miva.com/json-api/functions/productvariantlist_delete
"""

class ProductVariantListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductVariantListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_processed(self):
		"""
		Get processed.

		:returns: int
		"""

		if 'processed' in self.data:
			return self.data['processed']
		return 0


"""
API Response for ImageTypeList_Load_Query.

:see: https://docs.miva.com/json-api/functions/imagetypelist_load_query
"""

class ImageTypeListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ImageTypeListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ImageType(e)

	def get_image_types(self):
		"""
		Get image_types.

		:returns: list of ImageType
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ProductImage_Update_Type.

:see: https://docs.miva.com/json-api/functions/productimage_update_type
"""

class ProductImageUpdateType(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductImageUpdateType Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplateList_Load_Query.

:see: https://docs.miva.com/json-api/functions/attributetemplatelist_load_query
"""

class AttributeTemplateListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AttributeTemplate(e)

	def get_attribute_templates(self):
		"""
		Get attribute_templates.

		:returns: list of AttributeTemplate
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AttributeTemplateAttributeList_Load_Query.

:see: https://docs.miva.com/json-api/functions/attributetemplateattributelist_load_query
"""

class AttributeTemplateAttributeListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateAttributeListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AttributeTemplateAttribute(e)

	def get_attribute_template_attributes(self):
		"""
		Get attribute_template_attributes.

		:returns: list of AttributeTemplateAttribute
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AttributeTemplateOptionList_Load_Attribute.

:see: https://docs.miva.com/json-api/functions/attributetemplateoptionlist_load_attribute
"""

class AttributeTemplateOptionListLoadAttribute(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateOptionListLoadAttribute Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.AttributeTemplateOption(e)

	def get_attribute_template_options(self):
		"""
		Get attribute_template_options.

		:returns: list of AttributeTemplateOption
		"""

		return self.data['data'] if self.data['data'] is not None else []


"""
API Response for AttributeTemplateAttribute_Delete.

:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_delete
"""

class AttributeTemplateAttributeDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateAttributeDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplateAttribute_Insert.

:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_insert
"""

class AttributeTemplateAttributeInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateAttributeInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplateAttribute_Update.

:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_update
"""

class AttributeTemplateAttributeUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateAttributeUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplateOption_Delete.

:see: https://docs.miva.com/json-api/functions/attributetemplateoption_delete
"""

class AttributeTemplateOptionDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateOptionDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplateOption_Insert.

:see: https://docs.miva.com/json-api/functions/attributetemplateoption_insert
"""

class AttributeTemplateOptionInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateOptionInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplateOption_Update.

:see: https://docs.miva.com/json-api/functions/attributetemplateoption_update
"""

class AttributeTemplateOptionUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateOptionUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplate_Insert.

:see: https://docs.miva.com/json-api/functions/attributetemplate_insert
"""

class AttributeTemplateInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplate_Update.

:see: https://docs.miva.com/json-api/functions/attributetemplate_update
"""

class AttributeTemplateUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplate_Delete.

:see: https://docs.miva.com/json-api/functions/attributetemplate_delete
"""

class AttributeTemplateDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplateOption_Set_Default.

:see: https://docs.miva.com/json-api/functions/attributetemplateoption_set_default
"""

class AttributeTemplateOptionSetDefault(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateOptionSetDefault Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for AttributeTemplateProduct_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/attributetemplateproduct_update_assigned
"""

class AttributeTemplateProductUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateProductUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Branch_SetPrimary.

:see: https://docs.miva.com/json-api/functions/branch_setprimary
"""

class BranchSetPrimary(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BranchSetPrimary Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Branch_Update.

:see: https://docs.miva.com/json-api/functions/branch_update
"""

class BranchUpdate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BranchUpdate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Attribute_CopyTemplate.

:see: https://docs.miva.com/json-api/functions/attribute_copytemplate
"""

class AttributeCopyTemplate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeCopyTemplate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for Attribute_CopyLinkedTemplate.

:see: https://docs.miva.com/json-api/functions/attribute_copylinkedtemplate
"""

class AttributeCopyLinkedTemplate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeCopyLinkedTemplate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)


"""
API Response for ProductAttributeAndOptionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/productattributeandoptionlist_load_query
"""

class ProductAttributeAndOptionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		ProductAttributeAndOptionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.ProductAttributeListAttribute(e)

	def get_attributes(self):
		"""
		Get attributes.

		:returns: list of ProductAttributeListAttribute
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CategoryProductList_Load_Query.

:see: https://docs.miva.com/json-api/functions/categoryproductlist_load_query
"""

class CategoryProductListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CategoryProductListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.CategoryProduct(e)

	def get_category_products(self):
		"""
		Get category_products.

		:returns: list of CategoryProduct
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CouponPriceGroupList_Load_Query.

:see: https://docs.miva.com/json-api/functions/couponpricegrouplist_load_query
"""

class CouponPriceGroupListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CouponPriceGroupListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.CouponPriceGroup(e)

	def get_coupon_price_groups(self):
		"""
		Get coupon_price_groups.

		:returns: list of CouponPriceGroup
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupCustomerList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pricegroupcustomerlist_load_query
"""

class PriceGroupCustomerListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupCustomerListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PriceGroupCustomer(e)

	def get_price_group_customers(self):
		"""
		Get price_group_customers.

		:returns: list of PriceGroupCustomer
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupProductList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pricegroupproductlist_load_query
"""

class PriceGroupProductListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupProductListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PriceGroupProduct(e)

	def get_price_group_products(self):
		"""
		Get price_group_products.

		:returns: list of PriceGroupProduct
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CustomerPriceGroupList_Load_Query.

:see: https://docs.miva.com/json-api/functions/customerpricegrouplist_load_query
"""

class CustomerPriceGroupListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerPriceGroupListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.CustomerPriceGroup(e)

	def get_customer_price_groups(self):
		"""
		Get customer_price_groups.

		:returns: list of CustomerPriceGroup
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for OrderPriceGroupList_Load_Query.

:see: https://docs.miva.com/json-api/functions/orderpricegrouplist_load_query
"""

class OrderPriceGroupListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderPriceGroupListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.OrderPriceGroup(e)

	def get_order_price_groups(self):
		"""
		Get order_price_groups.

		:returns: list of OrderPriceGroup
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for OrderCouponList_Load_Query.

:see: https://docs.miva.com/json-api/functions/ordercouponlist_load_query
"""

class OrderCouponListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderCouponListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.OrderCoupon(e)

	def get_order_coupons(self):
		"""
		Get order_coupons.

		:returns: list of OrderCoupon
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for ChildCategoryList_Load_Query.

:see: https://docs.miva.com/json-api/functions/childcategorylist_load_query
"""

class ChildCategoryListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ChildCategoryListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.Category(e)

	def get_categories(self):
		"""
		Get categories.

		:returns: list of Category
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AvailabilityGroupCustomerList_Load_Query.

:see: https://docs.miva.com/json-api/functions/availabilitygroupcustomerlist_load_query
"""

class AvailabilityGroupCustomerListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupCustomerListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AvailabilityGroupCustomer(e)

	def get_availability_group_customers(self):
		"""
		Get availability_group_customers.

		:returns: list of AvailabilityGroupCustomer
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AvailabilityGroupProductList_Load_Query.

:see: https://docs.miva.com/json-api/functions/availabilitygroupproductlist_load_query
"""

class AvailabilityGroupProductListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupProductListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AvailabilityGroupProduct(e)

	def get_availability_group_products(self):
		"""
		Get availability_group_products.

		:returns: list of AvailabilityGroupProduct
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AvailabilityGroupCategoryList_Load_Query.

:see: https://docs.miva.com/json-api/functions/availabilitygroupcategorylist_load_query
"""

class AvailabilityGroupCategoryListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupCategoryListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AvailabilityGroupCategory(e)

	def get_availability_group_categories(self):
		"""
		Get availability_group_categories.

		:returns: list of AvailabilityGroupCategory
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AvailabilityGroupBusinessAccountList_Load_Query.

:see: https://docs.miva.com/json-api/functions/availabilitygroupbusinessaccountlist_load_query
"""

class AvailabilityGroupBusinessAccountListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupBusinessAccountListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AvailabilityGroupBusinessAccount(e)

	def get_availability_group_business_accounts(self):
		"""
		Get availability_group_business_accounts.

		:returns: list of AvailabilityGroupBusinessAccount
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupBusinessAccountList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pricegroupbusinessaccountlist_load_query
"""

class PriceGroupBusinessAccountListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupBusinessAccountListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PriceGroupBusinessAccount(e)

	def get_price_group_business_accounts(self):
		"""
		Get price_group_business_accounts.

		:returns: list of PriceGroupBusinessAccount
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupCategoryList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pricegroupcategorylist_load_query
"""

class PriceGroupCategoryListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupCategoryListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PriceGroupCategory(e)

	def get_price_group_categories(self):
		"""
		Get price_group_categories.

		:returns: list of PriceGroupCategory
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupExcludedCategoryList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pricegroupexcludedcategorylist_load_query
"""

class PriceGroupExcludedCategoryListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupExcludedCategoryListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PriceGroupCategory(e)

	def get_price_group_categories(self):
		"""
		Get price_group_categories.

		:returns: list of PriceGroupCategory
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupExcludedProductList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pricegroupexcludedproductlist_load_query
"""

class PriceGroupExcludedProductListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupExcludedProductListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PriceGroupProduct(e)

	def get_price_group_products(self):
		"""
		Get price_group_products.

		:returns: list of PriceGroupProduct
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for PriceGroupQualifyingProductList_Load_Query.

:see: https://docs.miva.com/json-api/functions/pricegroupqualifyingproductlist_load_query
"""

class PriceGroupQualifyingProductListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupQualifyingProductListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.PriceGroupProduct(e)

	def get_price_group_products(self):
		"""
		Get price_group_products.

		:returns: list of PriceGroupProduct
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for CouponCustomerList_Load_Query.

:see: https://docs.miva.com/json-api/functions/couponcustomerlist_load_query
"""

class CouponCustomerListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CouponCustomerListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.CouponCustomer(e)

	def get_coupon_customers(self):
		"""
		Get coupon_customers.

		:returns: list of CouponCustomer
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for BusinessAccountCustomerList_Load_Query.

:see: https://docs.miva.com/json-api/functions/businessaccountcustomerlist_load_query
"""

class BusinessAccountCustomerListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BusinessAccountCustomerListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.BusinessAccountCustomer(e)

	def get_business_account_customers(self):
		"""
		Get business_account_customers.

		:returns: list of BusinessAccountCustomer
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for RelatedProductList_Load_Query.

:see: https://docs.miva.com/json-api/functions/relatedproductlist_load_query
"""

class RelatedProductListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		RelatedProductListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.RelatedProduct(e)

	def get_related_products(self):
		"""
		Get related_products.

		:returns: list of RelatedProduct
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
API Response for AttributeTemplateProductList_Load_Query.

:see: https://docs.miva.com/json-api/functions/attributetemplateproductlist_load_query
"""

class AttributeTemplateProductListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateProductListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.AttributeTemplateProduct(e)

	def get_attribute_template_products(self):
		"""
		Get attribute_template_products.

		:returns: list of AttributeTemplateProduct
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']


"""
RequestBuilder response class
"""


class RequestBuilder(Response):
	pass