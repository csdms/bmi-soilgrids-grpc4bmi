# examples

Two examples--a [Python script](./run-model-through-grpc4bmi.py)
and a [Jupyter notebook](./run-model-through-grpc4bmi.ipynb)--that demonstrate how to run
the SoilGrids Data Component through the grpc4bmi server built in this project.

In a virtual environment,
install grpc4bmi and other dependencies:
```sh
pip install -r requirements.txt
```

Run the Python example:
```sh
python run-model-through-grpc4bmi.py
```
It'll produce output in the terminal,
as well as PNG files with visualizations.

Start JupyterLab and run the example notebook:
```sh
jupyter lab run-model-through-grpc4bmi.ipynb
```
