import requests
from lxml import html,etree,objectify
from urllib.parse import urlparse
import base64

"""
Assets that are parsed and inlined

"""
ALLOWED_EXTS=['css','js','png','jpg','gif','jpeg']
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def fetch_base_url(URL):
    raw_resp = requests.get(URL,headers=HEADERS)

    # Decode content
    if len(raw_resp.headers.get('Content-Type',None).split('=')) == 1:
            content_type = "UTF-8"
    else:
            content_type = raw_resp.headers.get('Content-Type',None).split('=')[1]

    return raw_resp.content.decode(content_type)


def parse_base_page(PAGE_CONTENT,URL):

    # build HTML tree from string
    resp = html.fromstring(PAGE_CONTENT)

    # replace relative links (/img.png) to https://example.com/img.png
    resp.make_links_absolute(URL)

    # Iterlinks function grabs all elements with remote assets like css,js,png
    # and iterate over them
    for element, attribute, link, pos in resp.iterlinks():
        # print(element,attribute,link,pos)
        # tag represents type of element i.e div, img, link ...
        link_tag = element.tag

        # get the extension of remote asset i.e css, js, jpeg, png
        # incase of <a href=="someurl"> it returns ""
        # then check if extension is one of supported ones and then download it
        link_ext = urlparse(link).path.split('/')[-1].split('.')[-1]
        if link_ext != "" and link_ext in ALLOWED_EXTS and attribute != None:
            new_elm = download_assets(link,link_tag,link_ext,element.items(),attribute)
            tmp_elm = element
            try:
                # replace the current element with newly generated element
                # We can't simply copy paste old element with new element.
                # the trick is to find the parent element and then match each
                # child node of that parent to find our element. Then we can
                # replace it with the new element.
                element.getparent().replace(tmp_elm,new_elm)
            except Exception as e:
                print(e)

    return html.tostring(resp).decode().strip()


"""
This function grabs the element and it's attributes, generates new equivalent
element with same attributes except for remote asset. It replaces the asset URL
with the inlined version. For eg.
    <link rel="stylesheet" src="..."> ==> <style> CSS HERE </style>
    <script href="">                  ==> <script> JS HERE </script>

    It encodes image assets into base64 format and replace the URL with the
    base64 encoded data

"""
def download_assets(link,link_tag,link_ext,attributes,elm_type):
    raw_resp = requests.get(link,headers=HEADERS)
    print('Downloading ',link)
    if link_ext in ['css','js']:
        resp = raw_resp.text
        try:
            if link_ext == 'css':
                elm = etree.Element('style')
                elm.text = resp.strip()
            else:
                elm = etree.Element('script')
                elm.text = resp.strip()
        except Exception as e:
            print(e)
    else:
        resp = raw_resp.content
        resp_base64 = base64.b64encode(resp)
        elm_src = 'data:image/' + link_ext + ';base64,' + resp_base64.decode()
        if link_tag != "":
            elm = etree.Element(link_tag,src=elm_src)
            for attr in attributes:
                if attr[0] not in ["src", "href", "srcset"]:
                    elm.set(attr[0],attr[1])
    return elm


