from flask import Flask, render_template, request, redirect, url_for
import boto3
import os,json

app = Flask(__name__)


USERNAME = 'sandeep'
PASSWORD = 'Sandeep46'

S3_BUCKET_NAME = 'sandeep46'
AWS_ACCESS_KEY_ID = 'AKIA56SSZ7JKEMJJGNEJ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION_NAME = 'us-east-1'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)



@app.route('/')
def index():
    return render_template('login.html')
# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            return render_template('file_share.html')
        else:
            return render_template('login.html', error='Wrong credentials')

    return render_template('login.html', error=None)


@app.route('/file_share', methods=['GET', 'POST'])
def file_share():
    if request.method == 'POST':
       
        email_addresses = request.form.getlist('email')
        file = request.files['file']
        emails=request.form.getlist('email')
        emails=[email for email in emails if email]

       
        s3_filename = file.filename
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, s3_filename, ExtraArgs = { 'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'})

        sunload= {'emails':emails,
                 'filename':file.filename
                }
        lambda_client.invoke(
            FunctionName='sandylambda',
            InvocationType='Event',
            Payload=json.dumps(sunload))

        return redirect(url_for('file_share'))

    return render_template('file_share.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
