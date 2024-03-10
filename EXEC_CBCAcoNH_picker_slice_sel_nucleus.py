#!/usr/env/bin python

"""
When I selected to slice at the HN dimension the resulting ucsf files contain no peaks, not even density.
"""

import pretty_errors
from commons.check_file_existence import check_executables_and_files, prepare_slice_directory
from commons.deep_picker import run_deep_picker_serial, run_deep_picker_parallel
from commons.get_3D_spectrum_info import get_3D_spectrum_info
from module.CBCAcoNH_picker_slice_one_dimension.lib.load_deep_picker_picked_peaks import load_all_deep_picker_picked_peaks_to_dataframe
from module.CBCAcoNH_picker_slice_one_dimension.lib.ucsfdata.extract_all_2D_slices import extract_all_2D_slices
from module.CBCAcoNH_picker_slice_one_dimension.lib.ucsfdata.gauge_bin_edges import gauge_bin_edges
from module.CBCAcoNH_picker_slice_one_dimension.lib.ucsfdata.slice_3D_spectrum import slice_3D_spectrum_at_sel_dimension_parallel

CBCAcoNH_ucsf = "/home2/srv/NMR/Peak_Picking/Ubiquitin/CBCAcoNH_MDD.ucsf"
NH_HSQC_peak_sparky = "/srv/NMR/Peak_Picking/Ubiquitin/15N_HSQC.list"
WORKDIR = "/srv/NMR/Peak_Picking/Ubiquitin/"
deep_picker_confidence_threshold = 0.5
dry_run = False
nucleus="HN"

check_executables_and_files(executables=['ucsfdata', 'deep_picker'], files=[CBCAcoNH_ucsf, NH_HSQC_peak_sparky])
prepare_slice_directory(WORKDIR, 'CBCAcoNH', dry_run)

CBCAcoNH_info = get_3D_spectrum_info(CBCAcoNH_ucsf)
slice_3D_spectrum_at_sel_dimension_parallel(CBCAcoNH_info, WORKDIR, CBCAcoNH_ucsf, nucleus)
bin_edges_dict = gauge_bin_edges(CBCAcoNH_info, WORKDIR, nucleus)
slice_ucsf_files_df = extract_all_2D_slices(NH_HSQC_peak_sparky, bin_edges_dict, CBCAcoNH_ucsf, WORKDIR, nucleus,
                                            CBCAcoNH_info["nuclei"].index(nucleus) + 1, dry_run)
# slice_ucsf_files_df : [shift, bin_index, slice_ucsf_file]
output_files = run_deep_picker_parallel(slice_ucsf_files_df, slice_dimensions=2, dry_run=dry_run)
# output_files = run_deep_picker_serial(slice_ucsf_files_df, slice_dimensions=2, dry_run=dry_run)
picked_peaks_df = load_all_deep_picker_picked_peaks_to_dataframe(output_files, slice_ucsf_files_df, nucleus,
                                                                 confidence_threshold=deep_picker_confidence_threshold)
picked_CBCAcoNH_df = picked_peaks_df.assign(Assignment='?-?-?-?') \
    .rename(columns={'Y_PPM': 'w1', 'X_PPM': 'w2', f'{nucleus}_shift': 'w3', 'HEIGHT': 'Data Height'}) \
    .query('CONFIDENCE > 0.5')[['Assignment', 'w1', 'w2', 'w3', 'Data Height']]
picked_CBCAcoNH_df[['w1', 'w2', 'w3']] = picked_CBCAcoNH_df[['w1', 'w2', 'w3']].round(3)
picked_CBCAcoNH_df['Data Height'] = picked_CBCAcoNH_df['Data Height'].astype(int)

print(f"Writing automatically picked CBCAcoNH peaks into file {WORKDIR}/picked_peaks_CBCAcoNH.list")
picked_CBCAcoNH_df.to_csv(f'{WORKDIR}/picked_peaks_CBCAcoNH.list', index=False, sep='\t')