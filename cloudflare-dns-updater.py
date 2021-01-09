#!/usr/bin/env python

import os
import sys
import requests
import time

token = os.getenv('TOKEN')
host = os.getenv('HOST')
host = host.split(',')
timeout = int(os.getenv('TIMEOUT'))
healthcheck_file = "/healthcheck"

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

def create_healthcheck_file():
    f = open(healthcheck_file, "w")
    f.write("OK")
    f.close()

def my_ip_address():

    # This list is adjustable, uncomment the one you want to use
    # url = 'http://myip.dnsomatic.com'
    # url = 'http://www.trackip.net/ip'
    # url = 'http://myexternalip.com/raw'
    url = 'https://api.ipify.org'
    try:
        ip_address = requests.get(url).text
    except:
        exit('%s: failed' % (url))
    if ip_address == '':
        exit('%s: failed' % (url))

    if ':' in ip_address:
        ip_address_type = 'AAAA'
    else:
        ip_address_type = 'A'

    return ip_address, ip_address_type

def do_dns_update(cf, zone_name, zone_id, dns_name, ip_address, ip_address_type):
    """Cloudflare API code - example"""

    try:
        params = {'name':dns_name, 'match':'all', 'type':ip_address_type}
        dns_records = cf.zones.dns_records.get(zone_id, params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records %s - %d %s - api call failed' % (dns_name, e, e))

    updated = False

    # update the record - unless it's already correct
    for dns_record in dns_records:
        old_ip_address = dns_record['content']
        old_ip_address_type = dns_record['type']

        if ip_address_type not in ['A', 'AAAA']:
            # we only deal with A / AAAA records
            continue

        if ip_address_type != old_ip_address_type:
            # only update the correct address type (A or AAAA)
            # we don't see this becuase of the search params above
            print('IGNORED: %s %s ; wrong address family' % (dns_name, old_ip_address))
            continue

        if ip_address == old_ip_address:
            print('UNCHANGED: %s %s' % (dns_name, ip_address))
            updated = True
            continue

        proxied_state = dns_record['proxied']
 
        # Yes, we need to update this record - we know it's the same address type

        dns_record_id = dns_record['id']
        dns_record = {
            'name':dns_name,
            'type':ip_address_type,
            'content':ip_address,
            'proxied':proxied_state
        }
        try:
            dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=dns_record)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones.dns_records.put %s - %d %s - api call failed' % (dns_name, e, e))
        print('UPDATED: %s %s -> %s' % (dns_name, old_ip_address, ip_address))
        updated = True

    if updated:
        return

    # no exsiting dns record to update - so create dns record
    dns_record = {
        'name':dns_name,
        'type':ip_address_type,
        'content':ip_address
    }
    try:
        dns_record = cf.zones.dns_records.post(zone_id, data=dns_record)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.dns_records.post %s - %d %s - api call failed' % (dns_name, e, e))
    print('CREATED: %s %s' % (dns_name, ip_address))

def main():

    while True:
        print('Renewing healthcheck file...")
        create_healthcheck_file()
        print('Checking to see if the public IP has changed...')
        for i in host:
            try:
                dns_name = i
            except:
                exit('usage: cloudflare-dns-updater.py fqdn-hostname')

            print('Checking ' + i + '...')
            
            host_name, zone_name = '.'.join(dns_name.split('.')[:2]), '.'.join(dns_name.split('.')[-2:])

            ip_address, ip_address_type = my_ip_address()

            print('MY IP: %s %s' % (dns_name, ip_address))

            cf = CloudFlare.CloudFlare(token=token)

            # grab the zone identifier
            try:
                params = {'name':zone_name}
                zones = cf.zones.get(params=params)
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                print('/zones %d %s - api call failed' % (e, e))
            except Exception as e:
                print('/zones.get - %s - api call failed' % (e))

            if len(zones) == 0:
                print('/zones.get - %s - zone not found' % (zone_name))

            if len(zones) != 1:
                print('/zones.get - %s - api call returned %d items' % (zone_name, len(zones)))

            zone = zones[0]

            zone_name = zone['name']
            zone_id = zone['id']

            do_dns_update(cf, zone_name, zone_id, dns_name, ip_address, ip_address_type)
            
        print('Now sleeping for ' + str(timeout) + ' seconds...')
        time.sleep(timeout)


if __name__ == '__main__':
    main()
