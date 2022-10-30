from flask import Flask, render_template, jsonify, Response, request
import json
import datetime


app = Flask(__name__)
TEMPLATES_AUTO_RELOAD = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

def parse_date(datestr):
    # datetime.datetime.strptime(datestr, '%a %b %m %H:%M:%S %z %Y') "%Y-%m-%dT%H:%M:%SZ"
    return datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%SZ") 

@app.route('/')
def index_view():
    username = request.args.get('username')
    user_str = str(username)
    print("given username is "+str(user_str))
    #first lets check if the given username is there

    with open('./users.json', 'r') as f:
        
        users = f.read();
        #print(dict(users))
        jsonUsers = json.loads(users)
        print(type(jsonUsers))

        if user_str in jsonUsers:
            print("present")
            with open('./posts.json', 'r') as p:
                posts_json = json.loads(p.read())
                #posts = json.loads(users)
                user_tweets = posts_json[user_str]
                print(posts_json[user_str])
                #lets order the posts now
                a = sorted([2,3,1,2])
                orderPosts = sorted(user_tweets , key=lambda d: parse_date(d['time'] ))

                
            
            return render_template('index.html', username = username,posts=orderPosts)
        else :
            print("nah")
            return render_template('index.html', username = False) 
        
        


    return render_template('index.html', username = username)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()

    
    return Response(posts, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='127.0.0.1')