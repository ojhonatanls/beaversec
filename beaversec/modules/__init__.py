# Module registry for BeaverSec modules.
# Keep this file in sync as modules are added/removed.

from . import arp_scan
from . import dns_enum
from . import dns_zone_transfer
from . import http_headers
from . import ping_sweep
from . import port_scanner
from . import service_detection
from . import shodan_enum
from . import snmp_enum
from . import ssl_cipher_scan
from . import ssl_scan
from . import subdomain_brute
from . import syn_scan
from . import udp_scan
from . import vuln_scanner
from . import whois_lookup

MODULES = {
    arp_scan.ArpScanModule.name: arp_scan.ArpScanModule,
    dns_enum.DNSEnum.name: dns_enum.DNSEnum,
    dns_zone_transfer.DNSZoneTransferModule.name: dns_zone_transfer.DNSZoneTransferModule,
    http_headers.HTTPHeadersModule.name: http_headers.HTTPHeadersModule,
    ping_sweep.PingSweepModule.name: ping_sweep.PingSweepModule,
    port_scanner.PortScannerModule.name: port_scanner.PortScannerModule,
    service_detection.ServiceDetectionModule.name: service_detection.ServiceDetectionModule,
    shodan_enum.ShodanEnumModule.name: shodan_enum.ShodanEnumModule,
    snmp_enum.SNMPEnumModule.name: snmp_enum.SNMPEnumModule,
    ssl_cipher_scan.SSLCipherScanModule.name: ssl_cipher_scan.SSLCipherScanModule,
    ssl_scan.SSLScanModule.name: ssl_scan.SSLScanModule,
    subdomain_brute.SubdomainBruteModule.name: subdomain_brute.SubdomainBruteModule,
    syn_scan.SynScanModule.name: syn_scan.SynScanModule,
    udp_scan.UDPScanModule.name: udp_scan.UDPScanModule,
    vuln_scanner.VulnScannerModule.name: vuln_scanner.VulnScannerModule,
    whois_lookup.WhoisLookup.name: whois_lookup.WhoisLookup,
}
