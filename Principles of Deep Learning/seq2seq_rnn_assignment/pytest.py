import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import typing

def is_float(element: typing.Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

def execute_notebook(notebook_filename):
	with open(notebook_filename) as ff:
		nb_in = nbformat.read(ff, nbformat.NO_CONVERT)
		
	ep = ExecutePreprocessor(timeout=500, kernel_name='python')
	nb_out = ep.preprocess(nb_in)
	return nb_out


def test_seq2seq_rnn():
	nb_out = execute_notebook('lstm_seq2seq_assignment.ipynb')
	# load the last cell's output
	print(float(nb_out[0]['cells'][-1]['outputs'][-1]['text']))
	assert is_float(nb_out[0]['cells'][-1]['outputs'][-1]['text']) == True
	assert float(nb_out[0]['cells'][-1]['outputs'][-1]['text']) < 200

if __name__ == '__main__':
	test_seq2seq_rnn()
