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
    header_reg = False  # ctrl if df already have register header filepath
    for line in fp:
        line = line.split()
        register_checker = line[0]
        line_list = register_checker.split()
        if(int(line_list[0][7]) == 0 and header_reg is False):
            nameCompany1 = ''.join([i for i in line[2] if not i.isdigit()])
            nameCompany = [nameCompany1 + " " + line[3]]
            df = pd.DataFrame(
                            columns=["Nome da Empresa",
                            "Num de Inscrição da Empresa", "Nome do Banco",
                            "Nome da Rua", "Número do Local",
                            "Nome da Cidade", "CEP", "UF"],
                            )
            df["Nome da Empresa"] = nameCompany

            bank_name = line[4]
            df["Nome do Banco"] = bank_name

        if(header_reg is True and line_list[0][7] == '1'):
            register_lote = line[1]
            company_subscription_number = register_lote[1:15]
            df["Num de Inscrição da Empresa"] = company_subscription_number[:2] + \
                                            "." + company_subscription_number[2:5] + \
                                            "." + company_subscription_number[5:8] + \
                                            "/" + company_subscription_number[8:12] + \
                                            "-" + company_subscription_number[12:15]
            df["Nome da Rua"] = line[4] + " " + line[5] + " " + line[6]
            df["Número do Local"] = line[7]
            city_name_and_uf = ''.join([i for i in line[8] if not i.isdigit()])
            cep_number = ''.join([i for i in line[8] if i.isdigit()])
            df["CEP"] = cep_number[0:5] + "-" + cep_number[5:]
            df["Nome da Cidade"] = city_name_and_uf[:-2]
            df["UF"] = city_name_and_uf[-2:]

        header_reg = True
