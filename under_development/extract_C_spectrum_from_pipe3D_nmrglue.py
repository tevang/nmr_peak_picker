import nmrglue as ng
import numpy as np

# TODO: I don't know if the file CBCAcoNH_MDD.ft3 is in the correct NMR Pipe format.

file_path = "/srv/NMR/Peak_Picking/Ubiquitin/CBCAcoNH_MDD.ft3"
pdic, pdata = ng.pipe.read(file_path)
mpdata = ng.fileio.pipe.create_data(pdata)
pshape = ng.fileio.pipe.find_shape(pdic)




hn = ng.pipe.make_uc(pdic, pdata, dim=0)
n = ng.pipe.make_uc(pdic, pdata, dim=1)

uc = {
    "hn": ng.pipe.make_uc(pdic, pdata, dim=0),
    "n": ng.pipe.make_uc(pdic, pdata, dim=1),
    "c": ng.pipe.make_uc(pdic, pdata, dim=2),
}

# Specific N and HN values for filtering
n_ppm = 115.438
hn_ppm = 8.671

"""
The resulting Hc-C slice must contain the following peaks:
      Assignment         w1         w2         w3         w4   Data Height 

          ?-?-?-?      7.136     10.274    115.432      8.670   3139690496 
          ?-?-?-?      6.798     16.217    115.428      8.668    476387584 
          ?-?-?-?      6.938     17.909    115.458      8.674    281673248 
          ?-?-?-?      3.045     35.230    115.437      8.671   1881223808 
          ?-?-?-?      6.666     42.035    132.398      8.007            0 
          ?-?-?-?      3.567     47.979    115.443      8.672    227306352 
          ?-?-?-?      7.135     67.944    115.432      8.669   1433053184 

"""


# Convert N and HN ppm values to bin indices
N_bin_index = uc["n"](n_ppm, "ppm") - 1
HN_bin_index = uc["hn"](hn_ppm, "ppm") - 1

# Hc,C,N,Hn -> Hn,N,Hc,C
reordered_pdata = np.transpose(pdata, (3, 2, 1, 0))
data_slice = reordered_pdata[int(HN_bin_index), int(N_bin_index), :, :].real

