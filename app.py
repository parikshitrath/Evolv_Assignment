# first run this app so that the table with required rows and column is made 
from flask import Flask
from flask import request
from flask_restful import reqparse
import sqlite3


app = Flask(__name__)

@app.route('/')
def root():
    try:
        # Connect to db
        db = sqlite3.connect('user.db')  
        cursor = db.cursor()
        
        # Create Table user
        cursor.execute('CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,author_name TEXT, blog_title TEXT , blog_content TEXT)')
        
        # Close db connection
        db.close()
        
        # Connect to db
        db = sqlite3.connect('comnt1.db')
        cursor = db.cursor()

        # Create Table comment
        cursor.execute('CREATE TABLE comnt1(id INTEGER PRIMARY KEY AUTOINCREMENT , blog_id TEXT , comment TEXT)')

        # Close db connection
        db.close()

        # Connect to db
        db = sqlite3.connect('comnt2.db')
        cursor = db.cursor()

        # Create Table comment
        cursor.execute('CREATE TABLE comnt2(id INTEGER PRIMARY KEY AUTOINCREMENT, comment_id , comment TEXT)')

        # Close db connection
        db.close()

        return "Tables Created"
    except:
        return "Tables Already Exists"

parser = reqparse.RequestParser()

@app.route('/add_blog' , methods=['POST'])
def add_blog():
    try:
        # Connect to db
        db = sqlite3.connect('user.db')
        cursor = db.cursor()

        # Get requested arguments
        try:
            author_name = request.args.get('author_name')
            blog_title = request.args.get('blog_title')
            blog_content = request.args.get('blog_content')
        except:
            return "Enter All 3 Arguments"

        # Using Parser to Return Data in Dictionary Form
        parser.add_argument("author_name")
        parser.add_argument("blog_title")
        parser.add_argument("blog_content")
        args = parser.parse_args()

        # Insert Data Into db
        cursor.execute('INSERT INTO user(author_name , blog_title , blog_content) VALUES("%s", "%s" , "%s")' % (author_name , blog_title , blog_content))
        db.commit()

        # Close db Connection
        db.close()

        return args
    except:
        return "No user table exists"

#By default methods=['GET']
@app.route('/display_blog' , methods=['GET'])
def display_blog():
    try:
        # Connect to db
        db = sqlite3.connect('user.db')
        cursor = db.cursor()

        # Get data from db
        cursor.execute('SELECT * FROM user')
        data = cursor.fetchall()

        # Close db connection
        db.close()

        return str(data)
    except:
        return "No tables for comments on blog created"

#By default methods=['GET']
@app.route('/display_blog_by_id/<int:id>' , methods=['GET'])
def display_blog_by_id(id):
    try:
        # Connect to db
        db = sqlite3.connect('user.db')
        cursor = db.cursor()

        # Get data from db
        try:
            cursor.execute('SELECT * FROM user WHERE id = "%s"' %id)
            data = cursor.fetchall()
            if data == []:
                error
        except:
            return "No data with id '%s' exists" %id

        # Close db connection
        db.close()

        return str(data)
    except:
        return "Table dosen't exists"

@app.route('/update_blog/<int:id>' , methods=['PUT'])
def update_blog(id):
    try:
        # Connect to db
        db = sqlite3.connect('user.db')  
        cursor = db.cursor()
        
        # Get requested arguments
        try:
            author_name = request.args.get('author_name')
            blog_title = request.args.get('blog_title')
            blog_content = request.args.get('blog_content')
        except:
            return "Enter All 3 Arguments"

        # Using Parser to Return Data in Dictionary Form
        parser.add_argument("author_name")
        parser.add_argument("blog_title")
        parser.add_argument("blog_content")
        args = parser.parse_args()  
        
        # Update data in db
        cursor.execute('UPDATE user SET author_name="%s", blog_title="%s" , blog_content="%s" WHERE id=%s' % (author_name , blog_title , blog_content , id))
        db.commit()
        
        # Close db connection
        db.close()

        return args
    except:
        return "table dosen't exists"

@app.route('/delete_blog/<int:idx>' , methods=['DELETE'])
def delete(idx):
    try:
        # Connect to db
        db = sqlite3.connect('user.db')  
        cursor = db.cursor()
        
        # Update data in db
        cursor.execute('DELETE FROM user WHERE id = "%s" ' % idx)
        cursor.execute('UPDATE user SET id = id - 1 WHERE id > "%s" ' % (idx))
        db.commit()
        
        # Close db connection
        db.close()
        return 'Deleted Blog With id: %d' %idx 
    except:
        return "TAble Dosen't Exists"

@app.route('/post_comment/<int:id>' , methods=['POST'])
def post_comment(id):
    try:
        # Connect to db
        db = sqlite3.connect('comnt1.db')
        cursor = db.cursor()

        # Get requested arguments
        # blog_id = request.args.get('blog_id')
        try:
            comment = request.args.get('comment')
        except:
            return "Enter an Comment"

        # Insert Data Into db
        cursor.execute('INSERT INTO comnt1(blog_id , comment) VALUES("%s" , "%s")' %(id , comment))
        db.commit()

        # Close db Connection
        db.close()

        return " ['%s'] comment added to blog with id : '%s' "  %(comment , id)
    except:
        return "Table Dosen't Exists"

@app.route('/get_comment/<int:id>' , methods=['GET'])
def get_comment(id):
    try:
        # Connect to db
        db = sqlite3.connect('comnt1.db')
        cursor = db.cursor()

        # Get data from db
        try:
            cursor.execute('SELECT * FROM comnt1 WHERE blog_id = "%s" ' %id)
            data = cursor.fetchall()
            if data == []:
                error 
        except:
            return "No Comment on blog with id '%s'" %id    

        # Close db connection
        db.close()

        return "[" + str(data)[10:-2] + "] is the comment on blog with id '%s'" %id 
    except:
        return "Table Dosen't exists"

@app.route('/post_comment_on_comment/<int:id>' , methods=['POST'])
def post_comment_on_comment(id):
    try:
        # Connect to db
        db = sqlite3.connect('comnt2.db')
        cursor = db.cursor()

        # Get requested arguments
        # comment_id = request.args.get('comment_id')
        comment = request.args.get('comment')

        # Insert Data Into db
        cursor.execute('INSERT INTO comnt2(comment_id , comment) VALUES("%s" , "%s")' %(id , comment))
        db.commit()

        # Close db Connection
        db.close()

        return " ['%s'] comment added to comment with id : '%s' "  %(comment , id)
    except:
        return "Table Dosen't Exists"

@app.route('/get_comment_on_a_comment/<int:id>' , methods=['GET'])
def get_comment_on_a_comment(id):
    # Connect to db
    try:
        db = sqlite3.connect('comnt2.db')
        cursor = db.cursor()

        # Get data from db
        cursor.execute('SELECT * FROM comnt2 WHERE comment_id = "%s" ' %id)
        data = cursor.fetchall()
        try:
            if data == [] :
                error
        except:
            return "No Comments on comment with id '%s'" %id

        # Close db connection
        db.close()

        return "Comments on comment '%s' : " %id + str(data)[10:-2] 
    except:
        return "Table Dosen't Exists"



if __name__ == '__main__':
    app.run(debug=True)