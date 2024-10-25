import os
import requests
requests.packages.urllib3.disable_warnings() 

def download_file(url, filename, rnew=False, chunk_size = 1024*1024, proxies={}):    
    if not rnew and os.path.exists(filename):    
        local_file_size = os.path.getsize(filename)
    else:
        local_file_size = 0


    response = requests.head(url)
    remote_file_size = int(response.headers['content-length'])    

    if remote_file_size == local_file_size:
        return True
    headers = {'Range': 'bytes=%d-' % local_file_size, 'Connection': 'close'}

    response = requests.get(url, headers=headers, stream=True, verify=False, proxies=proxies)

  
    with open(filename, "wb" if rnew else  'ab') as fp:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                fp.write(chunk)
           
    return os.path.getsize(filename) == remote_file_size


