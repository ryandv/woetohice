# woetohice

> Waterhouse has forgotten all of their names. He always immediately forgets the names. Even if he remembered them, he would not know their significance, as he does not actually have the organization chart of the Foreign Ministry (which runs Intelligence) and the Military laid out in front of him. They keep saying “woe to hice!” but just as he actually begins to feel sorry for this Hice fellow, whoever he is, he figures out that this is how they pronounce “Waterhouse.”
> Neal Stephenson, Cryptonomicon

This is a small utility for scraping transactions from TD credit card statement PDFs. It uses [pdfminer](https://pypi.org/project/pdfminer/) to search documents for text lines containing transaction dates and tries to find nearby text along the same horizontal line. To group transaction line items together, it uses ~machine learning~ a simple algorithm for finding fixed-radius near neighbors, merging pairs of points into a disjoint-set data structure. The approach is given in [this](https://cs.stackexchange.com/questions/85929/efficient-point-grouping-algorithm) StackExchange response.

No guarantees of correctness or even minimum functionality are made.

## Usage

```sh
$ virtualenv env
$ . env/bin/activate
$ python setup.py install
$ pip install -r requirements.txt
$ woetohice input.pdf
```
