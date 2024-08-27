import requests
class utils:
    import requests
    def get_prime_factors(n):
        # Step 1: Submit the number to FactorDB
        url = f"http://factordb.com/api?query={n}"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception("Failed to connect to FactorDB")

        data = response.json()

        # Step 2: Check the status and retrieve factors
        if data['status'] not in ['FF', 'CF']:
            raise Exception(f"Factorization not available for {n}")

        factors = []
        for factor in data['factors']:
            prime, exponent = factor
            factors.extend([int(prime)] * int(exponent))
        
        # Assuming n is a product of two primes, p and q
        if len(factors) != 2:
            # raise Exception(f"Unexpected number of factors for {n}: {factors}")
            return False

        return factors[0], factors[1]      
    import requests

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


    def decrypt(p,q,e,n,c):
        from Crypto.Util.number import getPrime, bytes_to_long,long_to_bytes


        phi=(p-1)*(q-1)
        d=pow(e,-1,phi)
        print(d)
        result=pow(c,d,n)
        print(long_to_bytes(result))
        return;
