# FunFoto

### Dependencies
- `python3`
- `OpenCV`
- `numpy`
- `tkinter`
- `PIL` (to install run `$pip3 install pillow`)

## Run the code with GUI
```python
python3 GUI.py
```

## Run the code without GUI
```python
python3 transform.py
```
This will run all the transformation functions one by one in the following order:
- Rotation
- Translation
- Shearing
- Reflection
- Perspective Transformation
- Non-Linear Warping

All the transformations will run with an interval of 2 seconds.

### Test Images
- All the test-images are in the `/img` folder


### Testing Environments
- MacOS
- Ubuntu
