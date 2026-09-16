# A grpc4bmi server for the SoilGrids Data Component.
FROM csdms/grpc4bmi:0.3.0

LABEL org.opencontainers.image.authors="Mark Piper <mark.piper@colorado.edu>"
LABEL org.opencontainers.image.source="https://github.com/csdms/soilgrids-grpc4bmi"
LABEL org.opencontainers.image.url="https://hub.docker.com/r/csdms/soilgrids-grpc4bmi"
LABEL org.opencontainers.image.vendor="CSDMS"

RUN pip install soilgrids grpc4bmi && \
    pip cache purge

WORKDIR /opt
ENV BMI_PORT=55555
ENTRYPOINT ["run-bmi-server", "--name", "soilgrids.BmiSoilGrids"]
EXPOSE ${BMI_PORT}
