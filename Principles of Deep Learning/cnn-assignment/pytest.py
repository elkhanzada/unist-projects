from operator import truediv
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from pprint import pprint

def is_correct(percentage):
    perc = int(percentage)
    if perc > 10 and perc <= 100:
        return True
    else:
        return False

def execute_notebook(notebook_filename):
    with open(notebook_filename) as ff:
        nb = nbformat.read(ff, nbformat.NO_CONVERT)
    
    pprint(nb['cells'][-1])
    return nb


def test_cnn_assignment():
    nb = execute_notebook('CNN_assignment.ipynb')

    task1 = nb['cells'][-2]['outputs'][-1]['text'].strip().split('\n')[0]
    task2 = nb['cells'][-2]['outputs'][-1]['text'].strip().split('\n')[1] 
    task3 = nb['cells'][-2]['outputs'][-1]['text'].strip().split('\n')[3]

    print(task1)
    print(task2)
    print(task3[-4:-2])

    assert task1 == "torch.Size([3, 224, 224])"
    assert task2 == "torch.Size([1, 100])"
    assert is_correct(task3[-4:-2])

if __name__ == '__main__':
    test_cnn_assignment()
