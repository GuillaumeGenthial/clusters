import os
import sys
import time
import random
import numpy as np
import cPickle as pickle
from optparse import OptionParser
import numpy as np

def apply_options(config, options):
    """
    Args:
        config (module) with parameters
        options : returned by args
    Returns:
        config class
    """
    file = config.__file__.split(".")[-2]+".py"
    print file
    config = config.config
    config.config_files = [config.config_files, file]
    if options.test:
        config.max_iter = 10
        config.n_epochs = 2
        config.train_files = "data/config_test/train.txt"
        config.dev_files = "data/config_test/dev.txt"
        config.test_files = "data/config_test/test.txt"

    if options.restore:
        config.restore = True
        
    if options.epochs != 20:
        config.n_epochs = options.epochs

    return config


def args(default):
    """
    Parses input from command line
    Args:
        default (string): default name of config file
    Returns:
        options
    """
    parser = OptionParser(usage='usage: %prog [options] ')
    parser.add_option('-c', '--config',
                      action='store',
                      dest='config',
                      default=default,
                      help='config file',)

    parser.add_option('-e', '--epochs',
                      action='store',
                      dest='epochs',
                      type=int,
                      default=20,
                      help='number of epochs',)
    
    parser.add_option('-t', '--test',
                      action='store_true',
                      dest='test',
                      default=False,
                      help='Use subset of dataset',)

    parser.add_option('-r', '--restore',
                      action='store_true',
                      dest='restore',
                      default=False,
                      help='Restore from latest weights',)
   
    (options, _) = parser.parse_args()


    return options

def get_all_dirs(path, shuffle=False):
    """
    Return a list of string of all dir name in path
    """
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    if shuffle:
        random.shuffle(dirs)
    return dirs

def get_all_files(path, shuffle=False):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    if shuffle:
        random.shuffle(files)
    return files

def check_dir(path):
    """
    Check if path exists
    if not, creates it
    """
    if not os.path.exists(path):
        os.makedirs(path)

def check_file(path):
    return os.path.isfile(path)

def pickle_dump(obj, path, verbose=True):
    """
    Dump obj in path with pickle highest protocol
    """
    if verbose:
        print "Dumping in file {}".format(path)
    with open(path, "wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    if verbose:
        print "- done."

def pickle_load(path, verbose=True):
    """
    Load obj in path
    """
    if verbose:
        print "Loading from file {}".format(path)
    with open(path, "rb") as f:
        return pickle.load(f)
    if verbose:
        print "- done."




class Progbar(object):
    """
    Progbar class copied from keras (https://github.com/fchollet/keras/)
    Displays a progress bar.
    Small edit : added strict arg to update
    # Arguments
        target: Total number of steps expected.
        interval: Minimum visual progress update interval (in seconds).
    """

    def __init__(self, target, width=30, verbose=1):
        self.width = width
        self.target = target
        self.sum_values = {}
        self.unique_values = []
        self.start = time.time()
        self.total_width = 0
        self.seen_so_far = 0
        self.verbose = verbose

    def update(self, current, values=[], exact=[], strict=[]):
        """
        Updates the progress bar.
        # Arguments
            current: Index of current step.
            values: List of tuples (name, value_for_last_step).
                The progress bar will display averages for these values.
            exact: List of tuples (name, value_for_last_step).
                The progress bar will display these values directly.
        """

        for k, v in values:
            if k not in self.sum_values:
                self.sum_values[k] = [v * (current - self.seen_so_far), current - self.seen_so_far]
                self.unique_values.append(k)
            else:
                self.sum_values[k][0] += v * (current - self.seen_so_far)
                self.sum_values[k][1] += (current - self.seen_so_far)
        for k, v in exact:
            if k not in self.sum_values:
                self.unique_values.append(k)
            self.sum_values[k] = [v, 1]

        for k, v in strict:
            if k not in self.sum_values:
                self.unique_values.append(k)
            self.sum_values[k] = v

        self.seen_so_far = current

        now = time.time()
        if self.verbose == 1:
            prev_total_width = self.total_width
            sys.stdout.write("\b" * prev_total_width)
            sys.stdout.write("\r")

            numdigits = int(np.floor(np.log10(self.target))) + 1
            barstr = '%%%dd/%%%dd [' % (numdigits, numdigits)
            bar = barstr % (current, self.target)
            prog = float(current)/self.target
            prog_width = int(self.width*prog)
            if prog_width > 0:
                bar += ('='*(prog_width-1))
                if current < self.target:
                    bar += '>'
                else:
                    bar += '='
            bar += ('.'*(self.width-prog_width))
            bar += ']'
            sys.stdout.write(bar)
            self.total_width = len(bar)

            if current:
                time_per_unit = (now - self.start) / current
            else:
                time_per_unit = 0
            eta = time_per_unit*(self.target - current)
            info = ''
            if current < self.target:
                info += ' - ETA: %ds' % eta
            else:
                info += ' - %ds' % (now - self.start)
            for k in self.unique_values:
                if type(self.sum_values[k]) is list:
                    info += ' - %s: %.4f' % (k, self.sum_values[k][0] / max(1, self.sum_values[k][1]))
                else:
                    info += ' - %s: %s' % (k, self.sum_values[k])

            self.total_width += len(info)
            if prev_total_width > self.total_width:
                info += ((prev_total_width-self.total_width) * " ")

            sys.stdout.write(info)
            sys.stdout.flush()

            if current >= self.target:
                sys.stdout.write("\n")

        if self.verbose == 2:
            if current >= self.target:
                info = '%ds' % (now - self.start)
                for k in self.unique_values:
                    info += ' - %s: %.4f' % (k, self.sum_values[k][0] / max(1, self.sum_values[k][1]))
                sys.stdout.write(info + "\n")

    def add(self, n, values=[]):
        self.update(self.seen_so_far+n, values)


