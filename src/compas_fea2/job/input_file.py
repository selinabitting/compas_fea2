from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from compas_fea2.base import FEAData
from compas_fea2.utilities._utils import timer


class InputFile(FEAData):
    """Input file object for standard FEA.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    """

    def __init__(self, name=None, **kwargs):
        super(InputFile, self).__init__(name=name, **kwargs)
        self._job_name = None
        self._job_data = None
        self._file_name = None
        self._extension = None

    @property
    def problem(self):
        return self._registration

    @property
    def model(self):
        return self.problem._registration

    @property
    def job_data(self):
        """The job_data property."""
        return self._generate_jobdata()

    @classmethod
    def from_problem(cls, problem):
        """Create an InputFile object from a :class:`compas_fea2.problem.Problem`

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            Problem to be converted to InputFile.

        Returns
        -------
        obj
            InputFile for the analysis.
        """
        input_file = cls()
        input_file._registration = problem
        input_file._job_name = problem._name
        input_file._file_name = '{}.{}'.format(problem._name, input_file._extension)
        return input_file

    # ==============================================================================
    # General methods
    # ==============================================================================
    def write_to_file(self, path=None):
        """Writes the InputFile to a file in a specified location.

        Parameters
        ----------
        path : str
            Path to the folder where the input file will be saved.

        Returns
        -------
        r : str
            Information about the results of the writing process.
        """
        path = path or self.problem.path
        # try:
        file_path = os.path.join(path, self._file_name)
        with open(file_path, 'w') as f:
            f.writelines(self.job_data)
        print('Input file generated in: {}'.format(file_path))
        # except:
        #     out = 'ERROR: input file not generated!'
        # print(out)

    def _generate_jobdata(self, *args, **kwargs):
        raise NotImplementedError('This method is not available for the selected backend!')


class ParametersFile(InputFile):
    """_summary_

    Parameters
    ----------
    InputFile : _type_
        _description_
    """
    pass