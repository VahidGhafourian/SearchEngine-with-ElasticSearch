from flask import Flask, request, make_response, render_template, redirect, url_for
from flask_restful import Api, Resource, reqparse
from jinja2 import TemplateNotFound
from CreateSpellCorrectionIndex.lib.Query import get, Farsi_test, make_it_ok
from elasticsearch import Elasticsearch
import requests as req
import webbrowser

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}

app = Flask(__name__, template_folder="templates", static_folder="templates")
api = Api(app)
Db = Elasticsearch("localhost:9200")

loginReqParser = reqparse.RequestParser()
loginReqParser.add_argument("username", type=str, required=True, help="username not sent!")
loginReqParser.add_argument("password", type=str, required=True, help="password not sent!")

postDocParser = reqparse.RequestParser()
postDocParser.add_argument("id", type=int, help="id not sent!")
postDocParser.add_argument("author_name", type=str, help="author name not sent!")
postDocParser.add_argument("topic", type=str, help="topic not sent!")
postDocParser.add_argument("title", type=str, help="title not sent!")
postDocParser.add_argument("tags", type=str, help="tags not sent!")
postDocParser.add_argument("likes", type=str, help="likes not sent!")
postDocParser.add_argument("body", type=str, help="body not sent!")
postDocParser.add_argument("_DELETE", type=str, help="delete method")
postDocParser.add_argument("_PUT", type=str, help="put method")

isLoggedIn = False


# handle not supported URIs
@app.errorhandler(404)
def not_found(error):
    return make_response(render_template("notfound.html"), 404)


class IndexHandler(Resource):
    def get(self):
        try:
            index = render_template("index.html"), 200
            return make_response(index)
        except TemplateNotFound:
            # file not found
            return make_response(render_template("notfound.html"), 404)


class LoginHandler(Resource):
    def get(self):
        try:
            index = render_template("login.html"), 200
            return make_response(index)
        except TemplateNotFound:
            # file not found
            return make_response(render_template("notfound.html"), 404)

    def post(self):
        global isLoggedIn
        params = loginReqParser.parse_args()
        if "username" not in params or "password" not in params:
            return make_response(render_template("badrequest.html"), 400)

        username = params["username"]
        password = params["password"]
        try:
            if username == password == "admin":
                isLoggedIn = True
                # managementhandler is our class, which is handling /admin
                return redirect(url_for("managementhandler"), 302)
            else:
                return make_response(render_template("login.html"), 401)
        except TemplateNotFound:
            return make_response(render_template("notfound.html"), 404)


class ManagementHandler(Resource):
    def get(self):
        if isLoggedIn:
            return make_response(render_template("management.html"), 200)
        return make_response(render_template("unauthorize.html"), 401)

class ShowHandler(Resource):
    def get(self):
        args = request.args
        if "title" not in args:
            return redirect(url_for("indexhandler"), 302)

        title = args["title"]
        
        resp = req.get("https://virgool.io/api/v1.3/search?q=" + title + "&page=1", headers=headers).json()['posts']
        isfindurl = False
        for post in resp:
            if post['title']== title:
                isfindurl = True
                return redirect(post['post_url'])
        if not isfindurl:
            # get document from DB with title
            search_param = {
                'query': {
                    'match': {
                        'title': title
                    }
                }
            }
            res = Db.search(body=search_param, index="virgool-index")
            doc = res["hits"]["hits"][0]['_source']
            # get  id,author name,topic,title,tags,likes,body and set them in html

            return make_response(
                render_template("showpage.html", author_name=doc['author_name'], docid=doc['id'], doctopic=doc['topic']
                                , doctitle=doc['title'], doclikes=doc['likes'], doctags=doc['tags'], docbody=doc['text']), 200)


