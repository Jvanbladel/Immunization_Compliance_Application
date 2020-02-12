import hashlib

def main(textToHash):
    encodedText = textToHash.encode('utf8')
    hash = hashlib.sha256(encodedText)
    finalOutput = hash.hexdigest()
    print(finalOutput)
    return finalOutput
main("Hi")