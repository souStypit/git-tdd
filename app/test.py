homehtml = open('app/templates/home.html', 'r')
homehtmltext = homehtml.read()
responsedata = b'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <title>My Webpage</title>\n</head>\n<body>\n    <h1>My Webpage</h1>\n</body>\n</html>' 
print(homehtmltext.encode())
print(responsedata)
print(homehtmltext.encode() == responsedata)