from flask import Flask

from scraping import main

app = Flask(__name__)


@app.route("/")
def scrape_ricardo():
    main()
    return 'Done', 200

if __name__ == "__main__":
    app.run()