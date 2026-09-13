# Testes e verificação

[← Voltar ao README](../README.md)

## Executar a suíte

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m unittest -q
```

`pytest` executa toda a suíte. `unittest` executa apenas os testes de
`tests/test_dijkstra.py`; não substitui a verificação dos recursos adicionais.

## Análise estática e formatação

Para verificar erros básicos e a formatação sem um arquivo de configuração:

```bash
ruff check --isolated --select E4,E7,E9,F .
ruff format --isolated --check .
```

## Cobertura dos testes

Os testes abrangem casos normais e limites, formatos, heurísticas, terminal,
gráficos e relatórios. Em grafos aleatórios, as distâncias são conferidas
contra Bellman–Ford do NetworkX, que não é usado para resolver as consultas
na implementação entregue.

## Próximos tópicos

- [Arquitetura, organização e SOLID](arquitetura.md)
- [Uso da linha de comando](uso.md)
