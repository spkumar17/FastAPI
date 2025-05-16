# Use official Python image
FROM python:3.9-slim 


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR src/app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .        
# and then copy the rest of the project files
# first dot is the current directory, second dot is the destination



# Expose port
EXPOSE 8000

# Run FastAPI app using Uvicorn
CMD ["uvicorn", "APP.main:app", "--host", "0.0.0.0", "--port", "8000"]
