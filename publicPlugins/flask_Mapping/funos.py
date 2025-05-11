import re


def nameLegitimacyChecks(name: str) -> bool:
    """
    此函数检查给定的名称是否合法。
    :param name: 名称。
    :return: bool
    """
    if _is_empty(name):
        return False
    if _contains_special_characters(name):
        return False
    if _starts_or_ends_with_dot(name):
        return False
    if _contains_consecutive_dots(name):
        return False
    if _contains_illegal_characters(name):
        return False
    if _exceeds_length_limit(name):
        return False
    if _is_reserved_name(name):
        return False
    if _is_all_digits(name):
        return False
    if _starts_with_digit(name):
        return False
    return True


def _contains_special_characters(name):
    """
    检查名称是否包含特殊字符（\\/:*?"<>|）
    """
    return re.search(r"[\\/:*?\"<>|]", name)


def _starts_or_ends_with_dot(name):
    """
    检查名称是否以点（.）开头或结尾
    """
    return name.startswith(".") or name.endswith(".")


def _contains_consecutive_dots(name):
    """
    检查名称是否包含连续的两个点（..）
    """
    return ".." in name


def _contains_illegal_characters(name):
    """
    检查名称是否包含非法字符（除了 a-zA-Z0-9._-）
    """
    return not re.match(r"^[a-zA-Z0-9._-]+$", name)


def _exceeds_length_limit(name):
    """
    检查名称长度是否超过 255 个字符
    """
    return len(name) > 255


def _is_empty(name):
    """
    检查名称是否为空字符串
    """
    return name == ""


def _is_reserved_name(name):
    """
    检查名称是否为 Windows 系统的保留名称（如 CON, PRN, AUX 等）
    """
    reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8",
                      "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
    return name.upper() in reserved_names


def _is_all_digits(name):
    """
    检查名称是否全部为数字
    """
    return name.isdigit()


def _starts_with_digit(name):
    """
    检查名称是否以数字开头
    """
    return name[0].isdigit()
