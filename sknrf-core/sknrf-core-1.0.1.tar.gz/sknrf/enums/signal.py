from collections import OrderedDict
from enum import Enum

from sknrf.device.signal import tf
from sknrf.widget.propertybrowser.view import Domain

transform_map = OrderedDict([
    (Domain.TF, tf.tf),
    (Domain.FF, tf.ff),
    (Domain.FT, tf.ft),
    (Domain.TT, tf.tt),
])

transform_label_map = OrderedDict([
    (Domain.TF, "Envelope"),
    (Domain.FF, "Frequency"),
    (Domain.FT, "Switching"),
    (Domain.TT, "Transient"),
])

transform_icon_map = {
    Domain.TF: ":/PNG/green/32/form_oval.png",
    Domain.FF: ":/PNG/red/32/circled_plus.png",
    Domain.FT: ":/PNG/blue/32/circled_plus.png",
    Domain.TT: ":/PNG/cyan/32/circled_plus.png",
}

transform_color_map = {
    Domain.TF: "green",
    Domain.FF: "red",
    Domain.FT: "blue",
    Domain.TT: "cyan",
}

transform_xlabel_map = {
    Domain.TF: r"$time$ $[s]$",
    Domain.FF: r"$freq$ $[Hz]$",
    Domain.FT: r"$time$ $[s]$",
    Domain.TT: r"$time$ $[s]$",
}
