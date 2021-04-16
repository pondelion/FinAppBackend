FROM public.ecr.aws/lambda/python:3.7

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN git clone --depth 1 https://github.com/pondelion/FinAppBackend.git
RUN cd FinAppBackend && \
    git checkout develop && \
    pipenv install --skip-lock --dev -e .
COPY ./fin_app/config/*  ./FinAppBackend/fin_app/config/
CMD ["app.handler"]
