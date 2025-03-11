import os
import urllib.request
import urllib
import imghdr
from PIL import Image
import posixpath
import re
from random import randint


BlackListed = ["ytimg.", "scx1.b-cdn.", "googleusercontent.", "alamy."]

def approve(url):
    url = url.lower()
    result = "NOTHING"
    for i in BlackListed:
        if url.find(i) >= 0:
            result = "BLACKLISTED"
            return result
    return result

class Bing:
    def __init__(self, prevlink, query, limit, output_dir, adult, timeout, filter='', verbose=True):
        self.prevlink = prevlink
        self.download_count = 0
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filter = filter
        self.verbose = verbose
        self.seen = set()

        assert type(limit) == int, "limit must be integer"
        self.limit = 32
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout

        # self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.page_counter = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                                      'Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}

    def get_filter(self, shorthand):
        if shorthand == "line" or shorthand == "linedrawing":
            return "+filterui:photo-linedrawing"
        elif shorthand == "photo":
            return "+filterui:photo-photo"
        elif shorthand == "clipart":
            return "+filterui:photo-clipart"
        elif shorthand == "gif" or shorthand == "animatedgif":
            return "+filterui:photo-animatedgif"
        elif shorthand == "transparent":
            return "+filterui:photo-transparent"
        else:
            return ""

    def save_image(self, link, file_path):
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        if not imghdr.what(None, image):
            print('[Error]Invalid image, not saving {}\n'.format(link))
            raise ValueError('Invalid image, not saving {}\n'.format(link))
        with open(str(file_path), 'wb') as f:
            f.write(image)

    def download_image(self, link):
        self.download_count += 1
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
                file_type = "jpg"

            if self.verbose:
                # Download the image
                print("[%] Downloading Image #{} from {}".format(self.download_count, link))

            self.save_image(link, self.output_dir.joinpath("Image_{}.{}".format(
                str(self.download_count), file_type)))
            if self.verbose:
                print("[%] File Downloaded !\n")

                return self.output_dir.joinpath("Image_{}.{}".format(
                str(self.download_count), file_type))

        except Exception as e:
            self.download_count -= 1
            print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))
            return "INVALID SEARCH!"

    def run(self):
        linkstoreturn = ""
        while self.download_count < 1:
            if self.verbose:
                print('\n\n[!!]Indexing page: {}\n'.format(self.page_counter + 1))
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + (
                              '' if self.filter is None else self.get_filter(self.filter))
            request = urllib.request.Request(request_url, None, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf8')
            if html == "":
                print("[%] No more images are available")
                return "INVALID SEARCH!"
            links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
            if self.verbose:
                print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
                print("\n===============================================\n")
            try:
                randomselection = randint(0, len(links)-5)
            except:
                randomselection = 0
            currentselection = 0
            if len(links) < 1:
                return "INVALID SEARCH!"
            else:
                for link in links:
                    if self.download_count < 1 and self.prevlink.find(link) == -1 and currentselection >= randomselection and approve(link) == "NOTHING":
                        self.seen.add(link)
                        pathtocheck = self.download_image(link)
                        print(pathtocheck)
                        if pathtocheck == "INVALID SEARCH!":
                            return "INVALID SEARCH!"
                        else:
                            image = Image.open(pathtocheck)
                            width, height = image.size
                            ratio = width / height
                            image.close()
                            if ratio < 1.35 or height < 360:
                                print("PICTURE INVALID, SEARCHING FOR ANOTHER..")
                                os.remove(pathtocheck)
                                self.download_count -= 1
                            else:
                                linkstoreturn = self.prevlink + linkstoreturn + link
                                return linkstoreturn.replace("INVALID SEARCH!", "")
                    currentselection = currentselection + 1
                self.page_counter += 1
        print("\n\n[%] Done. Downloaded {} images.".format(self.download_count))
        return linkstoreturn
