from concurrent.futures import ThreadPoolExecutor, as_completed

from module.CBCAcoNH_picker_slice_one_dimension.lib.ucsfdata.get_CBCAcoNH_info import get_CBCAcoNH_info


def extract_bin_edge_ppm_info(file_prefix, index, dimension_index):
    """
    Extracts upfield or downfield ppm info from ucsfdata command output.
    Returns:
    - The extracted ppm value as a float with three decimal places.
    """
    CBCAcoNH_info = get_CBCAcoNH_info(f"{file_prefix}{index}.ucsf")

    return (CBCAcoNH_info["upfield_ppm"][dimension_index], CBCAcoNH_info["downfield_ppm"][dimension_index])


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


def gauge_bin_edges(CBCAcoNH_info, workdir, nucleus):
    dim_index = CBCAcoNH_info["nuclei"].index(nucleus)

    # Extract parameters for N using their indices and convert to Decimal
    dim_bins = int(CBCAcoNH_info["matrix_size"][dim_index])

    upfield_ppm_values, downfield_ppm_values = _parallel_bin_edge_extraction(f"{workdir}/CBCAcoNH_slices/{nucleus}i", dim_bins, dim_index)
    sorted_dim_upfield_ppm_values = [round(float(value), 3) for value in
                                     sorted(upfield_ppm_values, key=lambda x: float(x), reverse=True)]
    sorted_dim_downfield_ppm_values = [round(float(value), 3) for value in
                                       sorted(downfield_ppm_values, key=lambda x: float(x), reverse=True)]

    return {f"{nucleus}_upfield_ppm_values": sorted_dim_upfield_ppm_values,
            f"{nucleus}_downfield_ppm_values": sorted_dim_downfield_ppm_values}




