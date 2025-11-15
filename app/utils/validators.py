from datetime import date, datetime
import re
import phonenumbers
from typing import Optional  # Importa Optional para tipos opcionais

def only_digits(s: str) -> str:
    return re.sub(r'\D', '', s or '')

def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF (apenas algoritmo dos dígitos verificadores).
    Aceita strings com máscara, retorna True se válido.
    """
    if not cpf:
        return False
    s = only_digits(cpf)
    if len(s) != 11:
        return False
    if s == s[0] * 11:
        return False
    def calc(digs):
        soma = sum(int(d) * i for d, i in zip(digs, range(len(digs)+1, 1, -1)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)
    d1 = calc(s[:9])
    d2 = calc(s[:9] + d1)
    return s[-2:] == d1 + d2

def normalize_cpf(cpf: str) -> Optional[str]:
    if not cpf:
        return None
    s = only_digits(cpf)
    return s if len(s) == 11 else None

def format_cpf_masked(cpf: str) -> str:
    s = only_digits(cpf or '')
    if len(s) != 11:
        return cpf or ''
    return f"{s[:3]}.{s[3:6]}.{s[6:9]}-{s[9:]}"

def validate_and_format_phone(raw: str, region: str = "BR") -> Optional[str]:
    """
    Retorna o número em formato E.164 (ex: +5511999998888) se válido, caso contrário None.
    """
    if not raw:
        return None
    try:
        pn = phonenumbers.parse(raw, region)
        if not phonenumbers.is_valid_number(pn):
            return None
        return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        return None

def validate_birthdate(value) -> bool:
    """Checagem simples: valor deve ser date e não no futuro."""
    if value is None:
        return True
    if isinstance(value, date):
        return value <= date.today()
    return False

def validate_and_format_phone(phone: str) -> str:
    """
    Valida e formata um número de telefone.
    """
    try:
        parsed_phone = phonenumbers.parse(phone, "BR")  # "BR" para números brasileiros
        if not phonenumbers.is_valid_number(parsed_phone):
            raise ValueError("Número de telefone inválido")
        return phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException as e:
        raise ValueError(f"Erro ao validar número de telefone: {e}")

def validate_birthdate(birthdate: str) -> str:
    """
    Valida a data de nascimento.
    """
    try:
        datetime.strptime(birthdate, "%Y-%m-%d")
        return birthdate
    except ValueError:
        raise ValueError("Data de nascimento inválida. Use o formato YYYY-MM-DD.")