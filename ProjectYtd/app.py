try:

    from flask import Flask

    from flask import redirect, url_for, request, render_template, send_file
    from io import BytesIO

    from flask_wtf.file import FileField
    from wtforms import SubmitField
    from flask_wtf import Form
    import sqlite3
    print("All Modules Loaded .... ")
except:
    print (" Some Module are missing ...... ")


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


@app.route('/', methods=["GET", "POST"])
def index():

    form = UploadForm()
    if request.method == "POST":

        if form.validate_on_submit():
            file_name = form.file.data
            database(name=file_name.filename, data=file_name.read() )
            return render_template("home.html", form=form)

    return render_template("home.html", form=form)


@app.route('/download', methods=["GET", "POST"])
def download():

    form = UploadForm()

    if request.method == "POST":

        conn= sqlite3.connect("YTD.db")
        cursor = conn.cursor()
        print("IN DATABASE FUNCTION ")
        c = cursor.execute(""" SELECT * FROM  my_table """)

        for x in c.fetchall():
            name_v=x[0]
            data_v=x[1]
            break

        conn.commit()
        cursor.close()
        conn.close()

        return send_file(BytesIO(data_v), attachment_filename='flask.pdf', as_attachment=True)


    return render_template("home.html", form=form)




class UploadForm(Form):
    file = FileField()
    submit = SubmitField("submit")
    download = SubmitField("download")

def database(name, data):
    conn= sqlite3.connect("YTD.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_table (name TEXT,data BLOP) """)
    cursor.execute("""INSERT INTO my_table (name, data) VALUES (?,?) """,(name,data))

    conn.commit()
    cursor.close()
    conn.close()



def query():
        conn= sqlite3.connect("YTD.db")
        cursor = conn.cursor()
        print("IN DATABASE FUNCTION ")
        c = cursor.execute(""" SELECT * FROM  my_table """)

        for x in c.fetchall():
            name_v=x[0]
            data_v=x[1]
            break

        conn.commit()
        cursor.close()
        conn.close()

        return send_file(BytesIO(data_v), attachment_filename='flask.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
