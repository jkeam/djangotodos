FROM registry.access.redhat.com/ubi9/python-311@sha256:8a067206cbdbf73a39261f11c028a6fa55369d44b6c08f3d5f4d5194bfad69a5

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
