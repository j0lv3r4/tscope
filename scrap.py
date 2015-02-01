# -*- coding: utf-8 -*-
import feedparser
import requests
import urllib
import json
import os.path
import io
import ConfigParser

TS_PATH = ''
DB_FILE_NAME = '.tscope_db'
CONFIG_FILE_NAME = '.tscope.conf'
DB_FULLPATH = TS_PATH + DB_FILE_NAME
CONFIG_FULLPATH = TS_PATH + CONFIG_FILE_NAME

# Console colors 
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray

# Helpers 
def print_info(message):
    print B + ' [!]' + W + ' ' + message + W


def print_success(message):
    print G + ' [+]' + W + ' ' + message + ':' + G + ' success!' + W


def print_error(message):
    print R + ' [!]' + O + ' ' + message + W


# Check if there is already a configuration file
if not os.path.isfile(CONFIG_FULLPATH):
    print_info('Config file missing, try to create a new one')
    # Create the configuration file as it doesn't exist yet
    print_info('Current path is: ' + CONFIG_FULLPATH)
    cfgfile = open(CONFIG_FULLPATH, 'w')

    # Add content to the file
    Config = ConfigParser.ConfigParser()
    Config.add_section('base')
    Config.set('base', 'project', 'http://project.url')
    Config.add_section('bit.ly')
    Config.set('bit.ly', 'api_key', 'XXX')
    Config.set('bit.ly', 'api_access_token', 'XXX')
    Config.set('bit.ly', 'api_url', 'https://api-ssl.bitly.com/v3/user/link_save')
    Config.write(cfgfile)
    cfgfile.close()
else:
    print_success('config file found')

# Load settings from `~tscope.conf`
try:
    print_info('getting setting from config file')

    parser = ConfigParser.SafeConfigParser()
    parser.read(CONFIG_FULLPATH)

    project_url = parser.get('base', 'project')
    bitly_api_key = parser.get('bit.ly', 'api_key')
    bitly_api_access_token = parser.get('bit.ly', 'api_access_token')
    bitly_api_url = parser.get('bit.ly', 'api_url')

    # Printing data
    print_info('project: ' + R + project_url)
    print_info('bit.ly api key: ' + R + bitly_api_key)
    print_info('bit.ly access token: ' + R + bitly_api_access_token)
    print_info('bit.ly api url: ' + R + bitly_api_url)
except IOError:
    print_error('Couldn\'t read config file')


def short_link(url):
    if 'bit.ly' in url:
        raise Exception('This is a bit.ly url, shouldn\'t be shortened again')
    query_args = {'access_token':bitly_api_access_token, 'longUrl':url}
    encode_args = urllib.urlencode(query_args)
    bitly_request = bitly_api_url + '?' + encode_args
    print_info('sending request to: ' + R + 'bit.ly' + W + ', query: ' + R + bitly_request)
    r = requests.get(bitly_request)
    status_code = r.json()['status_code']

    if status_code == 403:
        print_error('invalid access token')
        return
    else:
        link = r.json()['data']['link_save']['link']

        if status_code == 304:
            print_info('link already exists')
            return link
        else:
            print_success('link saved ' + R + link)
            return link 


def print_posts():
    try:
        print_info('getting posts')
        posts = feedparser.parse(project_url)
        f = open('db.txt', 'w')
        for post in posts.entries:
            print_info('printing posts on ' + R + 'db.txt ' + W + 'file')
            link = short_link(post.link).encode('utf-8')
            title = post.title.encode('utf-8')
            print_info('title : ' + R + title)
            print_info('link: ' + R + link)
            f.write(title + ' - ' + link + '\n')
    except:
        print_error(R + 'ERROR: ' + O + 'shortening link failed!')

def main():
    print_posts()

if __name__ == '__main__':
    main()
