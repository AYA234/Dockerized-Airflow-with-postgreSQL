
# Use an official Python runtime as a parent image 
FROM python:3.9-slim-buster
# Set the working directory in the container to /app 
WORKDIR /app
# Copy the current directory contents into the container at /app 
COPY . /app


#The next 3 lines are for the NetFree filter:Copy the ssl netfree sertificate and update in the environment.
COPY ./netfree-ca-bundle-curl.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/netfree-ca-bundle-curl.crt

# Install any needed packages specified in requirements.txt 
RUN pip install -r requirements.txt --no-cache-dir 

# Make port 8050 available to the world outside this container 
EXPOSE 8050 

# Run process_data.py when the container launches 
CMD ["python3", "./my_dash.py"]

