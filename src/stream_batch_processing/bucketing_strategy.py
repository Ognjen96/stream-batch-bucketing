from .interfaces import File, Bucket

class FirstFitDecreasing:
    def __init__(self, capacity_bytes):
        self._capacity_bytes = capacity_bytes

    def pack(self, files: list[File]) -> list[Bucket]:
        sorted_files = sorted(files, key=lambda file: file.size_bytes ,reverse=True)

        buckets  = []
        bucket_sizes  = []

        for file in sorted_files:

            placed = False

            for i in range(len(buckets)):
                if bucket_sizes[i] + file.size_bytes <= self._capacity_bytes:
                    buckets[i].append(file)
                    bucket_sizes[i] += file.size_bytes
                    placed = True
                    break

            if not placed:
                buckets.append([file])
                bucket_sizes.append(file.size_bytes)

        return [
            Bucket(files=tuple(bucket), size_bytes=size)
            for bucket, size in zip(buckets, bucket_sizes)
            ]