class BinFinder:
    def __init__(self, upfield_ppm_lvalues, downfield_ppm_values):
        self.lower_bounds = upfield_ppm_lvalues
        self.upper_bounds = downfield_ppm_values
        assert len(self.lower_bounds) == len(self.upper_bounds), \
            ("ERROR: upfield_ppm {len(self.lower_bounds)} and downfield_ppm {len(self.upper_bounds)} bin edges "
             "do not have the same size!")

    def find_bin_index(self, value):
        for index in reversed(range(len(self.lower_bounds))):
            if self.upper_bounds[index] <= value < self.lower_bounds[index]:
                return index
        return None
