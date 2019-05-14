

class CommandGenerator(object):
    def __init__(self, iterator, formating_function):
        self.iterator = iterator
        self.formating_function = formating_function

    def get_experiment(self, gpu: str):
        params = next(self.iterator)
        formated = self.formating_function(params, gpu)
        return formated