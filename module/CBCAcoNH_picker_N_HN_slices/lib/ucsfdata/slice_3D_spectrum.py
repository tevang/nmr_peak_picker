import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def slice_3D_spectrum_in_hn_dimension(index, workdir, CBCAcoNH_ucsf):
    """Slices the 3D spectrum in the HN dimension in parallel to find the edges of the bin with the provided index."""
    cmd = f"ucsfdata -w3 {index} {index} -o {workdir}/CBCAcoNH_slices/HNi{index}.ucsf {CBCAcoNH_ucsf}"
    subprocess.run(cmd, shell=True)


def slice_3D_spectrum_in_n_dimension(index, workdir, CBCAcoNH_ucsf):
    """Slices the 3D spectrum in the N dimension in parallel to find the edges of the bin with the provided index."""
    cmd = f"ucsfdata -w2 {index} {index} -o {workdir}/CBCAcoNH_slices/Ni{index}.ucsf {CBCAcoNH_ucsf}"
    subprocess.run(cmd, shell=True)


def slice_3D_spectrum_at_n_hn_dimensions_parallel(spectrum_info, workdir, CBCAcoNH_ucsf):
    print("Slicing 3D spectrum at the N and HN dimensions individually")
    n_index = spectrum_info["nuclei"].index("N")
    hn_index = spectrum_info["nuclei"].index("HN")

    n_bins = int(spectrum_info["matrix_size"][n_index])
    hn_bins = int(spectrum_info["matrix_size"][hn_index])

    with ThreadPoolExecutor() as executor:
        futures_w3 = [executor.submit(slice_3D_spectrum_in_hn_dimension, i, workdir, CBCAcoNH_ucsf) for i in range(hn_bins)]

        futures_w2 = [executor.submit(slice_3D_spectrum_in_n_dimension, i, workdir, CBCAcoNH_ucsf) for i in range(n_bins)]

        # Waiting for all futures to complete (optional, if you need to do something after each completes)
        for future in as_completed(futures_w3 + futures_w2):
            future.result()  # This would raise exceptions if any occurred during command execution

    print("Slicing of the 3D spectrum at the N and HN dimensions has finished.")
