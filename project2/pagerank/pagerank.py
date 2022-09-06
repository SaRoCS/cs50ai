import os
import random
import re
import sys
import copy

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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transition = {}
    linked = corpus[page]

    # if no linked pages use equal probability
    if len(linked) == 0:
        for corpus_page in corpus:
            transition[corpus_page] = 1 / len(corpus)
            return transition

    # probability of choosing random page
    prob_1 = (1 - damping_factor) / len(corpus)
    # probability based on links
    prob = damping_factor / len(linked)

    for corpus_page in corpus:
        if corpus_page in linked:
            transition[corpus_page] = prob_1 + prob
        else:
            transition[corpus_page] = prob_1
    return transition


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # randomly sample first page
    sample_prev = random.choice(list(corpus.keys()))
    probs = {sample_prev: 1}

    # take n - 1 samples
    for _ in range(n - 1):
        # get the transition model from previous sample and make a sample
        transition = transition_model(corpus, sample_prev, damping_factor)
        sample = random.choices(
            list(transition.keys()), weights=list(transition.values())
        )
        sample_prev = sample[0]
        # add or increment times sample has been picked
        if sample[0] in probs:
            probs[sample[0]] += 1
        else:
            probs[sample[0]] = 1

    # convert to probabilities
    for prob in probs:
        probs[prob] /= n
    return probs


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # assign a starting rank
    ranks = {key: 1 / len(corpus) for key in corpus.keys()}

    stop = False
    while stop is False:
        ranks_copy = copy.deepcopy(ranks)

        # find new rank
        for rank in ranks:
            prob_1 = (1 - damping_factor) / len(corpus)
            sigma = 0

            # get pages that link TO the current page
            incoming_links = []
            for page in corpus:
                if rank in corpus[page]:
                    incoming_links.append(page)

            # calculate the sum
            for i in incoming_links:
                sigma += ranks[i] / len(corpus[i])

            # update new ranks
            ranks_copy[rank] = prob_1 + damping_factor * sigma

        # check within accuracy
        for rank in ranks:
            if abs(ranks[rank] - ranks_copy[rank]) > 0.001:
                stop = False
                break
            stop = True

        # update ranks
        ranks = ranks_copy
    return ranks


if __name__ == "__main__":
    main()
