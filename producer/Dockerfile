
FROM python:3.9


# --- NETFREE CERT INTSALL ---
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
# --- END NETFREE CERT INTSALL ---

# Set the working directory inside the container
WORKDIR /app

# Create the shared_volume directory
RUN mkdir /test
RUN mkdir /shared_volume

# Copy the current directory contents into the container at /app
COPY . /app


#The next 3 lines are for the NetFree filter:Copy the ssl netfree sertificate and update in the environment.
COPY ./netfree-ca-bundle-curl.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/netfree-ca-bundle-curl.crt

# Install required Python packages
RUN pip install pandas --no-cache-dir --trusted-host pypi.python.org 

# Run the producer.py script when the container starts
CMD ["python", "producer.py"]

