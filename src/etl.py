import pandas as pd


def extract_data(file_path):
    '''Extraindo os dados'''
    df = pd.read_csv(f"{file_path}")
    return df


def transform_data(df): 
    '''Transformando os dados'''

    # Lista com os estados brasileiros
    estados = ["AC", "AL", "AP", 
              "AM", "BA", "CE", "DF", "ES", 
              "GO", "MA", "MT", "MS", "MG", 
              "PA", "PB", "PR", "PE", "PI", 
              "RJ", "RN", "RS", "RO", "RR", 
              "SC", "SP", "SE", "TO"]
    
    coluna_notas = ["nota_matematica", "nota_linguagens", "nota_ciencias", "nota_redacao"]

    # Elimina duplicadas da coluna "id"
    df = df.drop_duplicates(subset="id")
    
    # Elimina estados não identificados
    df = df[df["estado"].isin(estados)]

    # Elimina os valores nulos e converte a coluna "nota_matematica" para o tipo "float"
    df["nota_matematica"] = (
        df["nota_matematica"]
        .astype(str)
        .dropna()
        .str.replace(",", ".")
        .astype(float)
    )

    # Converte a coluna "nota_linguagens" para o tipo "float"
    df = df[df["nota_linguagens"] != "erro"]
    df["nota_linguagens"] = (
        df["nota_linguagens"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    # Converte a coluna "nota_ciencias" para o tipo "float"
    df["nota_ciencias"] = (
        df["nota_ciencias"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    # Converte a coluna "nota_redacao" para o tipo "float"
    df["nota_redacao"] = (
        df["nota_redacao"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    # Converte a coluna "ano" para o tipo "datetime"
    df["ano"] = pd.to_datetime(df["ano"], format="%Y")

    # Retira os valores negativos das colunas nota
    df[coluna_notas] = df[coluna_notas].mask(df[coluna_notas] < 0)

    # Retira os valores maiores que 999 das colunas nota
    df[coluna_notas] = df[coluna_notas].mask(df[coluna_notas] > 1000)

    # Elimina os valores nulos restatntes
    df = df.dropna()
    
    return df


def load_data(df):
    '''Carrega os dados limpos e cria um arquivo em csv'''
    return df.to_csv("data/enem_dataset_limpo.csv", index=False, encoding="utf-8")
    

def main():
    link = "data/enem_dataset_com_erros.csv"

    df = extract_data(link)
    df = transform_data(df)
    df = load_data(df)


if __name__ == "__main__":
    main()