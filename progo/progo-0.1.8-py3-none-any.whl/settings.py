import attr
from progo.params import (
    Resolution,
    FPS,
    AutoOff,
    LED,
    VideoFOV,
    PhotoFOV,
    MultishotFOV,
    MaxLensMode,
)


SETTINGS_ATTR_INT_MAP = {
    "resolution": 2,
    "fps": 3,
    "internal_5": 5,
    "internal_6": 6,
    "internal_13": 13,
    "internal_19": 19,
    "internal_24": 24,
    "internal_30": 30,
    "internal_31": 31,
    "internal_32": 32,
    "internal_37": 37,
    "internal_41": 41,
    "internal_42": 42,
    "internal_43": 43,
    "internal_44": 44,
    "internal_45": 45,
    "internal_47": 47,
    "internal_48": 48,
    "internal_54": 54,
    "auto_off": 59,
    "internal_60": 60,
    "internal_61": 61,
    "internal_62": 62,
    "internal_64": 64,
    "internal_65": 65,
    "internal_66": 66,
    "internal_67": 67,
    "internal_68": 68,
    "internal_69": 69,
    "internal_75": 75,
    "internal_76": 76,
    "internal_79": 79,
    "internal_83": 83,
    "internal_84": 84,
    "internal_85": 85,
    "internal_86": 86,
    "internal_87": 87,
    "internal_88": 88,
    "led": 91,
    "internal_96": 96,
    "internal_102": 102,
    "internal_103": 103,
    "internal_104": 104,
    "internal_105": 105,
    "internal_106": 106,
    "internal_111": 111,
    "internal_112": 112,
    "internal_114": 114,
    "internal_115": 115,
    "internal_116": 116,
    "internal_117": 117,
    "internal_118": 118,
    "video_fov": 121,
    "photo_fov": 122,
    "multi_shot_fov": 123,
    "internal_124": 124,
    "internal_125": 125,
    "internal_126": 126,
    "internal_128": 128,
    "shortcut_lower_left": 129,
    "shortcut_lower_right": 130,
    "shortcut_upper_left": 131,
    "shortcut_upper_right": 132,
    "internal_133": 133,
    "internal_134": 134,
    "internal_135": 135,
    "internal_139": 139,
    "internal_144": 144,
    "internal_145": 145,
    "internal_146": 146,
    "internal_147": 147,
    "internal_148": 148,
    "internal_149": 149,
    "internal_153": 153,
    "internal_14": 154,
    "internal_155": 155,
    "internal_156": 156,
    "internal_157": 157,
    "internal_158": 158,
    "internal_159": 159,
    "internal_160": 160,
    "internal_161": 161,
    "max_lens_mode": 162,
    "internal_163": 163,
    "internal_164": 164,
    "internal_165": 165,
    "internal_166": 166,
    "internal_167": 167,
    "internal_168": 168,
    "internal_169": 169,
}


@attr.s
class CameraSettings:
    resolution = attr.ib(converter=Resolution)
    fps = attr.ib(converter=FPS)
    internal_5 = attr.ib()
    internal_6 = attr.ib()
    internal_13 = attr.ib()
    internal_19 = attr.ib()
    internal_24 = attr.ib()
    internal_30 = attr.ib()
    internal_31 = attr.ib()
    internal_32 = attr.ib()
    internal_37 = attr.ib()
    internal_41 = attr.ib()
    internal_42 = attr.ib()
    internal_43 = attr.ib()
    internal_44 = attr.ib()
    internal_45 = attr.ib()
    internal_47 = attr.ib()
    internal_48 = attr.ib()
    internal_54 = attr.ib()
    auto_off = attr.ib(converter=AutoOff)
    internal_60 = attr.ib()
    internal_61 = attr.ib()
    internal_62 = attr.ib()
    internal_64 = attr.ib()
    internal_65 = attr.ib()
    internal_66 = attr.ib()
    internal_67 = attr.ib()
    internal_68 = attr.ib()
    internal_69 = attr.ib()
    internal_75 = attr.ib()
    internal_76 = attr.ib()
    internal_79 = attr.ib()
    internal_83 = attr.ib()
    internal_84 = attr.ib()
    internal_85 = attr.ib()
    internal_86 = attr.ib()
    internal_87 = attr.ib()
    internal_88 = attr.ib()
    led = attr.ib(converter=LED)
    internal_96 = attr.ib()
    internal_102 = attr.ib()
    internal_103 = attr.ib()
    internal_104 = attr.ib()
    internal_105 = attr.ib()
    internal_106 = attr.ib()
    internal_111 = attr.ib()
    internal_112 = attr.ib()
    internal_114 = attr.ib()
    internal_115 = attr.ib()
    internal_116 = attr.ib()
    internal_117 = attr.ib()
    internal_118 = attr.ib()
    video_fov = attr.ib()
    photo_fov = attr.ib()
    multi_shot_fov = attr.ib(converter=MultishotFOV)
    internal_124 = attr.ib()
    internal_125 = attr.ib()
    internal_126 = attr.ib()
    internal_128 = attr.ib()
    shortcut_lower_left = attr.ib()
    shortcut_lower_right = attr.ib()
    shortcut_upper_left = attr.ib()
    shortcut_upper_right = attr.ib()
    internal_133 = attr.ib()
    internal_134 = attr.ib()
    internal_135 = attr.ib()
    internal_139 = attr.ib()
    internal_144 = attr.ib()
    internal_145 = attr.ib()
    internal_146 = attr.ib()
    internal_147 = attr.ib()
    internal_148 = attr.ib()
    internal_149 = attr.ib()
    internal_153 = attr.ib()
    internal_14 = attr.ib()
    internal_155 = attr.ib()
    internal_156 = attr.ib()
    internal_157 = attr.ib()
    internal_158 = attr.ib()
    internal_159 = attr.ib()
    internal_160 = attr.ib()
    internal_161 = attr.ib()
    max_lens_mode = attr.ib()
    internal_163 = attr.ib()
    internal_164 = attr.ib()
    internal_165 = attr.ib()
    internal_166 = attr.ib()
    internal_167 = attr.ib()
    internal_168 = attr.ib()
    internal_169 = attr.ib()

    @classmethod
    def from_dict(cls, settings: dict):
        mapped_attrs = {
            k: settings.get(str(v)) for k, v in SETTINGS_ATTR_INT_MAP.items()
        }
        return cls(**mapped_attrs)
