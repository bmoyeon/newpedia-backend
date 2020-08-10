import re

def find_category(name):
    if re.compile('[가-기]+').findall(name[0]):
        category_name = 'ㄱ'
    elif re.compile('[나-니]+').findall(name[0]):
        category_name = 'ㄴ'
    elif re.compile('[다-디]+').findall(name[0]):
        category_name = 'ㄷ'
    elif re.compile('[라-리]+').findall(name[0]):
        category_name = 'ㄹ'
    elif re.compile('[마-미]+').findall(name[0]):
        category_name = 'ㅁ'
    elif re.compile('[바-비]+').findall(name[0]):
        category_name = 'ㅂ'
    elif re.compile('[사-시]+').findall(name[0]):
        category_name = 'ㅅ'
    elif re.compile('[아-이]+').findall(name[0]):
        category_name = 'ㅇ'
    elif re.compile('[자-지]+').findall(name[0]):
        category_name = 'ㅈ'
    elif re.compile('[차-치]+').findall(name[0]):
        category_name = 'ㅊ'
    elif re.compile('[카-키]+').findall(name[0]):
        category_name = 'ㅋ'
    elif re.compile('[타-티]+').findall(name[0]):
        category_name = 'ㅌ'
    elif re.compile('[파-피]+').findall(name[0]):
        category_name = 'ㅍ'
    elif re.compile('[하-히]+').findall(name[0]):
        category_name = 'ㅎ'
    else:
        category_name = '기타'

    return category_name
