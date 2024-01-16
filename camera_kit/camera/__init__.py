from __future__ import annotations

# global
import tomli
import tomli_w
import logging
import numpy as np
from pathlib import Path
from tomlkit import document
# typing
from numpy import typing as npt

LOGGER = logging.getLogger(__name__)


class CameraCoefficient:
    """ Class to represent camera coefficients
        intrinsic: Intrinsic camera matrix for the raw (distorted) images
        distortion: The distortion parameters
    """
    def __init__(self, name: str):
        """ Class initialization

        Args:
            name: Camera name
        """
        self.file_path = Path.cwd().joinpath('camera_info', name, 'calibration', 'coefficients.toml')
        self.intrinsic: npt.NDArray[np.float64] = np.identity(3)
        self.distortion: npt.NDArray[np.float64] = np.zeros(4)

    def save(self, dir_path: Path | str = "") -> None:
        """ Class method to load camera coefficients

        Args:
            dir_path: Directory path to the intrinsic and distorted parameters

        """
        if dir_path:
            dir_path = Path(dir_path)
            if not dir_path.is_dir():
                raise NotADirectoryError(f"Directory with given path '{dir_path}' not found.")
            self.file_path = Path(dir_path).joinpath('coefficients.toml')

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        toml = document()
        toml.add("intrinsic", self.intrinsic.tolist())
        toml.add("distortion", self.distortion.tolist())

        with self.file_path.open(mode='wb') as f:
            tomli_w.dump(toml, f)
        LOGGER.debug(f"Save new camera coefficients in folder {str(self.file_path.parent)}")

    def load(self, file_path: Path | str = "") -> None:
        """ Class method to load camera coefficients

        Args:
            file_path: File path to the intrinsic and distorted parameters

        """
        if file_path:
            fp = Path(file_path)
            # Check if path exist
            if not fp.is_file():
                raise FileNotFoundError(f"File with given path '{str(fp)}' not found.")
        else:
            fp = self.file_path
            if not fp.is_file():
                raise FileNotFoundError(f"File with default path '{str(fp)}' not found.")

        with fp.open(mode='rb') as f:
            coeffs = tomli.load(f)
            self.intrinsic = np.array(coeffs['intrinsic'], dtype=np.float64)
            self.distortion = np.array(coeffs['distortion'], dtype=np.float64)
        LOGGER.debug(f"Load camera coefficients successfully.")
