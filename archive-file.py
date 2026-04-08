import argparse
import logging
import multiprocessing
import eccodes as _
import pyfdb

_logger = logging.getLogger(__name__)


class FDBClient:
    def __init__(self) -> None:
        self.fdb = pyfdb.FDB()

    def archive_file(self, path: str) -> None:
        """Archives a file to FDB. Failure is indicated with a RuntimeError."""
        _logger.info("Archiving to FDB %s", path)
        try:
            with open(path, "rb") as f:
                self.fdb.archive(f.read())
        except pyfdb.pyfdb.FDBException as e:
            raise RuntimeError(e) from e

    def flush(self) -> None:
        _logger.info("Flushing FDB")
        self.fdb.flush()

def _worker(path: str) -> None:
    """Worker function that leaks the FDB client into a global, preventing GC."""
    global _fdb_client_ref
    client = FDBClient()
    client.archive_file(path)
    # Intentionally leak: assign to global so refcount never drops to zero
    # and __del__ / FDB destructor is never called in this process
    _fdb_client_ref = client

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive a GRIB file to FDB.")
    parser.add_argument("grib_file", help="Path to the GRIB file to archive.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    worker = multiprocessing.Process(target=_worker, args=(args.grib_file,))
    worker.start()
    worker.join()
