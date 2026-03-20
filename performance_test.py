import asyncio
import aiohttp
import random
import time
from typing import Dict

def format_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)  # Extract milliseconds
    h = int(seconds // 3600)  # Extract hours
    m = int((seconds % 3600) // 60)  # Extract minutes
    s = int(seconds % 60)  # Extract seconds
    return f"{h:02}:{m:02}:{s:02}:{ms:03}" 

tenant_endpoints = [
    {
        "api":"Z0FBQUFBQm05ZEFiNTJ6cE9tcWRsalViYVVHTnIwcWtXNjFUUUpLSXBPZlJ2MTZHRDh6WUlKdi1sVnhjYVYzUWFDQ1VsZE95WlRXMHQ5TWZyVENTa0pERjlBSURlQWRGWlB5OEZ3WWJuV3JxcmJuSng5VkpKN1U9",
        "ext":"/api/get-data",
        "xfun":"",
        "model":"Industry",
        "tenant":"Unkago"
    },
    {
        "api":"Z0FBQUFBQm05Y2RjYlk1THZWVXFEQjZnUWt1U21oNTdlSExQSVJhemlDaEdvWFlhQTFKcWRPa0tyT21qcVJJc3M0ZTRCVG1tMy1jdldpajQyV29Lb3gwaWY0a2dqVUs5azVJaW5Ob2lmdDNJZV8zNTRMN3Y1WTQ9",
        "ext":"/api/get-data",
        "xfun":"",
        "model":"Stock_Item",
        "tenant":"Demo"
    },
    {
        "api":"Z0FBQUFBQm05Y196aXhlNkstWjRYUHlvS2JRRUZCcHFRNlJfU2pyeFJWdHJRWjlkaE5oUnhvNDFMZkFaMnFxRDZTTlZpLTRCRkI2d3BUN1VIWXF1clo0OGpWVjhWQ3R1amYwQmwwemJVcVdTRm9OSmZnRVZDREE9",
        "ext":"/api/get-data",
        "xfun":"",
        "model":"GL_Entry",
        "tenant":"Probase"
    },
    {
        "api":"Z0FBQUFBQm05ZEg1eFNralQycWNueExBaXo4bmhwV1FBRE5nMDU3cUpwT3ZhTGFWeVVpLWRrSVhwdGhrUzdScF9RZWJXM2Z0dkk4ZW95ckc5bktuY0RNdGhWWFlvdkR6VFVqd3lNLXo2VG5mTnAwaHk0WnJoeTQ9",
        "ext":"/api/get-data",
        "xfun":"",
        "model":"Account",
        "tenant":"ABC ASSETS"
    },
    {
        "api":"Z0FBQUFBQm05ZEkyQ1ZBWFJ2LXNBUVRtRUhsRUZLTTNmVFlBV1BQVmF1TkR2Rk0xNVVLQXV1WnIwb0oyck83bGVBU0NrN2hWN0xDRDdndWpONm5hdmpUTVM0Ukt4alJ3VFVFZ25hX3YyUklXSHZpbDNuaTg2cXM9",
        "ext":"/api/get-data",
        "xfun":"",
        "model":"Smart_Invoice_Sale",
        "tenant": "Sandbox"
    },
    {
        "api":"Z0FBQUFBQm05ZElZQ1JTaVBvX3JwOVItVWZQVVdFMVdjOEkyZ1JfVmJpaks1TzdidGs5bkFEUXlwaGJCOUpDbmpOcVR4cGhDRjhhMFBmc2YzRGpicnRtU2QwZEZlRlYxS3ZEdXZvNllBUVR1aHNiR3BFbEtzWG89",
        "ext":"/api/get-data",
        "xfun":"",
        "model":"Purchase_Invoice",
        "tenant": "Lanzi"
    },
    
]


async def send_request(session: aiohttp.ClientSession, params: Dict):
    try:
        start_time = time.time()
        
        headers = {
            'Content-Type': "application/json",
            'api-key': params.get("api"),
            'api-key': "Z0FBQUFBQm5CRTlxLWFGZ0Y2bk1ocUtpQUhVb1FOTUtkd3NGdFhJN1BQTE1KcDVzbERtYlZyVVBlREFPNmdWS21LR2s2U0JUTFhod2ZMem9UOUEzanRQNGIybXBPZW1IeFJpb0xPRVlOcUFPLTdxWU9tRE5TMjg9",
            'xfun': params.get("xfun"),
            "model":params.get("model")
        }
        
        url = f"http://startapperp.com:8000{params.get('ext')}"
        
        async with session.get(url, headers=headers) as response:
            end_time = time.time()
            res = {"TENANT::::":params.get("tenant"), "\nSTATUS CODE::::": response.status, "\nRESPONSE::::": await response.text()}
            print(params.get("tenant"), {params.get("model")}, response.status, format_time(end_time - start_time))
            return res
    except Exception as e:
        return {"TENANT::::":params.get("tenant"), "ERROR::::": str(e)}

async def test_multitenancy():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(1000): 
            params = random.choice(tenant_endpoints)
            task = asyncio.create_task(send_request(session, params))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(test_multitenancy())
    print(f"Test completed in {time.time() - start_time:.2f} seconds.")