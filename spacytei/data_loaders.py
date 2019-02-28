import json
import requests


def get_doc_list(domain, app_name, collection='editions', verbose=True):
    """ retrieves a list of doc-uris stored in a dsebaseapp
        :param domain: Domain hosting the dsebaseapp instance, e.g. "http://127.0.0.1:8080"
        :param app_name: The name of the dsebaseapp instance.
        :verbose: Defaults to True and logs some basic information
        :return: A list of absolut URLs
    """

    endpoint = "{}/exist/restxq/{}/api/collections/{}".format(domain, app_name, collection)
    r = requests.get(endpoint)
    if r.status_code == 200:
        if verbose:
            print('connection to: {} status: all good'.format(endpoint))
    else:
        print(
            "There is a problem with connection to {}, status code: {}".format(
                r.status_code, endpoint
            )
        )
        return None
    hits = r.json()['result']['meta']['hits']
    all_files = requests.get("{}?page[size]={}".format(endpoint, hits)).json()['data']
    files = ["{}{}".format(domain, x['links']['self']) for x in all_files]
    if verbose:
        print("{} documents found".format(len(files)))
    return files
