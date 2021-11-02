from brickowl.models.orders import ExtendedOrder, OrderItemList, OrderList
from .base import APIEndpoint

from brickowl.models.orders import OrderList

class OrderMethods(APIEndpoint):

    def __init__(self, api):
        super(OrderMethods, self).__init__(api, "order")

    def list(self, status=None, orderTime=None, limit=None, listType=None):
        url = '{0}/list'.format(self.endpoint)
        data = {}

        if status: data['status'] = status
        if orderTime: data['order_time'] = orderTime
        if limit: data['limit'] = limit
        if listType: data['list_type'] = listType

        status, headers, respJson = self.api.get(url, data)
        if status in [400, 401, 403, 404, 405, 415, 422]: return OrderList().parseError(respJson)

        return OrderList().parse(respJson)
    
    def get(self, id, withItems=False):

        url = '{0}/view'.format(self.endpoint)
        data = { 'order_id' : id }

        status, headers, respJson = self.api.get(url, data)
        if status in [400, 401, 403, 404, 405, 415, 422]: return ExtendedOrder().parseError(respJson)
        
        order = ExtendedOrder().parse(respJson)

        if withItems:
            items = self.getItems(id)
            order.items = items

        return order
    
    def getItems(self, id):

        url = '{0}/items'.format(self.endpoint)
        data = { 'order_id' : id }

        status, headers, respJson = self.api.get(url, data)
        if status in [400, 401, 403, 404, 405, 415, 422]: return OrderItemList().parseError(respJson)

        return OrderItemList().parse(respJson)
    
    def addTracking(self, id, trackingId):

        url = '{0}/tracking'.format(self.endpoint)
        data = { 'order_id' : id, 'tracking_id' : trackingId }

        status, headers, respJson = self.api.post(url, data)
        if status in [400, 401, 403, 404, 405, 415, 422]: return False

        return True

    def setStatus(self, id, statusId):

        url = '{0}/set_status'.format(self.endpoint)
        data = { 'order_id' : id, 'status_id' : statusId }

        status, headers, respJson = self.api.post(url, data)
        if status in [400, 401, 403, 404, 405, 415, 422]: return False

        return True