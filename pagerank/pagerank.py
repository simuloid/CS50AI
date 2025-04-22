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
    if random.random() >= damping_factor or not corpus[page]:
        return random.choice(list(corpus.keys()))

    return random.choice(list(corpus[page]))
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rc = {}
    for page in corpus.keys():
        rc[page] = 0
    page = random.choice(list(corpus.keys()))
    for i in range(n):
        page = transition_model(corpus, page, damping_factor)
        rc[page] += 1
    for page in corpus.keys():
        rc[page] /= n
        
    return rc

def links_to(corpus, page):
    rc = []
    for p in corpus:
#        if p != page:
        if page in corpus[p]:
            rc.append(p)
    return rc

def fix_corpus(corpus):
    """
    Find all pages with no links and create links to all pages.

    Parameters
    ----------
    corpus : map of page onto set(pages)
        The graph of web pages that link to other web pages.

    Returns
    -------
    The corrected corpus

    """
    for p in corpus:
        if not corpus[p]:
            corpus[p] = corpus.keys()
    return corpus
            
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rc = {}
    samples = 0
    epsilon = 0.001
    corpus = fix_corpus(corpus)
    N = len(corpus)
    # Initialize probability of all pages as equal.
    for page in corpus:
        rc[page] = 1/N

    changed = True
    while changed:
        changed = False
        updates = {}
        for page in corpus:
            prp = (1-damping_factor) / N
            summation = 0
            for i in links_to(corpus, page):
                summation += rc[i]/len(corpus[i])
                
            prp += damping_factor * summation
            updates[page] = prp

        for page in corpus:            
            if abs(updates[page] - rc[page]) > epsilon:
                changed = True
            rc[page] = updates[page]
        
    return rc



if __name__ == "__main__":
    main()
