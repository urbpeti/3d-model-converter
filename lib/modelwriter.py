class ModelWriter:
    def __init__(self, model_writing_strategy):
        self._write_strategy = model_writing_strategy

    def write(self, path, model):
        self._write_strategy(path, model)
