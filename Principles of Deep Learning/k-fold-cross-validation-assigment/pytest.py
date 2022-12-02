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

    ep = ExecutePreprocessor(timeout=180, kernel_name='python')
    nb_out = ep.preprocess(nb_in)
    return nb_out


def test_model_selection():
    nb_out = execute_notebook('k_fold_cross_validation_assigment.ipynb')

    # load the last cell's output
    task1 = nb_out[0]['cells'][-1]['outputs'][-1]['text'].strip().split('\n')[0]
    task2 = nb_out[0]['cells'][-2]['outputs'][-1]['text'].strip().split('\n')[0]
    task3 = nb_out[0]['cells'][-3]['outputs'][-1]['text'].strip().split('\n')[0]

    task1_cell = 'k_test = 5\nk_fold_test = k_fold_data(input, k_test)\n\ncheck = True\n\nif len(k_fold_test) != k_test:    \n    check = False\nelse:\n    for fold in k_fold_test:\n        if len(fold[1]) != (input.shape[0] // k_test):\n            check = False\n            break\n\nprint(check)'
    task2_cell = 'print(sum(test_logs)/ len(test_dataset))'
    task3_cell = 'print(test)'

    assert task1 == "True"
    assert is_float(task2)
    assert task3 == "True"

    assert task1_cell == nb_out[0]['cells'][-1]['source']
    assert task2_cell == nb_out[0]['cells'][-2]['source']
    assert task3_cell == nb_out[0]['cells'][-3]['source']


if __name__ == '__main__':
    test_model_selection()