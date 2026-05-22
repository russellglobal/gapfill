"""工具函数测试"""

from gapfill.utils import detect_git, detect_tools, get_os_info


def test_detect_git():
    """git 应该被检测到（开发环境通常有 git）"""
    result = detect_git()
    assert result is True  # 测试环境假设有 git


def test_detect_tools_returns_dict():
    """detect_tools 应返回字典"""
    result = detect_tools()
    assert isinstance(result, dict)
    assert "git" in result  # git 应该存在


def test_get_os_info():
    """get_os_info 应返回包含 system 的字典"""
    result = get_os_info()
    assert "system" in result
    assert result["system"] in ("Windows", "Linux", "Darwin")
