from stream_batch_processing.bucketing_strategy import FirstFitDecreasing
from stream_batch_processing.interfaces import File

MB = 10**6
CAPACITY = 10 * MB


def make_files(sizes_mb: list[float]) -> list[File]:
    files = []
    for index, size_mb in enumerate(sizes_mb):
        name = f"f{index + 1}"
        size_bytes = round(size_mb * MB)
        files.append(File(name=name, size_bytes=size_bytes))
    return files


def test_example_for_ffd():
    files = make_files([3.0, 7.0, 0.4, 0.2, 6.5, 14.0, 2.5, 0.9, 4.0, 5.5])

    buckets = FirstFitDecreasing(CAPACITY).pack(files)

    sizes = [[file.size_bytes / MB for file in bucket.files] for bucket in buckets]
    assert sizes == [[14.0], [7.0, 3.0], [6.5, 2.5, 0.9], [5.5, 4.0, 0.4], [0.2]]