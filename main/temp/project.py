# -*- coding: utf-8 -*-

#from main import *
#from main import app
from main import render_template
from main import mongo
from main import datetime
from main import relativedelta
from main import request
from main import url_for, redirect, flash
from flask import Blueprint
from main import ObjectId
from main import abort

blueprint = Blueprint("project", __name__, url_prefix="/project")

@blueprint.route("/view")
def project_view():
    idx = request.args.get("idx")
    if idx is not None:
        col = mongo.db.version_list_customer
        data = col.find_one({"_id": ObjectId(idx)})
        result = {
            "id": data.get("_id"),
            "project_name1": data.get("project_name1"),
            "project_name2": data.get("project_name2"),
            "name": data.get("name"),
            "startdate": data.get("startdate"),
            "enddate": data.get("enddate"),
            "author": data.get("author"),
            "pubdate": data.get("pubdate")
        }
    
        #return(result['project_name'])
        return render_template("project_view.html", result=result)
    return abort(400)

@blueprint.route("/edit", methods=["GET", "POST"])
def project_edit():
    idx = request.args.get("idx")
    
    project_name1 = request.form.get("project_name1")
    project_name2 = request.form.get("project_name2")
    name = request.form.get("name")
    startdate = request.form.get("startdate")
    enddate = request.form.get("enddate")
    author = request.form.get("author")
    
    col = mongo.db.version_list_customer
    
    col.update_one({"_id": ObjectId(idx)}, {
            "$set": {
                "project_name1": project_name1,
                "project_name2": project_name2,
                "name": name,
                "startdate": startdate,
                "enddate": enddate,
                "author": author,

            }
        })
    flash("수정되었습니다.")
    return redirect(url_for("project.project_write"))


@blueprint.route("/delete/<idx>")
def project_delete(idx):
    col = mongo.db.version_list_customer    
    col.delete_one({"_id": ObjectId(idx)})
    
    flash("삭제되었습니다.")
    return redirect(url_for("project.project_write"))


@blueprint.route("/write", methods=["GET", "POST"])
def project_write():
    col = mongo.db.version_list_customer
    data = col.find({}).sort("pubdate",-1)
    
    if request.method == "POST":
        
        project_name1 = request.form.get("project_name1")
        project_name2 = request.form.get("project_name2")
        name = request.form.get("name")
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        author = request.form.get("author")
        
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)
        
        post = {
                "project_name1" : project_name1,
                "project_name2" : project_name2,
                "name" : name,
                "startdate" : startdate,
                "enddate" : enddate,
                "author" : author,
                "pubdate": current_utc_time,
                }
        col.insert_one(post)

        return redirect(url_for("project.project_write", data=data))
    
    else:
        return render_template("project_write.html", data=data)


