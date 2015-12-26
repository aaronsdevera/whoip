from sys import argv, stderr, exit
from geoip import geolite2
import time
import datetime
import subprocess
import folium
import sys, os, getopt
from urllib2 import urlopen
from json import load
import trparse
import re
from ipwhois import IPWhois

filepath = ''
fileurl = ''
comma_sep = lambda x: ', '.join([str(y) for y in x])

def doc():
    print 'WHOIP Usage:'
    print 'whoip.py -f <LISTFILE>'
    print 'whoip.py -t <TARGET IP ADDRESS>'
    print '-f, --list-file     :     Upload a list of IPs for processing'
    print '-t, --traceroute    :     Perform traceroute on target IP'
    print '-h, --help          :     Assistance'
    print 'Project Contact:
    print 'aaronsdevera [at] protonmail [dot] com
    print '@aaronsdevera'

def makelist(path):
    with open(path) as file:
        ungrouped_list = re.findall( r'[0-9]+(?:\.[0-9]+){3}', file.read())
        return ungrouped_list

def trace(target):

    p = subprocess.Popen(["traceroute", target],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, errors = p.communicate()
    traceroute = trparse.loads(output)

    hops = [0] * len(traceroute.hops)

    c = 0
    for each in hops:
        hops[c] = re.findall( r'[0-9]+(?:\.[0-9]+){3}', str(traceroute.hops[c]))
        c += 1
    
    return hops
    
def geoloc(kill_list):

    lists_of_IPlists = ''
    lists_of_IPs = ''

    # get final IP in list of IP lists
    if isinstance(kill_list[-1],str) == True:
        lists_of_IPlists = False
        lists_of_IPs = True
        open_location = kill_list[-1]
    if isinstance(kill_list[-1],list) == True:
        lists_of_IPlists = True
        lists_of_IPs = False
        open_location = kill_list[-1][0]
    
    map = folium.Map(location=geolite2.lookup(open_location).location, tiles='Stamen Toner',zoom_start=10)
    
    if lists_of_IPlists == True:
        for each in kill_list:
            for all in each:
                
                
                if all[:2] == 10 or all[:2] == str(10):
                    print 'Home ip 10.*.*.* skipped'

                else:
                    print 'Current IP: ' + all
                    
                    match = geolite2.lookup(all)
                    
                    
                    # WHOIS
                    #who = IPWhois(all).lookup_rdap(depth=1)
                    who = IPWhois(all).lookup()
                    who_nets = who['nets']

                    who_nets_name = who_nets[0]['name']
                    who_nets_desc = who_nets[0]['description']

                    
                    popup = 'WHOIS Description: %s ' % who_nets_desc + 'IP: %s' % match.ip + ',' + 'Country: %s' % match.country + ',' + 'Continent: %s' % match.continent + ',' + 'Subvisions: %s' % comma_sep(match.subdivisions) + ',' + 'Timezone: %s' % match.timezone + ',' + 'Location: %s' % comma_sep(match.location)

                    target_long_lat = comma_sep(match.location)
                    
                    map.circle_marker(match.location,radius=900, popup=popup,line_color='#3186cc', fill_color='#3186cc')
    if lists_of_IPs == True:
        for each in kill_list:
            if each[:2] == 10 or each[:2] == str(10):
                print 'Home ip 10.*.*.* skipped'

            else:
                print 'Current IP: ' + each
                
                match = geolite2.lookup(each)
                
                
                # WHOIS
                #who = IPWhois(all).lookup_rdap(depth=1)
                who = IPWhois(each).lookup()
                who_nets = who['nets']
                
                who_nets_name = who_nets[0]['name']
                who_nets_desc = who_nets[0]['description']
                
                
                popup = 'WHOIS Description: %s ' % who_nets_desc + 'IP: %s' % match.ip + ',' + 'Country: %s' % match.country + ',' + 'Continent: %s' % match.continent + ',' + 'Subvisions: %s' % comma_sep(match.subdivisions) + ',' + 'Timezone: %s' % match.timezone + ',' + 'Location: %s' % comma_sep(match.location)
                
                target_long_lat = comma_sep(match.location)
                
                map.circle_marker(match.location,radius=900, popup=popup,line_color='#3186cc', fill_color='#3186cc')
    
        
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H%M%S')
    filepath = 'viz/map'+timestamp+'.html'
    
    map.create_map(path=filepath)
    return filepath

def genmap(filepath):
    if sys.platform=='win32':
        os.startfile(filepath)
    elif sys.platform=='darwin':
        print 'Map file saved as ' + filepath
        subprocess.Popen(['open',filepath])
    else:
        try:
            subprocess.Popen(['xdg-open', filepath])
        except OSError:
            print 'Please open a browser on: ' + filepath
     
def main(argv):

    try:
        opts, args = getopt.getopt(argv,'hf:t:',['ifile=','ofile='])
    except getopt.GetoptError:
        print 'Error: Missing requirement'
        print 'Use arg "-h" or "--help" for assistance'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            doc()
            sys.exit()
        elif opt in ('-f', '--list-file'):
            ml = makelist(arg)
            print ml
            path = geoloc(ml)
            genmap(path)
        elif opt in ('-t', '--traceroute'):
            tr = trace(arg)
            path = geoloc(tr)
            genmap(path)

if __name__ == '__main__':
    main(sys.argv[1:])
