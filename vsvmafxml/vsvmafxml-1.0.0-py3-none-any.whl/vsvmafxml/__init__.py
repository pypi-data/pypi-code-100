import vapoursynth as vs
from defusedxml.ElementTree import parse


def XmlToProp(clip: vs.VideoNode, xml_file: str) -> vs.VideoNode:
    '''Store per-frame score from log of VMAF as a frame property in clip.'''
    if not isinstance(clip, vs.VideoNode):
        raise vs.Error('XmlToProp: this is not a clip')

    root = parse(xml_file).getroot()

    if root.tag != 'VMAF':
        raise vs.Error('XmlToProp: this is not a log of VMAF')

    if len(root.findall('frames/frame')) != clip.num_frames:
        raise vs.Error('XmlToProp: number of frames in xml file does not match input clip')

    def xml_to_prop(n: int, f: vs.VideoFrame) -> vs.VideoFrame:
        fout = f.copy()
        element = root.find(f"frames/frame[@frameNum='{n}']")
        for attribute in ['vmaf', 'vmaf_neg', 'vmaf_b', 'vmaf_4k',
                          'psnr_y', 'psnr_cb', 'psnr_cr',
                          'psnr_hvs_y', 'psnr_hvs_cb', 'psnr_hvs_cr', 'psnr_hvs',
                          'float_ssim', 'float_ms_ssim',
                          'ciede2000',
                          'cambi']:
            if element.get(attribute):
                fout.props[attribute] = float(element.get(attribute))
        return fout

    return clip.std.ModifyFrame(clips=clip, selector=xml_to_prop)
