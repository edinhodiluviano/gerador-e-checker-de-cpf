import pytest

import cpf


def test_should_always_pass():
    ...


cpfs_validos = [
    "00000000000",
    "11111111111",
    "22222222222",
    "33333333333",
    "44444444444",
    "55555555555",
    "66666666666",
    "77777777777",
    "88888888888",
    "99999999999",
    "00000000191",
    "78640734500",
    "41085921824",
    "38227593178",
    "51693314525",
    "57303734732",
    "49435142940",
    "98407460656",
    "48245706469",
    "04029587992",
    "65492612280",
    "97609867284",
    "95158088632",
    "63220509231",
    "13292301670",
    "91875881450",
    "36597905830",
    "62629646572",
    "72714465080",
    "04209866180",
    "58257730963",
]


@pytest.mark.parametrize("cpf_test", cpfs_validos)
def test_checar_cpf_valido(cpf_test):
    assert cpf.checar(cpf_test) is True


cpfs_invalidos = []
for i in cpfs_validos:
    dv = i[-2:]
    for new_dv in range(100):
        new_dv = str(new_dv).zfill(2)
        if new_dv != dv:
            new_cpf = i[:-2] + new_dv
            cpfs_invalidos.append(new_cpf)


# the code is not very fast, so we're running just some cases to speed up the
# test suite. Right now we're running 1/17's of cases
@pytest.mark.parametrize("cpf_test", cpfs_invalidos[::17])
def test_checar_cpf_invalido(cpf_test):
    assert cpf.checar(cpf_test) is False


cpfs_com_numeros_extras = []
for i in cpfs_validos:
    for extra_digit in range(10):
        extra_digit = str(extra_digit)
        cpfs_com_numeros_extras.append(i + extra_digit)
        cpfs_com_numeros_extras.append(extra_digit + i)


# the code is not very fast, so we're running just some cases to speed up the
# test suite. Right now we're running 1/17's of cases
@pytest.mark.parametrize("cpf_test", cpfs_com_numeros_extras[::17])
def test_checar_cpf_invalido_por_ter_numeros_extras(cpf_test):
    assert cpf.checar(cpf_test) is False


def _retirar_zero(cpf):
    return str(int(cpf))


def _adicionar_hifen(cpf):
    return cpf[:-2] + "-" + cpf[-2:]


def _adicionar_pontos(cpf):
    return cpf[:-8] + "." + cpf[-8:-5] + "." + cpf[-5:]


def _combinacoes(i):
    comb = (
        _retirar_zero(i),
        _adicionar_hifen(i),
        _adicionar_pontos(i),
        _adicionar_hifen(_retirar_zero(i)),
        _adicionar_pontos(_retirar_zero(i)),
        _adicionar_pontos(_adicionar_hifen(i)),
        _adicionar_pontos(_adicionar_hifen(_retirar_zero(i))),
    )
    return comb


cpfs_enfeitados = []
for i in cpfs_validos:
    for cpf_enfeitado in _combinacoes(i):
        cpfs_enfeitados.append((i, cpf_enfeitado))


@pytest.mark.parametrize("original,formatado", cpfs_enfeitados)
def test_formatacao_de_cpf(original, formatado):
    assert cpf.formatar(formatado) == original


seeds = list(range(100))


@pytest.mark.parametrize("seed", seeds)
def test_gerar_um_sem_regiao_retorn_cpf_valido(seed):
    cpf_gerado = cpf.gerar_um(seed=seed)
    assert cpf.checar(cpf_gerado) is True


regioes = list(range(10))


@pytest.mark.parametrize("regiao", regioes)
@pytest.mark.parametrize("seed", seeds[::17])
def test_gerar_um_com_regiao_retorn_cpf_valido(regiao, seed):
    cpf_gerado = cpf.gerar_um(regiao=regiao, seed=seed)
    assert cpf.checar(cpf_gerado) is True


@pytest.mark.parametrize("regiao", regioes)
@pytest.mark.parametrize("seed", seeds[::17])
def test_gerar_um_com_regiao_retorn_cpf_da_regiao(regiao, seed):
    cpf_gerado = cpf.gerar_um(regiao=regiao, seed=seed)
    assert cpf_gerado[-3] == str(regiao)


@pytest.mark.parametrize("seed", seeds[::17])
def test_gerar_com_seed_retorna_list(seed):
    resp = cpf.gerar(seed=seed)
    assert isinstance(resp, list)


def test_gerar_sem_seed_retorna_list():
    resp = cpf.gerar()
    assert isinstance(resp, list)


@pytest.mark.parametrize("seed", seeds[::17])
def test_gerar_10_com_seed_retorna_list_com_len_10(seed):
    resp = cpf.gerar(quantidade=10)
    assert len(resp) == 10


def test_gerar_10_sem_seed_retorna_list_com_len_10():
    resp = cpf.gerar(quantidade=10)
    assert len(resp) == 10


def test_gerar_10_sem_seed_retorna_list_10_cpfs_validos():
    resp = cpf.gerar(quantidade=10)
    for i in resp:
        assert cpf.checar(i) is True


@pytest.mark.parametrize("seed", seeds[::17])
def test_gerar_10_com_seed_retorna_list_10_cpfs_validos(seed):
    resp = cpf.gerar(quantidade=10, seed=seed)
    for i in resp:
        assert cpf.checar(i) is True


@pytest.mark.parametrize("seed", seeds[::17])
def test_gerar_10_com_seed_retorna_list_10_cpfs_unicos(seed):
    resp = cpf.gerar(quantidade=10, seed=seed)
    assert len(set(resp)) == 10


def test_gerar_10_sem_seed_com_regiao_retorna_list_10_cpfs_da_regiao():
    resp = cpf.gerar(quantidade=10, regiao=5)
    for i in resp:
        assert i[-3] == "5"


@pytest.mark.parametrize("seed", seeds[::17])
def test_gerar_10_com_seed_com_regiao_retorna_list_10_cpfs_da_regiao(seed):
    resp = cpf.gerar(quantidade=10, seed=seed, regiao=5)
    for i in resp:
        assert i[-3] == "5"
