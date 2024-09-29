# 1. Base Image
FROM python:3.12-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1 

# 3. Set work directory
WORKDIR /app

# 4. Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy project files
COPY . /app/

# 6. Run migrations and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# 7. Expose port 8000 for the Gunicorn server
EXPOSE 8000

# 8. Start Gunicorn server
CMD ["gunicorn", "jeommechu.wsgi:application", "--bind", "0.0.0.0:8000"]
