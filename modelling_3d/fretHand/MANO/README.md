# How to on Windows

1) navigate to the MANO folder
2) Execute `python -m venv env`
3) Execute `.\env\Scripts\activate`
4) Execute `pip install --upgrade pip setuptools wheel`
4) Execute `pip install -r requirements.txt`
5) Execute `python slider_func.py`


If we run into the chumpy problems do this:
1) go to `env/lib/sitepackagas/chumpy and change the following things
2) in ch.py change this line `want_out = 'out' in inspect.getargspec(func).args` to `   want_out = 'out' in inspect.getfullargspec(func).args`

3) in __init__.py change this line `from numpy import bool, int, float, complex, object, unicode, str, nan, inf` to this line `from numpy import bool_, int_, float_, complex_, object_, str_, nan, inf`