# Presto Python bindings

import requests
import urllib

headers = {'Content-Type': 'application/octet-stream'}

def f(x): return urllib.quote_plus(x).replace('+', '%20')

class Presto:
    def __init__(self, server_url):
        self.server_url = server_url

    def post(self, url, data):
        url = self.server_url+url
        return requests.post(url=url, data=data, headers=headers)

    def get(self, url):
        url = self.server_url+url
        return requests.get(url)

    def insert(self, path, start_line, contents):
        patch = self.post("/insert/%d/%s" % (start_line, path), contents)
        return patch

    def remove(self, path, start_line, end_line):
        patch = self.post("/remove/%d/%d/%s" % (start_line, end_line, path), "")
        return patch

    def replace(self, path, start_line, end_line, contents):
        patch = self.post("/replace/%d/%d/%s" % (start_line, end_line, path), contents)
        return patch

    def apply(self, path, patch):
        return self.post("/apply/%s" % path, patch)

    def revert(self, path, patch):
        return self.post("/revert/%s" % path, patch)

    def rewrite(self, source, match_template, rewrite_template):
        return self.get("/rewrite/%s/%s/%s" % (f(source), f(match_template), f(rewrite_template)))
