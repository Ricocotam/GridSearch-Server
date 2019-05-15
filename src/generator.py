"""Generate commands."""

class CommandGenerator(object):
    """Generator of commands using formating function applied on parameters."""
    def __init__(self, iterator, formating_function):
        self.iterator = iterator
        self.formating_function = formating_function

    def get_experiment(self, gpu: str):
        """Generate the command with parameters from iterator given a gpu."""
        params = next(self.iterator)
        formated = self.formating_function(params, gpu)
        return formated
