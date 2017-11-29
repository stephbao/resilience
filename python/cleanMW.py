import pandas as pd

df = pd.read_csv("pre_post_mannwhitney.csv", encoding = "ISO-8859-1", engine='python')

surveys = df['Surveys']
new = []

for s in surveys:
    x = s.split(':')
    if ('PSS' in x[0]):
        x[0] = x[0].strip()
        x[1] = x[1].strip()
        if (x[0][1] == 'o'):
            x[0] = 'PostPSS'
        elif (x[0][1] == 'r'):
            x[0] = 'PrePSS'

        if (x[1][1] == 'o'):
            x[1] = 'PostPSS'
        elif(x[1][1] == 'r'):
            x[1] = 'PrePSS'

    if ('CSSEC' in x[0]):
        x[0] = x[0].strip()
        x[1] = x[1].strip()
        if (x[0][1] == 'o'):
            x[0] = 'PostCSSEC'
        elif (x[0][1] == 'r'):
            x[0] = 'PreCSSEC'

        if (x[1][1] == 'o'):
            x[1] = 'PostCSSEC'
        elif(x[1][1] == 'r'):
            x[1] = 'PreCSSEC'

    if ('ISEL' in x[0]):
        x[0] = x[0].strip()
        x[1] = x[1].strip()
        if (x[0][1] == 'o'):
            x[0] = 'PostISEL'
        elif (x[0][1] == 'r'):
            x[0] = 'PreISEL'

        if (x[1][1] == 'o'):
            x[1] = 'PostISEL'
        elif(x[1][1] == 'r'):
            x[1] = 'PreISEL'

    if ('SF' in x[0]):
        x[0] = x[0].strip()
        x[1] = x[1].strip()
        if (x[0][1] == 'o'):
            x[0] = 'PostSF'
        elif (x[0][1] == 'r'):
            x[0] = 'PreSF'

        if (x[1][1] == 'o'):
            x[1] = 'PostSF'
        elif(x[1][1] == 'r'):
            x[1] = 'PreSF'

    if ('LS' in x[0]):
        x[0] = x[0].strip()
        x[1] = x[1].strip()
        if (x[0][1] == 'o'):
            x[0] = 'PostLS'
        elif (x[0][1] == 'r'):
            x[0] = 'PreLS'

        if (x[1][1] == 'o'):
            x[1] = 'PostLS'
        elif(x[1][1] == 'r'):
            x[1] = 'PreLS'

    if ('NBS' in x[0]):
        x[0] = x[0].strip()
        x[1] = x[1].strip()
        if (x[0][1] == 'o'):
            x[0] = 'PostNBS'
        elif (x[0][1] == 'r'):
            x[0] = 'PreNBS'

        if (x[1][1] == 'o'):
            x[1] = 'PostNBS'
        elif(x[1][1] == 'r'):
            x[1] = 'PreNBS'

    if ('BRS' in x[0]):
        x[0] = x[0].strip()
        x[1] = x[1].strip()
        if (x[0][1] == 'o'):
            x[0] = 'PostBRS'
        elif (x[0][1] == 'r'):
            x[0] = 'PreBRS'

        if (x[1][1] == 'o'):
            x[1] = 'PostBRS'
        elif(x[1][1] == 'r'):
            x[1] = 'PreBRS'

    new.append('|'.join(x))

df['Surveys'] = pd.Series(new, index=df.index)

df = df[df['p']!= 0]
df = df[df['p'] <= 0.06]

df.to_csv('pre_post_mannwhitney.csv', index=False)
