from koil.qt import FutureWrapper
from mikro.schema import Representation, RepresentationVariety
from napari import Viewer
import xarray as xr
from qtpy import QtWidgets
from qtpy.QtCore import Signal, QObject
import logging

logger = logging.getLogger(__name__)


class DownloadIndicator(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = QtWidgets.QLabel("Downloading")

    def setLabel(self, rep: Representation):
        self.label.setText(f"Downloading {rep.name}")


class StageHelper(QObject):
    openStack = Signal(xr.DataArray, Representation)
    openLabels = Signal(xr.DataArray, Representation)
    openImage = Signal(xr.DataArray, Representation)
    downloadingImage = Signal(Representation)
    downloadingDone = Signal(Representation)

    def __init__(self, viewer: Viewer, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.viewer = viewer

        self.downloadingDialog = DownloadIndicator()

        self.openImage.connect(self.open_xarray_as_rgb)
        self.openStack.connect(self.open_xarray_as_stack)
        self.openLabels.connect(self.open_xarray_as_labels)

        self.downloadingImage.connect(self.on_image_download)
        self.downloadingDone.connect(self.on_image_downloaded)

    def on_image_download(self, rep: Representation):
        self.downloadingDialog.setLabel(rep)
        self.downloadingDialog.show()

    def on_image_downloaded(self, rep: Representation):
        self.downloadingDialog.hide()

    def open_xarray_as_stack(self, array: xr.DataArray, rep: Representation):
        self.viewer.add_image(
            array,
            rgb=False,
            name=rep.name,
            metadata={"rep": rep},
        )  # why this werid transposing... hate napari

    def open_xarray_as_rgb(self, array: xr.DataArray, rep: Representation):
        self.viewer.add_image(
            array,
            rgb=True,
            name=rep.name,
            metadata={"rep": rep},
        )  # why this werid transposing... hate napari

    def open_xarray_as_labels(self, array: xr.DataArray, rep: Representation):
        self.viewer.add_labels(
            rep,
            rgb=False,
            name=rep.name,
            metadata={"rep": rep},
        )  # why this werid transposing... hate napari

    def open_as_layer(self, rep: Representation, stream=True):
        stream = False
        array = rep.data.squeeze()

        if (
            rep.variety == RepresentationVariety.VOXEL
            or rep.variety == RepresentationVariety.UNKNOWN
        ):
            if "t" in array.dims:
                raise NotImplementedError("Time series are not supported yet")

            elif "z" in array.dims:
                if "c" in array.dims:
                    array = array.transpose(*list("zxyc"))
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)

                    self.openStack.emit(array, rep)
                else:
                    array = array.transpose(*list("zxy"))
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)

                    self.openStack.emit(array, rep)

            elif "c" in array.dims:
                if array.sizes["c"] == 3:
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)

                    self.openImage.emit(array, rep)
                else:
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)
                    self.openStack.emit(array, rep)
            elif "x" in array.dims and "y" in array.dims:
                if not stream:
                    self.downloadingImage.emit(rep)
                    array = array.compute()
                    self.downloadingDone.emit(rep)
                self.openStack.emit(array, rep)
            else:
                raise NotImplementedError(f"What the fuck??? {array.dims}")

        elif rep.variety == RepresentationVariety.MASK:
            if "t" in array.dims:
                raise NotImplementedError("Time series are not supported yet")

            if "z" in array.dims:
                if "c" in array.dims:
                    raise NotImplementedError("We have not managed to do things yet...")
                else:
                    array = array.transpose(*list("zxy"))
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)
                    self.openLabels.emit(array, rep)
        else:
            raise NotImplementedError(
                f"Cannot open Representation of Variety {rep.variety}"
            )

    def get_active_layer_as_xarray(self):
        layer = self.viewer.active_layer
        data = layer.data
        ndim = layer.ndim

        if ndim == 2:
            # first two dimensions is x,y and then channel
            if layer.rgb:
                # We are dealing with an rgb image
                stack = (
                    xr.DataArray(data, dims=list("xyc"))
                    .expand_dims("z")
                    .expand_dims("t")
                    .transpose(*list("xyczt"))
                )
            else:
                stack = (
                    xr.DataArray(data, dims=list("xy"))
                    .expand_dims("c")
                    .expand_dims("z")
                    .expand_dims("t")
                    .transpose(*list("xyczt"))
                )

        if ndim == 3:
            # first three dimensios is z,x,y and then channel?
            if len(data.shape) == 3:
                stack = (
                    xr.DataArray(data, dims=list("zxy"))
                    .expand_dims("c")
                    .expand_dims("t")
                    .transpose(*list("xyczt"))
                )
            else:
                raise NotImplementedError("Dont know")

        return stack
