import csv
import logging
import os

import numpy as np

# Set up logging
logging.basicConfig(level=logging.DEBUG)

DEFAULT_LOG_PATH = "/Users/sum/python_tutorial/developer_x23/sandbox_x23/log"


def multiply_by_two(numbers):
    """Multiply every number by two"""
    return map(lambda x: x * 2, numbers)


def filter_odd_numbers(numbers):
    """Filter out odd numbers"""
    return filter(lambda x: x % 2 == 0, numbers)


def calculate_sum_neighbours(numbers):
    """Calculate the sum of each number and its neighbours, using wraparound"""
    length = len(numbers)
    return [(numbers[i - 1] + numbers[i] + numbers[(i + 1) % length]) for i in range(length)]


def apply_number_transformations(matrix):
    """Apply number transformations to the matrix"""
    number_transformations = [multiply_by_two, filter_odd_numbers, calculate_sum_neighbours]
    return [[apply_transformations([matrix[i][j]], number_transformations)[0] for j in range(len(matrix))] for i in
            range(len(matrix))]


def apply_transformations(numbers, transformations):
    """Apply a list of transformations to the numbers"""
    result = numbers
    for transformation in transformations:
        result = list(transformation(result))
    return result if result else [0]


def create_identity_matrix(n):
    """
    Create an n x n identity matrix.
    An identity matrix is a square matrix in which all the elements of the principal diagonal are ones
    and all other elements are zeros.
    """
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def double_diagonal(matrix):
    """Double the elements on the main diagonal"""
    return [[2 * element if i == j else element for j, element in enumerate(row)] for i, row in enumerate(matrix)]


def zero_out(matrix):
    """Set all elements below the main diagonal to zero, making the matrix upper triangular"""
    return [[element if i <= j else 0 for j, element in enumerate(row)] for i, row in enumerate(matrix)]


def log_to_csv(matrix, logfile):
    """Log the matrix to a CSV file"""
    with open(logfile, 'a') as f:
        writer = csv.writer(f)
        for row in matrix:
            writer.writerow(row)


def apply_matrix_transformations(matrix, transformations, logfile):
    """Apply a list of transformations to the matrix and log each step to a CSV file"""
    result = matrix
    for transformation in transformations:
        result = transformation(result)
        log_to_csv(result if isinstance(result, list) else [[result]], logfile)
    return result


def print_matrix(matrix):
    if isinstance(matrix, list):
        print(np.array(matrix))
    else:
        print(matrix)


def main():
    print("Welcome to the Matrix Transformations tool!")
    n = int(input("Please enter the size for the identity matrix: "))
    identity_matrix = create_identity_matrix(n)

    print("Original matrix:")
    print_matrix(identity_matrix)

    transformations = []
    if input(
            "Would you like to apply number transformations (multiplication by two, filtering out odd numbers, sum of neighbours)? (yes/no): ") == "yes":
        transformations.append(apply_number_transformations)
    if input("Would you like to double the elements on the main diagonal? (yes/no): ") == "yes":
        transformations.append(double_diagonal)
    if input("Would you like to zero out elements below the main diagonal? (yes/no): ") == "yes":
        transformations.append(zero_out)

    file_name = input("Please enter the name of the CSV file where the results will be logged (e.g., 'logfile.csv'): ")
    dir_path = input(
        "Please enter the directory where the CSV file will be saved or press 'Enter' to use the default directory: ").strip()
    dir_path = dir_path if dir_path else DEFAULT_LOG_PATH
    logfile = os.path.join(dir_path, file_name)
    result = apply_matrix_transformations(identity_matrix, transformations, logfile)

    print("\nResult:")
    print_matrix(result)


if __name__ == "__main__":
    main()