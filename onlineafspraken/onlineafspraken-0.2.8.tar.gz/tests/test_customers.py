from onlineafspraken.api import customers
from onlineafspraken.schema.customer import SetCustomerSchema, CustomerSchema


def test_set_and_get_customer():

    customer_set = customers.set_customer("Py", "Test", "py@jelmert.nl")

    assert isinstance(customer_set, SetCustomerSchema)
    assert customer_set.id

    customer = customers.get_customer(customer_set.id)

    assert isinstance(customer, CustomerSchema)
    assert customer.id == customer_set.id




