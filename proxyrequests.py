# -*- coding: utf-8 -*-

"""
This module allows you to make HTTP requests using automatically scraped proxies.
These proxies are high anonimous and https compatible.
"""

import requests
import random

USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


class browser:
    def __init__(self, delete_proxy=True, force_update=False, timeout=5):
        self.page = None
        self.url = None
        self._delete_proxy = delete_proxy
        self._force_update = force_update
        self._timeout = timeout
        self.proxies = set([])

        result = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/'
                              'proxy-list.txt', headers=USER_AGENT, timeout=10)
        if result.status_code == requests.codes.ok:
            parser = result.text.split('\n\n')[1].split('\n')
            for i in parser:
                if 'H' in i and 'S' in i and '+' in i:
                    proxy = i.split()[0]
                    try:
                        self.proxies.add(proxy)
                    except Exception:
                        pass

    def get(self, url, cookies=None):
        """
        Load the web and saves the result on page attribute.

        Arguments:
            url {string} -- The URL of the web you want to get

        Keyword Arguments:
            cookies {dictionary} -- Cookies with the format
                                    {'cookie_name': 'xxx', 'cookie_name': 'xxx'}
                                    (default: {None})
        """
        self.url = url

        if len(self.proxies) < 15 or self._force_update:
            result = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/'
                                  'proxy-list.txt', headers=USER_AGENT, timeout=10)
            if result.status_code == requests.codes.ok:
                parser = result.text.split('\n\n')[1].split('\n')
                for i in parser:
                    if 'H' in i and 'S' in i and '+' in i:
                        proxy = i.split()[0]
                        try:
                            self.proxies.add(proxy)
                        except Exception:
                            pass

        while True:
            proxy = random.choice(list(self.proxies))
            try:
                result = requests.get(self.url, proxies={"http": proxy, "https": proxy},
                                      headers=USER_AGENT, cookies=cookies, timeout=self._timeout)
                if result.status_code == requests.codes.ok:
                    self.page = result.content
                    self.url = result.url
                    break
                else:
                    if self._delete_proxy:
                        self.proxies.remove(proxy)
                    self.page = None
            except Exception:
                if self._delete_proxy:
                    self.proxies.remove(proxy)
                self.page = None


if __name__ == '__main__':
    browser = browser()
    print('Number of proxies: ' + str(len(browser.proxies)))
    browser.get('https://bytelix.com/')
    if browser.page:
        print('Web loaded correctly')
        print('Web content:')
        print(browser.page[:1000])
    else:
        print('Error loading web')
