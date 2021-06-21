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
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

print("Starting data extraction from 'modelo_arquivo.txt'...", "\n")

filepath = 'modelo_arquivo.txt'
with open(filepath) as fp:
    ctrl_creation_df_header = False  # ctrl if df_header_lote already have created df
    ctrl_creation_df_detail = False  # II

    for line in fp:
        line = line.split()

        line_list = line[0].split()

        if(line_list[0][7] == '0'):
            print("Reading Archive Register Header...")
            company_name_1 = ''.join([i for i in line[2] if not i.isdigit()])
            company_name = company_name_1 + " " + line[3]
            bank_name = line[4]

            if(ctrl_creation_df_header is False):
                df_header_lote = pd.DataFrame(
                                columns=["Nome da Empresa",
                                "Num de Inscrição da Empresa", "Nome do Banco",
                                "Nome da Rua", "Número do Local",
                                "Nome da Cidade", "CEP", "UF"],
                                )
                ctrl_creation_df_header = True
                print("Creating Header DataFrame to add data later...")
            print("Step finished.", "\n")
        if(ctrl_creation_df_header and line_list[0][7] == '1'):
            print("Reading Batch Register Header...")
            register_lote = line[1]
            company_subscription_number = register_lote[1:15]
            company_subscription_number_formated = company_subscription_number[:2] + \
                                            "." + company_subscription_number[2:5] + \
                                            "." + company_subscription_number[5:8] + \
                                            "/" + company_subscription_number[8:12] + \
                                            "-" + company_subscription_number[12:15]
            address = line[4] + " " + line[5] + " " + line[6]
            address_number = line[7]
            city_name_and_uf = ''.join([i for i in line[8] if not i.isdigit()])
            cep_number = ''.join([i for i in line[8] if i.isdigit()])
            cep_number_formated = cep_number[0:5] + "-" + cep_number[5:]
            city_name = city_name_and_uf[:-2]
            uf = city_name_and_uf[-2:]
            print("Step finished.")
            row = pd.Series([company_name, company_subscription_number_formated,
                            bank_name, address, address_number, city_name,
                            cep_number_formated, uf], index=df_header_lote.columns)

            df_header_lote = df_header_lote.append(row, ignore_index=True)
            print("Added data to Header DataFrame.", "\n")
        if(ctrl_creation_df_header and line_list[0][7] == '3'):
            print("Reading Segment Detail Record...")
            if(ctrl_creation_df_detail is False):
                df_detail_seg = pd.DataFrame(
                                columns=["Nome do Favorecido",
                                "Data de Pagamento", "Valor do Pagamento",
                                "Número do Documento Atribuído pela Empresa", "Forma de Lançamento"],
                                )
                ctrl_creation_df_detail = True
                print("Created Details DataFrame to add data later...")

            customer_name_1 = ''.join([i for i in line[0] if not i.isdigit()])
            customer_name = customer_name_1[1:] + " " + line[1] + " " + line[2]
            payment_date_and_price = ''.join([i for i in line[4] if i.isdigit()])
            payment_date = payment_date_and_price[0:2] + "/" \
                            + payment_date_and_price[2:4] \
                            + "/" + payment_date_and_price[4:8]

            price_with_comma = locale.currency(
                                float(payment_date_and_price[8:-2] + "." + payment_date_and_price[-2:]))
            doc_number_attr_by_company = line[3]
            payment_method = ("Crédito em Conta Corrente" if int(line[6]) == 0
                                                        else "Crédito em Conta Poupança")
            print("Step finished")
            row_details = pd.Series([customer_name, payment_date, price_with_comma,
                                    doc_number_attr_by_company, payment_method], index=df_detail_seg.columns)

            df_details_columns = pd.DataFrame(["Nome do Favorecido",
            "Data de Pagamento", "Valor do Pagamento",
            "Número do Documento Atribuído pela Empresa", "Forma de Lançamento"], index=df_detail_seg.columns)
            ## used to append into df_header_lote before concat df_detail_seg

            df_detail_seg = df_detail_seg.append(row_details, ignore_index=True)
            print("Added data to Segment Details DataFrame.", "\n")
    import pdb; pdb.set_trace()
    print("Starting merge DataFrames to prepare exportation...")
    major_df = df_header_lote.append(df_details_columns, ignore_index=True)
