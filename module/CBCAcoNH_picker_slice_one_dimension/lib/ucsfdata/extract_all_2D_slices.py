import subprocess

import pandas as pd

from commons.find_bin_indices_sel_nucleus_peaks import find_bin_indices_of_all_sel_nucleus_peaks


def extract_all_2D_slices(NH_HSQC_peak_sparky, bin_edges_dict, CBCAcoNH_ucsf, workdir, nucleus, dimension_index,
                          dry_run=False):
    peak_indices_df = find_bin_indices_of_all_sel_nucleus_peaks(NH_HSQC_peak_sparky, bin_edges_dict, nucleus)
    peaks = []
    for _, peak in peak_indices_df.iterrows():
        command = (f"ucsfdata -w{dimension_index} {peak[f'{nucleus}_bin_index']} {peak[f'{nucleus}_bin_index']} "
                   f"-r "
                   f"-o {workdir}/CBCAcoNH_slices/2D_slice_{nucleus}bin{int(peak[f'{nucleus}_bin_index'])}.ucsf "
                   f"{CBCAcoNH_ucsf}")

        try:
            if not dry_run:
                subprocess.run(command, shell=True, check=True)
                print(f"Command executed successfully: {command}")
            peak['slice_ucsf_file'] = f"{workdir}/CBCAcoNH_slices/2D_slice_{nucleus}bin{int(peak[f'{nucleus}_bin_index'])}.ucsf"
            peaks.append(peak.to_frame().T)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the command: {command}\nError: {e}")

    return pd.concat(peaks, ignore_index=True).astype({f'{nucleus}_bin_index': 'int'})
