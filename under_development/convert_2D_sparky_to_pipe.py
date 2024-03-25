import nmrglue as ng

# read in the Sparky file
sdic, sdata = ng.sparky.read('/home2/srv/NMR/Peak_Picking/Ubiquitin/15N_HSQC.ucsf')

# convert to NMRPipe format
C = ng.convert.converter()
C.from_sparky(sdic, sdata)
pdic, pdata = C.to_pipe()

# write results to NMRPipe file
ng.pipe.write('/home2/srv/NMR/Peak_Picking/Ubiquitin/15N_HSQC.ft2', pdic, pdata)