# -*- coding: utf-8 -*-

"""
This module allows you to make HTTP requests using automatically scraped proxies.
These proxies are high anonimous and https compatible.
"""

import requests
import random
import time
import sys

USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


class Browser:
    """This class allows loading pages using proxies.

    Args:
        delete_proxy (bool): Delete proxy that fails loading the web.
        force_update (bool): Force to update proxies on every web load.
        timeout (int): Timeout for loading the web.
    """

    def __init__(self, delete_proxy=True, force_update=False, timeout=5):
        self.page = None
        self.url = None
        self._delete_proxy = delete_proxy
        self._force_update = force_update
        self._timeout = timeout
        self.load_time = None
        self.used_proxies = 0
        self.proxies = set([])
        self.get_proxies()

    def load_web(self, url, cookies=None):
        """Load the web and saves the code on page attribute.

        Args:
            url (string): The URL of the web you want to get.
            cookies (dictionary): With the format {'cookie_name': 'value', 'cookie_name': 'value'}

        Attributes:
            load_time (float): Elapsed time until the page is fully loaded.
            used_proxies (int): Number of used proxies for loading the web.

        Returns:
            page (string): Contains the code of the page if succesfully loaded.
        """

        self.url = url
        self.used_proxies = 0
        timer = time.clock if sys.platform[:3] == 'win' else time.time
        start = timer()

        if len(self.proxies) < 15 or self._force_update:
            self.get_proxies()

        while self.proxies:
            proxy = random.choice(list(self.proxies))
            self.used_proxies += 1
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

        self.load_time = timer() - start

        return self.page

    def get_proxies(self):
        """Loads proxies and returns them in a list"""

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

        return list(self.proxies)

    def get_proxy(self):
        """Returns a random proxy on each call"""

        if not self.proxies:
            self.get_proxies()
        return random.choice(list(self.proxies))


if __name__ == '__main__':
    print('==== Starting browser ====')
    browser = Browser()
    print('Number of proxies: ' + str(len(browser.proxies)))
    print('Loading the web, please wait...')
    browser.get('https://www.google.com')
    if browser.page:
        print('Web loaded correctly')
    else:
        print('Error loading web')
    print('Elapsed time: %.2f seconds' % browser.load_time)
    print('Proxies used: ' + str(browser.used_proxies))
    print('Remaining proxies: ' + str(len(browser.proxies)))
    print('Random proxy: ' + browser.get_proxy())
