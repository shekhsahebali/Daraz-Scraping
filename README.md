# Daraz-Scraping
A web scraping project designed to extract product data from Daraz (an e-commerce platform). The script automates the collection of essential product information such as product names, prices, ratings, reviews, etc.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/).

### Recommended browser
Chromium-based browsers.
- Chromium version:- 145.0.7568.0 
```sh
npx @puppeteer/browsers install chrome@145.0.7568.0
```
- ChromeDriver version:- 145.0.7568.0 
```sh
npx @puppeteer/browsers install chromedriver@145.0.7568.0
```
for more info [https://www.chromium.org/getting-involved/download-chromium/](https://www.chromium.org/getting-involved/download-chromium/)

### Used python Library
```requests
pillow
selenium
beautifulsoup4
```
## Project Setup
- Clone the repo

```sh
git clone https://github.com/shekhsahebali/Daraz-Scraping.git
cd Daraz-Scraping
```
- Download browser/ChromeDriver.

```sh
npx @puppeteer/browsers install chrome@145.0.7568.0
npx @puppeteer/browsers install chromedriver@145.0.7568.0
```
- mv Chromium file to  
```sh
mv chrome/linux-145.0.7568.0/chrome-linux64 chromium
mv chromedriver/linux-145.0.7568.0/chromedriver-linux64 chromiumdriver
rm -r chrome chromedriver
```
- Install Library
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
### Run the Script
Done!!


