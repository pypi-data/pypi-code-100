from mikro.schema import Representation, RepresentationVariety
from napari import Viewer
import xarray as xr 

class StageHelper:

    def __init__(self, viewer: Viewer) -> None:
        self.viewer = viewer

    def open_as_layer(self, rep: Representation):

        if "mask" in rep.tags:
            self.viewer.add_labels(rep.data.sel(c=0).data, name=rep.name, metadata={"rep":rep})
        else:
            array = rep.data.squeeze()

            if rep.variety == RepresentationVariety.VOXEL or rep.variety == RepresentationVariety.UNKNOWN:
                if "t" in array.dims:
                    raise NotImplementedError("Time series are not supported yet")

                elif "z" in array.dims:
                    if "c" in array.dims:
                        raise NotImplementedError("We have not managed to do things yet...")
                    else:
                        self.viewer.add_image(array.transpose(*list("zxy")), rgb=False, name=rep.name, metadata={"rep":rep}) # why this werid transposing... hate napari
                elif "c" in array.dims:
                    if array.sizes["c"] == 3:
                        self.viewer.add_image(array, rgb=True, name=rep.name, metadata={"rep":rep})
                    else:
                        self.viewer.add_image(array, rgb=False, name=rep.name, metadata={"rep":rep})
                elif "x" in array.dims and "y" in array.dims:
                    self.viewer.add_image(array, rgb=False, name=rep.name, metadata={"rep":rep})
                else:
                    raise NotImplementedError(f"What the fuck??? {array.dims}")


            elif rep.variety == RepresentationVariety.MASK:
                if "t" in array.dims:
                    raise NotImplementedError("Time series are not supported yet")

                if "z" in array.dims:
                    if "c" in array.dims:
                        raise NotImplementedError("We have not managed to do things yet...")
                    else:
                        self.viewer.add_labels(array.transpose(*list("zxy")), name=rep.name, metadata={"rep":rep}) # why this werid transposing... hate napari
            else:
                raise NotImplementedError(f"Cannot open Representation of Variety {rep.variety}")


    def get_active_layer_as_xarray(self):
        layer = self.viewer.active_layer
        data = layer.data
        ndim = layer.ndim

        if ndim == 2:
            # first two dimensions is x,y and then channel
            if layer.rgb:
                # We are dealing with an rgb image
                stack = xr.DataArray(data, dims=list("xyc")).expand_dims("z").expand_dims("t").transpose(*list("xyczt"))
            else:
                stack = xr.DataArray(data, dims=list("xy")).expand_dims("c").expand_dims("z").expand_dims("t").transpose(*list("xyczt"))

        if ndim == 3:
            # first three dimensios is z,x,y and then channel?
            if len(data.shape) == 3:
                stack = xr.DataArray(data, dims=list("zxy")).expand_dims("c").expand_dims("t").transpose(*list("xyczt"))
            else:
                raise NotImplementedError("Dont know")

        return stack
