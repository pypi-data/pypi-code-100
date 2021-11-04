import uuid

from django import forms

from django.forms import ChoiceField

from data.models.models import Calibration, Hardware, Accessory, Channel, HardwareConfig, \
    CalibrationConstants, DHT22, MCP3008, \
    ModProbe, PiPico, VEML7700, HardwareChannelTypes, Hub, Category, AccessoryType, SPIIo, SerialIo, PwmIo, I2cIo, \
    DeviceFileIo, MCPAnalogIo, PiGpio, PiPicoAnalogIo, PiPicoACAnalogIo, HardwareIO, PMSA0031


class HubForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HubForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        categories = list(
            Category.objects.all().values_list('enum', 'name'))
        # categories = [('----', '-----')]
        # for chan_type in channel_types_temp:
        #     channel_types.append((chan_type['channel_type'], chan_type['channel_type']))

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

        self.fields['category'] = ChoiceField(choices=tuple(categories))

    class Meta:
        model = Hub
        fields = ("__all__")


class CalibrationConstantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CalibrationConstantForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap

        for name in self.fields.keys():
            if name == 'calibration':
                self.fields[name].widget = forms.HiddenInput()
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = CalibrationConstants
        fields = ("__all__")


class CalibrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CalibrationForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            if name == 'accessory':
                self.fields[name].widget = forms.HiddenInput()
            else:
                self.fields[name].widget.attrs.update({
                    'class': 'form-control',
                })

    class Meta:
        model = Calibration
        fields = ("__all__")


class HardwareForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HardwareForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name == 'type':
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Hardware
        fields = ("__all__")


class HardwareDHT22Form(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwareDHT22Form, self).__init__(*args, **kwargs)

    class Meta:
        model = DHT22
        fields = ("__all__")


class HardwareMCP3008Form(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwareMCP3008Form, self).__init__(*args, **kwargs)

    class Meta:
        model = MCP3008
        fields = ("__all__")


