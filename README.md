# httpAlive - URL Analysis Tool for Web Application Penetration

[Tool Link](https://github.com/aashishtechsecurity/httpAlive/)

---

![GitHub last commit](https://img.shields.io/github/last-commit/aashishtechsecurity/httpAlive) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/aashishtechsecurity/httpAlive) [![GitHub license](https://img.shields.io/github/license/aashishtechsecurity/httpAlive)](https://github.com/aashishtechsecurity/httpAlive/blob/main/LICENSE) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/aashishsec/)

## Overview

- The "httpAlive" tool is designed to efficiently probe for alive subdomains and URLs from a provided list.
- It includes features such as user-agent rotation, colorized output, multithreading, and a command-line interface (CLI) for ease of use.
- Works in all platforms.

## Features

1. **User-Agent Rotation:**
   - Randomly selects a user agent from a predefined list for each HTTP request to avoid detection.

2. **Colorized Output:**
   - Utilizes the `colorama` library to provide colorized and visually appealing output.

3. **Multithreading:**
   - Implements multithreading using Python's `concurrent.futures` module for concurrent execution of HTTP requests.

4. **HTTP Client:**
   - Utilizes the `httpx` library as the HTTP client with SSL certificate verification disabled.

5. **Command-Line Interface (CLI):**
   - Accepts command-line arguments through the `argparse` module for easy configuration.

6. **Output File:**
   - Saves results to an output file specified by the user (default: "httpAlive_output.txt").

7. **Banner Display:**
   - Displays a colorful banner at the beginning with information about the tool, author, and GitHub profile.

8. **Exception Handling:**
   - Includes exception handling to gracefully handle interruptions, such as `KeyboardInterrupt`.
     

## Installation

- Clone the repository to your local machine.

### Method 1

```bash

git clone https://github.com/aashishtechsecurity/httpAlive.git

cd httpAlive

pip install -r requirements.txt

```

### Method 2

```bash

git clone https://github.com/aashishtechsecurity/httpAlive.git

cd httpAlive

pip install .


```

### httpAlive help:

``` bash

██╗░░██╗████████╗████████╗██████╗░░░░░░░░█████╗░██╗░░░░░██╗██╗░░░██╗███████╗
██║░░██║╚══██╔══╝╚══██╔══╝██╔══██╗░░░░░░██╔══██╗██║░░░░░██║██║░░░██║██╔════╝
███████║░░░██║░░░░░░██║░░░██████╔╝█████╗███████║██║░░░░░██║╚██╗░██╔╝█████╗░░
██╔══██║░░░██║░░░░░░██║░░░██╔═══╝░╚════╝██╔══██║██║░░░░░██║░╚████╔╝░██╔══╝░░
██║░░██║░░░██║░░░░░░██║░░░██║░░░░░░░░░░░██║░░██║███████╗██║░░╚██╔╝░░███████╗
╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚═╝░░░░░░░░░░░╚═╝░░╚═╝╚══════╝╚═╝░░░╚═╝░░░╚══════╝
      
        Author   : Bande Aashish💕
                                              
        Github   : https://github.com/aashishtechsecurity
        
        Version  : v1.1.0
          
        httpAlive is a tool designed to efficiently probe for alive subdomains and Urls from a provided list.


usage: httpalive-Mark9.py [-h] -l list [-o output] [-c CONCURRENCY] [-t THREADS]

options:

  -h, --help            show this help message and exit.

  -l list, --DomainList list
                        [INFO]: List of Subdomains or URLs.

  -o output, --output output
                        [INFO]: File to save our output.

  -c CONCURRENCY, --concurrency CONCURRENCY
                        [INFO]: Concurrency level to make fast process.

  -t THREADS, --threads THREADS
                        [INFO]: Threading level to make fast process.

```

## Usage

- Create a file containing that contains list of URLs or subdoamins or both and give to httpAlive. The output contains status codes and content length.

- This python code will save the results of the analysis to a file named 'output.txt'.

- Run the script with urls or subdomain list.

### Note
- Do not give more threads. It might cause Race Condition

### Method 1

```bash

python ./httpAlive/httpAlive -l subdomainList.txt

```

### Method 2

```bash

httpAlive -l subdomainList.txt

```

## Tool Output

![image](https://github.com/aashishtechsecurity/httpAlive/assets/65489287/c15966b3-9795-4e30-b33a-a30b42438614)

## Contributing

- Contributions are welcome!
  
- If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.


![image](https://github.com/aashish36/JSScanner/assets/65489287/70f7e3a8-e95f-429b-9433-89087daad721)

