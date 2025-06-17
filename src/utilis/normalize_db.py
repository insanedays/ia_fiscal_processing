from sqlalchemy.inspection import inspect
from sqlalchemy.sql.sqltypes import String, Float, BigInteger, Integer, TIMESTAMP, Numeric
import pandas as pd
#columns
import unicodedata


def normalize_col_type_from_model(df: pd.DataFrame, model_class):
    mapper = inspect(model_class)

    for column in mapper.columns:
        col_name = column.name
        col_type = type(column.type)

        if col_name not in df.columns:
            continue  # ignora campos ausentes no DataFrame
        try:
        # Conversão baseada no tipo SQLAlchemy
            if col_type is String:
                df[col_name] = df[col_name].astype(str)
            elif col_type is Numeric:
                df[col_name] = df[col_name].astype(float)
            elif col_type in (Integer, BigInteger):
                df[col_name] = df[col_name].astype("Int64")
            elif col_type is TIMESTAMP:
                df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
        except Exception as e:
            print(f"[WARN] Falha ao converter coluna '{col_name}': {e}")
            raise

    return df

# from sqlalchemy import Numeric, Integer, BigInteger, Float, String, TIMESTAMP

# def normalize_col_type_from_model(df: pd.DataFrame, model_class):
#     mapper = inspect(model_class)

#     for column in mapper.columns:
#         col_name = column.name
#         col_type = column.type

#         if col_name not in df.columns:
#             continue

#         try:
#             print(f"[DEBUG] Coluna: {col_name} | Tipo no DF: {df[col_name].dtype} | Tipo no Modelo: {type(col_type)}")

#             if isinstance(col_type, String):
#                 df[col_name] = df[col_name].astype(str)

#             elif isinstance(col_type, (Integer, BigInteger)):
#                 is_int_compat = df[col_name].dropna().apply(lambda x: float(x).is_integer())
#                 if is_int_compat.all():
#                     df[col_name] = df[col_name].astype('Int64')
#                 else:
#                     print(f"[WARN] Coluna '{col_name}' contém valores não inteiros. Mantendo como float.")
#                     df[col_name] = df[col_name].astype(float)

#             elif isinstance(col_type, (Float, Numeric)):
#                 df[col_name] = df[col_name].astype(float)

#             elif isinstance(col_type, TIMESTAMP):
#                 df[col_name] = pd.to_datetime(df[col_name], errors='coerce')

#         except Exception as e:
#             print(f"[ERROR] Falha ao converter coluna '{col_name}': {e}")
#             raise

#     return df


def normalize_col(col_name):
    #  Remove accent marks, lowercase, and replace special characters
    col_name = unicodedata.normalize('NFKD', col_name).encode('ASCII', 'ignore').decode('utf-8')
    col_name = col_name.lower()
    col_name_new = col_name.replace(' ', '_') \
                       .replace('/', '_') \
                       .replace('(', '') \
                       .replace(')', '') \
                       .strip()
    
    print(f'{col_name_new} <- {col_name}')
    return col_name_new