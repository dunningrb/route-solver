from route_solver import RouteSolver
import time
import argparse


def setup():
    """Process command-line arguments.
    """

    ap = argparse.ArgumentParser(
        description=f'This program finds a best route between two U.S. cities.'
    )

    ap.add_argument('--start', help='The starting city.', required=True)
    ap.add_argument('--end', help='The ending city.', required=True)
    ap.add_argument('--opt', help='The choice of optimization:'
                                  '\n\tsegments.... fewest connecting roads,'
                                  '\n\tdistance.... shortest distance'
                                  '\n\ttime........ fastest time'
                                  '\n\taccidents... lowest-probability (cycling)')

    args = ap.parse_args()

    return {'start': args.start, 'end': args.end, 'opt': args.opt}


def list_to_str(list_, *, end_line=False, delimiter=None):
    """Covert the given list to a string and return it.
    """
    delimiter = '' if delimiter is None else delimiter
    string = delimiter.join([str(i) if type(i) is not str else i for i in list_])

    if end_line and not string.endswith('\n'):
        string += '\n'
    return string


if __name__ == "__main__":
    params = setup()
    solver = RouteSolver(start=params['start'], end=params['end'], opt=params['opt'])

    opt_string = {
        'segments': 'Optimizing for fewest connecting roads.',
        'distance': 'Optimizing for shortest distance.',
        'time': 'Optimizing for shortest time.',
        'accidents': 'Optimizing for smallest probability of a bicycling accident.'
    }[params['opt']]

    starting_at = params['start'].replace('_', ' ')
    ending_at = params['end'].replace('_', ' ')

    start_time = time.time()
    print('********* ROUTE SOLVER STARTING *********')
    print(f'Searching for route between {starting_at} and {ending_at}.')
    print(opt_string)
    solution = solver.solve()
    end_time = time.time()
    calc_time = end_time - start_time
    print(f'Found solution in {round(calc_time, 4)} seconds.')
    print(f'SOLUTION:')

    if solution is not None:
        route = list_to_str(solution.path, delimiter='\n\t\t')

        output = list()
        output.append(f'\tRoad segments:\t{solution.data.segments}')
        output.append(f'\n\tDistance: \t{solution.data.distance} miles')
        output.append(f'\n\tTravel Time:\t{round(solution.data.hours, 4)} hours')
        output.append(f'\n\tExpected cycling accidents: {round(solution.data.accidents, 6)}')
        output.append('\n\tConnecting cities:\n\t\t')
        output.append(route)

        print(list_to_str(output))
    else:
        print('No solution.')
    print('********* ROUTE SOLVER FINISHED *********')
