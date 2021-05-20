# -*- coding: utf-8 -*-
#from main import *
#from main import app
from main import mongo
from main import login_required
from main import url_for, redirect, flash
from main import abort
from main import ObjectId
from main import datetime
from main import request
from main import render_template
from main import session
from main import math
from flask import Blueprint

blueprint = Blueprint("board", __name__, url_prefix="/board")


@blueprint.route("/view")
@login_required
def board_view():
    idx = request.args.get("idx")
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", -1, type=int)
    keyword = request.args.get("keyword", "", type=str)

    if idx is not None:
        board = mongo.db.board
        #data = board.find_one({"_id": ObjectId(idx)})
        data = board.find_one_and_update({"_id": ObjectId(idx)}, {"$inc": {"view": 1}}, return_document=True)
        if data is not None:
            result = {
                "id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "pubdate": data.get("pubdate"),
                "writer_id": data.get("writer_id", "")
            }
            

            return render_template("view.html", result=result, page=page, search=search, keyword=keyword, title="글 상세보기")
    return abort(400)

@blueprint.route("/write", methods=["GET", "POST"])
@login_required
def board_write():
    if session["id"] is None or session["id"] == "":
        return redirect(url_for("board.member_login"))

    if request.method == "POST":
        #name = request.form.get("name")
        writer_id = session.get("id")
        title = request.form.get("title")
        contents = request.form.get("contents")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        board = mongo.db.board

        post = {
            "writer_id": writer_id,
            "name": session["name"],
            "title": title,
            "contents": contents,
            "view": 0,
            "pubdate": current_utc_time,
        }
        x = board.insert_one(post)
        return redirect(url_for("board.board_view", idx=x.inserted_id))
    else:
        return render_template("write.html", name=session["name"], title="글 작성")


@blueprint.route("/list")
def lists():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    search = request.args.get("search", -1, type=int)
    keyword = request.args.get("keyword", "", type=str)

    query = {}
    search_list = []

    if search == 0:
        search_list.append({"title": {"$regex": keyword}})
    elif search == 1:
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 2:
        search_list.append({"title": {"$regex": keyword}})
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 3:
        search_list.append({"name": {"$regex": keyword}})

    if len(search_list) > 0:
        query = {"$or": search_list}

    board = mongo.db.board
    datas = board.find(query).skip((page-1) * limit).limit(limit)

    tot_count = board.find(query).count()
    last_page_num = math.ceil(tot_count / limit)

    block_size = 5
    block_num = int((page-1) / block_size)
    block_start = int((block_size * block_num) + 1)
    block_last = math.ceil(block_start + (block_size-1))

    
    return render_template(
            "list.html", 
            datas=datas, 
            limit=limit, 
            page=page,
            block_start=block_start,
            block_last=block_last,
            last_page=last_page_num,
            search=search,
            keyword=keyword,
            title="게시판 리스트"
            )

@blueprint.route("/edit/<idx>", methods=["GET", "POST"])
def board_edit(idx):
    if request.method == "GET":
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})
        if data is None:
            flash("해당 게시물이 존재하지 않습니다.")
            return redirect(url_for("board.lists"))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template("edit.html", data=data, title="글 수정")
            else:
                flash("글 수정 권한이 없습니다.")
                return redirect(url_for("board.lists"))
    else:
        title = request.form.get("title")
        contents = request.form.get("contents")
        board = mongo.db.board

        data = board.find_one({"_id": ObjectId(idx)})

        if data.get("writer_id") == session.get("id"):
            board.update_one({"_id": ObjectId(idx)}, {
                "$set": {
                    "title": title,
                    "contents": contents,
                }
            })
            flash("수정되었습니다.")
            return redirect(url_for("board.board_view", idx=idx))
        else:
            flash("글 수정 권한이 없습니다.")
            return redirect(url_for("board.lists"))


@blueprint.route("/delete/<idx>")
def board_delete(idx):
    board = mongo.db.board
    data = board.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        board.delete_one({"_id": ObjectId(idx)})
        flash("삭제 되었습니다.")
    else:
        flash("글 삭제 권한이 없습니다.")
    return redirect(url_for("board.lists"))

