from behave import *


@given('we have behave installed')
def step_impl(context):
    pass


@when('we implement a test')
def step_impl(context):
    assert True is not False


@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False


@given('I put Red Tree Frog in a blender,')
def step_impl(context):
    pass


@given('I put iPhone in a blender,')
def step_impl(context):
    pass


@given('I put Galaxy Nexus in a blender,')
def step_impl(context):
    pass


@when('I switch the blender on')
def step_impl(context):
    assert True is not False


@then('it should transform into mush')
def step_impl(context):
    assert context.failed is False


@then('it should transform into toxic waste')
def step_impl(context):
    assert context.failed is False