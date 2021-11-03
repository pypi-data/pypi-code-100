import pyttsx3
import PyPDF2

def readitout(book,page_number,voice,speech_rate):

    toread = open(book, 'rb')
    read = PyPDF2.PdfFileReader(toread)
    last_page = read.numPages
    print('Total number of pages in a book is ' + str(last_page))

    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')
    if voice == 'female':
        speaker.setProperty('voice', voices[0].id)
    elif voice == 'male':
        speaker.setProperty('voice', voices[1].id)
    else:
        print('please pass either male or female in voice')
    speaker.setProperty('rate', speech_rate)

    page = read.getPage(page_number)
    content = page.extractText()
    speaker.say(content)
    speaker.runAndWait()
