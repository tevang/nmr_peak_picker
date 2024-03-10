from concurrent.futures import ThreadPoolExecutor, as_completed

from commons.get_4D_spectrum_info import get_spectrum_4D_info


def extract_bin_edge_ppm_info(file_prefix, index, dimension_index):
    """
    Extracts upfield or downfield ppm info from ucsfdata command output.
    Returns:
    - The extracted ppm value as a float with three decimal places.
    """
    spectrum_4D_info = get_spectrum_4D_info(f"{file_prefix}{index}.ucsf")

    return (spectrum_4D_info["upfield_ppm"][dimension_index], spectrum_4D_info["downfield_ppm"][dimension_index])


def _parallel_bin_edge_extraction(file_prefix, num_files, dimension_index):
    with ThreadPoolExecutor() as executor:
        # Submit tasks
        futures = [executor.submit(extract_bin_edge_ppm_info, file_prefix, i, dimension_index) for i in range(num_files)]

        # Collect results as they complete, formatting as strings with 3 decimal places
        upfield_ppm_values, downfield_ppm_values = [], []
        for future in as_completed(futures):
            upfield_ppm_values.append(f"{future.result()[0]:.3f}")
            downfield_ppm_values.append(f"{future.result()[1]:.3f}")

    return upfield_ppm_values, downfield_ppm_values


def gauge_bin_edges(spectrum_4D_info, workdir):
    n_index = spectrum_4D_info["nuclei"].index("N")
    hn_index = spectrum_4D_info["nuclei"].index("HN")

    # Extract parameters for N and HN using their indices and convert to Decimal
    n_bins = int(spectrum_4D_info["matrix_size"][n_index])
    hn_bins = int(spectrum_4D_info["matrix_size"][hn_index])

    N_upfield_ppm_values, N_downfield_ppm_values = _parallel_bin_edge_extraction(f"{workdir}/HCNH_NOESY_slices/Ni", n_bins, n_index)
    HN_upfield_ppm_values, HN_downfield_ppm_values = _parallel_bin_edge_extraction(f"{workdir}/HCNH_NOESY_slices/HNi", hn_bins, hn_index)
    sorted_N_upfield_ppm_values = [round(float(value), 3) for value in
                                   sorted(N_upfield_ppm_values, key=lambda x: float(x), reverse=True)]
    sorted_N_downfield_ppm_values = [round(float(value), 3) for value in
                                     sorted(N_downfield_ppm_values, key=lambda x: float(x), reverse=True)]
    sorted_HN_upfield_ppm_values = [round(float(value), 3) for value in
                                    sorted(HN_upfield_ppm_values, key=lambda x: float(x), reverse=True)]
    sorted_HN_downfield_ppm_values = [round(float(value), 3) for value in
                                      sorted(HN_downfield_ppm_values, key=lambda x: float(x), reverse=True)]

    return {"N_upfield_ppm_values": sorted_N_upfield_ppm_values,
            "N_downfield_ppm_values": sorted_N_downfield_ppm_values,
            "HN_upfield_ppm_values": sorted_HN_upfield_ppm_values,
            "HN_downfield_ppm_values": sorted_HN_downfield_ppm_values}




