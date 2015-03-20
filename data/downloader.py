import os
import csv
from urllib2 import urlopen, URLError, HTTPError


def download(row):
    # Open the url
    try:
        num = row['gutenberg_id']
        path = list(num[:len(num)-1])
        path.extend([num, num + ".txt"])
        path = "/".join(path)
        url = "http://mirrors.xmission.com/gutenberg/" + path
        # url = "http://www.gutenberg.org/ebooks/%d.txt.utf-8" % int(row['gutenberg_id'])
        f = urlopen(url)
        print "downloading " + url
        # Open our local file for writing
        if not os.path.exists(row['author']):
            os.makedirs(row['author'])
        with open(row['author'] + '/' + row['title'] + '.txt', "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


def main():

    with open('index.csv','rb') as csvfile:
        file_reader = csv.DictReader(csvfile)
        for row in file_reader:
            download(row)
            print(row)

if __name__ == '__main__':
    main()