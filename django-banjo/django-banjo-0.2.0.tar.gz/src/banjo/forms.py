from django import forms

type_fields = {
    str: lambda: forms.CharField(),
    bool: lambda: forms.BooleanField(required=False),
    int: lambda: forms.IntegerField(),
    float: lambda: forms.FloatField(),
}

class ApiRouteForm(forms.Form):
    """Dynamically instantiates a form matching a route's args dict
    Args should be a dict of {param_name: type}, where type is in 
    [str, bool, int, float].
    """

    @classmethod
    def for_args(cls, args, class_name=None):
        "Dynamically define a form class for the given route args"
        class_name = class_name or "ApiRouteFormWithArgs"
        fields = {name: type_fields[t]() for name, t in args.items()}
        return type(class_name, (ApiRouteForm,), fields)
