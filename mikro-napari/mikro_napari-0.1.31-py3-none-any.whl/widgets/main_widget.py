from arkitekt.schema.widgets import SearchWidget
from mikro_napari.helpers.stage import StageHelper
from arkitekt.messages.postman.provide.bounced_provide import BouncedProvideMessage
from qtpy import QtWidgets
from mikro.widgets import MY_TOP_REPRESENTATIONS, MY_TOP_SAMPLES
from mikro.schema import Representation, Sample
from arkitekt.qt.agent import QtAgent
from arkitekt.qt.widgets.magic_bar import MagicBar
from arkitekt.qt.widgets.settings_popup import SettingsPopup
from arkitekt.qt.widgets.provisions import ProvisionsWidget
from arkitekt.qt.widgets.templates import TemplatesWidget
from herre.qt import QtHerre
from fakts.qt import QtFakts
from fakts.grants.qt.qtbeacon import QtSelectableBeaconGrant


class NapariSettings(SettingsPopup):
    def __init__(self, magic_bar, *args, **kwargs):
        super().__init__(magic_bar, *args, **kwargs)
        self.layout.addWidget(ProvisionsWidget(magic_bar.agent))
        self.layout.addWidget(TemplatesWidget(magic_bar.agent))


class NapariMagicBar(MagicBar):
    settingsPopupClass = NapariSettings


class ArkitektWidget(QtWidgets.QWidget):
    def __init__(self, napari_viewer, *args, parent=None, **kwargs) -> None:
        super().__init__(*args, **kwargs, parent=parent)

        # Different Grants

        self.beacon_grant = QtSelectableBeaconGrant()
        self.fakts = QtFakts(
            grants=[self.beacon_grant],
            subapp="napari",
            hard_fakts={
                "herre": {"client_id": "go8CAE78FDf4eLsOSk4wkR4usYbsamcq0yTYqBiY"}
            },
        )
        self.herre = QtHerre()
        self.agent = QtAgent(self)

        self.helper = StageHelper(napari_viewer)

        self.magic_bar = NapariMagicBar(
            self.fakts, self.herre, self.agent, parent=self, darkMode=True
        )

        self.agent.register_ui(
            self.really_show,
            widgets={"rep": MY_TOP_REPRESENTATIONS},
            on_assign=self.really_show,
        )
        self.agent.register_ui(
            self.upload, widgets={"sample": MY_TOP_SAMPLES}, on_assign=self.upload
        )

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.magic_bar)
        self.setLayout(self.layout)

    def really_show(self, rep: Representation):
        """Show Representaiton

        Shows a Dialog for the user to accept or not

        Args:
            rep (Representation): [description]
        """
        self.helper.open_as_layer(rep)

    def upload(self, name: str = None, sample: Sample = None) -> Representation:
        """Upload an Active Image

        Uploads the curently active image on Napari

        Args:
            name (str, optional): How do you want to name the image?
            sample (Sample, optional): Which sample should we put the new image in?

        Returns:
            Representation: The uploaded image from the app
        """
        array = self.helper.get_active_layer_as_xarray()
        print(array)

        return Representation.objects.from_xarray(
            array, name=name, sample=sample, tags=[]
        )
