import os
import re
import requests
import string
import tkinter.messagebox as msgbox
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from collections import OrderedDict
from time import sleep



# Globals
# root_url - This will be the root of the url tree
# response - This is the response we get back from requests
# file_folder - Where the working files will be temperarly stored
# site - Main site look scrape (Change to user access)

# Classes

# Functions

def find_root_url(site):
    test_str = str(site)
    start_slash = test_str.find('/')
    folder = test_str.find('/', start_slash + 2)
    if folder == -1:
        return test_str, ''
    else:
        return test_str[0:folder], test_str[folder:]

def f_clean_title(text):
    return_str = ''
    for letter in text:
        if letter in string.ascii_letters or \
           letter in string.digits:
            return_str = ''.join((return_str, letter))
        elif letter in string.whitespace:
            return_str = ''.join((return_str, ('_')))
    return return_str.strip('_')

def scrape(site, file_folder):
    """Function scrapes and places in file_folder"""
        
    s = requests.Session()

    root_url, folder = find_root_url(site)
    response = s.get(str(site))
    # response.close() # Close the connection once received

    soup = BeautifulSoup(response.text, 'html.parser')
    tag_a = soup.find_all('a')
    holding = OrderedDict()

    for link in tag_a:
        try:
            holding[link.attrs['href']] = link.getText()
        except:
            msgbox.showerror('No links', "Site has no links.")
            return
            # print("{} has no href".format(link.getText()))

    ### Note : Hrefs with # at beginning are the same page
    ###         and do not need to be grabbed


    try:
        os.chdir(file_folder)
    except:
        msgbox.showerror('HELP', 'UNABLE TO FIND DIRECTORY\nEXITTING!')
        quit()

    counter = 0 # counter for file iteration

    for links in holding:
        yield links
    # exit()
    # Generate files
    for links in holding:
        if 'http://' in links or 'https://' in links:
            link = links
        elif links.startswith('//'):
            link = ''.join(('http:', links))
        elif links.startswith('/'):
            link = ''.join((root_url, links))
        elif links.startswith('#'):
            continue
        else:
            link = '/'.join((site, links))
            
        name = f_clean_title(holding[links])
        if name == '':
            name = str(counter)
            counter += 1
            fullname = ''.join((file_folder, '\\', name, '.html'))
        else:
            name = name.replace('___', '_')  # Get rid of  ___ from sites
            fullname = ''.join((file_folder, '\\', name[0:16], '.html'))

        with open(fullname, 'wb') as file_create:
            yield '*'
            try:
                response = s.get(str(link))
                for write in response.iter_lines():
                    file_create.write(write)
            except Exception as e:
                print(e)

            if response.text == '':
                file_create.close()
                os.remove(fullname)
                
            try:
                if response.text != '':
                    response.close()
            except:
                print("Couldn't close {} link".format(link))
            
    response.close()
    del counter
    yield 'Completed scrape from site {}'.format(str(site))


def produce(ordered_files, directory):
    """This will generate ordered file in the proper directory."""
    order = [os.path.join(directory, i) for i in ordered_files]
    filename = 'Final.html'
    fullname = os.path.join(directory, filename)

    first_re = re.compile(bytes('</body>|</html>'.encode())
                          , re.IGNORECASE)

    middle_re = re.compile(bytes('<html.*?>|<head.*?/>|<head.*?>.*?</head>|<body.*?>|</body>|</html>'.encode()), re.VERBOSE | re.DOTALL | re.IGNORECASE)

    end_re = re.compile(bytes('<html.*?>|<head.*?/>|<head.*?>.*?</head>|<body.*?>'.encode()), re.VERBOSE | re.DOTALL | re.IGNORECASE)
    with open(fullname, 'wb') as file:
        with open(order[0], 'rb') as first:
            print("Merging: ",order[0])
            infile = first.read()
            first.flush()
            outfile = re.sub(first_re, b'', infile)
            file.write(outfile)
            file.flush()
            os.fsync(file.fileno())

        for i in order[1:-1]:
            print("And ... ", i)
            with open(i, 'rb') as middle:
                infile = middle.read()
                middle.flush()
                outfile = re.sub(middle_re, b'', infile)
                file.write(outfile)
                file.flush()
                os.fsync(file.fileno())


        with open(order[-1], 'rb') as end:
            print("Finally ...", order[-1])
            infile = end.read()
            end.flush()
            outfile = re.sub(end_re, b'', infile)
            file.write(outfile)
            file.flush()
            os.fsync(file.fileno())
            file.close()
            

    return filename



if __name__ == '__main__':
    
    # input site to grab
    

    # site = 'http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python'
    # Separate root out (join later as required


    # Walk the OS created
    
    walk = os.walk(file_folder) # Generator to walk files
    files = next(walk)
    count = 1
    file_order = OrderedDict()
    for html_file in files[2]:
        file_order[count] = html_file
        count += 1





    
