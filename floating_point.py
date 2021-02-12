import os
import sys


class InvalidFile(OSError):
    """Raised if the path or permissions of a provided file is
    invalid.
    """

    def __init__(self, path,
                 message="Cannot open file."):
        self.path = path
        self.message = message

    def __str__(self):
        return (f"{self.path}: {self.message}")


class InvalidPrecision(ValueError):
    """Raised if precision is not either single or double."""

    def __init__(self, precision,
                 message="Precision must be either single or double."):
        self.precision = precision
        self.message = message

    def __str__(self):
        return (f"{self.precision}: {self.message}")


def floating_point(in_path, in_precision, out_path, out_precision):
    in_file, out_file = None, None

    # Attempt to open input file at in_path with read permission.
    try:
        in_file = open(in_path, "r")
    except PermissionError:
        raise InvalidFile(
            in_path, "Insufficient permission to read file.")
    except OSError:
        raise InvalidFile(in_file)

    # Attempt to open output file at out_path with write permission.
    try:
        out_file = open(out_path, "w")
    except PermissionError:
        raise InvalidFile(
            out_path, "Insufficient permission to write to file.")
    except OSError:
        raise InvalidFile(out_file)

    # Validate in_precision and out_precision.
    if (in_precision != "single") and (in_precision != "double"):
        raise InvalidPrecision(in_precision)
    elif (out_precision != "single") and (out_precision != "double"):
        raise InvalidPrecision(out_precision)


if __name__ == "__main__":
    # File paths in string form.
    in_path, out_path = "", ""
    # Precision of each file.
    in_precision, out_precision = "", ""

    try:
        # Get the input file.
        while os.path.isfile(in_path) == False:
            in_path = input("Please enter input file path: ")

        # Get the input precision.
        while (in_precision != "single") and (in_precision != "double"):
            in_precision = input(
                "Please enter the input precision (single/double): ")
            in_precision = in_precision.lower()

        # Get the output file.
        while os.path.isfile(out_path) == False:
            out_path = input("Please enter the output file path: ")

        # Get the output precision.
        while (out_precision != "single") and (out_precision != "double"):
            out_precision = input(
                "Please enter the output precision (single/double): ")
            out_precision = out_precision.lower()

    # If EOF is entered, exit.
    except EOFError:
        sys.exit()

    try:
        floating_point(in_path, in_precision, out_path, out_precision)
    except Exception as e:
        print(e)
