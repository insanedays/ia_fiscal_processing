## Ponto de Melhoria: Normalização da Tabela de Notas Fiscais

### Contexto atual

Atualmente, a tabela de notas fiscais (`NFHeader`) foi estruturada de forma desnormalizada, contendo varias informações da nota, incluindo os dados do emitente, destinatário.

Essa abordagem facilita o processamento inicial, mas apresenta limitações importantes para manutenção e escalabilidade.

---

### Limitações identificadas

- **Redundância de dados:** emitentes e destinatários se repetem em várias notas.
- **Manutenção dificultada:** atualizações cadastrais exigem alterações repetidas.
- **Armazenamento ineficiente:** dados textuais longos são duplicados.
- **Escalabilidade limitada:** itens da nota precisam ser extraídos e tratados separadamente para análises detalhadas.

---

### Proposta de melhoria

Estruturar a base em entidades normalizadas, separando claramente:

- Emitente
- Destinatário
- NFHeader (nota fiscal)
- NFItens (itens da nota)

#### Tabela: `Emitente`

| Campo                      | Tipo sugerido |
|---------------------------|---------------|
| cnpj (PK)                 | VARCHAR       |
| razao_social_emitente     | TEXT          |
| inscricao_estadual_emitente | VARCHAR     |
| uf_emitente               | CHAR(2)       |
| municipio_emitente        | TEXT          |

#### Tabela: `Destinatario`

| Campo                      | Tipo sugerido |
|---------------------------|---------------|
| cnpj (PK)                 | VARCHAR       |
| nome_destinatario         | TEXT          |
| uf_destinatario           | CHAR(2)       |
| indicador_ie_destinatario | VARCHAR       |
| destino_da_operacao       | VARCHAR       |
| consumidor_final          | BOOLEAN       |
| presenca_do_comprador     | VARCHAR       |

#### Tabela: `NFHeader`

| Campo                          | Tipo sugerido     | Comentário                           |
|-------------------------------|-------------------|--------------------------------------|
| chave_de_acesso (PK)          | VARCHAR           | Identificador único da NF            |
| modelo                        | VARCHAR           |                                      |
| serie                         | VARCHAR           |                                      |
| numero                        | VARCHAR           |                                      |
| natureza_da_operacao          | TEXT              |                                      |
| data_emissao                  | DATE              |                                      |
| evento_mais_recente           | TEXT              |                                      |
| data_hora_evento_mais_recente | TIMESTAMP         |                                      |
| valor_nota_fiscal             | DECIMAL(12,2)     |                                      |
| id_emitente                   | VARCHAR (FK)      | → `Emitente(cnpj)`                   |
| id_destinatario               | VARCHAR (FK)      | → `Destinatario(cnpj)`               |

#### Tabela: `NFItens`

| Campo                         | Tipo sugerido     | Comentário                            |
|------------------------------|-------------------|----------------------------------------|
| chave_de_acesso (FK)         | VARCHAR           | → `NFHeader(chave_de_acesso)`         |
| numero_produto               | INT               | Sequencial do item na nota            |
| descricao_do_produto_servico| TEXT              |                                        |
| codigo_ncm_sh                | INT               | Código NCM do produto                 |
| ncm_sh_tipo_de_produto       | TEXT              | Descrição resumida do tipo de produto |
| cfop                         | INT               | Código Fiscal de Operação             |
| quantidade                   | FLOAT             | Quantidade vendida                    |
| unidade                      | VARCHAR           | Unidade de medida (ex: KG, UN)        |
| valor_unitario               | DECIMAL(12,4)     | Preço unitário                        |
| valor_total                  | DECIMAL(12,2)     | Total = quantidade × valor_unitário   |

---

### Justificativa

- Permite consultas por produto, CFOP, NCM etc.
- Viabiliza análises detalhadas de vendas por item.
- Organiza o modelo conforme boas práticas de bancos relacionais.
- Reduz duplicação e melhora performance de leitura.

---

### Observação

A estrutura normalizada será considerada em versões futuras do banco, conforme a evolução da aplicação e a necessidade de garantir escalabilidade, performance e integração com outros sistemas de análise fiscal.
