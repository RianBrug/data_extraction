# file composition
# when line pos[8]
# header columns
#   == 0 ~> register header file     | df_header_lote_header
#      == 1 ~> reg lote header     | df_header_lote_header
# details columns
#      == 3 ~> reg detail          | df_header_lote_details
#      == 5 ~> reg detail trailer  - mark end details
#   == 9 ~> reg trailer file

import pandas as pd

filepath = 'modelo_arquivo.txt'
with open(filepath) as fp:
    header_reg = False  # ctrl if df_header_lote already have registeredd header file data

    for line in fp:
        line = line.split()

        register_checker = line[0]
        line_list = register_checker.split()
        if(header_reg is False and line_list[0][7] == '0'):
            company_name_1 = ''.join([i for i in line[2] if not i.isdigit()])
            company_name = [company_name_1 + " " + line[3]]
            df_header_lote = pd.DataFrame(
                            columns=["Nome da Empresa",
                            "Num de Inscrição da Empresa", "Nome do Banco",
                            "Nome da Rua", "Número do Local",
                            "Nome da Cidade", "CEP", "UF"],
                            )
            df_header_lote["Nome da Empresa"] = company_name

            bank_name = line[4]
            df_header_lote["Nome do Banco"] = bank_name

        if(header_reg and line_list[0][7] == '1'):
            register_lote = line[1]
            company_subscription_number = register_lote[1:15]
            df_header_lote["Num de Inscrição da Empresa"] = company_subscription_number[:2] + \
                                            "." + company_subscription_number[2:5] + \
                                            "." + company_subscription_number[5:8] + \
                                            "/" + company_subscription_number[8:12] + \
                                            "-" + company_subscription_number[12:15]
            df_header_lote["Nome da Rua"] = line[4] + " " + line[5] + " " + line[6]
            df_header_lote["Número do Local"] = line[7]
            city_name_and_uf = ''.join([i for i in line[8] if not i.isdigit()])
            cep_number = ''.join([i for i in line[8] if i.isdigit()])
            df_header_lote["CEP"] = cep_number[0:5] + "-" + cep_number[5:]
            df_header_lote["Nome da Cidade"] = city_name_and_uf[:-2]
            df_header_lote["UF"] = city_name_and_uf[-2:]

        header_reg = True

        import pdb; pdb.set_trace()
        if(header_reg and line_list[0][7] == '3'):
            register_detail = line[1]

            customer_name_1 = ''.join([i for i in line[0] if not i.isdigit()])
            customer_name = [customer_name_1[1:] + " " + line[1] + line[2]]
            df_detail_seg = pd.DataFrame(
                            columns=["Nome do Favorecido",
                            "Data de Pagamento", "Valor do Pagamento",
                            "Número do Documento Atribuído pela Empresa", "Forma de Lançamento"],
                            )
            df_detail_seg["Nome do Favorecido"] = customer_name
