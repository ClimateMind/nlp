# script to read in the pickled file of all the pocket articles' text extracted using DiffBot.
# Then output as a JSON that is compatible for inputting into Prodigy for text annotation.
import argparse
import pandas as pd
import pickle
import json

def get_if_exists(d, key):
    if key in d:
        return d[key]
    return ""

def main():
    #"all_pocket_diffbot_extract.p"
    diffbot_extract_file = args.diffbot_extract_file
    diffbot_extract      = open(diffbot_extract_file, "rb")
    data                 = pickle.load(diffbot_extract)

    # "all_pocket_tag_annotations.csv"
    tags_file_path = args.tags_file_path

    # data[0]['objects'][0].keys()
    # 'date', 'sentiment', 'images', 'author', 'estimatedDate', 'publisherRegion', 'icon', 'diffbotUri', 'siteName',
    # 'type', 'title', 'tags', 'publisherCountry', 'humanLanguage', 'pageUrl', 'html', 'text'

    text_list = []

    for article in data:

        try:
            article_json = article['objects']

            if (article_json[0]["type"]):
                doc_type = article_json[0]["type"]
                if (doc_type == "article"):
                    text     = article_json[0]["text"]
                    url      = article_json[0]["pageUrl"]
                    title    = article_json[0]["title"]
                    siteName = article_json[0]["siteName"]

                    diffbot_tags = get_if_exists(article_json[0], "tags")
                    unique_id    = get_if_exists(article_json[0], "diffbotUri")
                    date         = get_if_exists(article_json[0], "date")
                    author       = get_if_exists(article_json[0], "author")

                    if (url in unique_tag_annotations['pageURL'].tolist()):
                        pocket_tags = unique_tag_annotations.loc[unique_tag_annotations['pageURL'] == url , "tags"].tolist()[0]

                    if (pocket_tags):
                        items = {"text" : text, "title" : title, "diffbot_tags": tags, "date": date, "author": author,\
                                 "siteName": siteName, "unique_id": unique_id, "url": url, "doc_type": doc_type,\
                                 "pocket_tags": ", ".join(pocket_tags)}
                    else:
                        items = {"text" : text, "title" : title, "diffbot_tags": tags, "date": date, "author": author,
                                 "siteName": siteName, "unique_id": unique_id, "url": url, "doc_type": doc_type}

                    # RRR: Doesnt this mean that if its tag only, we only care about the ones that have pocket tags?
                    # RRR: Also test this works
                    if (args.tag_only):
                        if(pocket_tags and "effects" in pocket_tags):
                            text_list.append(items)

        except:
            print(article.keys())

    with open(args.output_file_path, 'w') as f:
        for item in text_list:
            f.write(json.dumps(item) + "\n")


# XXX: If possible, we could avoid storing data in pickle format
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Process data extracted from pocket")
    parser.add_argument('--diffbot_extract_file', help='Path to pickle file extracted using diffbot '\
                        '(Required)', required=True)
    parser.add_argument('--tags_file_path',   help='Path to csv file containing pocket metadata '\
                        '(Required)', required=True)
    parser.add_argument('--output_file_path',   help='Path to output jsonl file (Required)',
                         required=True)
    parser.add_argument('--tag_only',   help='Path to output jsonl file (Optional)')
    args = parser.parse_args()
    main()
