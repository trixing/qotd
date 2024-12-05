import csv

def run():
    quotes = []
    wf = open('quotes_short.csv', 'w')
    writer = csv.writer(wf, delimiter=',', quotechar='"')

    with open('quotes.csv') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        for l in reader:
            quote, author, tags = l
            if len(quote) < 32:
                writer.writerow((quote, author))
                quotes.append((quote, author))
    wf.close()
    print(len(quotes))

run()
