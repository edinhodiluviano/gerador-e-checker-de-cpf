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


def formatar(cpf: str) -> str:
    """Limpa o cpf de pontos e hifens e adiciona zeros à esquerda."""
    cpf = cpf.replace(".", "").replace("-", "")

    if len(cpf) < 11:
        cpf = cpf.zfill(11)
    elif len(cpf) > 11:
        msg = f"O CPF deve ter 11 dígitos. Mas {len(cpf)} dígitos foram dados"
        raise ValueError(msg)

    return cpf


def checar(cpf: str, regiao: bool = False) -> bool:
    """
    Verifica se o CPF dado tem os dígitos verificadores válidos.

    Retorna ``True`` quando um CPF é válido e ``False`` quando é inválido

    ``regiao`` é um parametro ``bool`` o qual checará ou não a região do CPF
    retornado em ``stdout``.
    ``False`` é o valor padrão e a região não será checada.
    """
    try:
        cpf = formatar(cpf)
    except ValueError:
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


def gerar_um(regiao: int = None, seeded_random: random.Random = None) -> str:
    """
    Gera um CPF aleatório para a região especificada e com a seed dada.

    Regiões:
    -----------
     0: Rio Grande do Sul
     1: Distrito Federal – Goiás – Mato Grosso – Mato Grosso do Sul – Tocantins
     2: Pará – Amazonas – Acre – Amapá – Rondônia – Roraima
     3: Ceará – Maranhão – Piauí
     4: Pernambuco – Rio Grande do Norte – Paraíba – Alagoas
     5: Bahia – Sergipe
     6: Minas Gerais
     7: Rio de Janeiro – Espírito Santo
     8: São Paulo
     9: Paraná – Santa Catarina
    """
    # raiz_int = random.randint(0, 999_999_999)
    # raiz_str = str(raiz_int).zfill(9)
    # dv = _calc_dv(raiz_str)
    # cpf = raiz_str + dv
    # return cpf

    if seeded_random is None:
        seeded_random = random

    if regiao is None:
        raiz_int = seeded_random.randint(0, 999_999_999)
    else:
        raiz_int = seeded_random.randint(0, 99_999_999)
        raiz_int = raiz_int * 10 + regiao
    raiz_str = str(raiz_int).zfill(9)
    dv = _calc_dv(raiz_str)
    cpf = raiz_str + dv
    return cpf


def gerar(
    quantidade: int = 1,
    regiao: int = None,
    seeded_random: random.Random = None,
) -> list:
    """
    Gera varios CPFs aleatórios para a região especificada e com a seed dada.

    ``quantidade`` é um ``int`` que especifica a quantos CPFs serão gerados.
    Se não for fornecido, apenas 1 CPF será gerado.
    ``regiao`` é um ``int`` que especifica a região cujos CPFs serão gerados.
    Se não for fornecido, uma região aleatória sera usada.

    Regiões:
    -----------
     0: Rio Grande do Sul
     1: Distrito Federal – Goiás – Mato Grosso – Mato Grosso do Sul – Tocantins
     2: Pará – Amazonas – Acre – Amapá – Rondônia – Roraima
     3: Ceará – Maranhão – Piauí
     4: Pernambuco – Rio Grande do Norte – Paraíba – Alagoas
     5: Bahia – Sergipe
     6: Minas Gerais
     7: Rio de Janeiro – Espírito Santo
     8: São Paulo
     9: Paraná – Santa Catarina
    """
    cpfs = [gerar_um(regiao, seeded_random) for i in range(quantidade)]
    return cpfs
