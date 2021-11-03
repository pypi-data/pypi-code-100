import requests
import bs4


class BmkgInfo:
    url = "https://www.bmkg.go.id"

    def __init__(self):
        self.content = None
        self.success = False
        self.status_code = 400
        self.message = None
        self.init()

    def init(self):
        try:
            res = requests.get(url=self.url)

            if res.status_code == 200:
                self.content = bs4.BeautifulSoup(res.text, "html.parser")
                self.success = True
                self.status_code = res.status_code
                self.message = "Success"
            else:
                self.status_code = res.status_code
                self.message = "Can't connect to server"
        except Exception as e:
            self.success = False
            self.message = str(e)


class WeatherForecast(BmkgInfo):
    def get_data(self):
        prakicu_list = []

        try:
            if self.success:
                prakicus = self.content.find_all("div", {"class": "service-block"})

                for prakicu in prakicus:
                    city = prakicu.find("h2", {"class": "kota"})
                    wf = prakicu.find_all("p")
                    time = wf[0]
                    weather = wf[1]
                    temp = prakicu.find("h2", {"class": "heading-md"})
                    img = prakicu.find("img")
                    img_src = self.url + "/" + str(img["src"]).replace(" ", "%20")

                    data = {
                        "city": city.text,
                        "hour": str(time.text).replace(u"\xa0", u" "),
                        "wheather": weather.text,
                        "temp": temp.text,
                        "image": img_src,
                    }
                    prakicu_list.append(data)

            else:
                print(self.message)
        except Exception as e:
            print(str(e))
        finally:
            return prakicu_list


class LatestEarthQuake(BmkgInfo):
    def get_data(self):

        latest_data = {}
        try:
            earthq = self.content.find("div", {"class": "gempabumi-detail"})
            time = earthq.find("span", {"class": "waktu"}).text
            magnitude = earthq.select_one("li span.ic.magnitude").next
            depth = earthq.select_one("li span.ic.kedalaman").next
            coordinate = earthq.select_one("li span.ic.koordinat").next
            location = earthq.select_one("li span.ic.lokasi").next
            felt = earthq.select_one("li span.ic.dirasakan").next

            latest_data = {
                "time": time,
                "magnitude": magnitude,
                "depth": depth,
                "coordinate": coordinate,
                "location": location,
                "felt": felt,
            }

        except Exception as e:
            print(str(e))
        finally:
            return latest_data


if __name__ == "__main__":
    wf = WeatherForecast()
    print(wf.get_data())

    leq = LatestEarthQuake()
    print(leq.get_data())
