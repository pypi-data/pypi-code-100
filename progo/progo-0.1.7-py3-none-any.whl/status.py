import attr
from attr.setters import convert
import requests

from progo.params import (
    AnalyticsState,
    ExposureMode,
    Flatmode,
    MediaModMicStatus,
    MediaModStatus,
    OTAStatus,
    Orientation,
    PairState,
    PairType,
    PresetGroup,
    SDStatus,
    TimeWarpSpeed,
    WAPState,
    WirelessBand,
)


STATUS_ATTR_INT_MAP = {
    "battery_present": 1,
    "battery_level": 2,
    "external_battery_present": 3,
    "external_battery_level": 4,
    "system_hot": 6,
    "system_busy": 8,
    "quick_capture": 9,
    "encoding": 10,
    "lcd_lock_active": 11,
    "video_progress": 13,
    "internal_14": 14,
    "wireless_enabled": 17,
    "pair_state": 19,
    "pair_type": 20,
    "pair_time": 21,
    "wap_scan_state": 22,
    "wap_scan_time": 23,
    "wap_prov_stat": 24,
    "remote_ctrl_version": 26,
    "remote_ctrl_connected": 27,
    "pair_state2": 28,
    "wlan_ssid": 29,
    "wap_ssid": 30,
    "app_count": 31,
    "preview_enabled": 32,
    "sd_status": 33,
    "photos_remaining": 34,
    "video_remaining": 35,
    "num_group_photo": 36,
    "num_group_video": 37,
    "num_total_photo": 38,
    "num_total_video": 39,
    "date_time": 40,
    "ota_status": 41,
    "download_cancel_pending": 42,
    "mode_group": 43,
    "locate_active": 44,
    "internal_46": 46,
    "internal_47": 47,
    "internal_48": 48,
    "multi_count_down": 49,
    "space_remaining": 54,
    "streaming_supp": 55,
    "wifi_bars": 56,
    "current_time_ms": 57,
    "num_hilights": 58,
    "last_hilight": 59,
    "next_poll": 60,
    "analytics_ready": 61,
    "analytics_size": 62,
    "in_context_menu": 63,
    "timelapse_remaining": 64,
    "exposure_type": 65,
    "exposure_x": 66,
    "exposure_y": 67,
    "gps_stat": 68,
    "wap_state": 69,
    "battery_percent": 70,
    "accessory_mic_status": 74,
    "digital_zoom": 75,
    "wireless_band": 76,
    "digital_zoom_active": 77,
    "mobile_video": 78,
    "first_time": 79,
    "sec_sd_stat": 80,
    "band_5ghz_available": 81,
    "system_ready": 82,
    "batt_ok_ota": 83,
    "capture_delay": 84,
    "video_low_temp": 85,
    "orientation": 86,
    "thermal_mit_mode": 87,
    "zoom_encoding": 88,
    "flatmode_id": 89,
    "internal_90": 90,
    "logs_ready": 91,
    "timewarp_1x_active": 92,
    "video_presets": 93,
    "photo_presets": 94,
    "timelapse_presets": 95,
    "preset_group": 96,
    "active_preset": 97,
    "preset_modified": 98,
    "live_burst_remaining": 99,
    "live_burst_total": 100,
    "capture_delay_active": 101,
    "media_mod_mic_status": 102,
    "timewarp_speed_ramp": 103,
    "linux_core_active": 104,
    "camera_lens_type": 105,
    "video_hindsight": 106,
    "scheduled_preset": 107,
    "scheduled_capture": 108,
    "creating_preset": 109,
    "media_mod_status": 110,
    "sd_rating_check_error": 111,
    "sd_write_speed_error": 112,
    "turbo_mode": 113,
    "camera_control": 114,
    "usb_connected": 115,
}


