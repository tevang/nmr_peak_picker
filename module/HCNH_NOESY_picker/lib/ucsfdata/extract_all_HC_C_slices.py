import subprocess

import pandas as pd

from commons.find_bin_indices_N_HN_peaks import find_bin_indices_of_all_N_HN_peaks


def extract_all_HC_C_slices(NH_HSQC_peak_sparky, bin_edges_dict, spectrum_4D_ucsf, workdir, dry_run=False):
    peak_indices_df = find_bin_indices_of_all_N_HN_peaks(NH_HSQC_peak_sparky, bin_edges_dict)
    peaks = []
    for _, peak in peak_indices_df.iterrows():
        command = (f"ucsfdata -w3 {peak['N_bin_index']} {peak['N_bin_index']} "
                   f"-w4 {peak['HN_bin_index']} {peak['HN_bin_index']} -r "
                   f"-o {workdir}/HCNH_NOESY_slices/HC-C_Nbin{int(peak['N_bin_index'])}_HNbin{int(peak['HN_bin_index'])}.ucsf "
                   f"{spectrum_4D_ucsf}")

        try:
            if not dry_run:
                subprocess.run(command, shell=True, check=True)
                print(f"Command executed successfully: {command}")
            peak['slice_ucsf_file'] = f"{workdir}/HCNH_NOESY_slices/HC-C_Nbin{int(peak['N_bin_index'])}_HNbin{int(peak['HN_bin_index'])}.ucsf"
            peaks.append(peak.to_frame().T)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the command: {command}\nError: {e}")

    return pd.concat(peaks, ignore_index=True).astype({'N_bin_index': 'int', 'HN_bin_index': 'int'})
