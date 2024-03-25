FROM public.ecr.aws/lambda/python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_KEY ''

# Install system dependencies
COPY ffmpeg /usr/local/bin/ffmpeg
COPY ffprobe /usr/local/bin/ffprobe
RUN chmod 777 -R /usr/local/bin/ffmpeg
RUN chmod 777 -R /usr/local/bin/ffprobe

# Copy all into lambda task root
COPY . ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip3 install -r requirements.txt



# Set the CMD to your handler.
CMD ["main.transcribe"]



