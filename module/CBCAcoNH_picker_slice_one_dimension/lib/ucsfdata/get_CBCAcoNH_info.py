import re
import subprocess

import numpy as np


def get_CBCAcoNH_info(ucsf_file_path):
    """
    Calls the 'ucsfdata' command on a given UCSF file and parses the output for spectrum parameters.

    Parameters:
    - ucsf_file_path: Path to the UCSF file.

    Returns:
    - A dictionary containing the parsed spectrum parameters.
    """
    # Execute the ucsfdata command and capture its output
    result = subprocess.run(["ucsfdata", ucsf_file_path], capture_output=True, text=True)
    output = result.stdout

    # Adjust the pattern to match the provided output format
    pattern = r"axis\s+w1\s+w2\s+w3[\s\n]+" \
              r"nucleus\s+(\S+)\s+(\S+)\s+(\S+)[\s\n]+" \
              r"matrix size\s+(\d+)\s+(\d+)\s+(\d+)[\s\n]+" \
              r"block size\s+(\d+)\s+(\d+)\s+(\d+)[\s\n]+" \
              r"upfield ppm\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)[\s\n]+" \
              r"downfield ppm\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)[\s\n]+" \
              r"spectrum width Hz\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)[\s\n]+" \
              r"transmitter MHz\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"

    matches = re.search(pattern, output, re.MULTILINE)

    if matches:
        # Map the captured groups to meaningful variable names for clarity
        (nucleus_w1, nucleus_w2, nucleus_w3,
         matrix_size_w1, matrix_size_w2, matrix_size_w3,
         block_size_w1, block_size_w2, block_size_w3,
         upfield_ppm_w1, upfield_ppm_w2, upfield_ppm_w3,
         downfield_ppm_w1, downfield_ppm_w2, downfield_ppm_w3,
         spectrum_width_hz_w1, spectrum_width_hz_w2, spectrum_width_hz_w3,
         transmitter_mhz_w1, transmitter_mhz_w2, transmitter_mhz_w3) = matches.groups()

        # Convert captured groups to appropriate types
        spectrum_info = {
            "nuclei": [nucleus_w1, nucleus_w2, nucleus_w3],
            "matrix_size": [int(matrix_size_w1), int(matrix_size_w2), int(matrix_size_w3)],
            "block_size": [int(block_size_w1), int(block_size_w2), int(block_size_w3)],
            "upfield_ppm": [float(upfield_ppm_w1), float(upfield_ppm_w2), float(upfield_ppm_w3)],
            "downfield_ppm": [float(downfield_ppm_w1), float(downfield_ppm_w2), float(downfield_ppm_w3)],
            "spectrum_width_hz": [float(spectrum_width_hz_w1), float(spectrum_width_hz_w2), float(spectrum_width_hz_w3)],
            "transmitter_mhz": [float(transmitter_mhz_w1), float(transmitter_mhz_w2), float(transmitter_mhz_w3)]
        }

        assert np.all([nucleus in ['HC', 'C', 'N', 'HN'] for nucleus in spectrum_info["nuclei"]]), \
            (f"ERROR: nucleus name(s) {spectrum_info['nuclei']} not in the supported ones ('HC', 'C', 'N', 'HN'). "
             f"Please rename your spectrum's nuclei using ucsfdata -aN argument and try again.")

        return spectrum_info
    else:
        raise ValueError("Could not parse spectrum parameters from the ucsfdata output.")

