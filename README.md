# Prosthetic_Guitar_Simulator
Oklahoma State University Senior Design project

## Clone the repo
```
git clone https://github.com/Thomas-J-Kidd/Prosthetic_Guitar_Simulator.git
```

## Downloading the model
Make sure that the model is present in in the `fretHand` folder

Your directory should look something like this using the `ls` command

```
⚡➜ fretHand (U main) ls
MANO  mano_v1_2
```


## Running the demo program for creating a 3D hand

1) Nagivate to the correct folder
```Prosthetic_Guitar_Simulator/3d_modelling/fretHand/MANO```

You can verify you are in the right place by using the `pwd` command

2) install the pyhon virtual environment

### Linux

*Install virtualenv if you haven't already*
```sudo apt-get install python3-venv```

*Create a virtual environment*
```python3 -m venv myenv```

*Activate the virtual environment*
```source myenv/bin/activate```


### Windows
*Install virtualenv if you haven't already*
```pip install virtualenv```

*Create a virtual environment*
```virtualenv myenv```

*Activate the virtual environment*
```myenv\Scripts\activate```

3) Install the python libraries
```pip install requirements.txt```

4) Run demo.py

Run the code by using `python demo.py`

5) Deactivate the environment

```deactivate```
