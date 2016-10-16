from flask import Flask, render_template, redirect, request
import pg

app = Flask('phonebook-16')
db = pg.DB(dbname='student_db')

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


if __name__ == '__main__':
    app.run(debug=True)
