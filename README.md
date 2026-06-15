# Dashboard de vendas e engajamento

Painel local construído exclusivamente a partir de `relatorio_final.csv`, a base tratada,
enriquecida e anonimizada. Nenhum arquivo bruto é lido pela aplicação.

## Executar

```powershell
python dashboard.py
```

Abra `http://127.0.0.1:8000` no navegador.
caso não funcione use : http://127.0.0.1:8000/

O painel inclui:

- total de vendas, valor total vendido e ticket médio;
- vendas por período e por UF;
- indicador de engajamento por aluno único e cobertura das métricas;
- filtros por período, curso, UF e feriado;
- envio ao navegador apenas das colunas necessárias, sem CPF, CEP ou identificador da transação.
  A associação de compras do mesmo aluno usa somente um hash derivado no servidor.
