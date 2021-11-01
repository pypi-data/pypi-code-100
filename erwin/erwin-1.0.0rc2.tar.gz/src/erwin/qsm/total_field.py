import json
import re

import nibabel
import numpy
import spire

from .. import entrypoint

class TotalField(spire.TaskFactory):
    """ Unwrapping and total susceptibility field of the MEDI toolbox.
    """
    
    def __init__(self, magnitude, phase, f_total, medi_toolbox, sd_noise=None):
        spire.TaskFactory.__init__(self, str(f_total))
        
        self.file_dep = [magnitude, phase]
        self.targets = [f_total]
        if sd_noise is not None:
            self.targets.append(sd_noise)
        
        self.actions = [
            (
                TotalField.total_field, (
                    magnitude, phase, medi_toolbox, f_total, sd_noise))]
    
    def total_field(
            magnitude_path, phase_path, medi_toolbox_path, f_total_path,
            sd_noise_path):
        
        import meg
        
        magnitude_image = nibabel.load(magnitude_path)
        phase_image = nibabel.load(phase_path)
        signal = magnitude_image.get_fdata() * numpy.exp(-1j*phase_image.get_fdata())
        
        with meg.Engine() as engine:
            engine("run('{}/MEDI_set_path.m');".format(medi_toolbox_path))
            
            engine["signal"] = signal
            # MEDI toolbox expects shape as a floating point array
            engine["shape"] = numpy.array(signal.shape[:3], float)
            
            # Compute the wrapped total field, as γ ΔB ΔTE [rad]
            """
            10.1002/mrm.21710
            From the multiecho data, the field shift was extracted on a 
            voxel‐by‐voxel basis using the following model for phase temporal 
            evolution φ(t) = φ0 + γΔBt. Here φ0 accounts for initial phase, γ 
            is the gyromagnetic ratio, and ΔB the field inhomogeneities. A 
            weighted linear least‐square algorithm was applied. The estimated 
            phase noise Δφ_{p,TE} = ΔS/S{p,TE} was used to weight each echo 
            phase, where S_{p,TE} denotes the signal amplitude at each echo and
            voxel, and where the noise ΔS = (σRe + σlm)/2 was defined as the
            average of the standard deviation of the real σ_{Re} and imaginary 
            parts σ_{lm} of the signal in a sufficiently large region of 
            background air with no signal. An error on the estimated ΔB was 
            readily derived from the linear fit. Error in the noise regions, as
            identified by the segmentation procedure described in the following
            section, was set to infinity, or equivalently, the corresponding
            diagonal elements in the weighting matrix (Eq. [9]) were set to 0.
            Finally, gradient warping was corrected in 3D using spherical
            harmonics coefficients provided by the scanner manufacturer.
            
            NOTE: two versions, one with equal TE, one with unequal TE
            """
            engine("[f_total_wrapped, sd_noise, residuals, phi_0] = Fit_ppm_complex(signal);")
            
            # Unwrap the total field
            engine("magnitude = sqrt(sum(abs(signal).^2, 4));")
            engine("f_total = unwrapPhase(magnitude, f_total_wrapped, shape);")
            engine("phi_0 = unwrapPhase(magnitude, phi_0, shape);")
            f_total = engine["f_total"]
            sd_noise = engine["sd_noise"]
            phi_0 = engine["phi_0"]
        
        nibabel.save(
            nibabel.Nifti1Image(f_total, magnitude_image.affine), f_total_path)
        nibabel.save(
            nibabel.Nifti1Image(phi_0, magnitude_image.affine), "phi_0.nii.gz")
        if sd_noise_path is not None:
            nibabel.save(
                nibabel.Nifti1Image(sd_noise, magnitude_image.affine), 
                sd_noise_path)

def main():
    return entrypoint(
        TotalField, [
            ("--magnitude", {"help": "Multi-echo magnitude image"}),
            ("--phase", {"help": "Multi-echo phase image"}),
            ("--f-total", {"help": "Total field image"}),
            ("--sd-noise", {"nargs": "?", "help": "Total field image"}),
            (
                "--medi", {
                    "dest": "medi_toolbox", 
                    "help": "Path to the MEDI toolbox"})])
