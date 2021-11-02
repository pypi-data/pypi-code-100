import os, requests, lxml, re, json
from bs4 import BeautifulSoup


class ImageScraper:

    def __init__(self, query: str = '', amount_to_return: int = 100):
        self.query = query
        self.amount_to_return = amount_to_return

    def get_images(self) -> list[str]:
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

        params = {
            "q": f"pexels {self.query}",
            "tbm": "isch",  # image query results param
            "hl": "en",
        }

        html = requests.get("https://www.google.com/search", params=params, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')

        all_script_tags = soup.select('script')

        # # https://regex101.com/r/48UZhY/4
        matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
        matched_images_data_fix = json.dumps(matched_images_data)
        matched_images_data_json = json.loads(matched_images_data_fix)

        # https://regex101.com/r/pdZOnW/3
        matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",',
                                               matched_images_data_json)

        # https://regex101.com/r/NnRg27/1
        matched_google_images_thumbnails = ', '.join(
            re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                       str(matched_google_image_data))).split(', ')

        # for fixed_google_image_thumbnail in matched_google_images_thumbnails:
        #     # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        #     google_image_thumbnail_not_fixed = bytes(fixed_google_image_thumbnail, 'ascii').decode('unicode-escape')
        #
        #     # after first decoding, Unicode characters are still present. After the second iteration, they were decoded.
        #     google_image_thumbnail = bytes(google_image_thumbnail_not_fixed, 'ascii').decode('unicode-escape')

        # removing previously matched thumbnails for easier full resolution image matches.
        removed_matched_google_images_thumbnails = re.sub(
            r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', '',
            str(matched_google_image_data))

        # https://regex101.com/r/fXjfb1/4
        # https://stackoverflow.com/a/19821774/15164646
        matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
                                                           removed_matched_google_images_thumbnails)

        full_res_imgs = []

        for fixed_full_res_image in matched_google_full_resolution_images:
            # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
            original_size_img_not_fixed = bytes(fixed_full_res_image, 'ascii').decode('unicode-escape')
            original_size_img = bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape')

            full_res_imgs.append(original_size_img)

        return full_res_imgs
