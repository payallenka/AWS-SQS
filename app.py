import os
import boto3
import uuid  # Import the uuid module
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load AWS credentials from environment variables
AWS_ACCESS_KEY_ID = 'AKIA5FTZCPHEIOYSCAS4'
AWS_SECRET_ACCESS_KEY = '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'

# Initialize SQS client
sqs = boto3.client('sqs', region_name='us-east-1', 
                   aws_access_key_id=AWS_ACCESS_KEY_ID, 
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
queue_url = 'https://sqs.us-east-1.amazonaws.com/905418275272/MyQueue.fifo'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_message', methods=['POST'])
def create_message():
    try:
        content = request.json
        message_body = content['message']
        message_group_id = content.get('message_group_id', 'default_group')
        message_deduplication_id = content.get('message_deduplication_id', str(uuid.uuid4()))
        
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageGroupId=message_group_id,
            MessageDeduplicationId=message_deduplication_id
        )
        
        return jsonify({'message_id': response['MessageId']})
    except Exception as e:
        app.logger.error(f"Error creating message: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/read_messages', methods=['GET'])
def read_messages():
    try:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        messages = response.get('Messages', [])
        return jsonify(messages)
    except Exception as e:
        app.logger.error(f"Error reading messages: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
