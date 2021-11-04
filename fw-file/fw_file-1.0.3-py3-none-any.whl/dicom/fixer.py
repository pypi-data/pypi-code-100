"""DICOM file Flywheel raw data element fixers."""
import dataclasses
import functools
import threading
import typing as t
from contextlib import contextmanager

from pydicom import config as pydicom_config
from pydicom import values
from pydicom.charset import default_encoding
from pydicom.datadict import dictionary_VR, get_entry
from pydicom.dataelem import RawDataElement
from pydicom.multival import MultiValue
from pydicom.util.fixer import fix_mismatch_callback

# Used for tracker data element callback
lock = threading.Lock()

# VRs that allow a backslash in their value.
# http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
backslash_compatible_VRs = {
    "UT",
    "ST",
    "LT",
    "FL",
    "FD",
    "AT",
    "OB",
    "OW",
    "OF",
    "SL",
    "SQ",
    "SS",
    "UL",
    "OB/OW",
    "OW/OB",
    "OB or OW",
    "OW or OB",
    "UN",
    "US",
}


def backslash_in_VM1_string_callback(
    raw_elem: RawDataElement,
    data_element_callback: t.Callable[..., RawDataElement] = None,
    **kwargs,
) -> RawDataElement:  # pylint: disable=invalid-name
    r"""A callback to fix \ in RawDataElement value.

    Fix value of RawDataElement with VM=1 and VR of type string that contains an
    invalid \ character (\ is the array delimiter in Dicom standard) and
    replaces with _. Use case is to handle non-compliant Dicom implementation that
    let e.g. SeriesDescription value containing \.
    """
    if callable(data_element_callback):
        raw_elem = data_element_callback(raw_elem, **kwargs)

    encodings = kwargs.get("encodings")
    if not encodings:
        encodings = [default_encoding]
    elif isinstance(encodings, str):
        encodings = [encodings]

    # Only fix VM for tag supported by get_entry
    try:
        vr, vm, _, _, _ = get_entry(raw_elem.tag)
    except KeyError:  # Not in the dictionary
        return raw_elem

    # only fix if VR matches
    if vr == raw_elem.VR and vm == "1":
        # only fix if is a VR string
        if vr not in backslash_compatible_VRs:
            value = values.convert_value(raw_elem.VR, raw_elem, encodings=encodings)
            if isinstance(value, MultiValue) and len(value) > 1:
                # replace \\ byte with /
                for encoding in encodings:
                    raw_elem = raw_elem._replace(
                        value=raw_elem.value.decode(encoding)
                        .replace("\\", "_")
                        .encode(encoding)
                    )
                    break

    return raw_elem


def handle_none_VR(
    raw_elem: RawDataElement,
) -> RawDataElement:  # pylint: disable=invalid-name
    """A callback to handle VR = None.

    Mirror the handling of pydicom pydicom.dataelement.DataElement_from_raw when
    VR is None but set VR to 'UN' for public tag that are not in the pydicom dictionary
    instead of raising a KeyError.
    """
    VR = raw_elem.VR
    if VR is None:
        try:
            VR = dictionary_VR(raw_elem.tag)
        except KeyError:
            # just read the bytes, no way to know what they mean
            if raw_elem.tag.is_private:
                # for VR for private tags see PS3.5, 6.2.2
                if raw_elem.tag.is_private_creator:
                    VR = "LO"
                else:
                    VR = "UN"

            # group length tag implied in versions < 3.0
            elif raw_elem.tag.element == 0:
                VR = "UL"
            else:
                VR = "UN"
        raw_elem = raw_elem._replace(VR=VR)

    # Testing that conversion can be performed with new VR,
    # If not, set it to OB
    try:
        values.convert_value(raw_elem.VR, raw_elem)
    except Exception:  # pylint: disable=broad-except
        raw_elem = raw_elem._replace(VR="OB")

    return raw_elem


