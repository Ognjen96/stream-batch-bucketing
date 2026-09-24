import pytest
 
from stream_batch_processing.sources.file_source import FileGenerator
 
AVG_SIZE_MB = 2.0
NUM_OF_FILES = 100
 
def generate_files(count: int = 100, seed: int = 42):
    return FileGenerator(count, AVG_SIZE_MB, seed).generate_files()
 
 
def test_generates_requested_number_of_files():
    files = generate_files(count=NUM_OF_FILES)
    assert len(files) == NUM_OF_FILES

 
def test_same_seed_gives_same_sizes():
    sizes_a = [file.size_mb for file in generate_files(seed=7)]
    sizes_b = [file.size_mb for file in generate_files(seed=7)]
    sizes_c = [file.size_mb for file in generate_files(seed=9)]

    assert sizes_a == sizes_b
    assert sizes_a != sizes_c
 
 
def test_all_sizes_are_positive():
    sizes = [file.size_mb for file in generate_files()]

    for i in sizes:
        assert i > 0
 
 
def test_average_size_matches_configured_mean():
    sizes = [file.size_mb for file in generate_files(count = 10000)]
    average = sum(sizes) / len(sizes)

    assert average == pytest.approx(AVG_SIZE_MB, rel=0.05)