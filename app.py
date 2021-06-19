# file composition
# when line pos[8]
# header columns
#   == 0 ~> register header file     | df_header
#      == 1 ~> reg lote header     | df_header
# details columns
#      == 3 ~> reg detail          | df_details
#      == 5 ~> reg detail trailer  - mark end details
#   == 9 ~> reg trailer file

import pandas as pd

filepath = 'modelo_arquivo.txt'
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        # print(" ISSO EH PRINT ? ")
        if(int(line[7]) == 0):
            line_columns = line.split()
            nameCompany1 = ''.join([i for i in line_columns[2] if not i.isdigit()])
            nameCompany = [nameCompany1 + " " + line_columns[3]]
            df = pd.DataFrame(
                            columns=["Nome da Empresa",
                            "Num de Inscrição da Empresa", "Nome do Banco",
                            "Nome da Rua", "Número do Local",
                            "Nome da Cidade", "CEP", "UF"],
                            )
            df["Nome da Empresa"] = nameCompany
        line = fp.readline()
        cnt += 1
