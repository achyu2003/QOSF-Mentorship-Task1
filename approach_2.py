Try this

import numpy as np
import cirq

def is_prime(n):
  """Returns True if n is a prime number, False otherwise."""
  for i in range(2, int(np.sqrt(n)) + 1):
    if n % i == 0:
      return False
  return True

def find_the_primes_numbers(number_1, number_2):
  """Finds the two prime numbers that sum a positive integer.

  Args:
    number_1: The positive integer to decompose.
    number_2: A list of two prime numbers to add to obtain number_1.

  Returns:
    A list of two prime numbers that sum number_1.
  """

  # Create a quantum circuit with two qubits.
  circuit = cirq.Circuit(cirq.H(cirq.LineQubit(0)), cirq.H(cirq.LineQubit(1)))

  # Apply a controlled-Z gate between the two qubits, controlled on the first qubit.
  circuit.append(cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)))

  # Measure the two qubits.
  circuit.append(cirq.measure(cirq.LineQubit(0), key='a'))
  circuit.append(cirq.measure(cirq.LineQubit(1), key='b'))

  # Simulate the circuit and get the results.
  simulator = cirq.Simulator()
  results = simulator.run(circuit, repetitions=1)

  # Get the measured values of the two qubits.
  a = results.measurements['a'][0]
  b = results.measurements['b'][0]

  # Convert the measured values to integers.
  a_int = int(a)
  b_int = int(b)

  # Check if the two measured values are prime numbers.
  if is_prime(a_int) and is_prime(b_int) and a_int + b_int == number_1:
    # If the two measured values are prime numbers and sum to number_1, return them.
    number_2[0] = a_int
    number_2[1] = b_int
    return number_2
  else:
    # Otherwise, return an empty list.
    return []

number_1 = 10
number_2 = []

# Find the two prime numbers that sum number_1.
result = find_the_primes_numbers(number_1, number_2)

# Print the two prime numbers.
if result:
  print(result)
else:
  print("No two prime numbers sum to", number_1)
