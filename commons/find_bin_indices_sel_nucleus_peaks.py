import pandas as pd

from commons.BinFinder import BinFinder
from module.HCNH_NOESY_picker.lib.read_NH_HSQC_peaks import read_hn_hsqc_peak_sparky

def _get_indices(row, bin_finder, nucleus):
    return pd.Series({f'{nucleus}_shift': row[nucleus], f'{nucleus}_bin_index': bin_finder.find_bin_index(row[nucleus])})

def find_bin_indices_of_all_sel_nucleus_peaks(NH_HSQC_peak_sparky, bin_edges_dict, nucleus):
    peaks_df = read_hn_hsqc_peak_sparky(NH_HSQC_peak_sparky)

    bin_finder = BinFinder(bin_edges_dict[f'{nucleus}_downfield_ppm_values'], bin_edges_dict[f'{nucleus}_upfield_ppm_values'])

    peak_indices_df = peaks_df.apply(lambda row: _get_indices(row, bin_finder, nucleus), axis=1)

    return peak_indices_df.astype({f'{nucleus}_bin_index': 'int'})
