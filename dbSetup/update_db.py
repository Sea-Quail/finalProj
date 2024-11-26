import argparse
import inspect
<<<<<<< HEAD
import io
import multiprocessing
from contextlib import redirect_stderr, redirect_stdout

import services
=======
import signal

import services


def timeout_handler(signum, frame):
    raise TimeoutError("Function call timed out")
>>>>>>> 36231da (Sneaking in CI update to only update each for about 10 seconds)


def wrapper(result_queue, func, args, kwargs):
    """Wrapper function to call the target function and put the result in a queue."""
    f = io.StringIO()
    with redirect_stdout(f), redirect_stderr(f):
        result = func(*args, **kwargs)
    result_queue.put((result, f.getvalue()))


def run_function(func, args=(), kwargs={}):
    """
    Runs a function and captures its output.

    :param func: The function to execute.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.
    :return: A tuple containing the result of the function and its output.
    """
    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=wrapper, args=(result_queue, func, args, kwargs)
    )
    process.start()
    process.join()

<<<<<<< HEAD
    # If completed, retrieve the result and output
    return result_queue.get()
=======
    # If no tables are specified, call all functions in services
    tables_to_update = (
        args.tables
        if (args.tables and args.tables != ["ci"])
        else get_all_service_functions()
    )
    isCI = True if args.tables == "test" else False

    # Execute updates
    update_tables(tables_to_update, isCI)
>>>>>>> 36231da (Sneaking in CI update to only update each for about 10 seconds)


def get_all_service_functions():
    """Retrieve all update functions from the services module."""
    return [
        name.replace("upload_", "").replace("_csv", "")
        for name, func in inspect.getmembers(services, inspect.isfunction)
        if name.startswith("upload_") and name.endswith("_csv")
    ]


<<<<<<< HEAD
def update_table(table):
    func_name = f"upload_{table}_csv"
    if hasattr(services, func_name):
        func = getattr(services, func_name)
        result, output = run_function(func)  # Call the function and capture output
        print(output)
    else:
        print(f"Unknown table: {table}")


def update_tables(tables):
    if tables == ["0"]:
        tables = get_all_service_functions()

    processes = []
    for table in tables:
        p = multiprocessing.Process(target=update_table, args=(table,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
=======
def update_tables(tables, isCI):
    for table in tables:
        func_name = f"upload_{table}_csv"
        if hasattr(services, func_name):
            func = getattr(services, func_name)
            if isCI:
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                try:
                    func()  # Call function in test mode
                except TimeoutError:
                    print(f"Update for table {table} timed out")
                finally:
                    signal.alarm(0)  # Disable the alarm
            else:
                func()  # Call function normally
        else:
            print(f"Unknown table: {table}")
>>>>>>> 36231da (Sneaking in CI update to only update each for about 10 seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update database tables.")
    parser.add_argument(
        "tables",
        metavar="T",
        type=str,
        nargs="*",
        help="Names of the tables to update (e.g., people teams allstarfull schools). If no tables are provided, all will be updated.",
    )
    args = parser.parse_args()

    # If no tables are specified, call all functions in services
    tables_to_update = args.tables if args.tables else ["0"]

    # Execute updates
    update_tables(tables_to_update)
