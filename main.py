from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import glob
from PIL import Image

from random import randint

from palette_classification import color_processing, palette
from pipeline import pipeline, segmentation_filter, user_palette_classification_filter
from utils import segmentation_labels, utils
import io


# config
segmentation_model = 'cloud' # should be in ['local', 'cloud']
device = 'cuda' if torch.cuda.is_available() else 'cpu'
verbose = False

# setting paths
palettes_path = 'palette_classification/palettes/'

# loading reference palettes for user palette classification filter
palette_filenames = glob.glob(palettes_path + '*.csv')
reference_palettes = [palette.PaletteRGB().load(
    palette_filename.replace('\\', '/'), header=True) for palette_filename in palette_filenames]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)) -> JSONResponse:
    """
    Endpoint to upload an image and convert it to RGB format.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    # Convert to RGB
    image_rgb = image.convert("RGB")

    # instantiating pipeline
    pl = pipeline.Pipeline()

    sf = segmentation_filter.SegmentationFilter(segmentation_model)
    pl.add_filter(sf)

    # executing pipeline: sf
    img, masks = pl.execute(image_rgb, device, verbose)
    img_segmented = color_processing.colorize_segmentation_masks(masks, segmentation_labels.labels)

    # adding user palette classification filter
    upcf = user_palette_classification_filter.UserPaletteClassificationFilter(reference_palettes)
    pl.add_filter(upcf)

    # executing pipeline: sf -> upcf
    user_palette = pl.execute(image_rgb, device, verbose)
    print('User palette:', user_palette)

    user_identified_palette = user_palette.description()


    return JSONResponse(content={"message": "Image uploaded successfully", "palette": user_identified_palette})

