 

def extract_host_port_from_requests_headers(headers:requests.structures.CaseInsensitiveDict=None,port:int=None):
    # non good code. requires better logic in port, and host extraction
    import requests
    host = ""
    try:
        port = int(port) if port else 80
        for header in request_headers:
            if header.startswith(b'Host:'):
                host_with_port = header.split(b' ')[1].decode()
                if ':' in host_with_port:
                    host, port_str = host_with_port.split(':')
                    try:
                        port = int(port_str)
                    except ValueError:
                        pass  # Invalid port, use the default
                else:
                    host = host_with_port
                break
        return host, port
    except Exception as error:
        #print(str(error))
        return 'no host found in headers'
import requests
req = requests.get('http://google.com')


#extract_host_port_from_requests_headers(request_headers)
#extract_host_port_from_requests_headers(headers=req.headers,port=None)