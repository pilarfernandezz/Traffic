import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dist = {}
    for c in corpus.keys():
        dist[c] = 0

    if len(corpus[page]) == 0:
        for d in dist.keys():
            dist[d] = 1 / len(corpus.keys())
    else: 
        linkedPagesProb = damping_factor / len(corpus[page]) # choose a link at random linked to by `page`
        allPagesProb = (1 - damping_factor) / len(corpus.keys()) # choose a link at random chosen from all pages in the corpus.
        
        for c in corpus.keys():
            if c in corpus[page]:
                dist[c] = linkedPagesProb + allPagesProb
            else: 
                dist[c] = allPagesProb

    return dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    pages = []
    for c in corpus.keys():
        pages.append(c)
        ranks[c] = 0

    # Starting with a page at random
    rand = random.randrange(len(pages))
    page = pages[rand]
    ranks[page] += 1

    i = 0
    while (i < n - 1):
        model = transition_model(corpus, page, damping_factor)
        p = []
        for m in model.keys():
            p.append(model[m])
            
        rand = random.choices(pages, weights=p,k=1)[0]
        page = rand
        ranks[rand] += 1
        i += 1

    for r in ranks:
        ranks[r] /= n

    return ranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    N = len(corpus)
    for c in corpus.keys():
        ranks[c] = 1 / N
    
    while True:
        ranksUpdated = {}
        for mainPage in corpus:
            summatory = 0
            for page in corpus:
                if len(corpus[page]) == 0:
                    summatory += ranks[page] / N
                elif mainPage in corpus[page]:
                    summatory += ranks[page] / len(corpus[page])

            result = summatory * damping_factor + (1 - damping_factor) / N
            ranksUpdated[mainPage] = result

        hasBiggest = False
        for page in corpus: 
            if abs(ranks[page] - ranksUpdated[page]) > .001:
                hasBiggest = True
                ranks = ranksUpdated

        if hasBiggest == False:
            return ranks

if __name__ == "__main__": 
    main()
