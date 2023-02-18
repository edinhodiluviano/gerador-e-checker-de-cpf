"""
Gera ou checa um CPF.

Acesse https://github.com/pedrokpp/gerador-e-checker-de-cpf
para mais informações.

Funções:
-----------
    checar(cpf, regiao)
    gerar(quantidade, regiao)
"""

import random


def _calc_dv(cpf: str) -> str:
    dv = 0
    for position, digit in enumerate(cpf):
        digit = int(digit)
        dv += (position + 1) * digit
    dv = dv % 11
    if dv == 10:
        dv = 0
    dv = str(dv)
    cpf += dv
    dv = 0
    for position, digit in enumerate(cpf):
        digit = int(digit)
        dv += position * digit
    dv = dv % 11
    if dv == 10:
        dv = 0
    dv = str(dv)
    cpf += dv
    return cpf[-2:]


def checar(cpf: str, regiao: bool = False):
    """
    Verifica se o CPF dado tem os dígitos verificadores válidos.

    Retorna ``True`` quando um CPF é válido e ``False`` quando é inválido

    ``regiao`` é um parametro ``bool`` o qual checará ou não a região do CPF
    retornado em ``stdout``.
    ``False`` é o valor padrão e a região não será checada.
    """
    # limpa o cpf de pontos e hifens 000.000.000-00
    if "." in cpf and "-" in cpf:
        cpf = cpf.replace(".", "").replace("-", "")

    if len(cpf) < 11:
        cpf = cpf.zfill(11)
    elif len(cpf) > 11:
        return False

    regiao_dict = {
        "0": "Rio Grande do Sul",
        "1": "Distrito Federal – Goiás – Mato Grosso – Mato Grosso do Sul – Tocantins",  # NOQA: E501
        "2": "Pará – Amazonas – Acre – Amapá – Rondônia – Roraima",
        "3": "Ceará – Maranhão – Piauí",
        "4": "Pernambuco – Rio Grande do Norte – Paraíba – Alagoas",
        "5": "Bahia – Sergipe",
        "6": "Minas Gerais",
        "7": "Rio de Janeiro – Espírito Santo",
        "8": "São Paulo",
        "9": "Paraná – Santa Catarina",
    }
    if regiao:
        regiao_digit = cpf[-3]
        regiao_str = regiao_dict[regiao_digit]
        print(f"Regiões: {regiao_str}")

    dv = _calc_dv(cpf[:9])
    return dv == cpf[-2:]


def gerar(quantidade=1, regiao=-1):
    """Gera um CPF aleatório.
    Retorna uma lista com os CPFs gerados (já checados).
    ``quantidade`` é um parametro ``int`` que remete a quantos CPFs serão gerados. ``1`` é o valor padrão e será gerado apenas 1 CPF.
    ``regiao`` é um parametro ``int`` que remete à região cujos CPFs serão gerados. ``-1`` é o valor padrão e será utilizado uma região aleatória.

    Regiôes:
    -----------
         0:  Rio Grande do Sul
         1:  Distrito Federal – Goiás – Mato Grosso – Mato Grosso do Sul – Tocantins
         2:  Pará – Amazonas – Acre – Amapá – Rondônia – Roraima
         3:  Ceará – Maranhão – Piauí
         4:  Pernambuco – Rio Grande do Norte – Paraíba – Alagoas
         5:  Bahia – Sergipe
         6:  Minas Gerais
         7:  Rio de Janeiro – Espírito Santo
         8:  São Paulo
         9: Paraná – Santa Catarina
    """
    valid_rcpf = []
    valid_cpfs = []
    while len(valid_rcpf) != quantidade:
        raw_cpfs = []
        for i in range(quantidade):
            rcpf = ""
            for x in range(11):
                if x == 8:
                    if regiao == -1:
                        rcpf += str(random.randint(0, 9))
                    else:
                        rcpf += str(regiao)
                else:
                    rcpf += str(random.randint(0, 9))
            raw_cpfs.append(rcpf)
            if checar(raw_cpfs[i],False):
                valid_rcpf.append(raw_cpfs[i])
    for i in range(len(valid_rcpf)):
        valid_cpfs.append(valid_rcpf[i][:3]+"."+valid_rcpf[i][3:6]+"."+valid_rcpf[i][6:9]+"-"+valid_rcpf[i][9::])  # NOQA E226
    return valid_cpfs
