from .interfaces import File, Bucket

class FirstFitDecreasing:
    def __init__(self, capacity_mb):
        self._capacity_mb = capacity_mb

    def pack(self, files: list[File]) -> list[Bucket]:
        sorted_files = sorted(files, key=lambda file: file.size_mb ,reverse=True)

        buckets  = []
        bucket_sizes  = []

        for file in sorted_files:

            placed = False

            for i in range(len(buckets)):
                if bucket_sizes[i] + file.size_mb <= self._capacity_mb:
                    buckets[i].append(file)
                    bucket_sizes[i] += file.size_mb
                    placed = True
                    break

            if not placed:
                buckets.append([file])
                bucket_sizes.append(file.size_mb)

        result = []
        for bucket, size in zip(buckets, bucket_sizes):
            new_bucket = Bucket(files=tuple(bucket), size_mb=size)
            result.append(new_bucket)

        
        return result