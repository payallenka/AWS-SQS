// Replace 'YOUR_ACCESS_KEY_ID' and 'YOUR_SECRET_ACCESS_KEY' with your actual AWS credentials
const accessKeyId = 'AKIA5FTZCPHEM6Z5BLVI';
const secretAccessKey = 'tQHNVgC0dATjKWCzHlZaDHg5Aoa/SYDDHzD8P1sO';

// Replace 'YOUR_BUCKET_NAME' with your actual bucket name
const bucketName = 'django-static-1335';

// Replace 'us-west-2' with your actual bucket region
const bucketRegion = 'us-east-1';

// Initialize AWS SDK
AWS.config.update({
    credentials: new AWS.Credentials(accessKeyId, secretAccessKey),
    region: bucketRegion
});

const s3 = new AWS.S3();

function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    const params = {
        Bucket: bucketName,
        Key: file.name,
        Body: file,
        ACL: 'public-read' // Adjust permissions as needed
    };

    s3.upload(params, (err, data) => {
        if (err) {
            console.error('Error uploading file:', err);
        } else {
            console.log('File uploaded successfully:', data.Location);
            alert('File uploaded successfully!');
        }
    });
}
