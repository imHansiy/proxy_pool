# -*- coding: utf-8 -*-
import sys
import argparse
from fetcher.proxyFetcher import ProxyFetcher

def test_fetcher_service(service_name):
    """
    Dynamically tests a specific proxy fetcher service.
    """
    fetcher = ProxyFetcher()
    if hasattr(fetcher, service_name):
        service_func = getattr(fetcher, service_name)
        print(f"--- Testing {service_name} ---")
        try:
            count = 0
            for proxy in service_func():
                print(proxy.to_dict)
                count += 1
            print(f"--- {service_name} finished, found {count} proxies. ---")
        except Exception as e:
            print(f"An error occurred while testing {service_name}: {e}")
    else:
        print(f"Error: Service '{service_name}' not found in ProxyFetcher.")
        print("Available services are:")
        for name in dir(fetcher):
            if name.startswith('freeProxy'):
                print(f"  - {name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test a specific proxy fetcher service.')
    parser.add_argument('service', type=str, help='The name of the service to test (e.g., freeProxy06).')
    
    # If no arguments are provided, print help and a list of available services
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        print("\nAvailable services:")
        fetcher = ProxyFetcher()
        for name in dir(fetcher):
            if name.startswith('freeProxy'):
                print(f"  - {name}")
        sys.exit(1)

    args = parser.parse_args()
    test_fetcher_service(args.service)