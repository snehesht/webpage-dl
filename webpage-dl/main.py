import argparse
from urldownloader import download_assets, fetch_base_url, parse_base_page


def main(args):
    html_resp = fetch_base_url(args.url)
    webpage = parse_base_page(html_resp, args.url)

    with open(args.output, 'w') as fp:
        fp.write(webpage)
    print('Done')

if __name__=="__main__":
    parser = argparse.ArgumentParser('Webpage downloader and archiver')
    parser.add_argument('-u','--url', help="URL to download", type=str)
    parser.add_argument('-o','--output', help="Save webpage to file eg. output.html", type=str)
    #parser.add_argument('--compress', help="minify css, html, js", store_action=True)

    args = parser.parse_args()
    main(args)



