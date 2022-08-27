from flask import Flask, render_template, url_for, flash, redirect
from forms import SearchForm
import datetime
from data import get_graph_data, getPostsFromPushshift, filterPushshiftData
app = Flask(__name__)


app.config['SECRET_KEY'] = '3c44f33efa8672eb6c1841838378e5290269658c'

searches = [
    {
        'subreddit': 'jujutsushi',
        'term': 'Blog post 1',
        'date_posted': 'May 30, 2022'
    },
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title='home',searches=searches)

@app.route("/about")
def about():
    return render_template('about.html',title ='about')

@app.route("/trends", methods=['GET','POST'])
def trends():
    form = SearchForm()
    #validation?
    if form.validate_on_submit():
        flash('Search', 'success')
        global subreddit, category, num_posts, term_data, after,before,time_seg,segments
        subreddit = form.subreddit.data 
        category = form.category.data 
        num_posts = form.num_posts.data
        term_data = form.term_data.data
        dt_format = "%y,%m,%d"
        after_date =  (form.after.data)
        bf_date = form.before.data
        after = int((datetime.datetime.strptime(after_date.strftime(dt_format), dt_format)).timestamp())
        before = int((datetime.datetime.strptime(bf_date.strftime(dt_format), dt_format)).timestamp())
        time_seg = form.time_seg.data
        segments = form.segments.data
        return redirect(url_for('graph'))
    return render_template('trends.html',title ='trends', form=form)



#add export button as csv 
@app.route("/graph", methods=['GET','POST'])
def graph():
    form = SearchForm()
    data = get_graph_data(subreddit,term_data,after,before,time_seg,segments)
    print(data)
    td = term_data.split()
    text = ','.join(td)
    #text[text.find(td[-1])] = "and"+td[-1]
    
    labeltext = ("Occurance of " + text  + " in r/" + subreddit + " posts")
    print(labeltext)
    #testing
    #a = int(datetime.datetime(2021,4,1).timestamp())
    #b = int(datetime.datetime(2021,4,5).timestamp())
    #print(getPostsFromPushshift('jujutsushi','toji',a,b,'days',1))
    return render_template('graph.html',title ='graph',chart_data = data, term_data =term_data.split(","), labeltext= labeltext)






# @app.route("/register", methods=['GET','POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('home'))

#     return render_template('register.html', title='Register', form=form)

# @app.route("/login", methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash('You have been logged in!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)

if __name__=='__main__':
    #getData2()
    app.run(debug=True)