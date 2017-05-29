import os
import docker
import CloudFlare
from datetime import datetime


def point_domain(name):
    try:
        r = cf.zones.dns_records.post(zone_id,
                                      data={u'type': u'CNAME', u'name': name, u'content': target_domain, u'ttl': 120,
                                            u'proxied': False})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        print '/zones.dns_records.post %s - %d %s' % (name, e, e)


def check_container(c):
    for prop in c.attrs.get(u'Config').get(u'Env'):
        if u'VIRTUAL_HOST' in prop or u'FLARE_DOMAIN' in prop:
            value = prop.split("=")[1].strip()
            if ',' in value:
                for v in value.split(","):
                    point_domain(v)
            else:
                point_domain(value)


def init():
    for c in client.containers.list(all=True):
        check_container(c)


try:
    zone_id = os.environ['ZONE_ID']
except KeyError as e:
    exit('ZONE_ID not defined')

try:
    email = os.environ['EMAIL']
except KeyError as e:
    exit('EMAIL not defined')

try:
    token = os.environ['TOKEN']
except KeyError as e:
    exit('TOKEN not defined')

try:
    target_domain = os.environ['TARGET_DOMAIN']
except KeyError as e:
    exit('TARGET_DOMAIN not defined')

cf = CloudFlare.CloudFlare(email=email, token=token)
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

init()

t = datetime.now().time().strftime("%s")

for event in client.events(since=t, filters={'status': u'start'}, decode=True):
    if event.get(u'status') == u'start':
        try:
            print u'started %s' % event.get(u'id')
            check_container(client.containers.get(event.get(u'id')))
        except docker.errors.NotFound as e:
            print 'Ignoring %s' % event.get(u'from')
