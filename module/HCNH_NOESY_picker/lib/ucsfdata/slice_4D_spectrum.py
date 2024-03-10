import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def slice_4D_spectrum_in_hn_dimension(index, workdir, spectrum_4D_ucsf):
    """Slices the 4D spectrum in the HN dimension in parallel to find the edges of the bin with the provided index."""
    cmd = f"ucsfdata -w4 {index} {index} -o {workdir}/HCNH_NOESY_slices/HNi{index}.ucsf {spectrum_4D_ucsf}"
    subprocess.run(cmd, shell=True)


def slice_4D_spectrum_in_n_dimension(index, workdir, spectrum_4D_ucsf):
    """Slices the 4D spectrum in the N dimension in parallel to find the edges of the bin with the provided index."""
    cmd = f"ucsfdata -w3 {index} {index} -o {workdir}/HCNH_NOESY_slices/Ni{index}.ucsf {spectrum_4D_ucsf}"
    subprocess.run(cmd, shell=True)


def slice_4D_spectrum_at_n_hn_dimensions_parallel(spectrum_info, workdir, spectrum_4D_ucsf):
    print("Slicing 4D spectrum at the N and HN dimensions individually")
    n_index = spectrum_info["nuclei"].index("N")
    hn_index = spectrum_info["nuclei"].index("HN")

    n_bins = int(spectrum_info["matrix_size"][n_index])
    hn_bins = int(spectrum_info["matrix_size"][hn_index])

    with ThreadPoolExecutor() as executor:
        futures_w4 = [executor.submit(slice_4D_spectrum_in_hn_dimension, i, workdir, spectrum_4D_ucsf) for i in range(hn_bins)]

        futures_w3 = [executor.submit(slice_4D_spectrum_in_n_dimension, i, workdir, spectrum_4D_ucsf) for i in range(n_bins)]

        # Waiting for all futures to complete (optional, if you need to do something after each completes)
        for future in as_completed(futures_w4 + futures_w3):
            future.result()  # This would raise exceptions if any occurred during command execution

    print("Slicing of the 4D spectrum at the N and HN dimensions has finished.")
