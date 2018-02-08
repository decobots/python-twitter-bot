import httplib2
from xml.etree import ElementTree as etree
from urllib.parse import urlencode


def picture_id(pho):
    """
    function rearranges dictionary in format that I like a little more. TODO: get rid of that function
    :param pho: array with photo tags
    """
    for tag in pho:
        yield {'photo_id': tag.attrib['id'], 'secret': tag.attrib['secret'],
               "farm": tag.attrib["farm"], "server": tag.attrib["server"]}


def flickr_query_to_get_list_of_pictures(request_h):
    """
    f. to get list of photos
    :param request_h:
    :return: byte string with xml response from flivkr inside it
    """
    payload = {'method': 'flickr.people.getPublicPhotos',
               'api_key': '1a19ecf3ddf46b3323bca01dc8afbd81',
               'user_id': '76163487@N05'
               }
    resp, content = request_h.request('https://api.flickr.com/services/rest/?&{}'.format(urlencode(payload)), "POST")
    xml = etree.fromstring(content.decode('utf-8'))
    xml = xml[0]  # get child of root (list of <photo> tags)
    return xml


def flickr_query2(request_h2, photo_index):
    """
    function to load photo from server
    :rtype: object
    """
    resp2, content2 = request_h2.request('https://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(
        photo_index["farm"], photo_index["server"], photo_index['photo_id'], photo_index["secret"]))
    return content2


if __name__ == "__main__":
    h = httplib2.Http(".cache")
    c = flickr_query_to_get_list_of_pictures(h)

    photos = list(picture_id(c))

    for i, p in enumerate(photos):
        pic = flickr_query2(h, p)
        with open("pic{}.jpg".format(i), "wb") as file:
            file.write(pic)
