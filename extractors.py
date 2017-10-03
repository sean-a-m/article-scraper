from lxml import html
from lxml import etree
import requests
import string

def nyt(dom):
    return dom.xpath('//p[@class="story-body-text story-content"]')

def aj(dom):
    #style attribute is used only on reporting credits at end of document
    return dom.xpath('//div[@id="article-body"]/p[not(@style)][not(@class)]')

def advocate(dom):
    return dom.xpath("//div[@itemprop='articleBody']/p")

def csmon(dom):
    #TODO: Ignore text from pubdata spans and last line
    return dom.xpath("//div[@class='eza-body']/p[not(p/span[@class='pubdata'])]")

def trib(dom):
    #tribune -- p/a is related stories links, /strong is related stories headers
    return dom.xpath("//div[@class='trb_ar_page']/p[not(//strong)]")

def guardian(dom):
    return dom.xpath("//div[@itemprop='articleBody']/p")

def lemonde(dom):
    return dom.xpath("//div[@id='articleBody']/p")

def latimes(dom):
    return dom.xpath("//div[@class='trb_ar_page']/p")

def npr(dom):
    return dom.xpath("//div[@id='storytext']/p")

def reuters(dom):
    dom = dom.xpath("//div[contains(@class,'ArticleBody_body')]//p")
    #removes attribution at the end
    return dom[:-1]

def spiegel(dom):
    return dom.xpath("//div[@class='article-section clearfix']/p")

def wsj_snippet(dom):
    #TODO: paywall
    #if the full article is available, the snippet xpath will return none, so try the full article xpath next
    snippet = dom.xpath("//div[@class='wsj-snippet-body']/p")
    if snippet:
        return snippet
    else:
        return dom.xpath("//div[@id='wsj-article-wrap']/p")

def wapo(dom):
    return dom.xpath("//article[@itemprop='articleBody']/p[not(@channel)][not(descendant::em)]")


def atlantic(dom):
    return dom.xpath("//div[@itemprop='articleBody']/section/p")

def bbc(dom):
    return dom.xpath("//div[@class='story-body']/div/p[not(@class)] | p[@class='story-body__introduction']")

def pbs(dom):
    return dom.xpath("//div[@itemprop='articleBody']/p")

#This assumes the page elements being passed are paragraph elements or something that works the same way
def default_text_joiner(page_elements):
    text_elements_filtered = [el.text_content() for el in page_elements[:5] if el != None]
    sep = "\n"
    return sep.join(text_elements_filtered)


def get_dom(link):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        return html.fromstring(response.content.decode(response.encoding))
    else:
        return None

def pf(id_feed, dom):
    return {
        4: aj(dom),
        3: advocate(dom),
        111: bbc(dom),
        104: csmon(dom),
        105: trib(dom),
        7: guardian(dom),
        8: lemonde(dom),
        9: latimes(dom),
        106: npr(dom),
        102: reuters(dom),
        103: reuters(dom),
        101: reuters(dom),
        100: reuters(dom),
        99: reuters(dom),
        13: spiegel(dom),
        14: nyt(dom),
        16: wsj_snippet(dom),
        17: wsj_snippet(dom),
        18: wsj_snippet(dom),
        97: wapo(dom),
        98: wapo(dom),
        15: latimes(dom),
        79: atlantic(dom),
        112: pbs(dom)
    }.get(id_feed, None)

def dparser(link, id_feed):
    try:
        dom = get_dom(link)
        extract = pf(id_feed, dom)
        if extract:
            return default_text_joiner(extract)
        else:
            return None
    except:
        #TODO: log errors
        return None





