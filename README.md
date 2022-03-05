# recipes-recommendation

## Requirements

- gcloud (don't forget to do `gcloud auth login`)
- docker
- python 3.7

## Google cloud components

- GAR used to store the docker images
- service account to schedule scraping job
- cloud scheduler to schedule scraping job
- cloud run to run scraping job

## Scraping

Since some requirements (like tensorflow) are heavy the image build is done in two steps. First we build the base image that contains only the python requirements. This is done with the command
```
docker build scraping -t base_image
```
Then any image can be built by starting with this one. This saves a lot of development time for when we change the code and not the dependencies.

To build the image run
```
docker build scraping/script -t scraping
```
To run it locally to test run
```
docker run --env-file=.env -p 5000:5000 scraping
```
The `.env` file contains the two environment variables MONGO_USERNAME and MONGO_PASSSWORD used to connect to the MongoDB database.

To push the image to the GAR it's important to first tell docker how to do it (only needed once)
```
gcloud auth configure-docker us-east4-docker.pkg.dev
```
and then just do
```
docker tag scraping us-east4-docker.pkg.dev/my-project-gmap-252012/recipes-recommendation/scraping
docker push us-east4-docker.pkg.dev/my-project-gmap-252012/recipes-recommendation/scraping
```

## Resources

Info about using selenium in docker: https://dev.to/googlecloud/using-headless-chrome-with-cloud-run-3fdp

Place to check to know what version of chrome is installed: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
(the version of chromedriver-binary must be the same)

Schedule docker container on cloud run: https://cloud.google.com/run/docs/triggering/using-scheduler