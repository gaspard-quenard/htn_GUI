# htn_GUI


# Create virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install git+https://gitlab.com/pavel.krupala/pyqt-node-editor.git # Strange thing here, if I put this in requirements.txt, the code bug when creating a new node
pip3 install -r requirements.txt
```

# Run the app

If you are using a virtual environment, make sure to activate it first.


```bash
python3 main.py
```