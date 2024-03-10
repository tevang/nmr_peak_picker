import os
import re

import pandas as pd

# TOFIX: you must adapt this for tab files with one dimensional peaks.

def extract_bin_indices_from_file_path(file_path):
    # Get the basename of the file
    basename = os.path.basename(file_path)

    # Define the regular expression pattern to match the bin indices
    pattern = r'C_Nbin(\d+)_HNbin(\d+)_peaks\.tab'

    # Attempt to find a match in the basename
    match = re.search(pattern, basename)

    if match:
        # Extract N_bin_index and HN_bin_index from the match groups
        N_bin_index = int(match.group(1))
        HN_bin_index = int(match.group(2))
        return N_bin_index, HN_bin_index
    else:
        # Return None or raise an error if the pattern does not match
        return None, None


def load_deep_picker_output_to_dataframe(file_path, slice_ucsf_files_df):
    """
    Reads an output file from DEEP Picker and returns a DataFrame of peaks.

    Parameters:
    - file_path: Path to the DEEP Picker output file.
    - slice_ucsf_files_df: [N_shift, N_bin_index, HN_shift, HN_bin_index, slice_ucsf_file]

    Returns:
    - DataFrame with columns corresponding to the DEEP Picker output.
    """

    N_bin_index, HN_bin_index = extract_bin_indices_from_file_path(file_path)
    slice_df = slice_ucsf_files_df.query(f"N_bin_index == {N_bin_index} and HN_bin_index == {HN_bin_index}")

    assert slice_df.shape[0] == 1, ("There should be only one correct N_shift and HN_shift. More were found:\n"
                                    f"{slice_df.to_string(index=False)}")

    peaks_data = []

    column_names = ['INDEX', 'X_AXIS', 'Y_AXIS', 'X_PPM', 'Y_PPM', 'XW', 'YW', 'X1', 'X3', 'Y1', 'Y3', 'HEIGHT', 'ASS',
                    'CONFIDENCE', 'POINTER']

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("FORMAT"):
                break

        for line in file:
            if line.strip():  # Ensure the line is not empty
                parts = line.split()
                peak_data = [
                    int(parts[0]),  # INDEX
                    float(parts[1]),  # X_AXIS
                    float(parts[2]),  # Y_AXIS
                    float(parts[3]),  # X_PPM
                    float(parts[4]),  # Y_PPM
                    float(parts[5]),  # XW
                    float(parts[6]),  # YW
                    int(parts[7]),  # X1
                    int(parts[8]),  # X3
                    int(parts[9]),  # Y1
                    int(parts[10]),  # Y3
                    float(parts[11]),  # HEIGHT
                    parts[12],  # ASS
                    float(parts[13]),  # CONFIDENCE
                    parts[14] if len(parts) > 14 else None  # POINTER, if present
                ]
                peaks_data.append(peak_data)

    return pd.DataFrame(peaks_data, columns=column_names) \
        .assign(N_shift=slice_df['N_shift'].values[0],
                HN_shift=slice_df['HN_shift'].values[0]) \
        [['X_PPM', 'Y_PPM', 'HEIGHT', 'CONFIDENCE', 'N_shift', 'HN_shift']]

def load_all_deep_picker_picked_peaks_to_dataframe(output_files, slice_ucsf_files_df, confidence_threshold=0.5):
    picked_peaks_list = [load_deep_picker_output_to_dataframe(file_path, slice_ucsf_files_df)
                         for file_path in output_files]
    return pd.concat(picked_peaks_list, ignore_index=True) \
        .query(f"CONFIDENCE > {confidence_threshold}")