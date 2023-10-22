
import pylab
import numpy as np
import tempfile
import os
from qiskit import BasicAer
from qiskit.tools.visualization import plot_histogram

from qiskit.exceptions import MissingOptionalLibraryError
from qiskit.circuit.library.phase_oracle import PhaseOracle
from qiskit_algorithms import AmplificationProblem
from qiskit_algorithms import Grover
from qiskit.primitives import Sampler

dimacs_cnf = []

def generate_dimacs_cnf_string(target, prime_list):
    num_variables = len(prime_list)
    num_clauses = num_variables + num_variables * (num_variables - 1) // 2 + 2

    # Add the header line to the string
    dimacs_cnf.append(f"p cnf {num_variables} {num_clauses}")

    # Add clauses for at least one number is selected
    at_least_one_clause = " ".join(str(i + 1) for i in range(num_variables))
    dimacs_cnf.append(at_least_one_clause)

    # Add clauses for at most one number is selected
    for i in range(num_variables):
        for j in range(i + 1, num_variables):
            dimacs_cnf.append(f"-{i + 1} -{j + 1}")

    # Add clauses for the sum constraint
    for i, prime in enumerate(prime_list):
        dimacs_cnf.append(f"{i + 1} {prime}")

    # Add a dummy clause to find all solutions
    dimacs_cnf.append(at_least_one_clause)

    # print("\n".join(dimacs_cnf))
    return "\n".join(dimacs_cnf)


def find_the_primes_numbers(num_1, list_nums):
    '''
    num_1 : integer value that is the positive number to decompose,
    
    list_nums : integer list that has two prime numbers to add to obtain number_1.
    Return the number_a and number_b
    '''
    input_3sat_instance = generate_dimacs_cnf_string(num_1, list_nums)
    
    fp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    fp.write(input_3sat_instance)
    file_name = fp.name
    fp.close()
    oracle = None
    try:
        oracle = PhaseOracle.from_dimacs_file(file_name)
    except ImportError as ex:
        print(ex)
    finally:
        os.remove(file_name)
    problem = None
    if oracle is not None:
        problem = AmplificationProblem(oracle, is_good_state=oracle.evaluate_bitstring)

    grover = Grover(sampler=Sampler())
    result = None
    if problem is not None:
        result = grover.amplify(problem)
        print(result.assignment)

    if result is not None:
    display(plot_histogram(result.circuit_results[0]))





target_number = 18  # Change this to your target number
prime_numbers = [1,3,5,7,11,13,15] # Change this to your list of prime numbers

find_the_primes_numbers(target_number, prime_numbers)
