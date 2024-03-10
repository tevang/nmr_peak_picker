import pandas as pd

from commons.BinFinder import BinFinder
from module.HCNH_NOESY_picker.lib.read_NH_HSQC_peaks import read_hn_hsqc_peak_sparky


def _get_indices(row, N_bin_finder, HN_bin_finder):
    return pd.Series({'N_shift': row['N'], 'N_bin_index': N_bin_finder.find_bin_index(row['N']),
                      'HN_shift': row['HN'], 'HN_bin_index': HN_bin_finder.find_bin_index(row['HN'])})

def find_bin_indices_of_all_N_HN_peaks(NH_HSQC_peak_sparky, bin_edges_dict):
    peaks_df = read_hn_hsqc_peak_sparky(NH_HSQC_peak_sparky)

    N_bin_finder = BinFinder(bin_edges_dict['N_downfield_ppm_values'], bin_edges_dict['N_upfield_ppm_values'])
    HN_bin_finder = BinFinder(bin_edges_dict['HN_downfield_ppm_values'], bin_edges_dict['HN_upfield_ppm_values'])

    peak_indices_df = peaks_df.apply(lambda row: _get_indices(row, N_bin_finder, HN_bin_finder), axis=1)

    return peak_indices_df.astype({'N_bin_index': 'int', 'HN_bin_index': 'int'})
