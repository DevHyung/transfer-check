import datetime
import xlsxwriter
# Create a workbook and add a worksheet.
fileName = input("파일명을 입력하세요(확장자포함) ::")
workbook = xlsxwriter.Workbook(fileName+'_RESULT.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write_row(0,0,['카드번호','트랜잭션ID','사용자구분코드','출발ID','출발_호선','출발수단','출발시간','도착ID','도착_호선','도착수단','도착시간','환승시간(초)'])
row = 1
col = 0

# Start from the first cell. Rows and columns are zero indexed.
def get_second(first, last):
    try:
        first_time = datetime.datetime(int(first[0:4]), int(first[4:6]), int(first[6:8]), int(first[8:10]), int(first[10:12]), int(first[12:]))
        last_time = datetime.datetime(int(last[0:4]), int(last[4:6]), int(last[6:8]), int(last[8:10]), int(last[10:12]), int(last[12:]))
        td = last_time - first_time
        return td.seconds
    except:
        return "안찍고내림"

f = open(fileName,'r',encoding='utf8').readlines()
f2 = open(fileName+'_RESULT.csv','w')
f2.writelines(['카드번호',',','트랜잭션ID',',','사용자구분코드',',','출발ID',',','출발_호선',',','출발수단',',','출발시간',',','도착ID',',','도착_호선',',','도착수단',',','도착시간',',','환승시간(초)',',','\n'])
#번호,일련번호,카드번호,승차일시,트랜잭션ID,교통수단코드,환승횟수,표준노선ID,교통사업자ID,표준차량ID,사용자구분코드,운행출발일시,표준승차정류장ID,하차일시,표준하차정류장ID,이용객수_다인승,승차금액,하차금액,임시필드
lines = f
oldCardNo = ''
oldTranjectionId = 0
oldLineIdx = 1
isFirst = True
for line in lines[1:]:
    datas = line.split(',')
    #
    if isFirst:
        oldCardNo = datas[2]
        oldTranjectionId = datas[4]
        isFirst = False
    else:
        newCardNo = datas[2]
        newTranjectionId = datas[4]
        newLineIdx = oldLineIdx + 1
        if oldCardNo == newCardNo and oldTranjectionId == newTranjectionId: #환승
            lateIdx = 0
            firstIdx = 0
            print("{}줄과 {}줄 환승".format(oldLineIdx,newLineIdx))
            #print("\t old는 {} 그리고 new는 {} ".format(str(lines[oldLineIdx].split(',')[3]),str(lines[newLineIdx].split(',')[3])))
            if lines[oldLineIdx].split(',')[3] > lines[newLineIdx].split(',')[3]:
                #print("나중에 내린거 {}".format(lines[oldLineIdx].split(',')[3]))
                firstIdx = newLineIdx
                lateIdx = oldLineIdx
            else:
                #print("나중에 내린거 {}".format(lines[newLineIdx].split(',')[3]))
                firstIdx = oldLineIdx
                lateIdx = newLineIdx

            #출발수단코드 계산
            if len(str(lines[firstIdx].split(',')[14]).strip()) <= 4: #지하철코드
                startCode = '0'
            else:#버스코드
                startCode = '1'
            #도착수단코드계산
            if len(str(lines[lateIdx].split(',')[12]).strip()) <= 4: #지하철코드
                endCode = '0'
            else:#버스코드
                endCode = '1'
            print(lines[0].split(','))
            print(lines[firstIdx].split(','))
            print(lines[lateIdx].split(','))

            #print("카드번호 : {} \n 트랜잭션ID : {} \n 사용자구분코드 : {} \n 출발ID : {} \n 출발호선 : {} \n 출발수단 : {} \n 도착 ID : {} \n 도착호선 : {} \n 도착수단 : {} \n 환승시간(초) : {}"
            #      .format( oldCardNo, oldTranjectionId, datas[10], lines[firstIdx].split(',')[14], lines[firstIdx].split(',')[14],
            #               startCode, lines[lateIdx].split(',')[12],lines[lateIdx].split(',')[12],endCode,get_second(lines[firstIdx].split(',')[13],lines[lateIdx].split(',')[3])))
            worksheet.write_row(row,col, [oldCardNo, oldTranjectionId, datas[10], lines[firstIdx].split(',')[14], lines[firstIdx].split(',')[14],startCode, lines[firstIdx].split(',')[13],lines[lateIdx].split(',')[12],lines[lateIdx].split(',')[12],endCode,lines[lateIdx].split(',')[3],get_second(lines[firstIdx].split(',')[13],lines[lateIdx].split(',')[3])])
            f2.writelines([oldCardNo, ',',oldTranjectionId,',',datas[10], ',',lines[firstIdx].split(',')[14], ',',lines[firstIdx].split(',')[14],',',startCode, ',',lines[firstIdx].split(',')[13],',',lines[lateIdx].split(',')[12],',',lines[lateIdx].split(',')[12],',',endCode, ',',lines[lateIdx].split(',')[3],',',str ( get_second(lines[firstIdx].split(',')[13],lines[lateIdx].split(',')[3]) ),',','\n'])
            row+=1
        oldCardNo = newCardNo
        oldTranjectionId = newTranjectionId
        oldLineIdx += 1
workbook.close()
f2.close()
# 데이터셋 보는곳
"""
for line in lines:
    datas = line.split(',')
    print(datas)
"""

