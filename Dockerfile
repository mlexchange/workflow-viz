FROM python:3.11

# Create and set working directory
WORKDIR /app

# Install Python dependencies
RUN python -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remainder of the code into the image
COPY . ./

EXPOSE 8095
EXPOSE 8888

CMD ["python", "app.py"]