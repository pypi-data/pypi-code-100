from django import forms



####Custom field choice with others
class CustomSelectWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(CustomSelectWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(CustomSelectWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)



class FormForm(forms.Form):
   char_field_with_list = forms.CharField(required=True)

   def __init__(self, *args, **kwargs):
        _data_list = kwargs.pop('data_list', None)
        super(FormForm, self).__init__(*args, **kwargs)

    # the "name" parameter will allow you to use the same widget more than once in the same
    # form, not setting this parameter differently will cuse all inputs display the
    # same list.
        self.fields['char_field_with_list'].widget = CustomSelectWidget(data_list=_data_list, name='data-list')

