FROM ollama/ollama
COPY ollama/pull-llama3.sh /usr/local/bin/pull-llama3.sh
RUN chmod +x /usr/local/bin/pull-llama3.sh

WORKDIR /root
ENTRYPOINT [ "/usr/local/bin/pull-llama3.sh" ]