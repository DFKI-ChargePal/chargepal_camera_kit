# Camera Kit

A tool kit to work and interface to serial cameras



## Installation for users

1) Clone the repository 
```shell
  git clone git@git.ni.dfki.de:gjohn/ssl_dataset.git
```

2) Navigate to the repository directory
```shell
  cd ssl_dataset
 ```

3) Initialize [poetry](https://python-poetry.org/)
```shell
  poetry install
```


## Getting started

### Camera Classes
Currently, there are two camera classes implemented. To choose between the different camera types, the string used for 
initialization is analyzed. This means it is mandatory that the string starts with the camera type id.

The following type ids are currently available:

- `build_in`
- `realsense`


### Minimal Demo

If you have an usb or an integrated camera you can run the following minimal example. 

``` python
import camera_kit as ck

with ck.camera_manager('build_in_camera') as cm:
    while not ck.user_signal.stop():
        cm.render()

```
To stop the program press `ESC` or `Q` on your keyboard

### Camera Calibration


## Implement an own camera class
