from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    # Date,
    # Boolean,
    # Text,
    ForeignKey,
    TIMESTAMP,
    Numeric,
    BigInteger
)
from sqlalchemy.orm import relationship,declarative_base

Base = declarative_base()


class NFHeader(Base):
    __tablename__ = "nf_header"

    chave_de_acesso = Column(String(60), primary_key=True)
    modelo = Column(String(80))
    serie = Column(BigInteger)
    numero = Column(BigInteger)
    natureza_da_operacao = Column(String(255))
    data_emissao = Column(TIMESTAMP)
    evento_mais_recente = Column(String(255))
    data_hora_evento_mais_recente = Column(TIMESTAMP)
    cpf_cnpj_emitente = Column(String(14))
    razao_social_emitente = Column(String(255))
    inscricao_estadual_emitente = Column(String(20))
    uf_emitente = Column(String(2))
    municipio_emitente = Column(String(100))
    cnpj_destinatario = Column(String(14))
    nome_destinatario = Column(String(255))
    uf_destinatario = Column(String(2))
    indicador_ie_destinatario = Column(String(80))
    destino_da_operacao = Column(String(80))
    consumidor_final = Column(String(80))
    presenca_do_comprador = Column(String(80))
    valor_nota_fiscal = Column(Float(15, 2))

    itens = relationship("NFItens", back_populates="nf_header", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<NFHeader(chave_de_acesso='{self.chave_de_acesso}', numero={self.numero})>"


class NFItens(Base):
    __tablename__ = "nf_itens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chave_de_acesso = Column(String(60), ForeignKey("nf_header.chave_de_acesso"), nullable=False)
    numero_produto = Column(Integer, nullable=False)
    descricao_do_produto_servico = Column(String(200), nullable=False)
    codigo_ncm_sh = Column(String, nullable=False)
    ncm_sh_tipo_de_produto = Column(String(255), nullable=False)
    cfop = Column(String, nullable=False)
    quantidade = Column(Numeric(15, 2), nullable=False)
    unidade = Column(String(25))
    valor_unitario = Column(Numeric(15, 2))
    valor_total = Column(Numeric(15, 2))

    nf_header = relationship("NFHeader", back_populates="itens")

    def __repr__(self):
        return f"<NFItens(id={self.id}, descricao='{self.descricao}')>"