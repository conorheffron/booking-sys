FROM python:3.13

ARG DEBUG

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=${DEBUG}

# Copy project files
COPY . /

# Set work directory
WORKDIR /

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py test

EXPOSE 8000
# For running our application

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]