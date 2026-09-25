# stream-batch-bucketing

Assignment: Data source emits messages following Poisson distribution at rate of about 10msgs/min. Data processing system should create minibatches formed so that minibatch creation is triggered with the first message and contains messages that come in in next 5 minutes. Once minibatch is formed it is sent to a worker pool (10 threads). Creation of new minibatch should not wait for first one to complete.

In parallel with this another process is gathering 100 files nightly and sending them for processing. File sizes are following exp distribution. Processing of small files by individual workers is inefficient and files should be packed into buckets with 10MB in size before being sent to worker pool. Model this system using OOP & SOLID principles. Strategy for bucketing should be easy to change (concrete strategy does not need to be optimal). System should be easy to extend and maintain. Write tests and mocks for data sources and files.

## Quick start

```bash
git clone https://github.com/Ognjen96/stream-batch-bucketing.git # Clone the repo from git
cd stream-batch-bucketing                                        # Go to the root of the repo
docker build -t stream-batch-processing .                        # Build docker file
docker run --rm stream-batch-processing                          # demo, set to 300 seconds, can be set to 5 minutes as per task, by changing in code variables.
docker run --rm stream-batch-processing pytest -v                # tests
docker stop stream-batch-processing                              # stop the execution of container
```

Press Ctrl+C to stop the demo early, the worker pool finishes the tasks it has already started.


## Architecture

<img width="651" height="181" alt="Diagram" src="https://github.com/user-attachments/assets/ee057ebb-2ca9-4585-a8b9-da67c6333c83" />


### Message source

Simulated message source emits messages following Poisson distribution at rate of about 10msgs/min. This is an input to the batcher, whose job is to create minibatches and send it to the worker pool to do the transformation. When the first message arrives, the window of 5 minutes is opened, every message that arrives during that time will be that part of the same mini-batch, after 5 minute window elapses, mini-batch is formed.

### File source

Simulated file source creates 100 files following exp distribution with the avarage file size of 2MB. Those files are sent to the bucketing strategy module, which packs the files in a 10MB bucket (file larger that 10MB gets a bucket of its own), for this particular case, strategy for bucketing which was used is First Fit Decreasing. After the files are stored in buckets, they are then sent to worker pool for processing.

Same worker pool is used for message and file source.

## Design decisions

- A message arriving exactly at the deadline opens a new window.
- When the deadline and a message happen at the same time, the deadline is handled first, and the message will open the new bucket.
- On shutdown, the open window is flushed, so no messages are lost.
- Files larger than 10 MB get a bucket of their own.
- Both flows share one worker pool of 10 threads.
- Sizes are in MB, the capacity check uses a small tolerance.

## Adding a bucketing strategy

Since the bucketing strategy is suppose to be easy to change, `BucketingStrategy` protocol in `interfaces.py` is created. It gives us the possibility to create as many bucketing strategies as we want, and choose which one we want to use. For this assignment only one strategy was created and it is First Fit Decreasing.

```python
class BucketingStrategy(Protocol):
    def pack(self, files: list[File]) -> list[Bucket]: ...
```

If you want to add another strategy:
1. Create a class with 'pack' method, signature must be the same as defined above!! (Same parameters and return value).
2. Select the following strategy in '__main__.py, where it is applied'


## Tests

**Message source** (`test_message_source.py`): 
1. Message ids are sequential
2. The same seed gives the same delays and a different seed different ones
3. Over 10,000 messages the average delay is within 5% of 6 seconds

**File source** (`test_file_source.py`): 
1. The generator returns the requested number of files
2. The same seed gives the same sizes; every size is positive
3. Over 10,000 files the average size is within 5% of 2 MB.