def transform_dic(input_dic):
    trans_dic = input_dic.copy()

    # N,Hn,C,Hc -> Hc,C,N,Hn
    key_mapping = {
        'FDF1': 'TEMP_FDF3',  # Temporarily rename to avoid overwrite
        'FDF2': 'TEMP_FDF4',  # Temporarily rename to avoid overwrite
        'FDF3': 'FDF1',
        'FDF4': 'FDF2',
    }

    # Update keys according to the mapping
    for old_key, new_key in key_mapping.items():
        for k in list(trans_dic.keys()):
            if k.startswith(old_key):
                trans_dic[k.replace(old_key, new_key)] = trans_dic.pop(k)

    # Rename temporary keys to their final names
    for old_key, new_key in {'TEMP_FDF4': 'FDF4', 'TEMP_FDF3': 'FDF3'}.items():
        for k in list(trans_dic.keys()):
            if k.startswith(old_key):
                trans_dic[k.replace(old_key, new_key)] = trans_dic.pop(k)

    nodim_dic = {'FDMAGIC': 0.0, 'FDFLTFORMAT': 4008636160.0, 'FDFLTORDER': 2.3450000286102295,
                 'FDSIZE': trans_dic['FDF2FTSIZE'],                         # CHANGED
                 'FDREALSIZE': trans_dic['FDF2FTSIZE'],                     # CHANGED
                 'FDSPECNUM': trans_dic['FDF1FTSIZE'],                      # CHANGED
                 'FDQUADFLAG': 1.0, 'FD2DPHASE': 2.0, 'FDTRANSPOSED': 0.0,  # CHANGED
                 'FDDIMCOUNT': 2.0,                                         # CHANGED
                 'FDDIMORDER': [2.0, 1.0, 3.0, 4.0],                        # CHANGED
                 'FDDIMORDER1': 2.0,                                        # CHANGED
                 'FDDIMORDER2': 1.0,                                        # CHANGED
                 'FDDIMORDER3': 3.0,                                        # CHANGED
                 'FDDIMORDER4': 4.0,                                        # CHANGED
                 'FDNUSDIM': 0.0, 'FDPIPEFLAG': 0.0, 'FDCUBEFLAG': 0.0, 'FDPIPECOUNT': 0.0, 'FDSLICECOUNT': 0.0,
                 'FDSLICECOUNT1': 0.0,
                 'FDFILECOUNT': 1.0,                                        # CHANGED
                 'FDTHREADCOUNT': 0.0, 'FDTHREADID': 0.0, 'FDFIRSTPLANE': 0.0,
                 'FDLASTPLANE': 0.0, 'FDPARTITION': 0.0, 'FDPLANELOC': 0.0, 'FDMAX': 0.0, 'FDMIN': 0.0, 'FDSCALEFLAG': 0.0,
                 'FDDISPMAX': 0.0, 'FDDISPMIN': 0.0, 'FDPTHRESH': 0.0, 'FDNTHRESH': 0.0, 'FDUSER1': 0.0, 'FDUSER2': 0.0,
                 'FDUSER3': 0.0, 'FDUSER4': 0.0, 'FDUSER5': 0.0, 'FDUSER6': 0.0, 'FDLASTBLOCK': 0.0, 'FDCONTBLOCK': 0.0,
                 'FDBASEBLOCK': 0.0, 'FDPEAKBLOCK': 0.0, 'FDBMAPBLOCK': 0.0, 'FDHISTBLOCK': 0.0, 'FD1DBLOCK': 0.0,
                 'FDMCFLAG': 0.0, 'FDNOISE': 0.0,
                 'FDRANK': 0.0, 'FDTEMPERATURE': 0.0, 'FDPRESSURE': 0.0, 'FD2DVIRGIN': 1.0, 'FDTAU': 0.0, 'FDDOMINFO': 0.0,
                 'FDMETHINFO': 0.0, 'FDSCORE': 0.0, 'FDSCANS': 0.0, 'FDSRCNAME': '', 'FDUSERNAME': '', 'FDOPERNAME': '',
                 'FDTITLE': '', 'FDCOMMENT': ''}

    dim34_dic = {'FDF3LABEL': 'Z', 'FDF3APOD': 0.0, 'FDF3OBS': 0.0, 'FDF3OBSMID': 0.0, 'FDF3SW': 0.0, 'FDF3ORIG': 0.0,
                 'FDF3FTFLAG': 0.0, 'FDF3AQSIGN': 0.0, 'FDF3SIZE': 1.0, 'FDF3QUADFLAG': 1.0, 'FDF3UNITS': 0.0,
                 'FDF3P0': 0.0, 'FDF3P1': 0.0, 'FDF3CAR': 0.0, 'FDF3CENTER': 1.0, 'FDF3OFFPPM': 0.0,
                 'FDF3APODCODE': 0.0, 'FDF3APODQ1': 0.0, 'FDF3APODQ2': 0.0, 'FDF3APODQ3': 0.0, 'FDF3LB': 0.0,
                 'FDF3GB': 0.0, 'FDF3GOFF': 0.0, 'FDF3C1': 0.0, 'FDF3ZF': 0.0, 'FDF3X1': 0.0, 'FDF3XN': 0.0,
                 'FDF3FTSIZE': 0.0, 'FDF3TDSIZE': 0.0, 'FDF4LABEL': 'A', 'FDF4APOD': 0.0, 'FDF4OBS': 0.0,
                 'FDF4OBSMID': 0.0, 'FDF4SW': 0.0, 'FDF4ORIG': 0.0, 'FDF4FTFLAG': 0.0, 'FDF4AQSIGN': 0.0,
                 'FDF4SIZE': 1.0, 'FDF4QUADFLAG': 1.0, 'FDF4UNITS': 0.0, 'FDF4P0': 0.0, 'FDF4P1': 0.0,
                 'FDF4CAR': 0.0, 'FDF4CENTER': 1.0, 'FDF4OFFPPM': 0.0, 'FDF4APODCODE': 0.0, 'FDF4APODQ1': 0.0,
                 'FDF4APODQ2': 0.0, 'FDF4APODQ3': 0.0, 'FDF4LB': 0.0, 'FDF4GB': 0.0, 'FDF4GOFF': 0.0, 'FDF4C1': 0.0,
                 'FDF4ZF': 0.0, 'FDF4X1': 0.0, 'FDF4XN': 0.0, 'FDF4FTSIZE': 0.0, 'FDF4TDSIZE': 0.0}

    trans_dic['FDF2APODDF'] = trans_dic['FDF4APODDF']
    del trans_dic['FDF4APODDF'], trans_dic['FDF1SIZE'], trans_dic['FDF2SIZE']

    trans_dic = {**trans_dic, **nodim_dic, **dim34_dic}
    return trans_dic

transformed_pdic = transform_dic(pdic)


# Path to the output NMRPipe file
output_file_path = "/srv/NMR/Peak_Picking/Ubiquitin/Hc-C_slice.ft2"

# Write the slice data and its corresponding dictionary to an NMRPipe file
ng.pipe.write(output_file_path, transformed_pdic, data_slice, overwrite=True)
