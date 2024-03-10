"""
PROBLEM: NMRglue does not read 1D Sparky spectra!
"""
import nmrglue as ng


CBCAcoNH_ucsf = "/home2/srv/NMR/Peak_Picking/Ubiquitin/CBCAcoNH_slices/C_Nbin53_HNbin365.ucsf"
sdic, sdata = ng.sparky.read(CBCAcoNH_ucsf)
sudic = ng.sparky.guess_udic(sdic, sdata)

C = ng.convert.converter()
C.from_sparky(sdic, sdata, sudic)
pdic, pdata = C.to_pipe()

output_file_path = "/srv/NMR/Peak_Picking/Ubiquitin/C_Nbin53_HNbin365.ft2"

ng.pipe.write(output_file_path, pdic, pdata, overwrite=True)
