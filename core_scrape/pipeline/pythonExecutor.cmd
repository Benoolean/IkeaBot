echo off
set arg1=%1
cd ../../env/Scripts
CALL activate.bat

cd ../../core_scrape/ikea_product_scraper
python product_spider.py %arg1% %*
pause