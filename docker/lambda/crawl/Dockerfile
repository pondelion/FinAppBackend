FROM public.ecr.aws/lambda/python:3.7

RUN yum install -y git
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN git clone https://github.com/pondelion/FinAppBackend.git && \
    cd FinAppBackend && \
    git checkout develop && \
    # pipenv install --skip-lock --dev -e . && \
    # pipenv run pip freeze > requirements.txt && \
    # pipenv lock --keep-outdated --requirements > requirements.txt && \
    pip install -r requirements.txt && \
    pip install -e .
    # pipenv --rm
COPY ./lambda/example_handler.py .
RUN cp FinAppBackend/lambda/crawl/functions/* .
COPY ./fin_app/config/*  ./FinAppBackend/fin_app/config/
CMD ["app.handler"]
