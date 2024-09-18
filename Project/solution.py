from bap import BAProblem

def read_solution_from_file(file_path):
    """
    Reads the solution from a file and converts it into a list of tuples.

    Each tuple represents (mooring time, berth section) for a vessel.

    :param file_path: Path to the file containing the solution
    :return: A list of tuples representing the solution
    """
    try:
        with open(file_path, 'r') as file:
            solution_str = file.read().strip()
            solution = eval(solution_str)
            if isinstance(solution, list) and all(isinstance(item, tuple) and len(item) == 2 for item in solution):
                return solution
            else:
                raise ValueError("Solution format is invalid. It should be a list of (ui, vi) tuples.")
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise ValueError(f"An error occurred while reading the solution: {e}")


if __name__ == '__main__':
    bap = BAProblem()
    input_file = 'Data/ex100.dat'  # Input file path
    solution_file = 'Data/ex100.plan'  # Input file path for the solution

    # Load the BAP problem
    bap.load(input_file)

    # Example solution (list of tuples representing (mooring time, berth section))
    solution = read_solution_from_file(solution_file)

    # Check if the solution is valid
    if bap.check(solution):
        print("Valid solution.")
        # Calculate and print the total cost
        print("Total cost:", bap.cost(solution))
    else:
        print("Invalid solution.")
