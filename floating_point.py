"""
Program that converts a IBM Hexadecimal Floating Point binary file to a
IEEE754 binary file.
"""
__author__ = "Dan Skaf, Elijah J. Passmore, Finn Mountfort Will McKenzie"
__license__ = "GPL-3.0"

import os
import sys
import struct


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


def hfp_single_to_float(input):
    """Converts a single precision hexadecimal floating point to primitive
    floating point.

    Args:
        input (int): int version of hexadecimal string.
    Returns:
        (float) Converted hfp.
    """
    binaryString = format(input, "032b")
    signStr = binaryString[0]
    exponentStr = binaryString[1:8]
    mantissaStr = "0." + binaryString[8:]
    exponent = int(exponentStr, 2)
    sign = int(signStr, 2)
    mantissa = get_value(mantissaStr)

    return (16 ** (exponent - 64) * mantissa * (-1)**(sign))


def hfp_double_to_float(input):
    """Converts a double precision hexadecimal floating point to primitive
    floating point

    Args:
        input (int): int version of hexadecimal string
    Returns:
        (float) Converted hfp.
    """
    binaryString = format(input, "064b")
    signStr = binaryString[0]
    exponentStr = binaryString[1:8]
    mantisaStr = "0." + binaryString[8:]
    exponent = int(exponentStr, 2)
    sign = int(signStr, 2)
    mantissa = get_value(mantisaStr)

    return (16 ** (exponent - 64) * mantissa * (-1)**(sign))


def get_value(string_fraction):
    """Normalizes and returns the float value of a mantissa.

    Args:
        string_fraction (string): binary string of mantissa.
    Returns:
        (float) Converted mantissa.
    """
    result = 0.0
    length = len(string_fraction)
    i = 0
    n = 0

    while i < length:
        if string_fraction[i] == ".":
            i += 1
        if string_fraction[i] == "1":
            result += (1 * 2 ** n)
        i += 1
        n -= 1

    return result


def read_single_precision(in_path):
    """Parses the single binary file into a hexadecimal string and then returns
    the primitive float value.

    Args:
        in_path (_io.BufferedReader): file reader of HFP binary file.
    Returns:
        (floating point) primitive float value.
    """
    try:
        length = 0
        hex_str = ""
        float_list = []
        # with open(in_path, "rb") as in_stream:
        with in_path as in_stream:
            while True:
                word = in_stream.read(4)
                if length > 0:
                    hex_as_int = int(hex_str, 16)
                    float_list.append(hfp_single_to_float(hex_as_int))
                if word:
                    length += 1
                    hex_str = ""
                    for b in word:
                        if b == 0:
                            hex_str += "00"
                        else:
                            hex_str += hex(b)[2:]
                else:
                    break

        return float_list
    except Exception as e:
        print(e)


def read_double_precision(in_path):
    """Parses the double binary file into a hexadecimal string and then returns
    the primitive float value.

    Args:
        in_path (_io.BufferedReader): file reader of HFP binary file.
    Returns:
        (floating point) primitive float value.
    """
    try:
        with in_path as in_stream:
            while True:
                word = in_stream.read(8)
                if word:
                    hex_str = ""
                    for b in word:
                        if b == 0:
                            hex_str += "00"
                        else:
                            hex_str += hex(b)[2:]
                else:
                    break
        hex_as_int = int(hex_str, 16)
        return hfp_double_to_float(hex_as_int)
    except Exception as e:
        print(e)


def floating_point(in_path, in_precision, out_path, out_precision):
    """Converts a IBM Hexadecimal floating point to a specified precision and
    writes to specified file name and path.

    Args:
        in_path (string): path to IBM file.
        in_precision (string): precision of IBM file.
        out_path (string): path to output file.
        out_precision (string): precision of IEEE754 file.
    """
    in_file, out_file = None, None

    # Validate in_precision and out_precision.
    if (in_precision != "single") and (in_precision != "double"):
        raise InvalidPrecision(in_precision)
    elif (out_precision != "single") and (out_precision != "double"):
        raise InvalidPrecision(out_precision)

    # Attempt to open input file at in_path with read permission.
    try:
        in_file = open(in_path, "rb")
        if in_precision == "single":
            intermFloat = read_single_precision(in_file)
        else:
            intermFloat = read_double_precision(in_file)
    except PermissionError:
        raise InvalidFile(
            in_path, "Insufficient permission to read file.")
    except OSError:
        raise InvalidFile(in_file)

    # Attempt to open output file at out_path with write permission.
    try:
        out_file = open(out_path, "wb")
        if out_precision == "single":
            result = struct.pack('f', intermFloat)
        else:
            result = struct.pack('d', intermFloat)
        out_file.write(result)
        print("Created " + out_precision + " IEEE754 file at " + out_path)
    except PermissionError:
        raise InvalidFile(
            out_path, "Insufficient permission to write to file.")
    except OSError:
        raise InvalidFile(out_file)


if __name__ == "__main__":
    # File paths in string form.
    in_path, out_path = "", ""
    # Precision of each file.
    in_precision, out_precision = "", ""
    try:
        # Get the input path.
        while os.path.isfile(in_path) == False:
            in_path = input("Please enter input file path: ")

        # Get the input precision.
        while (in_precision != "single") and (in_precision != "double"):
            in_precision = input(
                "Please enter the input precision (single/double): ")
            in_precision = in_precision.lower()

        # Get the output path.
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