def handle_un_VR(
    raw_elem: RawDataElement,
) -> RawDataElement:  # pylint: disable=invalid-name
    """A callback to handle VR=UN.

    Mirror pydicom.dataelem.DataElement_from_raw when VR is UN but
    instead set VR to 'OB' when decoding value raises with the inferred VR.
    """
    VR = raw_elem.VR
    if (
        VR == "UN"
        and not raw_elem.tag.is_private
        and pydicom_config.replace_un_with_known_vr
    ):
        # handle rare case of incorrectly set 'UN' in explicit encoding
        # see also DataElement.__init__()
        if (
            raw_elem.length == 0xFFFFFFFF
            or raw_elem.value is None
            or len(raw_elem.value) < 0xFFFF
        ):
            try:
                VR = dictionary_VR(raw_elem.tag)
                raw_elem = raw_elem._replace(VR=VR)
            except KeyError:
                pass

        # Testing that conversion can be performed with new VR,
        # If not,  set it to OB
        try:
            values.convert_value(raw_elem.VR, raw_elem)
        except Exception:  # pylint: disable=broad-except
            raw_elem = raw_elem._replace(VR="OB")

    return raw_elem


def converter_exception_callback(
    raw_elem: RawDataElement,
    data_element_callback: t.Callable[..., RawDataElement] = None,
    **kwargs,
) -> RawDataElement:
    """A callback to catch NotImplementedError when raw_elem contains an invalid VR."""
    if callable(data_element_callback):
        raw_elem = data_element_callback(raw_elem, **kwargs)

    if raw_elem.VR is None:
        return handle_none_VR(raw_elem)

    if raw_elem.tag == 0x00080005 and raw_elem.VR == "UN":
        # Handle special case when 0x00080005 (Specific Character Set) is UN which
        # prohibits decoding text VR.
        raw_elem = raw_elem._replace(VR="CS")
        return raw_elem

    try:
        raw_elem = fix_mismatch_callback(raw_elem, **kwargs)
    except NotImplementedError:
        # Handle invalid VR for which a converters are not defined
        if raw_elem.tag in [0xFFFEE0DD]:
            # 0xFFFEE0DD is a sequence delimiter with VR='NONE' in pydicom,
            # To handle the edge case where an extra sequence delimiter is
            # found in the DataSet setting its VR to OB to avoid conversion (setting
            # it to UN or None will raise because VR inference will happen downstream).
            raw_elem = raw_elem._replace(VR="OB")
        else:
            raw_elem = raw_elem._replace(VR="UN")
            raw_elem = handle_un_VR(raw_elem)

    return raw_elem


@dataclasses.dataclass
class TrackingEvent:
    """Dataclass to hold tracking event information."""

    action: str
    field: str
    old: t.Optional[str]
    new: str

    def __repr__(self):
        """Return representation of tracking event."""
        return f"{self.action.capitalize()} {self.field}: {self.old} -> {self.new}"


class TrackedRawDataElement(RawDataElement):
    """RawDataElement subclass adding change tracking to _replace events."""

    def __new__(cls, *args, **kwargs) -> "TrackedRawDataElement":
        """Return a new TrackedRawDataElement instance."""
        tracked = super().__new__(cls, *args, **kwargs)
        tracked.original = RawDataElement(*args, **kwargs)
        tracked.events = []
        return tracked

    # pylint: disable=arguments-differ
    def _replace(self, **kwargs) -> "TrackedRawDataElement":
        """Extend namedtuple _replace with change event tracking."""
        # pylint: disable=no-member
        for key, val in kwargs.items():
            old = getattr(self, key)
            event = TrackingEvent(action="replace", field=key, old=old, new=val)
            self.events.append(event)
        raw_elem = super()._replace(**kwargs)  # calls new
        # NOTE updating the extra namedtuple attrs
        raw_elem.original = self.original
        raw_elem.events = self.events
        return raw_elem

    def export(self) -> dict:
        """Return the original dataelem, the events and the final version as a dict."""
        # pylint: disable=no-member
        return {"original": self.original, "events": self.events, "final": self}


