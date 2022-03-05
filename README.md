# recipes-recommendation

Since some requirements (like tensorflow) are heavy the image build is done in two steps. First we build the base image that contains only the python requirements. This is done with the command
```
docker build . -t base_image
```
Then any image can be built by starting with this one. This saves a lot of development time for when we change the code and not the dependencies.

## Scraping

To build the image run
```
docker build scraping -t scraping
```
To run it locally to test run
```
docker run --env-file=.env scraping
```
The `.env` file contains the two environment variables MONGO_USERNAME and MONGO_PASSSWORD used to connect to the MOngoDB database.

## Resources

Info about using selenium in docker: https://dev.to/googlecloud/using-headless-chrome-with-cloud-run-3fdp

Place to check to know what version of chrome is installed: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
(the version of chromedriver-binary must be the same)