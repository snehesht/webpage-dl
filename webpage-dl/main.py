import requests
import celery
import argparse


def main():
    pass

if __name__=="__main__":
    parser = argparse.ArgumentParser('Webpage downloader and archiver')
    parser.add_argument('-u','--url', help="URL to download", type=str)
    parser.add_argument('-o','--output' help="Save webpage to file eg. output.html", type=str)
    parser.add_argument('--compress', help="minify css, html, js", store_action=True)

    args = parser.parse_args()
    main(args)



