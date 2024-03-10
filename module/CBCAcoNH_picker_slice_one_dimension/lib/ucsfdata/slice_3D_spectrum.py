import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def slice_3D_spectrum_in_sel_dimension(index, workdir, CBCAcoNH_ucsf, dim_index, nucleus):
    """Slices the 3D spectrum in the N dimension in parallel to find the edges of the bin with the provided index."""
    cmd = f"ucsfdata -w{dim_index} {index} {index} -o {workdir}/CBCAcoNH_slices/{nucleus}i{index}.ucsf {CBCAcoNH_ucsf}"
    subprocess.run(cmd, shell=True)


def slice_3D_spectrum_at_sel_dimension_parallel(spectrum_info, workdir, CBCAcoNH_ucsf, nucleus):
    """
    Slices the 3D spectrum in the given dimension.
    """
    print(f"Slicing 3D spectrum at the {nucleus} dimension.")
    dim_index = spectrum_info["nuclei"].index(nucleus)

    dim_bins = int(spectrum_info["matrix_size"][dim_index])

    with ThreadPoolExecutor() as executor:
        futures_wN = [executor.submit(slice_3D_spectrum_in_sel_dimension, i, workdir, CBCAcoNH_ucsf, dim_index + 1, nucleus) for i in range(dim_bins)]

        # Waiting for all futures to complete (optional, if you need to do something after each completes)
        for future in as_completed(futures_wN):
            future.result()  # This would raise exceptions if any occurred during command execution

    print(f"Slicing of the 3D spectrum at the {nucleus} dimension has finished.")
