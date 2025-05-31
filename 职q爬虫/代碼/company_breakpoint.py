def company_breakpoint(df, idd):
    targetvalue = idd
    for index, row in df.iloc[::-1].iterrows():
        if row['companyid'] == targetvalue:
            df = df.drop(index)
        else:
            break

    return df


def delete(dftt):
    dftt = dftt.iloc[1:]
    return dftt
