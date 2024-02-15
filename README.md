# transcriber_backend-using-chatGpt-

I created a Docker application which utilizes the chatGpt api and to transcribe voice recordings to text.At the moment it can only process mp3 files.For voice recordings over 25mb, they have to be split into 5min components before using the chatGpt api to transcribe.I am doing this for recordings that are less than 25mb also.

The aim is to run this docker image in AWS Lambda.

Pushing from local to aws ecr:

1)aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 997329144140.dkr.ecr.ap-southeast-1.amazonaws.com
2)docker tag {image_id} 997329144140.dkr.ecr.ap-southeast-1.amazonaws.com/transcriber-app:{image_id}
3)docker push 997329144140.dkr.ecr.ap-southeast-1.amazonaws.com/transcriber-app:{image_id}

Unfortunately the lambda hangs halfway without showing any error message.But all the dependencies are satisfied.


