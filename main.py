import logging
import time
from src.image_analyzer import ImageAnalazer
from src.color_table import ColorTable
from src.data_base import DataBase, PhotoTable
from src.flickr import Flickr
from src.logger import init_logging
from src.twitter import Twitter
from src.plate_maker import create_plate

log = logging.getLogger()

if __name__ == "__main__":
    init_logging("log.log")
    will_be_uploaded_N_photos = 1

    with DataBase() as db:
        table = PhotoTable(db=db, table_name="main_photos")
        twitter = Twitter(table=table)
        flickr = Flickr(table=table)
        color_table = ColorTable()
        for _ in range(will_be_uploaded_N_photos):
            pictures = flickr.get_photos()
            photo = flickr.random_photo(pictures)
            photo = flickr.get_photo(photo)
            average_color_of_photo = ImageAnalazer(photo.data).avg_color
            nearest_color = color_table.nearest_color(average_color_of_photo.lab)
            color_sample = create_plate(nearest_color.color)
            color_sample = twitter.upload_photo(color_sample)
            photo = twitter.upload_photo(photo)
            twitter.create_post(nearest_color.color.name, [color_sample, photo])
            time.sleep(2)
