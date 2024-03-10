#!/usr/env/bin python

from commons.check_file_existence import check_executables_and_files, prepare_slice_directory
from commons.deep_picker import run_deep_picker_serial, run_deep_picker_parallel
from module.HCNH_NOESY_picker.lib.load_deep_picker_picked_peaks import load_all_deep_picker_picked_peaks_to_dataframe
from module.HCNH_NOESY_picker.lib.ucsfdata.extract_all_HC_C_slices import extract_all_HC_C_slices
from module.HCNH_NOESY_picker.lib.ucsfdata.gauge_bin_edges import gauge_bin_edges
from commons.get_4D_spectrum_info import get_spectrum_4D_info
from module.HCNH_NOESY_picker.lib.ucsfdata.slice_4D_spectrum import slice_4D_spectrum_at_n_hn_dimensions_parallel

spectrum_4D_ucsf = "/srv/NMR/Peak_Picking/Ubiquitin/4D_HCNH_NOESY_NUS_reconstructed.ucsf"
NH_HSQC_peak_sparky = "/srv/NMR/Peak_Picking/Ubiquitin/15N_HSQC.list"
WORKDIR = "/srv/NMR/Peak_Picking/Ubiquitin/"
deep_picker_confidence_threshold = 0.5
dry_run=False
parallel_execution = True

check_executables_and_files(executables=['ucsfdata', 'deep_picker'], files=[spectrum_4D_ucsf, NH_HSQC_peak_sparky])
prepare_slice_directory(WORKDIR, 'HCNH_NOESY', dry_run)

spectrum_4D_info = get_spectrum_4D_info(spectrum_4D_ucsf)
slice_4D_spectrum_at_n_hn_dimensions_parallel(spectrum_4D_info, WORKDIR, spectrum_4D_ucsf)
bin_edges_dict = gauge_bin_edges(spectrum_4D_info, WORKDIR)
slice_ucsf_files_df = extract_all_HC_C_slices(NH_HSQC_peak_sparky, bin_edges_dict,
                                                spectrum_4D_ucsf, WORKDIR, dry_run)
# slice_ucsf_files_df : [N_shift, N_bin_index, HN_shift, HN_bin_index, slice_ucsf_file]
output_files = run_deep_picker_parallel(slice_ucsf_files_df, slice_dimensions=2, dry_run=dry_run) if parallel_execution \
    else run_deep_picker_serial(slice_ucsf_files_df, slice_dimensions=2, dry_run=dry_run)
picked_peaks_df = load_all_deep_picker_picked_peaks_to_dataframe(output_files, slice_ucsf_files_df,
                                                                 confidence_threshold=deep_picker_confidence_threshold)
picked_4D_HCNH_NOESY_df = picked_peaks_df.assign(Assignment='?-?-?-?') \
    .rename(columns={'Y_PPM': 'w1', 'X_PPM': 'w2', 'N_shift': 'w3', 'HN_shift': 'w4', 'HEIGHT': 'Data Height'}) \
    .query('CONFIDENCE > 0.5')[['Assignment', 'w1', 'w2', 'w3', 'w4', 'Data Height']]
picked_4D_HCNH_NOESY_df[['w1', 'w2', 'w3', 'w4']] = picked_4D_HCNH_NOESY_df[['w1', 'w2', 'w3', 'w4']].round(3)
picked_4D_HCNH_NOESY_df['Data Height'] = picked_4D_HCNH_NOESY_df['Data Height'].astype(int)

print(f"Writing automatically picked 4D HCNH NOESY peaks into file {WORKDIR}/picked_peaks_4D_HCNH_NOESY.list")
picked_4D_HCNH_NOESY_df.to_csv(f'{WORKDIR}/picked_peaks_4D_HCNH_NOESY.list', index=False, sep='\t')