from .base import BaseModel, ObjectListModel

class OrderList(ObjectListModel):

    def __init__(self):
        super().__init__(list=[], listObject=Order)

class Order(BaseModel):

    def __init__(self,
        order_id=None,
        order_date=None,
        total_quantity=None,
        total_lots=None,
        base_order_total=None,
        status=None,
        status_id=None
    ):

        super().__init__()

        self.order_id = order_id
        self.order_date = order_date
        self.total_quantity = total_quantity
        self.total_lots = total_lots
        self.base_order_total = base_order_total
        self.status = status
        self.status_id = status_id

class ExtendedOrder(BaseModel):
    def __init__(self,
        order_id=None,
        order_time=None,
        processed_time=None,
        iso_order_time=None,
        iso_processed_time=None,
        store_id=None,
        ship_method_name=None,
        ship_method_id=None,
        status=None,
        status_id=None,
        weight=None,
        ship_total=None,
        buyer_note=None,
        total_quantity=None,
        total_lots=None,
        base_currency=None,
        payment_method_type=None,
        payment_currency=None,
        payment_total=None,
        base_order_total=None,
        sub_total=None,
        coupon_discount=None,
        payment_method_note=None,
        payment_transaction_id=None,
        tax_rate=None,
        tax_amount=None,
        tracking_number=None,
        buyer_name=None,
        combine_with=None,
        refund_shipping=None,
        refund_adjustment=None,
        refund_subtotal=None,
        refund_total=None,
        refund_note=None,
        my_cost_total=None,
        affiliate_fee=None,
        brickowl_fee=None,
        seller_note=None,
        customer_email=None,
        customer_user_id=None,
        customer_username=None,
        message_count=None,
        utm_source=None,
        utm_medium=None,
        ship_first_name=None,
        ship_last_name=None,
        ship_country_code=None,
        ship_country=None,
        ship_post_code=None,
        ship_street_1=None,
        ship_street_2=None,
        ship_city=None,
        ship_region=None,
        ship_phone=None,
        billing_first_name=None,
        billing_last_name=None,
        billing_country_code=None,
        billing_country=None,
        billing_post_code=None,
        billing_street_1=None,
        billing_street_2=None,
        billing_city=None,
        billing_region=None,
        billing_phone=None,
        items=None
    ):

        super().__init__()

        self.order_id = order_id
        self.order_time = order_time
        self.processed_time = processed_time
        self.iso_order_time = iso_order_time
        self.iso_processed_time = iso_processed_time
        self.store_id = store_id
        self.ship_method_name = ship_method_name
        self.ship_method_id = ship_method_id
        self.status = status
        self.status_id = status_id
        self.weight = weight
        self.ship_total = ship_total
        self.buyer_note = buyer_note
        self.total_quantity = total_quantity
        self.total_lots = total_lots
        self.base_currency = base_currency
        self.payment_method_type = payment_method_type
        self.payment_currency = payment_currency
        self.payment_total = payment_total
        self.base_order_total = base_order_total
        self.sub_total = sub_total
        self.coupon_discount = coupon_discount
        self.payment_method_note = payment_method_note
        self.payment_transaction_id = payment_transaction_id
        self.tax_rate = tax_rate
        self.tax_amount = tax_amount
        self.tracking_number = tracking_number
        self.buyer_name = buyer_name
        self.combine_with = combine_with
        self.refund_shipping = refund_shipping
        self.refund_adjustment = refund_adjustment
        self.refund_subtotal = refund_subtotal
        self.refund_total = refund_total
        self.refund_note = refund_note
        self.my_cost_total = my_cost_total
        self.affiliate_fee = affiliate_fee
        self.brickowl_fee = brickowl_fee
        self.seller_note = seller_note
        self.customer_email = customer_email
        self.customer_user_id = customer_user_id
        self.customer_username = customer_username
        self.message_count = message_count
        self.utm_source = utm_source
        self.utm_medium = utm_medium
        self.ship_first_name = ship_first_name
        self.ship_last_name = ship_last_name
        self.ship_country_code = ship_country_code
        self.ship_country = ship_country
        self.ship_post_code = ship_post_code
        self.ship_street_1 = ship_street_1
        self.ship_street_2 = ship_street_2
        self.ship_city = ship_city
        self.ship_region = ship_region
        self.ship_phone = ship_phone
        self.billing_first_name = billing_first_name
        self.billing_last_name = billing_last_name
        self.billing_country_code = billing_country_code
        self.billing_country = billing_country 
        self.billing_post_code = billing_post_code
        self.billing_street_1 = billing_street_1
        self.billing_street_2 = billing_street_2
        self.billing_city = billing_city
        self.billing_region = billing_region
        self.billing_phone = billing_phone
        self.items = items if items else OrderItemList()

class OrderItemList(ObjectListModel):

    def __init__(self):
        super().__init__(list=[], listObject=OrderItem)

class OrderItem(BaseModel):

    def __init__(self,
        image_small=None,
        name=None,
        type=None,
        color_name=None,
        color_id=None,
        boid=None,
        lot_id=None,
        condition=None,
        ordered_quantity=None,
        personal_note=None,
        bl_lot_id=None,
        external_lot_ids=None,
        remaining_quantity=None,
        weight=None,
        public_note=None,
        order_item_id=None,
        base_price=None,
        ids=None
    ):

        super().__init__()

        self.image_small = image_small
        self.name = name
        self.type = type
        self.color_name = color_name
        self.color_id = color_id
        self.boid = boid
        self.lot_id = lot_id
        self.condition = condition
        self.ordered_quantity = ordered_quantity
        self.personal_note = personal_note
        self.bl_lot_id = bl_lot_id
        self.external_lot_ids = external_lot_ids if external_lot_ids else ExternalLotIDs()
        self.remaining_quantity = remaining_quantity
        self.weight = weight
        self.public_note = public_note
        self.order_item_id = order_item_id
        self.base_price = base_price
        self.ids = ids if ids else OrderItemIDsList()

class ExternalLotIDs(BaseModel):

    def __init__(self,
        other=None
    ):

        super().__init__()

        self.other = other

class OrderItemIDsList(ObjectListModel):

    def __init__(self):
        super().__init__(list=[], listObject=OrderItemIDs)

class OrderItemIDs(BaseModel):

    def __init__(self,
        id=None,
        type=None
    ):

        super().__init__()

        self.id = id
        self.type = type