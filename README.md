# Wireguard telegram bot monitor
Pet project, which allows you to monitor connections to your wireguard VPN(with help of [subspace](https://github.com/subspacecommunity/subspace))

## Example
send `/wg` to bot
he will reply something like
```
interface: wg0
    public key: ******
    private key: (hidden)
    listening port: 51820

peer: ******
    endpoint: 91.******:47503
    allowed ips: 10.******/32, fd00::******/128
    latest handshake: 33 seconds ago
    transfer: 177.47 MiB received, 1.70 GiB sent
    name: ThinkPadE14-Mint

peer: ******
    endpoint: 91.******:60437
    allowed ips: 10.******/32, fd00::******/128
    latest handshake: 4 hours, 35 minutes, 35 seconds ago
    transfer: 15.32 MiB received, 407.67 MiB sent
    name: GalaxyA50
```
with nice markdown(bold and italic text)