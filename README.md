# Floating point
A python program that converts a IBM Hexadecimal Floating Point binary file to IEEE754 to binary file. 

# Author 
Dan Skaf

Elijah Passmore

## Dependencies 
Requires latest `python 3` package to run
## Usage 
`cd` into directory of program and run`$ python3 floating-point.py`  then follow prompts to enter file and precision.

The output can be validated using a hexdump program like `xxd` or `hexdump`

```$ xxd -b output.bin```

### Testing 
The test binary files located in the `test` directory have single and double precision positive and negative floating point numbers. 

