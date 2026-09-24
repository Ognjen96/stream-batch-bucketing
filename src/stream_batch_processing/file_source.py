import random

from .interfaces import File


class FileGenerator:
    def __init__(self, count: int, avg_size_mb: int, seed: random.Random) -> None:
        self._count = count
        self._avg_size_mb = avg_size_mb
        self._rng = random.Random(seed)


    def generate_files(self) -> list[File]:
        file_list = []
        for i in range(self._count):
            file = File(name = f"File_{i:03d}", size_mb = self._rng.expovariate(1 / self._avg_size_mb))
            file_list.append(file)

        return file_list