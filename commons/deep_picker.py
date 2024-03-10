import os.path
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_deep_picker(ucsf_file, slice_dimensions, dry_run):
    """
    Runs the deep_picker command for a single UCSF file and logs the output.
    """
    output_file = ucsf_file.replace(".ucsf", "") + "_peaks.tab"
    log_file = output_file.replace("_peaks.tab", ".log")  # Create log file name
    if slice_dimensions == 2:
        command = f"deep_picker -in {ucsf_file} -out {output_file}"
    elif slice_dimensions == 1:
        command = f"deep_picker_1d -in {ucsf_file} -out {output_file}"  # FIXME: does not support ucsf format

    if not dry_run:
        with open(log_file, "w") as log:  # Open the log file for writing
            try:
                # Execute the command and redirect stdout and stderr to the log file
                subprocess.run(command, shell=True, check=True, stdout=log, stderr=log)
                print(f"Command executed successfully for {ucsf_file}")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while executing the command for {ucsf_file}: {e}")
                # Optionally, write the error to the log file as well
                log.write(f"An error occurred: {e}\n")
                output_file = None  # Set to None if the command fails
    else:
        if not os.path.exists(output_file):
            output_file = None

    return output_file


def run_deep_picker_parallel(slice_ucsf_files_df, slice_dimensions, dry_run=False):
    """
    Executes the deep_picker command in parallel for all given UCSF files and returns a list of output files.
    """
    output_files = []
    with ThreadPoolExecutor() as executor:
        # Use a future-to-file mapping to keep track of output files
        future_to_ucsf = {executor.submit(run_deep_picker, ucsf_file, slice_dimensions, dry_run): ucsf_file for ucsf_file in slice_ucsf_files_df['slice_ucsf_file'].values}

        for future in as_completed(future_to_ucsf):
            ucsf_file = future_to_ucsf[future]
            try:
                output_file = future.result()
                if output_file:
                    output_files.append(output_file)
            except Exception as exc:
                print(f'{ucsf_file} generated an exception: {exc}')
    return output_files

def run_deep_picker_serial(slice_ucsf_files_df, slice_dimensions, dry_run=False):
    """
    Executes the deep_picker command serially for all given UCSF files and returns a list of output files.
    """
    output_files = []
    for ucsf_file in slice_ucsf_files_df['slice_ucsf_file'].values:
        try:
            output_file = run_deep_picker(ucsf_file, slice_dimensions, dry_run=dry_run)
            if output_file:
                output_files.append(output_file)
        except Exception as exc:
            print(f'{ucsf_file} generated an exception: {exc}')
    return output_files
