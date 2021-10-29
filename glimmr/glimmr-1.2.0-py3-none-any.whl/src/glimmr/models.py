from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SystemData:
    auto_disabled: bool
    auto_remove_devices: bool
    auto_update: bool
    default_set: bool
    enable_auto_brightness: bool
    enable_auto_disable: bool
    enable_letter_box: bool
    enable_pillar_box: bool
    skip_demo: bool
    skip_tour: bool
    use_center: bool
    abl_amps: int
    abl_volts: int
    audio_gain: float
    audio_min: float
    ambient_scene: int
    audio_scene: int
    auto_disable_delay: int
    auto_discovery_frequency: int
    auto_remove_devices_after: int
    auto_update_time: int
    baud_rate: int
    bottom_count: int
    cam_type: int
    capture_mode: int
    crop_delay: int
    device_mode: int
    discovery_timeout: int
    h_sectors: int
    led_count: int
    left_count: int
    open_rgb_port: int
    preview_mode: int
    previous_mode: int
    right_count: int
    sector_count: int
    stream_mode: int
    top_count: int
    usb_selection: int
    v_sectors: int
    ambient_color: str
    device_name: str
    ds_ip: str
    open_rgb_ip: str
    rec_dev: str
    theme: str
    time_zone: str
    units: int
    black_level: int
    crop_black_level: int
    version: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> SystemData:
        """Return Info object from GLIMMR API response.

        Args:
            data: The data from the GLIMMR device API.

        Returns:
            A info object.
        """
        print(data)
        return SystemData(
            auto_disabled=data.get("autoDisabled", "UNKNOWN"),
            auto_remove_devices=data.get("autoRemoveDevices", "UNKNOWN"),
            auto_update=data.get("autoUupdate", "UNKNOWN"),
            default_set=data.get("defaultSet", "UNKNOWN"),
            enable_auto_brightness=data.get("enableAutoBrightness", "UNKNOWN"),
            enable_auto_disable=data.get("enableAutoDisable", "UNKNOWN"),
            enable_letter_box=data.get("enableLetterBox", "UNKNOWN"),
            enable_pillar_box=data.get("enablePillarBox", "UNKNOWN"),
            skip_demo=data.get("skipDemo", "UNKNOWN"),
            skip_tour=data.get("skipTour", "UNKNOWN"),
            use_center=data.get("useCenter", "UNKNOWN"),
            abl_amps=data.get("ablAmps", "UNKNOWN"),
            abl_volts=data.get("ablVolts", "UNKNOWN"),
            audio_gain=data.get("audioGain", "UNKNOWN"),
            audio_min=data.get("audioMin", "UNKNOWN"),
            ambient_scene=data.get("ambientScene", "UNKNOWN"),
            audio_scene=data.get("audioScene", "UNKNOWN"),
            auto_disable_delay=data.get("autoDisableDelay", "UNKNOWN"),
            auto_discovery_frequency=data.get("autoDiscoveryFrequency", "UNKNOWN"),
            auto_remove_devices_after=data.get("autoRemoveDevicesAfter", "UNKNOWN"),
            auto_update_time=data.get("autoUpdateTime", "UNKNOWN"),
            baud_rate=data.get("baudRate", "UNKNOWN"),
            bottom_count=data.get("bottomCount", "UNKNOWN"),
            cam_type=data.get("camType", "UNKNOWN"),
            capture_mode=data.get("captureMode", "UNKNOWN"),
            crop_delay=data.get("cropDelay", "UNKNOWN"),
            device_mode=data.get("deviceMode", "UNKNOWN"),
            discovery_timeout=data.get("discoveryTimeout", "UNKNOWN"),
            h_sectors=data.get("hSectors", "UNKNOWN"),
            led_count=data.get("ledCount", "UNKNOWN"),
            left_count=data.get("leftCount", "UNKNOWN"),
            open_rgb_port=data.get("openRgbPort", "UNKNOWN"),
            preview_mode=data.get("previewMode", "UNKNOWN"),
            previous_mode=data.get("previousMode", "UNKNOWN"),
            right_count=data.get("rightCount", "UNKNOWN"),
            sector_count=data.get("sectorCount", "UNKNOWN"),
            stream_mode=data.get("streamMode", "UNKNOWN"),
            top_count=data.get("topCount", "UNKNOWN"),
            usb_selection=data.get("usbSelection", "UNKNOWN"),
            v_sectors=data.get("vSectors", "UNKNOWN"),
            ambient_color=data.get("ambientColor", "UNKNOWN"),
            device_name=data.get("deviceName", "UNKNOWN"),
            ds_ip=data.get("dsIp", "UNKNOWN"),
            open_rgb_ip=data.get("openRgbIp", "UNKNOWN"),
            rec_dev=data.get("recDev", "UNKNOWN"),
            theme=data.get("theme", "UNKNOWN"),
            time_zone=data.get("timeZone", "UNKNOWN"),
            units=data.get("units", "UNKNOWN"),
            black_level=data.get("blackLevel", "UNKNOWN"),
            crop_black_level=data.get("cropBlackLevel", "UNKNOWN"),
            version=data.get("version", "UNKNOWN")
        )

    def to_dict(self):
        return {
            "autoDisabled": self.auto_disabled,
            "autoRemoveDevices": self.auto_remove_devices,
            "autoUpdate": self.auto_update,
            "defaultSet": self.default_set,
            "enableAutoBrightness": self.enable_auto_brightness,
            "enableAutoDisable": self.enable_auto_disable,
            "enableLetterBox": self.enable_letter_box,
            "enablePillarBox": self.enable_pillar_box,
            "skipDemo": self.skip_demo,
            "skipTour": self.skip_tour,
            "useCenter": self.use_center,
            "ablAmps": self.abl_amps,
            "ablVolts": self.abl_volts,
            "audioGain": self.audio_gain,
            "audioMin": self.audio_min,
            "ambientScene": self.ambient_scene,
            "audioScene": self.audio_scene,
            "autoDisableDelay": self.auto_disable_delay,
            "autoDiscoveryFrequency": self.auto_discovery_frequency,
            "autoRemoveDevicesAfter": self.auto_remove_devices_after,
            "autoUpdateTime": self.auto_update_time,
            "baudRate": self.baud_rate,
            "bottomCount": self.bottom_count,
            "camType": self.cam_type,
            "captureMode": self.capture_mode,
            "cropDelay": self.crop_delay,
            "deviceMode": self.device_mode,
            "discoveryTimeout": self.discovery_timeout,
            "hSectors": self.h_sectors,
            "ledCount": self.led_count,
            "leftCount": self.left_count,
            "openRgbPort": self.open_rgb_port,
            "previewMode": self.preview_mode,
            "previousMode": self.previous_mode,
            "rightCount": self.right_count,
            "sectorCount": self.sector_count,
            "streamMode": self.stream_mode,
            "topCount": self.top_count,
            "usbSelection": self.usb_selection,
            "vSectors": self.v_sectors,
            "ambientColor": self.ambient_color,
            "deviceName": self.device_name,
            "dsIp": self.ds_ip,
            "openRgbIp": self.open_rgb_ip,
            "recDev": self.rec_dev,
            "theme": self.theme,
            "timeZone": self.time_zone,
            "units": self.units,
            "blackLevel": self.black_level,
            "cropBlackLevel": self.crop_black_level,
            "version": self.version
        }
