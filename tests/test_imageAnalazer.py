from src.image_analyzer import  ImageAnalazer


def test_avg_color(photo):
    im = ImageAnalazer(photo.data)
    avg = im.avg_color
    assert avg.rgb_values == (90, 70, 63)