def filter_none_vr_replacement(event: TrackingEvent) -> bool:
    """Return True except for VR=None replacement events."""
    return not (event.field == "VR" and event.old is None)


class Tracker:
    """A class to track RawDataElement in dataset."""

    def __init__(self):
        """Initializes the tracker instance."""
        self.data_elements = []

    def track(self, raw_elem: RawDataElement) -> TrackedRawDataElement:
        """Return a TrackedRawDataElement from a RawDataElement.

        Args:
            raw_elem (RawDataElement): The RawDataElement instance.

        Returns:
            TrackedRawDataElement: The tracked RawDataElement.
        """
        tracked_elem = TrackedRawDataElement(*raw_elem)
        self.data_elements.append(tracked_elem)
        return tracked_elem

    def trim(
        self,
        event_filter: t.Callable[[TrackingEvent], bool] = filter_none_vr_replacement,
    ) -> None:
        """Filter tracked events and remove data elements without any changes.

        Args:
            event_filter (t.Callable[[TrackingEvent], bool]): Event filter that
                should return True given an event which is to be kept. Default:
                filter_none_vr_replacement
        """
        for de in self.data_elements:
            de.events = [evt for evt in de.events if event_filter(evt)]
        self.data_elements = [de for de in self.data_elements if de.events]

    def __repr__(self):
        """Return representation of the tracker instance."""
        strings = []
        for raw_elem in self.data_elements:
            trace = raw_elem.export()
            events = "None"
            if trace["events"]:
                events = "\n" + "\n".join([f"\t{e}" for e in trace["events"]])
            strings.append(
                f"- original: {trace['original']}\n"
                f"  events: {events} \n"
                f"  final: {trace['final']}\n"
            )
        return "\n".join(strings)


def tracker_callback(
    raw_elem: RawDataElement,
    data_element_callback: t.Callable[..., RawDataElement] = None,
    tracker: Tracker = None,
    **kwargs,
) -> RawDataElement:
    """A callback to enable event tracking for raw_elem.

    Args:
        raw_elem (RawDataElement): The RawDataElement instance.
        data_element_callback (callable, optional): A data element callback.
        tracker (Tracker): The Tracker instance.
        **kwargs: Any additional data_element_callback kwargs.

    Returns:
        RawDataElement: The tracked RawDataElement instance modified by
            data_element_callback if defined.
    """
    if tracker:
        raw_elem = tracker.track(raw_elem)
    if data_element_callback:
        raw_elem = data_element_callback(raw_elem, **kwargs)
    return raw_elem


@contextmanager
def pydicom_callback(
    data_element_callback: t.Callable[..., RawDataElement] = None,
    **data_element_callback_kwargs,
) -> t.Iterator[None]:
    """Generic pydicom config context manager.

    Args:
        data_element_callback (Callable): The data_element_callback function.
        **data_element_callback_kwargs (dict): The data_element_callback kwargs.
    """
    data_element_callback_bk = pydicom_config.data_element_callback
    data_element_callback_kwargs_bk = pydicom_config.data_element_callback_kwargs
    pydicom_config.data_element_callback = data_element_callback
    pydicom_config.data_element_callback_kwargs = data_element_callback_kwargs
    try:
        yield
    finally:
        pydicom_config.data_element_callback = data_element_callback_bk
        pydicom_config.data_element_callback_kwargs = data_element_callback_kwargs_bk


@contextmanager
def raw_elem_tracker(tracker: Tracker = None) -> t.Iterator[None]:
    """A contextmanager for tracking changes made to RawDataElement.

    Args:
        tracker (Tracker): The Tracker instance.
    """
    if not tracker:
        yield
        return

    with lock:
        data_element_callback_bk = pydicom_config.data_element_callback
        pydicom_config.data_element_callback = functools.partial(
            tracker_callback,
            data_element_callback=pydicom_config.data_element_callback,
            tracker=tracker,
        )
        try:
            yield
        finally:
            pydicom_config.data_element_callback = data_element_callback_bk