class HardwareModProbeForm(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwareModProbeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ModProbe
        fields = ("__all__")


class HardwarePiPicoForm(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwarePiPicoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PiPico
        fields = ("__all__")


class HardwareVEML7700Form(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwareVEML7700Form, self).__init__(*args, **kwargs)

    class Meta:
        model = VEML7700
        fields = ("__all__")


class HardwarePMSA0031Form(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwarePMSA0031Form, self).__init__(*args, **kwargs)

    class Meta:
        model = PMSA0031
        fields = ("__all__")


class AccessoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AccessoryForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            # if name == 'channels':
            #     self.fields[name]= forms.ModelChoiceField(queryset=Channel.objects.all().values(('id')), empty_label="(Nothing)")
            # else:
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

        categories = list(
            Category.objects.all().values_list('enum', 'name'))
        self.fields['category'] = ChoiceField(choices=tuple(categories))

        types = list(
            AccessoryType.objects.all().values_list('type', 'type'))
        self.fields['type'] = ChoiceField(choices=tuple(types))

    class Meta:
        model = Accessory
        fields = ("__all__")


class ChannelForm(forms.ModelForm):

    def __init__(self, hardware_type=None, *args, **kwargs):
        super(ChannelForm, self).__init__(*args, **kwargs)
        if hardware_type is not None:
            channel_types_temp = list(
                HardwareChannelTypes.objects.filter(hardware_type=hardware_type).values('channel_type'))
            channel_types = [('----', '-----')]
            for chan_type in channel_types_temp:
                channel_types.append((chan_type['channel_type'], chan_type['channel_type']))
            self.fields['type'] = ChoiceField(choices=tuple(channel_types))

        # self.fields['type'] = ChoiceField(queryset=HardwareChannelTypes.objects.filter(hardware_type=hardware_type).values_list('channel_type'))
        # self.fields['type'].queryset = HardwareChannelTypes.objects.filter(hardware_type=hardware_type)

        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            if name == 'hardware':
                self.fields[name].widget = forms.HiddenInput()
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Channel
        fields = ("__all__")


class HardwareConfigForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HardwareConfigForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = HardwareConfig
        fields = ("__all__")


class HardwareIoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HardwareIoForm, self).__init__(*args, **kwargs)
        # self.fields['type'] = ChoiceField(choices=tuple(channel_types))

        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        # print('asdf')
        # for name in self.fields.keys():
        #     if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
        #         self.fields[name].widget = forms.HiddenInput()
        #     print(name)
        #     self.fields[name].widget.attrs.update({
        #         'class': 'form-control',
        #     })

    class Meta:
        model = HardwareIO
        fields = ("__all__")


class SPIIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(SPIIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = SPIIo
        fields = ("__all__")


class SerialIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(SerialIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = SerialIo
        fields = ("__all__")


class PwmIoForm(HardwareIoForm):
    def __init__(self, *args, **kwargs):
        super(PwmIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = PwmIo
        fields = ("__all__")


class I2cIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(I2cIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = I2cIo
        fields = ("__all__")


class DeviceFileIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(DeviceFileIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = DeviceFileIo
        fields = ("__all__")


class MCPAnalogIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(MCPAnalogIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = MCPAnalogIo
        fields = ("__all__")


class PiPicoAnalogIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(PiPicoAnalogIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = PiPicoAnalogIo
        fields = ("__all__")


class PiPicoACAnalogIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(PiPicoACAnalogIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = PiPicoACAnalogIo
        fields = ("__all__")


class PiGpioForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(PiGpioForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = PiGpio
        fields = ("__all__")


DHT22 = 'DHT22'
MCP3008 = 'MCP3008'
ModProbe = 'ModProbe'
PiPico = 'PiPico'
VEML7700 = 'VEML7700'
PMSA0031 = 'PMSA0031'
CHOICES = (('DHT22', 'DHT22'), ('MCP3008', 'MCP3008'), ('ModProbe', 'ModProbe'), ('PiPico', 'PiPico'),
           ('VEML7700', 'VEML7700'), ('PMSA0031', 'PMSA0031'))


class HardwareTypeForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(HardwareTypeForm, self).__init__(*args, **kwargs)

    type = forms.ChoiceField(choices=CHOICES)


SPI = 'SPI'
Serial = 'Serial'
PWM = 'PWM'
I2C = 'I2C'
DeviceFile = 'Device File'
MCPChannel = 'MCP Channel'
PiPicoAnalog = 'Pi Pico Analog'
PiPicoACAnalog = 'Pi Pico AC Analog'
PiGPIO = 'Pi GPIO'

hardware_io_choices = (
    (SPI, SPI), (Serial, Serial), (PWM, PWM), (I2C, I2C), (DeviceFile, DeviceFile), (MCPChannel, MCPChannel),
    (PiPicoAnalog, PiPicoAnalog), (PiPicoACAnalog, PiPicoACAnalog), (PiGPIO, PiGPIO))


class HardwareIOTypeForm(forms.Form):
    type = forms.ChoiceField(choices=hardware_io_choices)
    parent_hardware = forms.CharField()
    child_hardware = forms.CharField()
    child_channel = forms.CharField()
    hub = forms.CharField()
    parent_hardware.widget = forms.HiddenInput()
    child_hardware.widget = forms.HiddenInput()
    child_channel.widget = forms.HiddenInput()
    hub.widget = forms.HiddenInput()

    # def __init__(self, *args, **kwargs):
    #     super(HardwareTypeForm, self).__init__(*args, **kwargs)
    def __init__(self, *args, **kwargs):
        super(HardwareIOTypeForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['type', 'parent_hardware', 'child_hardware', 'child_channel', 'hub']


from django.forms.models import inlineformset_factory, BaseModelFormSet, BaseInlineFormSet, BaseModelForm
from data.models.models import HardwareStats, DataTransformer, DataTransformerConstants, HardwareDataTransformer, \
    HardwareStatsDataTransformer, DataTransformerTypes


# DataTransformerInlineFormset = inlineformset_factory(DataTransformer, DataTransformer, fk_name='data_transformer_parent',
#                                                      extra=1,exclude =['updated_at','created_at'],formset=DataTransformerForm)

class DataConstantsTransformerForm(forms.ModelForm):
    id = forms.UUIDField(required=False,
                         widget=forms.HiddenInput(attrs={'class': 'form-control'}),initial=uuid.uuid4)

    index = forms.IntegerField(required=False,
                               widget=forms.HiddenInput(attrs={'class': 'form-control'}),
                               initial=0)
    value = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_transformer = forms.ModelChoiceField(required=False, queryset=DataTransformer.objects.all(),
                                              widget=forms.HiddenInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DataTransformerConstants
        fields = ('__all__')


class HardwareTransformerForm(forms.ModelForm):
    id = forms.UUIDField(required=False,
                         widget=forms.HiddenInput(attrs={'class': 'form-control'}),initial=uuid.uuid4)
    index = forms.IntegerField(required=False,
                               widget=forms.HiddenInput(attrs={'class': 'form-control'}),
                               initial=0)
    data_transformer = forms.ModelChoiceField(required=False, queryset=DataTransformer.objects.all(),
                                              widget=forms.HiddenInput(attrs={'class': 'form-control'}))

    class Meta:
        model = HardwareDataTransformer
        fields = ('__all__')


class HardwareStatsTransformerForm(forms.ModelForm):
    id = forms.UUIDField(required=False,
                         widget=forms.HiddenInput(attrs={'class': 'form-control'}),initial=uuid.uuid4)
    index = forms.IntegerField(required=False,
                               widget=forms.HiddenInput(attrs={'class': 'form-control'}),
                               initial=0)
    data_transformer = forms.ModelChoiceField(required=False, queryset=DataTransformer.objects.all(),
                                              widget=forms.HiddenInput(attrs={'class': 'form-control'}))

    class Meta:
        model = HardwareStatsDataTransformer
        fields = ('__all__')


class BaseInlineFormSetWithAddMoreButton(BaseInlineFormSet):
    def as_p(self):
        button_id = str(self.prefix) + 'add_more'
        empty_form_id = str(self.prefix) + 'empty_form'
        empty_form_as_p = str(self.empty_form.as_p())
        div_name = str(self.prefix) + 'div'

        forms_as_p = BaseInlineFormSet.as_p(self)
        p = f"""<div class="row" id="{div_name}">
        {forms_as_p}
        </div>
        <input type="button" value="Add More" id="{button_id}">
                    <div id="{empty_form_id}" style="display:none">
                    {empty_form_as_p}
                    </div>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
        <script>
    $('#{button_id}').click(function() {{
        var form_idx = $('#id_{self.prefix}-TOTAL_FORMS').val();
        var empty_form = document.getElementById('{empty_form_id}').innerHTML.replace(/__prefix__/g, form_idx);        
        
        var d1 = document.getElementById('{div_name}');
        d1.insertAdjacentHTML('afterend', empty_form);
        $('#id_{self.prefix}-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    }});
</script>"""
        print(p)
        return p


DataConstantsTransformerInlineFormset = inlineformset_factory(DataTransformer, DataTransformerConstants, formset=BaseInlineFormSetWithAddMoreButton, extra=0,
                                                              form=DataConstantsTransformerForm, can_delete_extra=True)
# HardwareTransformerInlineFormset = inlineformset_factory(DataTransformer, HardwareDataTransformer, extra=1,
#                                                          form=HardwareTransformerForm, can_delete_extra=True)
HardwareStatsTransformerInlineFormset = inlineformset_factory(DataTransformer, HardwareStatsDataTransformer, extra=0, formset=BaseInlineFormSetWithAddMoreButton,
                                                              form=HardwareStatsTransformerForm, can_delete_extra=True)

from django.utils.safestring import mark_safe


class DataTransform(forms.ModelForm):
    id = forms.UUIDField(required=False,
                         widget=forms.HiddenInput(attrs={'class': 'form-control'}),
                         initial=uuid.uuid4)
    accessory = forms.ModelChoiceField(required=False, queryset=Accessory.objects.all(),
                                       widget=forms.HiddenInput(attrs={'class': 'form-control'}))

    parent = forms.ModelChoiceField(required=False, queryset=DataTransformer.objects.all(),
                                    widget=forms.HiddenInput(attrs={'class': 'form-control'}))

    type = forms.ModelChoiceField(required=False, queryset=DataTransformerTypes.objects.all())

    def __init__(self, *args, **kwargs):
        print('Init Data Transform')

        super(DataTransform, self).__init__(*args, **kwargs)

        try:
            if self.instance.get_children().count() >= 0:
                print('Adding to child form node: ' + str(self.instance.get_children().count() + 1))

                self.nested_data_transformer_form = dataTransformerInlineFormset(
                    instance=self.instance,
                    queryset=self.instance.get_children(),
                    data=self.data if self.is_bound else None,
                    files=self.files if self.is_bound else None,
                    initial=[{'parent': str(self.instance.pk), 'accessory': str(self.instance.accessory.id),
                              'id': str(uuid.uuid4())}],
                    prefix=str(self.instance.id) + 'dataTransformerInlineFormset'
                )
                self.nested_data_transformer_form.extra = self.instance.get_children().count()


        except Exception as e:
            print(str(e))
            # self.nested_data_transformer_form = dataTransformerInlineFormset(
            #     instance=self.instance,
            #     data=self.data if self.is_bound else None,
            #     files=self.files if self.is_bound else None,
            #     prefix=str(self.instance.id) + 'dataTransformerInlineFormset'
            # )
            # self.nested_data_transformer_form.extra = 0

        self.nested_constants_form = DataConstantsTransformerInlineFormset(
            instance=self.instance,
            queryset=self.instance.datatransformerconstants_set,
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            prefix=str(self.instance.id) + 'DataConstantsTransformerInlineFormset',
            initial=[{'data_transformer': str(self.instance.pk), 'id': str(uuid.uuid4())}]

        )
        self.nested_constants_form.extra = self.instance.datatransformerconstants_set.count()

        hardware_outputs = self.instance.hardwaredatatransformer_set.first()
        self.nested_hardware_outputs_form = HardwareTransformerForm(
            instance=hardware_outputs,
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            prefix=str(self.instance.id) + 'HardwareTransformerForm',
            initial={'data_transformer': str(self.instance.pk), 'id': str(uuid.uuid4())}
        )

        self.nested_hardware_stats_form = HardwareStatsTransformerInlineFormset(
            instance=self.instance,
            queryset=self.instance.hardwarestatsdatatransformer_set,
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            prefix=str(self.instance.id) + 'HardwareStatsTransformerInlineFormset',
            initial=[{'data_transformer': str(self.instance.pk), 'id': str(uuid.uuid4())}]

        )
        self.nested_hardware_stats_form.extra = self.instance.hardwarestatsdatatransformer_set.count()

    def as_p(self):
        print('wtf')
        print('instance: ' + str(self.instance.id))
        forms = '<div class="row"><div class="col-6">'

        forms = super(DataTransform, self).as_p()
        forms = forms + '</div><div class="col-6">'

        if hasattr(self, 'nested_constants_form') and self.nested_constants_form is not None:
            forms = forms + '\n  -' + self.nested_constants_form.as_p()
        if hasattr(self, 'nested_hardware_outputs_form') and self.nested_hardware_outputs_form is not None:
            forms = forms + '\n  -' + self.nested_hardware_outputs_form.as_p()
        if hasattr(self, 'nested_hardware_stats_form') and self.nested_hardware_stats_form is not None:
            forms = forms + '\n  -' + self.nested_hardware_stats_form.as_p()
        if hasattr(self, 'nested_data_transformer_form') and self.nested_data_transformer_form is not None:
            print('netdatatransform with number elements: ' + str(len(self.nested_data_transformer_form)))
            forms = forms + '\n       -' + self.nested_data_transformer_form.as_p()
        forms = forms + '</div></div>'

        return mark_safe(forms)

    def save(self, commit=True):
        print('node')
        print('save: ' + str(self.instance.id))
        root_node = super(DataTransform, self).save(commit)
        if hasattr(self,
                   'nested_constants_form') and self.nested_constants_form is not None:
            self.nested_constants_form.instance.refresh_from_db()
            if self.nested_constants_form.is_valid():
                self.nested_constants_form.save(commit)
            else:
                print(self.nested_constants_form.errors)
        if hasattr(self,
                   'nested_hardware_outputs_form') and self.nested_hardware_outputs_form is not None:

            if self.nested_hardware_outputs_form.is_valid():
                self.nested_hardware_outputs_form.save(commit)
            else:
                print(self.nested_hardware_outputs_form.errors)
        if hasattr(self,
                   'nested_hardware_stats_form') and self.nested_hardware_stats_form is not None:
            self.nested_hardware_stats_form.instance.refresh_from_db()

            if self.nested_hardware_stats_form.is_valid():
                self.nested_hardware_stats_form.save(commit)
            else:
                print(self.nested_hardware_stats_form.errors)
        if hasattr(self,
                   'nested_data_transformer_form') and self.nested_data_transformer_form is not None:
            self.nested_data_transformer_form.instance.refresh_from_db()

            if self.nested_data_transformer_form.is_valid():
                self.nested_data_transformer_form.save(commit)
            else:
                print(self.nested_data_transformer_form.errors)
        root_node.refresh_from_db()
        return root_node

    class Meta:
        model = DataTransformer
        fields = ['id', 'accessory', 'parent', 'type']


# DataTransformerFormset = form_factory(DataTransformer,formset=DataTransformerForm)
dataTransformerInlineFormset = inlineformset_factory(DataTransformer, DataTransformer,
                                                     fk_name='parent',
                                                     can_delete_extra=True,
                                                     form=DataTransform,
                                                     formset=BaseInlineFormSetWithAddMoreButton,
                                                     extra=0
                                                     )


class DataTransformRoot(forms.ModelForm):
    id = forms.UUIDField(required=False,
                         widget=forms.HiddenInput(attrs={'class': 'form-control'}),initial=uuid.uuid4)
    accessory = forms.ModelChoiceField(required=True, queryset=Accessory.objects.all(),
                                       widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    type = forms.ModelChoiceField(required=True, queryset=DataTransformerTypes.objects.all())

    # def __init__(self, *args, **kwargs):
    #     super(HardwareTypeForm, self).__init__(*args, **kwargs)
    def __init__(self, *args, **kwargs):
        super(DataTransformRoot, self).__init__(*args, **kwargs)
        # self.fields['accessory'].initial = str(self.instance.accessory.pk)

        # types = list(
        #     DataTransformerTypes.objects.all().values_list('type', 'type'))
        # self.fields['type'] = ChoiceField(choices=tuple(types))
        try:
            if hasattr(self.instance, 'get_children'):
                print('Adding to root form node: ' + str(self.instance.get_children().count() + 1))

                self.nested_data_transformer_form = dataTransformerInlineFormset(
                    instance=self.instance,
                    queryset=self.instance.get_children(),
                    data=self.data if self.is_bound else None,
                    files=self.files if self.is_bound else None,
                    initial=[{'parent': str(self.instance.pk), 'accessory': str(self.instance.accessory.id),
                              'id': str(uuid.uuid4())}],
                    prefix=str(self.instance.id) + 'dataTransformerInlineFormset',
                )
                self.nested_data_transformer_form.extra = self.instance.get_children().count()

            else:

                self.nested_data_transformer_form = dataTransformerInlineFormset(
                    instance=self.instance,
                    data=self.data if self.is_bound else None,
                    files=self.files if self.is_bound else None,
                    prefix=str(self.instance.id) + 'dataTransformerInlineFormset',
                    initial=[{'parent': str(self.instance.pk), 'accessory': str(self.instance.accessory.id),
                              'id': str(uuid.uuid4())}],
                )
                self.nested_data_transformer_form.extra = 0
        except Exception as e:
            print(str(e))

        self.nested_constants_form = DataConstantsTransformerInlineFormset(
            instance=self.instance,
            queryset=self.instance.datatransformerconstants_set,
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            prefix=str(self.instance.id) + 'DataConstantsTransformerInlineFormset',
            initial=[{'data_transformer': str(self.instance.pk), 'id': str(uuid.uuid4())}]

        )
        self.nested_constants_form.extra = self.instance.datatransformerconstants_set.count()

        hardware_outputs = self.instance.hardwaredatatransformer_set.first()
        self.nested_hardware_outputs_form = HardwareTransformerForm(
            instance=hardware_outputs,
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            prefix=str(self.instance.id) + 'HardwareTransformerForm',
            initial={'data_transformer': str(self.instance.pk), 'id': str(uuid.uuid4())}
        )

        self.nested_hardware_stats_form = HardwareStatsTransformerInlineFormset(
            instance=self.instance,
            queryset=self.instance.hardwarestatsdatatransformer_set,
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            prefix=str(self.instance.id) + 'HardwareStatsTransformerInlineFormset',
            initial=[{'data_transformer': str(self.instance.pk), 'id': str(uuid.uuid4())}]

        )
        self.nested_hardware_stats_form.extra = self.instance.hardwarestatsdatatransformer_set.count()

    def as_p(self):
        print('root')
        print('instance: ' + str(self.instance.id))
        forms = '<div class="row"><div class="col-6">'

        forms = forms + super(DataTransformRoot, self).as_p()
        forms = forms + '</div><div class="col-6">'
        if hasattr(self, 'nested_constants_form') and self.nested_constants_form is not None:
            forms = forms + '\n  -' + self.nested_constants_form.as_p()
        if hasattr(self, 'nested_hardware_outputs_form') and self.nested_hardware_outputs_form is not None:
            forms = forms + '\n  -' + self.nested_hardware_outputs_form.as_p()
        if hasattr(self, 'nested_hardware_stats_form') and self.nested_hardware_stats_form is not None:
            forms = forms + '\n  -' + self.nested_hardware_stats_form.as_p()
        if hasattr(self, 'nested_data_transformer_form') and self.nested_data_transformer_form is not None:
            print('netdatatransform with number elements: ' + str(len(self.nested_data_transformer_form)))
            forms = forms + '\n       -' + self.nested_data_transformer_form.as_p()
        forms = forms + '</div></div>'
        return mark_safe(forms)

    def save(self, commit=True):
        print('root')
        print('save: ' + str(self.instance.id))
        root_node = super(DataTransformRoot, self).save(commit)
        if hasattr(self,
                   'nested_constants_form') and self.nested_constants_form is not None:
            self.nested_constants_form.instance.refresh_from_db()
            if self.nested_constants_form.is_valid():
                self.nested_constants_form.save(commit)
            else:
                print(self.nested_constants_form.errors)
        if hasattr(self,
                   'nested_hardware_outputs_form') and self.nested_hardware_outputs_form is not None:

            if self.nested_hardware_outputs_form.is_valid():
                self.nested_hardware_outputs_form.save(commit)
            else:
                print(self.nested_hardware_outputs_form.errors)
        if hasattr(self,
                   'nested_hardware_stats_form') and self.nested_hardware_stats_form is not None:
            self.nested_hardware_stats_form.instance.refresh_from_db()

            if self.nested_hardware_stats_form.is_valid():
                self.nested_hardware_stats_form.save(commit)
            else:
                print(self.nested_hardware_stats_form.errors)
        if hasattr(self,
                   'nested_data_transformer_form') and self.nested_data_transformer_form is not None:
            self.nested_data_transformer_form.instance.refresh_from_db()

            if self.nested_data_transformer_form.is_valid():
                self.nested_data_transformer_form.save(commit)
            else:
                print(self.nested_data_transformer_form.errors)
        root_node.refresh_from_db()
        return root_node.get_root()

    class Meta:
        model = DataTransformer
        fields = ['id', 'accessory', 'type']
# DataTransformerFormset = form_factory(DataTransformer,formset=DataTransformerForm)
