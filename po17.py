from flask import Flask, render_template, redirect, request, session
import pg

app = Flask('phonebook-16')
db = pg.DB(dbname='student_db')
app.secret_key = "check"

###### HOME #####
@app.route('/')
def home():
    return render_template(
        'layout.html',
        title = 'Welcome to the home'
    )

 #### Jump to the add student page ######
@app.route('/add_student')
def add_student():
    return render_template(
        'add_student.html',
        title = 'Add student'
    )

@app.route('/add_the_student', methods=['POST'])
def add_the_student():
    name = request.form.get('name')
    website = request.form.get('website')
    git_user = request.form.get('git_user')
    db.insert(
        'student',
        name = name,
        website = website,
        git_user = git_user
    )
    return redirect('/all_student')

##### Jump to the all the student page ####
@app.route('/all_student')
def all_students_page():
    student_list = db.query('select * from student').namedresult()
    return render_template(
        'all_student.html',
        title = 'All students',
        student_list = student_list
    )

#### The update form page #######
@app.route('/update_student')
def update_student():
    id = request.args.get('id')
    student_list = db.query("select * from student where id = %s" % id).namedresult()[0]
    return render_template(
        'update_student.html',
        title = 'Update form',
        student_list = student_list,
    )

#### Submit the Update Infomation #####
@app.route('/update_the_student', methods=['POST'])
def update_the_student():
    name = request.form.get('name')
    website = request.form.get('website')
    git_user = request.form.get('git_user')
    db.update(
        'student',
            {
                'id' : id,
                'name' : name,
                'website' : website,
                'git_user' : git_user
            }
    )
    return redirect('/')

##### Delete ########
@app.route('/delete_student')
def delete_student():
    id = request.args.get('id')
    student_list = db.query("select * from student where id = %s " % id).namedresult()[0]
    db.delete(
        'student', {
            'id' : id
            }
    )
    return redirect('/')


#### CREATE A ACCOUNT ####
@app.route('/new_account')
def new_account():
    return render_template(
        'create_account.html',
        title = 'Create account'
    )

@app.route('/create_account', methods=['POST'])
def create_account():
    user_name = request.form.get('name')
    password = request.form.get('password')
    db.insert(
        'account',{
            'user_name': user_name,
            'password': password
        }
    )
    return redirect('/')

### LOG IN TO USER PAGE ####
@app.route('/login')
def login():
    return render_template(
        'user_login.html',
        title = 'Log in page'
    )

@app.route('/user_login', methods =['POST'])
def user_login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    query = db.query("select * from account where user_name = '%s'" % user_name).namedresult()
    if len(query) > 0:
        account_list_first = query[0]
        if account_list_first.password == password:
            session['user_name'] = user_name
            return render_template(
                'personal_page.html'
                )
        else:
            return redirect('/')
    else:
        return redirect('/')






if __name__ == '__main__':
    app.run(debug=True)