@blueprint.route("/schedule")
def project_schedule():
    
    day = datetime.now() #현재 날짜 계산
    
    #table 헤더 값을 구함 현재 달에서 -3, +8
    th = [
            '<th>' + (day - relativedelta(months = 3)).strftime('%Y-%m') + '</th>',
            '<th>' + (day - relativedelta(months = 2)).strftime('%Y-%m') + '</th>',
            '<th>' + (day - relativedelta(months = 1)).strftime('%Y-%m') + '</th>',
            '<th style="background-color:#FA58AC"><font color="#FFFFFF">' + day.strftime('%Y-%m') + '</font></th>',
            '<th>' + (day + relativedelta(months = 1)).strftime('%Y-%m') + '</th>',
            '<th>' + (day + relativedelta(months = 2)).strftime('%Y-%m') + '</th>',
            '<th>' + (day + relativedelta(months = 3)).strftime('%Y-%m') + '</th>',
            '<th>' + (day + relativedelta(months = 4)).strftime('%Y-%m') + '</th>',
            '<th>' + (day + relativedelta(months = 5)).strftime('%Y-%m') + '</th>',
            '<th>' + (day + relativedelta(months = 6)).strftime('%Y-%m') + '</th>',
            '<th>' + (day + relativedelta(months = 7)).strftime('%Y-%m') + '</th>'
        ]
    
    #version_list_TCS DB 연결
    col = mongo.db.version_list_TCS
    
    #version_list_TCS에 저장된 data중 가장 최신 date의 data만 find
    date_temp = list(col.find({}, {"_id":0, "date":1}))
    date = sorted(date_temp, reverse = True, key = lambda x:(x['date']))
    
    #DB에서 enddate가 table th 범위 안에 있고 date가 오늘 날짜 인것만 find
    data = list(col.find({"$and": [ {"enddate":{"$gte":(day - relativedelta(months = 3)).strftime('%Y-%m-%d')}}, 
                                    {"enddate":{"$lte":(day + relativedelta(months = 8)).strftime('%Y-%m-%d')}},
                                    {"date":(date[0]['date'])}
                                    ]}, {"project_key":1,"project_name":1 , "name":1, "enddate":1, "date":1} ))
    
    #data에서 중복 제거한 project_key 값을 추출하여 project_key_only에 저장
    project_key_only = []
    for i in range(len(data)):
        if data[i]['project_key'] not in project_key_only:
            project_key_only.append(data[i]['project_key'])
    
    
    #project_key를 key로 하는 dict 형태로 data를 변경하여 temp에 저장
    temp = {}
    for i in range(0, len(project_key_only)):
        temp1 = []
        for j in range(0, len(data)):
            if project_key_only[i] == data[j]['project_key']:
                temp1.append([data[j]['project_name'], data[j]['name'], data[j]['enddate']])
        temp.setdefault(project_key_only[i],temp1)
    
    
    #temp에 저장된 data를 월별로 final에 저장
    final = []
    for i in range(0, len(project_key_only)):
        first_temp = ''
        second_temp = ''
        third_temp = ''
        fourth_temp = ''
        fifth_temp =''
        sixth_temp = ''
        seventh_temp = ''
        eightth_temp = ''
        nineth_temp = ''
        tenth_temp = ''
        eleventh_temp = ''
        for j in range(0, len(temp[project_key_only[i]])):
            if temp[project_key_only[i]][j][2][:-3] == (day - relativedelta(months = 3)).strftime('%Y-%m'):
                first_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day - relativedelta(months = 2)).strftime('%Y-%m'):
                second_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day - relativedelta(months = 1)).strftime('%Y-%m'):
                third_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day.strftime('%Y-%m')):
                fourth_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day + relativedelta(months = 1)).strftime('%Y-%m'):
                fifth_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day + relativedelta(months = 2)).strftime('%Y-%m'):
                sixth_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day + relativedelta(months = 3)).strftime('%Y-%m'):
                seventh_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day + relativedelta(months = 4)).strftime('%Y-%m'):
                eightth_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day + relativedelta(months = 5)).strftime('%Y-%m'):
                nineth_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day + relativedelta(months = 6)).strftime('%Y-%m'):
                tenth_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
            if temp[project_key_only[i]][j][2][:-3] == (day + relativedelta(months = 7)).strftime('%Y-%m'):
                eleventh_temp += str(temp[project_key_only[i]][j][1]) + ' (' + str(temp[project_key_only[i]][j][2][8:]) + '일)' + '<br>'
        final.append({ 
                        "project_key": project_key_only[i], 
                        "project_name1": temp[project_key_only[i]][j][0],
                        "type": "TCS",
                        "1st": first_temp[:-4], 
                        "2st":second_temp[:-4], 
                        "3st": third_temp[:-4], 
                        "4st": fourth_temp[:-4], 
                        "5st": fifth_temp[:-4], 
                        "6st": sixth_temp[:-4], 
                        "7st": seventh_temp[:-4],
                        "8st": eightth_temp[:-4],
                        "9st": nineth_temp[:-4],
                        "10st": tenth_temp[:-4],
                        "11st": eleventh_temp[:-4]
                        })
        
    
    #고객사 프로젝트 리스트 연결, 검색
    col = mongo.db.version_list_customer
    c_data = list(col.find({}, {"_id":0}))
    
    for i in range(0, len(c_data)):
        if c_data[i]['project_name1'] == '':
            c_data[i]['project_name1'] = c_data[i]['project_name2']
    
    c_data = sorted(c_data, reverse = False, key = lambda x:(x['enddate']))
    
    
    #고객사 프로젝트 DB에서 중복을 제거한 고객사 프로젝트 리스트를 c_project_name에 저장
    c_project_name = []
    for i in range(0, len(c_data)):
        c_project_name.append(c_data[i]['project_name2'])
    c_project_name = list(set(c_project_name))
    
    #c_data를 dic 형식으로 변경하여 c_data_dic에 저장
    c_data_dic = {}
    for i in range(0, len(c_project_name)):
        c_temp = []
        for j in range(0, len(c_data)):
            if c_data[j]['project_name2'] == c_project_name[i]:
                c_temp.append([c_data[j]['project_name1'], c_data[j]['name'], c_data[j]['startdate'], c_data[j]['enddate']])
        c_data_dic.setdefault(c_project_name[i], c_temp)
    

    c_final = []
    for i in range(0, len(c_project_name)):
        first_temp = ''
        second_temp = ''
        third_temp = ''
        fourth_temp = ''
        fifth_temp =''
        sixth_temp = ''
        seventh_temp = ''
        eightth_temp = ''
        nineth_temp = ''
        tenth_temp = ''
        eleventh_temp = ''
        project_name = ''
        for j in range(0, len(c_data_dic[c_project_name[i]])):
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day - relativedelta(months = 3)).strftime('%Y-%m'):
                first_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day - relativedelta(months = 2)).strftime('%Y-%m'):
                second_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day - relativedelta(months = 1)).strftime('%Y-%m'):
                third_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day.strftime('%Y-%m')):
                fourth_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day + relativedelta(months = 1)).strftime('%Y-%m'):
                fifth_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day + relativedelta(months = 2)).strftime('%Y-%m'):
                sixth_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day + relativedelta(months = 3)).strftime('%Y-%m'):
                seventh_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day + relativedelta(months = 4)).strftime('%Y-%m'):
                eightth_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day + relativedelta(months = 5)).strftime('%Y-%m'):
                nineth_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day + relativedelta(months = 6)).strftime('%Y-%m'):
                tenth_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            if c_data_dic[c_project_name[i]][j][3][:-3] == (day + relativedelta(months = 7)).strftime('%Y-%m'):
                eleventh_temp += str(c_data_dic[c_project_name[i]][j][1]) + ' (' + str(c_data_dic[c_project_name[i]][j][3][8:]) + '일)' + '<br>'
            project_name = c_data_dic[c_project_name[i]][j][0]
        c_final.append({
                        "project_key": '',
                        "project_name1": project_name,
                        "type": c_project_name[i], 
                        "1st": first_temp[:-4], 
                        "2st":second_temp[:-4], 
                        "3st": third_temp[:-4], 
                        "4st": fourth_temp[:-4], 
                        "5st": fifth_temp[:-4], 
                        "6st": sixth_temp[:-4], 
                        "7st": seventh_temp[:-4],
                        "8st": eightth_temp[:-4],
                        "9st": nineth_temp[:-4],
                        "10st": tenth_temp[:-4],
                        "11st": eleventh_temp[:-4]
                        })
    
    result_final = final + c_final
    
    result_final = sorted(result_final, reverse = True, key = lambda x:(x['project_name1']))
    
    col = mongo.db.project_schedule_list
    col.delete_many({})
    for i in range(0, len(result_final)):
        col.insert_one({
                    'project_key': result_final[i]['project_key'],
                    'project_name': result_final[i]['project_name1'],
                    'type' : result_final[i]['type'],
                    '1st': result_final[i]['1st'],
                    '2st': result_final[i]['2st'],
                    '3st': result_final[i]['3st'],
                    '4st': result_final[i]['4st'],
                    '5st': result_final[i]['5st'],
                    '6st': result_final[i]['6st'],
                    '7st': result_final[i]['7st'],
                    '8st': result_final[i]['8st'],
                    '9st': result_final[i]['9st'],
                    '10st': result_final[i]['10st'],
                    '11st': result_final[i]['11st']
                })
    
    
    #project_schedule_list collection에 등록되어 있는 Document를 _id 빼고 검색
    data = list(col.find({},{'_id':0}))
    
    td = []
    #data를 리스트 형식으로 변한해서 td에 집어 넣는 구문
    for i in range(0, len(data)):
        if data[i]['type'] == "TCS":
            td.append(['<td class="first td1" width="200" style=word-break:break-all"><a href="https://tcs.telechips.com:8443/projects/' + data[i]['project_key'] + '?selectedItem=com.atlassian.jira.jira-projects-plugin%3Arelease-page&status=no-filter"><font color="white" size="2">' + data[i]['project_name'] + '</font></a></td>', \
                       data[i]['type'], data[i]['1st'], data[i]['2st'], data[i]['3st'], data[i]['4st'], data[i]['5st'], data[i]['6st'], data[i]['7st'], data[i]['8st'], data[i]['9st'], data[i]['10st'], data[i]['11st']])
        else:
            td.append([data[i]['project_name'], data[i]['type'], data[i]['1st'], data[i]['2st'], data[i]['3st'], data[i]['4st'], data[i]['5st'], data[i]['6st'], data[i]['7st'], data[i]['8st'], data[i]['9st'], data[i]['10st'], data[i]['11st']])

    return render_template("project_schedule.html", th=th, td=td)