class SearchHandler(Resource):
    def get(self):
        args = request.args
        if "q" not in args:
            return make_response(render_template("badrequest.html"), 400)
        else:
            query = args["q"]

        # process query and get 10 results from DB
        search_param = {
            'query': {
                'match': {
                    'text': query
                }
            }
        }
        res = Db.search(body=search_param, index="virgool-index")
        results = res["hits"]["hits"]
        # set search results (document titles (r0,...r9)
        titles = list()
        for item in results:
            titles.append(item['_source']['title'])
            
        is_Farsi = Farsi_test(query)
        if is_Farsi:
            query = make_it_ok(query)
            correction = get(query)
            if str.strip(correction[0])!=query:
                return make_response(
                    render_template("index.html", dym0="Did you mean :", dym=correction[0],
                    n0=("1. " if len(titles) > 0 else ""), r0=(titles[0] if len(titles) > 0 else ""),
                    n1=("2. " if len(titles) > 1 else ""), r1=(titles[1] if len(titles) > 1 else ""),
                    n2=("3. " if len(titles) > 2 else ""), r2=(titles[2] if len(titles) > 2 else ""),
                    n3=("4. " if len(titles) > 3 else ""), r3=(titles[3] if len(titles) > 3 else ""),
                    n4=("5. " if len(titles) > 4 else ""), r4=(titles[4] if len(titles) > 4 else ""),
                    n5=("6. " if len(titles) > 5 else ""), r5=(titles[5] if len(titles) > 5 else ""),
                    n6=("7. " if len(titles) > 6 else ""), r6=(titles[6] if len(titles) > 6 else ""),
                    n7=("8. " if len(titles) > 7 else ""), r7=(titles[7] if len(titles) > 7 else ""),
                    n8=("9. " if len(titles) > 8 else ""), r8=(titles[8] if len(titles) > 8 else ""),
                    n9=("10. " if len(titles) > 9 else ""), r9=(titles[9] if len(titles) > 9 else "")),200)
            else:
                return make_response(
                    render_template("index.html", dym0="", dym=correction[0],
                    n0=("1. " if len(titles) > 0 else ""), r0=(titles[0] if len(titles) > 0 else ""),
                    n1=("2. " if len(titles) > 1 else ""), r1=(titles[1] if len(titles) > 1 else ""),
                    n2=("3. " if len(titles) > 2 else ""), r2=(titles[2] if len(titles) > 2 else ""),
                    n3=("4. " if len(titles) > 3 else ""), r3=(titles[3] if len(titles) > 3 else ""),
                    n4=("5. " if len(titles) > 4 else ""), r4=(titles[4] if len(titles) > 4 else ""),
                    n5=("6. " if len(titles) > 5 else ""), r5=(titles[5] if len(titles) > 5 else ""),
                    n6=("7. " if len(titles) > 6 else ""), r6=(titles[6] if len(titles) > 6 else ""),
                    n7=("8. " if len(titles) > 7 else ""), r7=(titles[7] if len(titles) > 7 else ""),
                    n8=("9. " if len(titles) > 8 else ""), r8=(titles[8] if len(titles) > 8 else ""),
                    n9=("10. " if len(titles) > 9 else ""), r9=(titles[9] if len(titles) > 9 else "")),200)
        else:
            return make_response(
                    render_template("index.html", dym0="", dym=correction[0],
                    n0=("1. " if len(titles) > 0 else ""), r0=(titles[0] if len(titles) > 0 else ""),
                    n1=("2. " if len(titles) > 1 else ""), r1=(titles[1] if len(titles) > 1 else ""),
                    n2=("3. " if len(titles) > 2 else ""), r2=(titles[2] if len(titles) > 2 else ""),
                    n3=("4. " if len(titles) > 3 else ""), r3=(titles[3] if len(titles) > 3 else ""),
                    n4=("5. " if len(titles) > 4 else ""), r4=(titles[4] if len(titles) > 4 else ""),
                    n5=("6. " if len(titles) > 5 else ""), r5=(titles[5] if len(titles) > 5 else ""),
                    n6=("7. " if len(titles) > 6 else ""), r6=(titles[6] if len(titles) > 6 else ""),
                    n7=("8. " if len(titles) > 7 else ""), r7=(titles[7] if len(titles) > 7 else ""),
                    n8=("9. " if len(titles) > 8 else ""), r8=(titles[8] if len(titles) > 8 else ""),
                    n9=("10. " if len(titles) > 9 else ""), r9=(titles[9] if len(titles) > 9 else "")),200)


