import logging
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import glob
from app.palette_classification import color_processing, palette
from app.pipeline import pipeline, segmentation_filter, user_palette_classification_filter
from app.utils import segmentation_labels, utils

from celery import Celery

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# config
segmentation_model = 'cloud' # should be in ['local', 'cloud']
device = 'cuda' if torch.cuda.is_available() else 'cpu'
verbose = False

# setting paths
palettes_path = 'app/palette_classification/palettes/'

# loading reference palettes for user palette classification filter
palette_filenames = glob.glob(palettes_path + '*.csv')
reference_palettes = [palette.PaletteRGB().load(
    palette_filename.replace('\\', '/'), header=True) for palette_filename in palette_filenames]


@celery_app.task(name="create_task")
def create_task(file_contents: bytes):
    try:
        
        image = Image.open(io.BytesIO(file_contents))
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

        user_identified_palette = user_palette.description()
        logger.info(f'User palette: {user_palette}')
        logger.info(f'User palette description: {user_identified_palette}')

        return {"message": "Image processed successfully", "palette": user_identified_palette}
    except Exception as e:
        logger.error(f"Error in create_task: {e}")
        return {"error": str(e)}