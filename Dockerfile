# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the environment variables
ENV DATABASE_URL=mongodb+srv://halleluyaholudele:qVnrzlakAxa8pPON@childimmunisation.rc4alj8.mongodb.net/?retryWrites=true&w=majority&appName=childimmunisation
ENV DEFAULT_DATABASE=childimmunisation
ENV SECRET_KEY=YN_OdvQXnb60g0adPmn2M2VZfHips2gakIvL4ILdcwY
ENV ALGORITHM=HS256
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY app/requirements.txt ./

# Install pipenv and compile dependencies
RUN pip install -r requirements.txt
# Copy the rest of the backend code into the container
COPY app /app

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the app with uvicorn
CMD ["sh", "-c", "cd /app && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
