import os

import h5py
import numpy as np
import typer
from PIL import Image

app = typer.Typer()


def convert_nika_mask_to_tiff(
    nika_mask_path,
    tiff_path,
    invert=True,
    mask_key="M_ROIMask",
):
    """
    Converts a Nika/Igor HDF5 mask file to a TIFF image.
    The mask data is assumed to be stored under the `M_ROIMask` dataset.
    The mask is rotated and flipped to align with the data in detector images.
    For use with PyFAI, the mask values are inverted by default.

    Parameters:
    nika_mask_path (str):
        Path to the input Nika HDF5 file containing the mask.
    tiff_path (str):
        Path where the output TIFF image will be saved.
    invert (bool, optional):
        If True, inverts the mask values. Default is True.
    mask_key (str, optional):
        Key in the HDF5 file where the mask data is stored. Default is "M_ROIMask".
    """

    # Masks exported from Nika/Igor have zeros for areas to be masked out
    with h5py.File(nika_mask_path, "r") as hdf_file:
        if mask_key in hdf_file.keys():
            mask_data = hdf_file[mask_key][:]
            if invert:
                mask_data = np.where(mask_data == 0, 1, 0)

            mask_image = Image.fromarray(mask_data.astype("uint8"))
            mask_image = mask_image.transpose(Image.FLIP_TOP_BOTTOM)
            mask_image = mask_image.rotate(-90, expand=True)
            mask_image.save(tiff_path, format="TIFF")
            print(f"Saved mask to {tiff_path}")


def convert_tiff_to_nika_mask(
    tiff_path,
    nika_mask_path,
    invert=False,
    mask_key="MROI_Mask",
):
    """
    Converts a TIFF image to a Nika/Igor HDF5 mask file.
    The data is saved under the `M_ROIMask` dataset and with data type uint8,
    To follow Irena mask convenctions, the mask is rotated and flipped,
    inverted (if needed, e.g. when exporting with PyFAI),
    and the it is ensured that the file path ends in _mask.hdf.

    Parameters:
        tiff_path (str): The file path to the input TIFF image.
        nika_mask_path (str): The file path to save the output Nika mask HDF5 file.
        invert (bool): Whether to invert the mask.
        mask_key (str): The key to use for the mask dataset.
    """
    mask_image = Image.open(tiff_path)
    mask_image = mask_image.rotate(90, expand=True)
    mask_image = mask_image.transpose(Image.FLIP_TOP_BOTTOM)
    mask_data = np.array(mask_image)
    if invert:
        mask_data = np.where(mask_data == 0, 1, 0)
    if not nika_mask_path.endswith("_mask.hdf"):
        nika_mask_path = nika_mask_path.replace(".hdf", "_mask.hdf")
        print("Modyfied output file path such that it ends with '_mask.hdf'.")

    with h5py.File(nika_mask_path, "w") as hdf_file:
        hdf_file.create_dataset(mask_key, data=mask_data.astype("uint8"), dtype="uint8")
        print(f"Saved mask to {nika_mask_path}")


@app.command()
def convert_mask(
    input_path: str = typer.Argument(..., help="Path to the input mask file."),
    output_path: str = typer.Argument(..., help="Path to the output mask file."),
    invert: bool = typer.Option(
        False,
        help="If set, the mask will be inverted during conversion: "
        + "non-zero values become 0, and zero values become 1. "
        + "Nika/Igor masks out non-zero values.",
    ),
    mask_key: str = typer.Option(
        "M_ROIMask",
        help="Key for the mask data in the HDF5 file",
    ),
):
    """
    Convert between Nika/Igor HDF5 mask and TIFF mask formats.
    """
    # Check that the input file exists
    if not os.path.exists(input_path):
        typer.echo(f"Error: Input file {input_path} does not exist.")
        raise typer.Exit(code=1)

    # Determine conversion direction based on file extensions
    if (
        input_path.lower().endswith(".tiff") or input_path.lower().endswith(".tif")
    ) and output_path.lower().endswith(".hdf"):
        print(
            f"Converting TIFF image at {input_path}"
            + f" to Nika HDF5 mask at {output_path}...",
        )
        convert_tiff_to_nika_mask(
            tiff_path=input_path,
            nika_mask_path=output_path,
            invert=invert,
            mask_key=mask_key,
        )
    elif input_path.lower().endswith(".hdf") and (
        output_path.lower().endswith(".tiff") or output_path.lower().endswith(".tif")
    ):
        print(
            f"Converting Nika HDF5 mask at {input_path}"
            + f" to TIFF image at {output_path}...",
        )
        convert_nika_mask_to_tiff(
            nika_mask_path=input_path,
            tiff_path=output_path,
            invert=invert,
            mask_key=mask_key,
        )
    else:
        print(
            "Error: Unsupported file format. Please provide a pair of files: "
            + "one .tiff/.tif and one .hdf file. The first given file must exist.",
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
