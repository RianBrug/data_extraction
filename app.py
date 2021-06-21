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

print("Starting data extraction from 'modelo_arquivo.txt'...")

filepath = 'modelo_arquivo.txt'
with open(filepath) as fp:
    header_reg = False  # ctrl if df_header_lote already have registeredd header file data
    header_detail = False  # II

    for line in fp:
        line = line.split()

        line_list = line[0].split()

        if(line_list[0][7] == '0'):
            company_name_1 = ''.join([i for i in line[2] if not i.isdigit()])
            company_name = company_name_1 + " " + line[3]

            if(header_reg is False):
                df_header_lote = pd.DataFrame(
                                columns=["Nome da Empresa",
                                "Num de Inscrição da Empresa", "Nome do Banco",
                                "Nome da Rua", "Número do Local",
                                "Nome da Cidade", "CEP", "UF"],
                                )
            bank_name = line[4]

        if(header_reg and line_list[0][7] == '1'):
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

            row = pd.Series([company_name, company_subscription_number_formated,
                            bank_name, address, address_number, city_name,
                            cep_number_formated, uf], index=df_header_lote.columns)

            df_header_lote = df_header_lote.append(row, ignore_index=True)

        header_reg = True

        if(header_reg and line_list[0][7] == '3'):
            # register_detail = line[1]
            if(header_detail):
                customer_name_1 = ''.join([i for i in line[0] if not i.isdigit()])
                customer_name = [customer_name_1[1:] + " " + line[1] + " " + line[2]]
                df_detail_seg = pd.DataFrame(
                                columns=["Nome do Favorecido",
                                "Data de Pagamento", "Valor do Pagamento",
                                "Número do Documento Atribuído pela Empresa", "Forma de Lançamento"],
                                )
            df_detail_seg["Nome do Favorecido"] = customer_name
            payment_date_and_price = ''.join([i for i in line[4] if i.isdigit()])
            df_detail_seg["Data de Pagamento"] = payment_date_and_price[0:2] + "/" \
                                                + payment_date_and_price[2:4] \
                                                + "/" + payment_date_and_price[4:8]

            price_with_comma = locale.currency(float(payment_date_and_price[8:-2] + "." + payment_date_and_price[-2:]))
            df_detail_seg["Valor do Pagamento"] = price_with_comma

        header_detail = True


def main():

    filepath = 'modelo_arquivo.txt'
    with open(filepath) as fp:
        header_reg = False  # ctrl if df_header_lote already have registeredd header file data
        header_detail = False  # II

        for line in fp:
            line = line.split()

            line_list = line[0].split()
            import pdb; pdb.set_trace()

            # create series from data

if __name__ == "__main__":

    main()
