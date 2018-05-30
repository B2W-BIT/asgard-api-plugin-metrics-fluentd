# Fluentd Metrics

## Changelog

 * 0.1.0
    - Implementação inicial

## Env vars
* Todas as env são lidas pela `asgard-api-sdk`. As que são necessária aqui são 
as que possuem sufixo `_FLUENTD_ADDRESS_<N>`. Mais detalhes na doc da `asgard-api-sdk`.


* HOLLOWMAN_FLUENTD_ADDRESS_N = IP:PORTA

Importante ter o IP e PORTA no endereço do fluentd. Esse código assume que esse endereço é a api
de monitoring do fluentd, então fará o acesso em http://<IP>:<PORTA>/api/plugins.json

## Routes:

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


## Running tests:
`$ py.test --cov=fluentdmetrics --cov-report term-missing -v -s`
