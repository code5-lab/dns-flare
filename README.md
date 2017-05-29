Automatically creates CNAMES pointing to a specific domain when other containers are created

### Usage

To run it:

    version: '2'
    services:
      dns_flare:
        build: .
        volumes:
          - /var/run/docker.sock:/var/run/docker.sock
        environment:
          - "EMAIL=<cloud flare email>"
          - "ZONE_ID=<cloud flare zone id>"
          - "TOKEN=<cloud flare api token>"
          - "TARGET_DOMAIN=<cloud flare target domain>"

Then start any containers you want registered with an env var `VIRTUAL_HOST=subdomain.youdomain.com` or `FLARE_DOMAIN=subdomain.youdomain.com`

    $ docker run -e VIRTUAL_HOST=foo.bar.com  ...

or

    $ docker run -e FLARE_DOMAIN=foo.bar.com  ...

Highly inspired and compatible with https://github.com/jwilder/nginx-proxy

Pull requests are welcome and ideas for future development