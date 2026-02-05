import csv


def fit(words, rows=6, columns=10):
    lines = []
    line = words[0]
    for w in words[1:]:
        if len(w) + len(line) + 1 <= columns:
            line += ' '
            line += w
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines

def fit_quote(quote, author, rows=6, columns=10):
        if len(quote) > (rows*columns):
            return None
        words = [w.strip() for w in quote.split(' ')]
        wordlen = [len(w) for w in words]
        if max(wordlen) > 8:
            return None
        # try to fit in as narrow as possible
        lines = fit(words, rows, (columns-2))
        if len(lines) > rows:
            lines = fit(words, rows, (columns-1))
            if len(lines) > rows:
                lines = fit(words, rows, columns)
                if len(lines) > rows:
                    return None
                
        short_author = ''
        author = [a.strip() for a in author.split(',')]
        if len(author) > 1:
            short_author = author[-1]
            if len(short_author) < (columns-2) and author[0]:
                short_author = author[0][0] + '.' + short_author
        elif author:
            short_author = author[0]
        if short_author:
            lines.append('-' + short_author)
        return '|'.join(lines)


def main():
    quotes = 0
    wf = open('quotes_short.csv', 'w')
    writer = csv.writer(wf, delimiter=',', quotechar='"')

    with open('quotes.csv') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        for l in reader:
            quote, author, tags = l
            tags = '|'.join([a.strip() for a in tags.split(',')])

            vestaboard_quote = fit_quote(quote, author)
            if vestaboard_quote is not None:
                writer.writerow((quote, author, tags, vestaboard_quote))
                quotes += 1
    wf.close()
    print(quotes)

if __name__ == '__main__':
    main()
