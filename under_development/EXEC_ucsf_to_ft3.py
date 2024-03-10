import nmrglue as ng
from nmrglue.fileio.pipe import iter3D

CBCAcoNH_ucsf = "/srv/NMR/Peak_Picking/Ubiquitin/CBCAcoNH_MDD.ucsf"
sdic, sdata = ng.sparky.read(CBCAcoNH_ucsf)
sudic = ng.sparky.guess_udic(sdic, sdata)

C = ng.convert.converter()
C.from_sparky(sdic, sdata, sudic)
pdic, pdata = C.to_pipe()

output_file_path = "/srv/NMR/Peak_Picking/Ubiquitin/CBCAcoNH_MDD.fid"

ng.pipe.write(output_file_path, pdic, pdata, overwrite=True)



xiter = iter3D(output_file_path,"x","x")
for dic, YXplane in xiter:
    # process X and Y axis
    xiter.write("/srv/NMR/Peak_Picking/Ubiquitin/CBCAcoNH_MDD_2D_slice%03d.ft2", YXplane, dic)