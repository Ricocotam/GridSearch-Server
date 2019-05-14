import threading
from typing import Iterator, List, Callable

import fabric


class Server(object):
    def __init__(self, name: str, set_generator: Iterator,
                 connection: fabric.Connection, 
                 prefixs: List[str]):
        self.name = name
        self.generator = set_generator
        self.prefixs = prefixs
    
    def add_prepro(self, *commands):
        self.prefixs.extend(commands)

    def start_experiment(self, gpu: str):
        pass

    


class GPU(object):
    def __init__(self, name: str, nb_max_exp: int, server: Server):
        self.name = name
        self.nb_max_exp = nb_max_exp
        self.server = server

        self.thread = threading.Thread(target=self.run_experiments,
                                       name=f"{self.server.name}:{self.name}")        
        self.threads = []

        self.killing_lock = threading.Lock()
        self.nb_to_kill = 0
    
    def change_nb_xp(self, new_nb: int):
        """Change the number max of experiment on this GPU.

        If the new max is greater than the previous, starts the new experiments
        ASAP.

        If the new max is lower, each time an experiment ends it will kills
        itself if there are too many ones already running.

        Parameters
        -----------
            new_nb : the new number of experiment
        
        Thread Safety
        --------------
            Not thread safe
        """
        if new_nb > self.nb_max_exp:
            new_threads = [
                threading.Thread(target=self.run_one_experiment, 
                                 name=f"{self.server.name}:{self.name}-{i}")
                for i in range(self.nb_max_exp, new_nb)
            ]
            self.threads.extend(new_threads)
            for thread in new_threads:
                thread.start()
        else:
            with self.killing_lock:
                self.nb_to_kill += self.nb_max_exp - new_nb
        self.nb_max_exp = new_nb

    def start(self):
        self.thread.start()

    def run_experiments(self):
        """Run the experiments on the GPU.
        
        This is ran inside a thread. The thread ends when all subthreads end.
        A subthread ends when either the number of max experiment changes or
        when there's not more experiment to run.

        Raise
        ------
            RuntimeError : if called more than one times
        """
        if len(self.threads) > 0:
            raise RuntimeError
        
        self.threads = [
            threading.Thread(target=self.run_one_experiment, 
                             name=f"{self.server.name}:{self.name}-{i}")
            for i in range(self.nb_max_exp)
        ]

        for thread in self.threads:
            thread.start()
        
        all_joined = False
        prev_len = len(self.threads)

        while True:
            if all_joined and len(self.threads) == prev_len:
                break
            all_joined = False
            
            for thread in self.threads:
                thread.join()
            
            all_joined = True
            prev_len = len(self.threads)


    def run_one_experiment(self):
        """One thread running one experiment at the time.
        
        The thread stops when either there's no more parameter
        set to try or if the number of experiments/gpu has been reduced.
        """
        while True:
            with self.killing_lock:
                if self.nb_to_kill > 0:
                    self.nb_to_kill -= 1
                    break

            self.server.start_experiment(self.name)
