from extr import *
from articles import *
import numpy as np
import glob
from PIL import Image, ImageTk
def scrape_em():
    nlp = spacy.load('en_core_web_lg')
    wbpg = get_webpage('https://physicstoday.scitation.org/department/all-departments?pageSize=20')
    soup = BeautifulSoup(wbpg, 'html.parser')
    articles = soup.find_all('article')
    wbpgs = []
    for link in articles:
        item = link.find('a')
        item = 'https://physicstoday.scitation.org' + item.get('href')
        wbpgs.append(item)
    return wbpgs


def create_em(wbpgs, item_no=1):
    site = get_webpage(wbpgs[item_no])
    site = BeautifulSoup(site, 'html.parser')
    title = site.title.string
    try:
        author = i.find('div', attrs={'class':'entryAuthor'}).get_text().strip()
    except:
        author = 'Unknown / Anonym'
    paragraphs = site.findAll('p')
    new = ''
    for item in paragraphs:
        new += item.text
    return new, title

def make_precis(text):
    fs = FrequencySummarizer()
    text = fs.clean(text)
    summary = fs.summarize(text,2)
    return str(summary)

def make_wdcld(text, item_no):
    fig = plt.figure()
    mask = choose_mask()
    wc = WordCloud(max_font_size=200, mode='RGBA',  min_font_size=50, relative_scaling=0.7, max_words=100, mask=mask).generate(text)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    path = '/Users/bartlomiejkos/Documents/ProgrammingNew/Python/show me your letters/clouds/'
    fig.savefig(path + 'new' + str(item_no) + '.jpg')
    filepath = path + 'new' + str(item_no) + '.jpg'
    #plt.show()
    return fig, filepath

def choose_mask():
    images = glob.glob("/Users/bartlomiejkos/Documents/ProgrammingNew/Python/show me your letters/proj-letters-of-physics/masks-wordclouds/*.png")
    n = np.random.randint(0, len(images))
    mask = np.array(Image.open(images[n]))  
    return mask 


def to_df(df, item_no, title, path, summary):
    new = pd.Series({'No':item_no, 'Title':title, 'Summary':summary, 'Filepath':path})
    df = df.append(new, ignore_index=True)
    return df

