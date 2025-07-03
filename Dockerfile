FROM registry.access.redhat.com/ubi9/python-312:9.6-1749631862

# python settings
ENV PYTHONDONTWRITEBYTECODE 1

# Add application sources with correct permissions for OpenShift
USER 0
ADD . .
RUN chown -R 1001:0 ./
USER 1001

# Install the dependencies
RUN pip install -U "pip>=19.3.1" && \
    pip install -r requirements.txt

# Port for app
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