@attr.s
class CameraStatus:
    battery_present = attr.ib(converter=bool)
    battery_level = attr.ib()
    external_battery_present = attr.ib(converter=bool)
    external_battery_level = attr.ib()
    system_hot = attr.ib(converter=bool)
    system_busy = attr.ib(converter=bool)
    quick_capture = attr.ib()
    encoding = attr.ib(converter=bool)
    lcd_lock_active = attr.ib(converter=bool)
    video_progress = attr.ib()
    internal_14 = attr.ib()
    wireless_enabled = attr.ib(converter=bool)
    pair_state = attr.ib()
    pair_type = attr.ib(converter=PairType)
    pair_time = attr.ib()
    wap_scan_state = attr.ib()
    wap_scan_time = attr.ib()
    wap_prov_stat = attr.ib()
    remote_ctrl_version = attr.ib()
    remote_ctrl_connected = attr.ib(converter=bool)
    pair_state2 = attr.ib()
    wlan_ssid = attr.ib()
    wap_ssid = attr.ib()
    app_count = attr.ib()
    preview_enabled = attr.ib(converter=bool)
    sd_status = attr.ib(converter=SDStatus)
    photos_remaining = attr.ib()
    video_remaining = attr.ib()
    num_group_photo = attr.ib()
    num_group_video = attr.ib()
    num_total_photo = attr.ib()
    num_total_video = attr.ib()
    date_time = attr.ib()
    ota_status = attr.ib(converter=OTAStatus)
    download_cancel_pending = attr.ib(converter=bool)
    mode_group = attr.ib()
    locate_active = attr.ib()
    internal_46 = attr.ib()
    internal_47 = attr.ib()
    internal_48 = attr.ib()
    multi_count_down = attr.ib()
    space_remaining = attr.ib()
    streaming_supp = attr.ib()
    wifi_bars = attr.ib()
    current_time_ms = attr.ib()
    num_hilights = attr.ib()
    last_hilight = attr.ib()
    next_poll = attr.ib()
    analytics_ready = attr.ib(converter=AnalyticsState)
    analytics_size = attr.ib()
    in_context_menu = attr.ib()
    timelapse_remaining = attr.ib()
    exposure_type = attr.ib(converter=ExposureMode)
    exposure_x = attr.ib()
    exposure_y = attr.ib()
    gps_stat = attr.ib()
    wap_state = attr.ib(converter=WAPState)
    battery_percent = attr.ib()
    accessory_mic_status = attr.ib()
    digital_zoom = attr.ib()
    wireless_band = attr.ib(converter=WirelessBand)
    digital_zoom_active = attr.ib(converter=bool)
    mobile_video = attr.ib()
    first_time = attr.ib()
    sec_sd_stat = attr.ib()
    band_5ghz_available = attr.ib()
    system_ready = attr.ib()
    batt_ok_ota = attr.ib()
    capture_delay = attr.ib()
    video_low_temp = attr.ib()
    orientation = attr.ib(converter=Orientation)
    thermal_mit_mode = attr.ib()
    zoom_encoding = attr.ib()
    flatmode_id = attr.ib(converter=Flatmode)
    internal_90 = attr.ib()
    logs_ready = attr.ib()
    timewarp_1x_active = attr.ib()
    video_presets = attr.ib()
    photo_presets = attr.ib()
    timelapse_presets = attr.ib()
    preset_group = attr.ib(converter=PresetGroup)
    active_preset = attr.ib()
    preset_modified = attr.ib()
    live_burst_remaining = attr.ib()
    live_burst_total = attr.ib()
    capture_delay_active = attr.ib(converter=bool)
    media_mod_mic_status = attr.ib(converter=MediaModMicStatus)
    timewarp_speed_ramp = attr.ib(converter=TimeWarpSpeed)
    linux_core_active = attr.ib(converter=bool)
    camera_lens_type = attr.ib()
    video_hindsight = attr.ib()
    scheduled_preset = attr.ib()
    scheduled_capture = attr.ib()
    creating_preset = attr.ib()
    media_mod_status = attr.ib(converter=MediaModStatus)
    sd_rating_check_error = attr.ib()
    sd_write_speed_error = attr.ib()
    turbo_mode = attr.ib()
    camera_control = attr.ib()
    usb_connected = attr.ib(converter=bool)

    @classmethod
    def from_dict(cls, status: dict):
        mapped_attrs = {k: status.get(str(v)) for k, v in STATUS_ATTR_INT_MAP.items()}
        return cls(**mapped_attrs)
