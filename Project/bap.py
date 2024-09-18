# import search

class BAProblem:
    def __init__(self):
        """Initialize the BAP problem."""
        self.initial = None
        self.S = 0  # Size of berth space
        self.N = 0  # Number of vessels
        self.vessels = []  # To store the vessel information (ai, pi, si, wi)

    def load(self, fh):
        """Loads the BAP problem from a file."""
        try:
            with open(fh, 'r') as file:
                lines = file.readlines()

            # Filter out comment lines and empty lines
            config_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]

            if len(config_lines) == 0:
                raise ValueError("File is empty or contains only comments.")

            # First line defines S (berth space size) and N (number of vessels)
            self.S, self.N = map(int, config_lines[0].split())

            # Remaining N lines define the vessels' parameters (ai, pi, si, wi)
            for i in range(1, self.N + 1):
                ai, pi, si, wi = map(int, config_lines[i].split())
                self.vessels.append((ai, pi, si, wi))

        except FileNotFoundError:
            raise FileNotFoundError(f"File '{fh}' not found.")
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")

    def cost(self, sol):
        """Calculate the total weighted flow time for a given solution."""
        total_cost = 0
        for i, (ui, vi) in enumerate(sol):
            ai, pi, si, wi = self.vessels[i]
            ci = ui + pi  # Departure time (mooring start + processing time)
            fi = ci - ai  # Flow time (departure time - arrival time)
            total_cost += wi * fi  # Add the weighted flow time to the total
        return total_cost

    def check(self, sol):
        """Check if the given solution satisfies the BAP constraints."""
        for i, (ui, vi) in enumerate(sol):
            ai, pi, si, wi = self.vessels[i]

            # Ensure vessels do not overlap in berth sections or time
            for j in range(i + 1, len(sol)):
                uj, vj = sol[j]
                aj, pj, sj, wj = self.vessels[j]

                # Check if vessels overlap in berth sections
                if not (vi + si <= vj or vj + sj <= vi):
                    # Check if vessels overlap in time
                    if not (ui + pi <= uj or uj + pj <= ui):
                        return False  # Overlap found, invalid solution

        return True  # No overlap, valid solution
