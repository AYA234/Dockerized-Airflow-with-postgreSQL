FROM puckel/docker-airflow:latest

# --- NETFREE CERT INTSALL ---
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh
RUN cat  /home/netfree-unix-ca.sh | sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
# --- END NETFREE CERT INTSALL ---


#The next 3 lines are for the NetFree filter:Copy the ssl netfree sertificate and update in the environment.
USER root
COPY ./netfree-ca-bundle-curl.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/netfree-ca-bundle-curl.crt
#End

# Copy the requirements file to the Docker image and install packages
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir --trusted-host pypi.python.org

# Install additional packages
RUN pip install dash pandas --no-cache-dir --trusted-host pypi.python.org

# Expose the port for the webserver
EXPOSE 8082