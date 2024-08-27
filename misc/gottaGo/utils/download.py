def download_file(url, local_filename):
    # Send a GET request to the URL
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Check for any HTTP errors

        # Open the local file in write-binary mode
        with open(local_filename, 'wb') as file:
            # Write the response content to the file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)

    print(f"Downloaded file saved as: {local_filename}")
import sys
import requests
arg1=str(sys.argv[1])
arg2=str(sys.argv[2])

if __name__ == "__main__":
    download_file(arg1,arg2)

