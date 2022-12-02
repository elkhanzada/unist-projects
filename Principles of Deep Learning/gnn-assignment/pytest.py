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
		
	ep = ExecutePreprocessor(timeout=60, kernel_name='python')
	nb_out = ep.preprocess(nb_in)
	return nb_out

def test_gnn_node_classification():
	nb_out = execute_notebook('gnn_node_classification_assignment.ipynb')
	# load the last cell's output
	print(float(nb_out[0]['cells'][-1]['outputs'][-1]['text']))
	assert is_float(nb_out[0]['cells'][-1]['outputs'][-1]['text']) == True
	assert float(nb_out[0]['cells'][-1]['outputs'][-1]['text']) > 0.5

if __name__ == '__main__':
	test_gnn_node_classification()
