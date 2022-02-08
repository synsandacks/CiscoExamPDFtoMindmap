import PyPDF2
import re

def pdftotext(pdffile):
    pdfFile = open(pdffile, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    numPages = pdfReader.numPages
    pdfText = ''

    for page in range(numPages):
        pdfPage = pdfReader.getPage(page)
        pdfText += pdfPage.extractText()
    pdfFile.close()

    pdfText = pdfText.split('any time without notice.')[1]
    pattern = r'\d\d\d\d Cisco Systems, Inc. This document is Cisco Public. Page \d'
    pdfText = pdfText.replace('\n', '')
    pdfText = re.sub(pattern, '', pdfText)
    pdfText.strip('  ')
    return pdfText

def objectiveBuilder(textList):
    newlist = []
    while len(textList) > 1:
        loopString = ''
        if re.match(r'\d\d%|\d\.\d', textList[0]):
            loopString += textList[0]
            textList.remove(textList[0])

            while len(textList) > 1 and not re.match(r'\d\d%|\d\.[1-9]', textList[0]):
                loopString += f' {textList[0]}'
                textList.remove(textList[0])
            newlist.append(loopString)

        if not re.match(r'\d\d%|\d\.\d', textList[0]):
                newlist[-1] += f' {textList[0]}'
                textList = []
            
    return newlist
    
def makemd(exam, list, outfile):
    with open(outfile, 'w') as f:
        f.write(f'# {exam}\n')

        for objective in list:
            if re.search(r'\d\.0', objective):
                f.write(f'## {objective}\n')
            
            if re.search(r'\d\.[1-9]\s', objective):
                f.write(f'### {objective}\n')
            
            if re.search(r'\d\.\d\.[a-zA-Z]', objective):
                f.write(f'#### {objective}\n')
        f.close()


def main():
    pdf = 'pdfs\\200-301-CCNA.pdf'
    outFile = '200-301-CCNA.md'
    exam = 'CCNA Exam v1.0 (CCNA 200-301)'
    pdfText = pdftotext(pdf)
    pdfText = pdfText.split()
    objectives = objectiveBuilder(pdfText)
    makemd(exam, objectives, outFile)


if __name__ == '__main__':
    main()