import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy import signals
from scrapy.linkextractors import LinkExtractor
from pydispatch import dispatcher
import json
import os
from tqdm import tqdm
from os.path import exists



class VRoidSpider(scrapy.Spider):
    name = "VRoidSpider"
    baseUrl = "https://hub.vroid.com"
    headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            ### Future Versions Might Need This Header To Be Updated To Match Updates To Webiste/
            "x-api-version": "10"
    }
    cookies = {
        "_vroid_session":"bec9e805513ad35b88d526c79db9eaab"
    }

    model_href_format = "/en/characters/{}/models/{}"
    model_preview_format = "/api/character_models/{}/optimized_preview"
    model_download_format = "/api/character_models/{}/versions/{}/download"
    models = {}
    dwl_count = 0
    mode = None
    progress_bar = None
    max_models = None
    max_duplicate_models = None

    #### 
    # Different Modes Of Operation
    # scrape, crawl, download
    # Scrape: `-a mode=s` Crawls for N models based on parameters and downloads them.
    # Crawl: `-a mode=c` Crawls for N models and saves their information into a JSON file.
    # Download: `-a mode=d` Loads a JSON file of crawled models and downloads them.
    # Cookie: `-a cookie=rndomcookietoken` Token extracted to access VRoid Hub.


    def __init__(self, max_models=200, json_file = None, max_duplicate_models = 50, mode="s", cookie=""):
        if cookie != "":
            self.cookies["_vroid_session"] = cookie
        self.mode = mode
        print("\n\n==========  Initializing Spider ==========")
        # Set up a Signal such that the function `self.spider_closed` is called when the spider stops crawling.        
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        self.max_duplicate_models = int(max_duplicate_models)

        # The Maximum Number Of Unique Models We'll Scrape For
        self.max_models = int(max_models)

        # If A File Is Provided When The Scraper Is Called We Load That File Up.
        if json_file is not None:
            print("Loading Model List From File: " + json_file)
            # print(os.listdir())
            with open(json_file) as in_file:
                self.models = json.loads(in_file.read())
                print("Loaded {} Models From File".format(len(self.models)))

                # If We Load Models From File We Append Them To The Max Duplicate Models Found In Case We're Drawing From The Same Model Distribution When Scraping.
                # Controlling for if models were scraped or imported adds too much additional complexity.
                self.max_duplicate_models += len(self.models)
        else:
            print("No Model File Provided.")
        
        print("Max Model Count: ", max_models)
        print("Max Duplicate Models Found: ", max_duplicate_models)
        print("Spider Initialized................")
        print("\n\n")

        # Initialize Progress Bar.
        # self.progress_bar = tqdm(total=self.max_models)
        # self.progress_bar.update(len(self.models))


    def start_requests(self):
        urls = [
            "/api/character_models?characterization_allowed_user=&corporate_commercial_use=&credit=&is_downloadable=false&max_id=8823678805132214866&personal_commercial_use="
        ]


        if self.mode == "c" or self.mode == "s":
            for url in urls:
                yield scrapy.Request(url=(self.baseUrl+url), headers=self.headers, callback=self.crawl)
        elif self.mode == "d":
            for model in self.models.values():
                yield scrapy.Request(
                    url=(self.baseUrl + self.model_download_format.format(model["id"], model["latest_character_model_version"]["id"])),
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.download_model,
                )
                # yield scrapy.Request(
                #     url=(self.baseUrl + self.model_download_format.format(model["id"]), model["latest_character_model_version"]["id"]),
                #     headers=self.headers,
                #     callback=self.download_model,
                # )


    def download_model(self, response):
        id = response.request.meta['redirect_urls'][0].split('/')[5]
        
        print("Download Model")
        odn = './_data/lustrous/raw/vroid'

        if not os.path.isdir(os.path.join(odn, id[-1])):
            os.mkdir(os.path.join(odn, id[-1]))

        # MakeDir For Folder
        if not os.path.exists(os.path.join(odn, id[-1], id)):
            os.mkdir(os.path.join(odn, id[-1], id))


        path = os.path.join(odn, id[-1], id, (id + ".vrm"))
        json_path = os.path.join(odn, id[-1], id, (id + ".json"))
        with open(path, 'wb') as write_file:
            write_file.write(response.body)
        with open(json_path, 'w') as json_file:
            if type(json.dumps(self.models[id])) is str:
                json_file.write(json.dumps(self.models[id]))
            else:
                print("Hell Naww")
        return


    def crawl(self, response):
        results = json.loads(response.body)

        modelsAdded = 0
        modelNotAdded = 0

        tempModels = []

        for model in results['data']:
            if model["id"] not in self.models:
                # Add The Model To Our Dictionary
                self.models[model["id"]] = model
                # Generate A Href For Our Model
                self.models[model["id"]]["href"] = self.model_href_format.format(model["character"]["id"], model["id"])
                self.models[model["id"]]["url"] = self.baseUrl + self.model_href_format.format(model["character"]["id"], model["id"])
                tempModels.append(self.models[model["id"]])
                modelsAdded += 1
            else:
                modelNotAdded += 1

        # self.progress_bar.update(modelsAdded)

        if(modelsAdded < 5):
            if (self.max_duplicate_models < 0):
                print("Stopping Spider. Max Duplicate Models Found")
                return
            else:
                self.max_duplicate_models -= modelNotAdded


        if len(self.models) > self.max_models:
            
            print("Stopping Spider. Reached Max Models")
            return
        else:
            yield scrapy.Request(url=(self.baseUrl+results['_links']["next"]["href"]), headers=self.headers, callback=self.crawl)
            if self.mode == "s":
                for model in tempModels:
                    if model["is_downloadable"] == True:
                        # check if file exists

                        self.dwl_count += self.dwl_count
                        id = model["id"]
                        path = os.path.join('files', (id + ".vrm"))
                        if not exists(path):
                            print("File Not Found, Downloading Model Nr: {}".format(self.dwl_count))
                            yield scrapy.Request(url=(self.baseUrl + self.model_download_format.format(model["id"], model["latest_character_model_version"]["id"])), headers=self.headers, cookies=self.cookies, callback=self.download_model)
                        else:
                            print("File Found, Skipping Download For Model Nr: {} ".format(self.dwl_count))

    def spider_closed(self, spider):

        # CLose Progress Bar To Limit Clutter In Output
        # self.progress_bar.close()
        
        print("\n\n========== Finished Crawling ==========\n\n")
        print("Models Collected: ")
        print(len(self.models))
        with open(os.path.join('data', 'datmodels.json'), 'w') as outfile:
            json.dump(self.models, outfile)

    