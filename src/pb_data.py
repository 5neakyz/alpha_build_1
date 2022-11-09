import dataclasses

@dataclasses.dataclass
class pb_data():
    """
    Data structure to hold the progress bar data.
    """
    progress: int = 0
    total: int = 0

    def add_to_progress(self, value):
        self.progress += value
        return self.progress

if __name__ == '__main__':
    pb = pb_data()
    pb.total = 100
    for _ in range(10):
        pb.add_to_progress(10)
        print(f"{pb.total}/{pb.progress}")
