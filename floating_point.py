import os
import sys


def floating_point(in_file, in_precision, out_file, out_precision):
    raise NotImplementedError


if __name__ == "__main__":
    # File objects.
    in_file, out_file = None, None
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

    # Attempt to open input file at in_path with read permission.
    try:
        in_file = open(in_path, "r")
    except:
        print("Unable to read file: " + in_path)
        sys.exit()

    # Attempt to open output file at out_path with write permission.
    try:
        out_file = open(out_path, "w")
    except:
        print("Unable to write to file: " + out_path)
        sys.exit()

    floating_point(in_file, in_precision, out_file, out_precision)
