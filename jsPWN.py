import time
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import jsbeautifier
import re

# Prints help if arguments are missing
currentGlobalCounter = 0;

try:

    print("Fetching HTML and parsing it ...")

    # Reads the target url from the command line argument

    target = sys.argv[1]

    # Reads the htmlTag used to store the remote scripts

    if (len(sys.argv) == 3):
        htmlTag = sys.argv[2]
    else:
        htmlTag = "pre"

    # Makes firefox browser headless -> Prevents selenium from opening window

    os.environ['MOZ_HEADLESS'] = '1'

    # Prepares firefox driver for selenium

    browser = webdriver.Firefox()

    # Sends a GET request to the provided target by opening the browser

    browser.get(target)

    # Gets the HTML source code of the target

    targetSourceCode = browser.page_source

    # Delay of 5 seconds, because after browser is opened scripts take time to load

    time.sleep(5)

    # Close the browser, from now on targetSourceCode is set

    browser.close()

    # Creates a parsable object out of the HTML source code

    soup = BeautifulSoup(targetSourceCode, 'html.parser')

    # Parse all <script> tags and their content respectivly

    allScriptTags = soup.find_all("script")

    # Original sourceCodeFetch + 8 seconds per remote Script + 1 second for the local scripts

    print(f"Runtime will be about {5 + len(allScriptTags) * 8 + 1} seconds... Fetching {len(allScriptTags)} scripts")

    # Creates outputDirectory name after full target URL(replace for compatability)

    outputDirectory = target.replace("/", "SLASH").replace("?", "QUESTION")

    # Cuts the length if it exceededs 255 bytes(Linux maxFileNameLength)

    if (len(outputDirectory) > 255):

        outputDirectory = outputDirectory[:252] + "CUT"
        print("Filename length > 255 -> Cutting it off")

    os.mkdir(outputDirectory)

    # Used for naming of the outputFile

    i = 0

    # Iterate through all parsed scriptTags

    for scriptTag in allScriptTags:

        # Increase counter for naming convention

        i += 1

        # Checks if the scriptTag is available locally or remotely

        if " src=" in str(scriptTag) or " src =" in str(scriptTag):

            # Open and create the outputFile for remote source code

            with open(outputDirectory + "/" + str(i) + ".js", "w") as file:

                # Parses the url(as string) of the remote script out of script tag

                urlOfRemoteScript = str(scriptTag["src"])

                # Checks if src is given as "/something" instead of https://example.com/something

                if (urlOfRemoteScript[:4] != "http" and urlOfRemoteScript[:5] != "https"):

                    # Parse domain out of target url from command line argument

                    targetDomain = target.replace("https://", "")
                    targetDomain = re.sub(r"/.*", "", targetDomain)

                    # Get the urlScheme from the target command line argument

                    urlScheme = ""

                    if (target[:7] == "http://"):
                        urlScheme = "http://"
                    elif (target[:8] == "https://"):
                        urlScheme = "https://"
                    else:
                        print(
                            f"ERROR: --->  Unkown urlScheme({urlScheme}) <---")

                    # Combine the domain and path back to a URL

                    urlOfRemoteScript = f"{urlScheme}{targetDomain}{urlOfRemoteScript}"

                # GETs the remote javascript and converts it to a string(same as at top basically)

                browser = webdriver.Firefox()
                browser.get(urlOfRemoteScript)
                remoteHTML = str(browser.page_source)
                print(
                    f"Fetching remote script {i} from: {urlOfRemoteScript} ...")
                time.sleep(5)

                browser.close()

                soup2 = BeautifulSoup(remoteHTML, 'html.parser')

                try:

                    remoteJavascript = soup2.find_all(htmlTag)

                    if (len(remoteJavascript) != 1):
                        if (len(remoteJavascript) == 0):
                            raise Exception()
                        else:

                            print(
                                f"{urlOfRemoteScript} has to be fetched manually, as the given html tag '<{htmlTag}>' occurs more than once")

                    else:

                        # Turns the remoteJavascript into a string(for writing to file)

                        remoteDecodedJavascript = str(remoteJavascript)

                        # Beautify the remoteDecodedJavascript

                        finalJavascript = jsbeautifier.beautify(
                            remoteDecodedJavascript)

                        # Writes the remoteDecodedJavascript to the file

                        file.write(finalJavascript)
                except:

                    print(
                        f"Provided HTML tag '<{htmlTag}'> not found on: {urlOfRemoteScript}")

        else:

            # Open and create the outputFile for local source code

            with open(outputDirectory + "/" + str(i) + ".js", "w") as file:

                # Write the beautified javascript the file("string" remove <script)

                file.write(str(jsbeautifier.beautify(scriptTag.string)))

                print(f"Fetching local script {i} from {target} ...")

        if (i == len(allScriptTags)):
            print(
                f"----------------\n\nSuccesfully fetched {i} scripts from: {target}\n\nOutput directory is {outputDirectory}\n\n----------------")
        currentGlobalCounter++
except:
    print("-------------------------------------------")
    print(f"ERROR occured while fetching: {allScriptTags[currentGlobalCounter - 1]}")
    print("-------------------------------------------")
    print('Usage: python3 jsPWN.py "https://example.com/" h1')
    print("Requirements: pip install -r requirements.txt\n")
    print("The second argument(h1) is the HTML tag used to embed the javascript into the HTML context on remote pages.")
    print("So, if the target website has: <script src = 'https://example.com/'> you need to check how the javascript on https://example.com/ is embedded")
    print("As most websites use <pre> anyway, checking this for one of the external scripts should be sufficent\n")
    print("Example: <html><body><pre>window.alert(1)</pre></body></html>   --->   python3 jsPWN.py 'https://example.com' pre")
    print("-------------------------------------------")
