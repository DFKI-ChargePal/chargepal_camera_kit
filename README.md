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

### Further demos

More demos can be found under the folder [demos](demos)


## Documentation

To show the library documentation install the docs dependencies of this package

```shell
poetry install --with docs
```

Afterward you can start a local server and open the documentation in your browser
```shell
mkdocs serve
```


## Implement an own camera class

You can add your own camera by creating a concrete class of the abstract class `CameraBase`

```python
from camera_kit import CameraBase


class MyCamera(CameraBase):
    
    type_id = "my_camera"

    def __init__(self, name, frame_size, launch):
        super().__init__(name, frame_size, launch)

    def start(self):
        # Call start procedure of base class
        self._on_start()
        if not self.alive:
            # Set up your camera stream
            # ...
            self.alive = True
            assert self._thread
            self._thread.start()

    def update(self):
        new_frame = None
        # Read next frame from your camera and convert it to a numpy array
        self.color_frame = new_frame

    def end(self):
        # Call end procedure of base class
        self._on_end()
        # Destroy/Release your camera stream
        # ...
```