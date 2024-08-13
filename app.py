from flask import Flask, render_template, jsonify, send_file
import boto3
import io

app = Flask(__name__)

# Initialize S3 client for local stack
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',  # Local stack endpoint
    aws_access_key_id='test',  # Use your credentials here
    aws_secret_access_key='test'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buckets')
def list_buckets():
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return jsonify(buckets)

@app.route('/buckets/<bucket_name>/keys')
def list_keys(bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    keys = [obj['Key'] for obj in response.get('Contents', [])]
    return jsonify(keys)

@app.route('/buckets/<bucket_name>/keys/<key_name>/download')
def download_file(bucket_name, key_name):
    response = s3_client.get_object(Bucket=bucket_name, Key=key_name)
    return send_file(
        io.BytesIO(response['Body'].read()),
        attachment_filename=key_name,
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
