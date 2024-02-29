import streamlit as st
import pandas as pd


def get_count_sum_google(row):
    return row['Amount (Merchant Currency)'].count(), row['Amount (Merchant Currency)'].sum()


def get_count_sum_apple(row):
    return row['Units Sold'].sum(), row['Proceeds'].sum()


def main():

    apple_commission_factor = 0.85
    google_commission_factor = 0.85

    st.set_page_config(
        page_title="Stores Earnings Parser For Brazilian Tax Authorities", layout="wide")

    st.header("Android - Google")

    google_file = st.file_uploader(
        "Import your \"PlayApp_????.csv\" file here:",
        type=["csv"],
        accept_multiple_files=False,
        key="google_file"
    )

    if google_file != None:
        df = pd.read_csv(google_file)

        # Brasil
        # Sales
        df_filtered = df.loc[(df['Transaction Type'] == 'Charge')
                             & (df['Buyer Currency'] == 'BRL')]

        [google_br_sales_count, google_br_sales_sum] = get_count_sum_google(
            df_filtered)

        # Refund
        df_filtered = df.loc[(df['Transaction Type'] == 'Charge refund')
                             & (df['Buyer Currency'] == 'BRL')]

        [google_br_refund_count, google_br_refund_sum] = get_count_sum_google(
            df_filtered)

        # Balance
        google_br_balance_count = google_br_sales_count - google_br_refund_count
        google_br_balance_sum = google_br_sales_sum + google_br_refund_sum

        # Exterior
        # Sales
        df_filtered = df.loc[(df['Transaction Type'] == 'Charge')
                             & (df['Buyer Currency'] != 'BRL')]

        [google_ex_sales_count, google_ex_sales_sum] = get_count_sum_google(
            df_filtered)

        # Refund
        df_filtered = df.loc[(df['Transaction Type'] == 'Charge refund')
                             & (df['Buyer Currency'] != 'BRL')]

        [google_ex_refund_count, google_ex_refund_sum] = get_count_sum_google(
            df_filtered)

        # Balance
        google_ex_balance_count = google_ex_sales_count - google_ex_refund_count
        google_ex_balance_sum = google_ex_sales_sum + google_ex_refund_sum

        # commissions
        google_br_commission = google_br_balance_sum * google_commission_factor
        google_ex_commission = google_ex_balance_sum * google_commission_factor

        # Totals
        google_total_sales_count = google_br_sales_count + google_ex_sales_count
        google_total_sales_sum = google_br_sales_sum + google_ex_sales_sum
        google_total_refund_count = google_br_refund_count + google_ex_refund_count
        google_total_refund_sum = google_br_refund_sum + google_ex_refund_sum
        google_total_balance_count = google_br_balance_count + google_ex_balance_count
        google_total_balance_sum = google_br_balance_sum + google_ex_balance_sum
        google_total_commission = google_br_commission + google_ex_commission

        data = {
            '': ['Brasil', 'Exterior', 'TOTAL'],
            'Sales Count': [google_br_sales_count, google_ex_sales_count, google_total_sales_count],
            'Sales Sum': [google_br_sales_sum, google_ex_sales_sum, google_total_sales_sum],
            'Refund Count': [google_br_refund_count, google_ex_refund_count, google_total_refund_count],
            'Refund Sum': [google_br_refund_sum, google_ex_refund_sum, google_total_refund_sum],
            'Balance Count': [google_br_balance_count, google_ex_balance_count, google_total_balance_count],
            'Balance Sum': [google_br_balance_sum, google_ex_balance_sum, google_total_balance_sum],
            'Net Balance': [google_br_commission, google_ex_commission, google_total_commission]
        }

        df = pd.DataFrame(data)

        st.table(df.style.format({
            'Sales Count': '{:,.0f}',
            'Sales Sum': 'R$ {:,.2f}',
            'Refund Count': '{:,.0f}',
            'Refund Sum': 'R$ {:,.2f}',
            'Balance Count': '{:,.0f}',
            'Balance Sum': 'R$ {:,.2f}',
            'Net Balance': 'R$ {:,.2f}',
        }, thousands='.', decimal=','))

    st.divider()

    st.header("iOS - Apple")

    apple_file = st.file_uploader(
        "Import your \"financial_report.csv\" file here:",
        type=['csv'],
        accept_multiple_files=False,
        key="apple_file"
    )

    if apple_file != None:

        df = pd.read_csv(apple_file, skip_blank_lines=True, skiprows=2)

        # Remover linhas que não traguem valor nenhum na primeira coluna
        df = df[df.iloc[:, 0].notna()]

        # Converte a coluna de Proceeds para float
        df['Proceeds'] = df['Proceeds'].astype(float)
        # Adiciona a comissão da Apple aos valores que estãoão líquidos
        df['Proceeds'] = df['Proceeds'].div(0.85)

        # Brasil
        # Sales
        df_filtered = df.loc[(
            df['Country or Region (Currency)'] == 'Brazil (BRL)')]

        [apple_br_sales_count, apple_br_sales_sum] = get_count_sum_apple(
            df_filtered)

        # Exterior
        # Sales
        df_filtered = df.loc[(
            df['Country or Region (Currency)'] != 'Brazil (BRL)')]

        [apple_ex_sales_count, apple_ex_sales_sum] = get_count_sum_apple(
            df_filtered)

        # commissions
        apple_br_commission = apple_br_sales_sum * apple_commission_factor
        apple_ex_commission = apple_ex_sales_sum * apple_commission_factor

        # Totals
        apple_total_sales_count = apple_br_sales_count + apple_ex_sales_count
        apple_total_sales_sum = apple_br_sales_sum + apple_ex_sales_sum
        apple_total_commision = apple_br_commission + apple_ex_commission

        data = {
            '': ['Brasil', 'Exterior', 'TOTAL'],
            'Sales Count': [apple_br_sales_count, apple_ex_sales_count, apple_total_sales_count],
            'Sales Sum': [apple_br_sales_sum, apple_ex_sales_sum, apple_total_sales_sum],
            'Net Balance': [apple_br_commission, apple_ex_commission, apple_total_commision],
        }

        df = pd.DataFrame(data)

        st.table(df.style.format({
            'Sales Count': '{:,.0f}',
            'Sales Sum': 'R$ {:,.2f}',
            'Net Balance': 'R$ {:,.2f}',
        }, thousands='.', decimal=','))


if __name__ == "__main__":
    main()
