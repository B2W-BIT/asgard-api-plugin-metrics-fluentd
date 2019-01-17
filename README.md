# Fluentd Metrics

## Changelog

  [Changelog](./CHANGELOG.md)


# Descrição

Plugin para a Asgard API que expõe métricas sobre um cluster de Fluentd.

## Endpoints implementados por esse plugin

* /plugins/<plugin-id>
    Retorna um JSON contendo os campos desse plugin (<plugin-id>) que foram buscados em todos os nós do fluentd.
    Apresentamos os valores individuais, usando o IP do nó com sufixo da chave.
    Exemplo de resposta:
    ```
    GET /plugins/<plugin_id>

    Response:
    {
      "retry_count_<IP>": <N>,
      "buffer_queue_length_<IP>": <N>,
      "buffer_total_queued_size_<IP>: <N>,
      "retry_start_min_<IP>: -<N>,
      "retry_next_min_<IP>: +<N>,
    }
    ```
* /retry_count/<plugin-id>
    Retorna os dados sumarizados para todos os nós do fluentd.
    Os campos numéricos serão somados: `buffer_queue_length`, `buffer_total_queued_size`, `retry_count`. 
    Exemplo de resposta:
    ```
    GET /retry_count/<plugin-id>

    Response:
    {
      "retry_count": each(<IP>).sum(retry_count),
      "buffer_queue_length": each(<IP>).sum(buffer_queue_length),
      "buffer_total_queued_size": each(<IP>).sum(buffer_total_queued_size),
    }
    ```

## Instalação desse plugin em sua Asgard API

Basta colocar o pacote python `asgard-api-plugin-metrics-fluentd` como dependencia do seu deploy da Asgard API.

## Detalhes sobre a interface de plugin da Asgard API

Esse passo a passo está detalhado no repositório da [asgard-api-plugin-metrics-mesos](https://github.com/B2W-BIT/asgard-api-plugin-metrics-mesos)

## Env vars
* Todas as env são lidas pela `asgard-api-sdk`. As que são necessária aqui são 
as que possuem sufixo `_FLUENTD_ADDRESS_<N>`. Mais detalhes na doc da `asgard-api-sdk`.


* HOLLOWMAN_FLUENTD_ADDRESS_N = IP:PORTA

Importante ter o IP e PORTA no endereço do fluentd. Esse código assume que esse endereço é a api
de monitoring do fluentd, então fará o acesso em http://<IP>:<PORTA>/api/plugins.json

## Running tests:

É necessário ter uma cópia da asgard-api, clonada na mesma pasta conde está esse cópdigo.

`$ pipenv install --dev`
`$ pipenv run py.test --cov=./ --cov-report term-missing -v -s`