class AccessHandler(Resource):
    def get(self):
        args = request.args
        withID = True

        if not isLoggedIn:
            return make_response(render_template("unauthorize.html"), 401)

        if "id" not in args and "title" not in args or "id" in args and "title" in args:
            return make_response(render_template("badrequest.html"), 400)
        elif "id" in args and "title" not in args:
            withID = True
            id = args["id"]
        elif "id" not in args and "title" in args:
            withID = False
            title = args["title"]

        # we have id or title

        if withID:
            try :
                res = Db.get(index="virgool-index", id=id)
                doc = res['_source']
                # set author_name,docid,doctopic,doctitle,doclikes,doctags,docbody (return make_response...)
                res = f"found document with id : {id} in database"

                return make_response(render_template(
                "management.html", result=res, author_name=doc['author_name'], docid=doc['id'], doctopic=doc['topic']
                                        , doctitle=doc['title'], doclikes=doc['likes'], doctags=doc['tags'], docbody=doc['text']), 200)
            except:
                res = f"no document with id : {id} in database"

                return make_response(render_template(
                "management.html", result=res, author_name="", docid="", doctopic=""
                                         , doctitle="", doclikes="", doctags="", docbody=""), 404)

        else:
            # get document from DB with title
            search_param = {
                'query': {
                    'match': {
                        'title': title
                    }
                }
            }
            res = Db.search(body=search_param, index="virgool-index")
            doc = res["hits"]["hits"][0]['_source']
            # set author_name,docid,doctopic,doctitle,doclikes,doctags,docbody (return make_response...)

            if doc['title']==title:
                res = f"found document with title : {title} in database"

                return make_response(render_template(
                "management.html", result=res, author_name=doc['author_name'], docid=doc['id'], doctopic=doc['topic']
                                        , doctitle=doc['title'], doclikes=doc['likes'], doctags=doc['tags'], docbody=doc['text']), 200)

            else:
                res = f"no document with title : {title} in database"

                return make_response(render_template(
                "management.html", result=res, author_name="", docid="", doctopic=""
                                        , doctitle="", doclikes="", doctags="", docbody=""), 404)

    def post(self):
        if not isLoggedIn:
            return make_response(render_template("unauthorize.html"), 401)

        params = postDocParser.parse_args()

        if params["_DELETE"] == "DELETE":
            return self.delete()
        elif params["_PUT"] == "PUT":
            return self.put()

        if "title" is None or "id" is None or "body" is None:
            return make_response(render_template("badrequest.html"), 400)

        id = params["id"]
        author_name = params["author_name"]
        topic = params["topic"]
        title = params["title"]
        tags = params["tags"]
        likes = params["likes"]
        body = params["body"]

        # check whether DB contains doc with that id or not (check conflict(select docs from DB with given id))
        try:
            # if DB contains id
            res2 = Db.get(index="virgool-index", id=id)
            res = f"We couldn't add this document to the database. There is a document with id : {id} in our database"
            return make_response(render_template(
            "management.html", result=res, author_name="", docid="", doctopic=""
                                    , doctitle="", doclikes="", doctags="", docbody=""), 409)
        except :
            # if document with given id not found in DB:
#             add document to the DB (id,author_name,topic,title,tags,likes,body)
            d = {'id': id , 'topic': topic, 'author_name': author_name, 'title': title, 'text': body, 'likes': likes, 'tags': tags}
            Db.index(index='virgool-index', id=id, body=d)
        
            res = f"Document with id : {id} successfully added to the database"
            return make_response(render_template(
            "management.html", result=res, author_name="", docid="", doctopic=""
                                    , doctitle="", doclikes="", doctags="", docbody=""), 201)

        

    def delete(self):
        if not isLoggedIn:
            return make_response(render_template("unauthorize.html"), 401)

        params = postDocParser.parse_args()

        if "id" is None:
            return make_response(render_template("badrequest.html"), 400)

        id = params["id"]

        # check whether DB contains a document with that id
        try:
            # if DB contains id
            res2 = Db.get(index="virgool-index", id=id)
            res2 = res2['_source']
          #   delete document in DB
            Db.delete(id=id, index="virgool-index")
            res = f"Document with id : {id} deleted from database"
            return make_response(render_template(
            "management.html", result=res, author_name=res2['author_name'], docid=res2['id'], doctopic=res2['topic']
                                    , doctitle=res2['title'], doclikes=res2['likes'], doctags=res2['tags'], docbody=res2['text']), 200)
        except :
        # if no document with given id found:
            res = f"No document with id : {id} found in database"
            return make_response(render_template(
            "management.html", result=res, author_name="", docid="", doctopic=""
                                    , doctitle="", doclikes="", doctags="", docbody=""), 404)

    def put(self):
        if not isLoggedIn:
            return make_response(render_template("unauthorize.html"), 401)

        params = postDocParser.parse_args()

        if "title" is None or "id" is None or "body" is None:
            return make_response(render_template("badrequest.html"), 400)

        id = params["id"]
        author_name = params["author_name"]
        topic = params["topic"]
        title = params["title"]
        tags = params["tags"]
        likes = params["likes"]
        body = params["body"]

        # check whether DB contains doc with that id
        try:
            # if DB contains id
            res2 = Db.get(index="virgool-index", id=id)
            d = {'id': id , 'topic': topic, 'author_name': author_name, 'title': title, 'text': body, 'likes': likes, 'tags': tags}
            Db.index(index='virgool-index', id=id, body=d)
            res = f"document with id : {id} updated successfully"
            return make_response(render_template(
            "management.html", result=res, author_name=author_name, docid=id, doctopic=topic
                                    , doctitle=title, doclikes=likes, doctags=tags, docbody=body), 200)
        except :
        #   if doc not found in DB:
            res = f"No document with id : {id} in database"
            return make_response(render_template(
            "management.html", result=res, author_name=author_name, docid=id, doctopic=topic
                                    , doctitle=title, doclikes=likes, doctags=tags, docbody=body), 404)


api.add_resource(IndexHandler, "/")
api.add_resource(SearchHandler, "/search")
api.add_resource(LoginHandler, "/login")
api.add_resource(ManagementHandler, "/admin")
api.add_resource(AccessHandler, "/admin/documents")
api.add_resource(ShowHandler, "/show")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
